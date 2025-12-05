import os, tempfile, tarfile, shutil, secrets, time, requests
from flask import Flask, render_template, abort, request, jsonify, session, g
from pathlib import Path
import markdown
import sqlite3
import numpy as np
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import is_address

def auth_addr_from_request():
    addr = session.get("wallet_address")
    if addr: return addr.lower()
    auth = (request.headers.get("Authorization") or "").strip()
    tok = auth
    if auth.lower().startswith("bearer "): tok = auth.split(None, 1)[1].strip()
    if tok and is_address(tok): return tok.lower()
    return None

app = Flask(__name__)
app.secret_key = "1c5da44f5c278ac7f41f666501347d7572a18ae6"
BLOG_DIR = Path("templates/blog")
DOCS_DIR = Path("templates/docs")
VLAD_DIR = Path("templates/vlad")
DATABASE = "thrum.db"

ETHERSCAN_API_URL = os.getenv("ETHERSCAN_API_URL", "https://api.etherscan.io/v2/api")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "MW1A7GNV5IQ2X3PCCRITR9RMP2YKRWTYY1").strip()
PAY_CHAIN_ID = int(os.getenv("PAY_CHAIN_ID", "11155111"))             # 1 = Ethereum mainnet
MIN_CONFIRMATIONS = int(os.getenv("MIN_CONFIRMATIONS", "1")) #"12"))  # adjust for UX
WEI_PER_CREDIT = int(os.getenv("WEI_PER_CREDIT", str(10**14))) # 0.0001 ETH/credit
MAX_TOPUP_WEI = int(os.getenv("MAX_TOPUP_WEI", str(10**18)))

# --------- Helpers ----------

def require_login():
    addr = session.get("wallet_address")
    if not addr: return None
    return addr.lower()

def get_or_assign_deposit_address(user_addr: str) -> str:
    db = get_db()
    row = db.execute(
        "SELECT address FROM deposit_pool WHERE assigned_to = ? AND is_active = 1 LIMIT 1",
        (user_addr.lower(),),
    ).fetchone()
    if row: return row["address"]

    # assign a fresh unassigned address
    row = db.execute("SELECT address FROM deposit_pool WHERE assigned_to IS NULL AND is_active = 1 LIMIT 1").fetchone()
    if not row: raise RuntimeError("deposit_pool_empty")

    db.execute(
        "UPDATE deposit_pool SET assigned_to = ?, assigned_at = CURRENT_TIMESTAMP WHERE address = ?",
        (user_addr.lower(), row["address"]),
    )
    db.commit()
    return row["address"]

def etherscan_txlist(address: str):
    if not ETHERSCAN_API_KEY: raise RuntimeError("missing_ETHERSCAN_API_KEY")
    params = {
        "chainid": str(PAY_CHAIN_ID),
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 9999999999,
        "page": 1,
        "offset": 200,
        "sort": "desc",
        "apikey": ETHERSCAN_API_KEY,
    }
    r = requests.get(ETHERSCAN_API_URL, params=params, timeout=15)
    data = r.json()

    # Etherscan returns {status,message,result}; "No transactions found" is common
    if data.get("message") == "No transactions found": return []
    if data.get("status") != "1": raise RuntimeError(f"etherscan_error: {data.get('result')}")
    return data.get("result") or []

# Returns number of NEW credits added during this call
def sync_and_credit(user_addr: str, deposit_addr: str) -> int:
    db = get_db()
    txs = etherscan_txlist(deposit_addr)
    newly_credited = 0
    dep = deposit_addr.lower()
    usr = user_addr.lower()

    # Process newest-first list; order doesn't matter due to tx_hash primary key
    for tx in txs:
        to_addr = (tx.get("to") or "").lower()
        if to_addr != dep: continue

        tx_hash = (tx.get("hash") or "").lower()
        if not tx_hash.startswith("0x"): continue

        is_error = int(tx.get("isError", "0"))
        conf = int(tx.get("confirmations", "0") or 0)
        value_wei = int(tx.get("value", "0") or 0)
        block_number = int(tx.get("blockNumber", "0") or 0)

        # enforce "1 ETH fill" cap per tx if you want it
        if value_wei > MAX_TOPUP_WEI: value_wei = MAX_TOPUP_WEI

        # upsert deposit row
        existing = db.execute(
            "SELECT is_credited, credited_credits FROM deposits WHERE tx_hash = ?",
            (tx_hash,),
        ).fetchone()

        if not existing:
            db.execute(
                """
                INSERT INTO deposits
                  (tx_hash, user_address, deposit_address, value_wei, block_number, confirmations, is_error, is_credited, credited_credits)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)
                """,
                (tx_hash, usr, dep, value_wei, block_number, conf, is_error),
            )
        else:
            db.execute(
                """
                UPDATE deposits
                SET confirmations = ?, block_number = ?, is_error = ?, value_wei = ?
                WHERE tx_hash = ?
                """,
                (conf, block_number, is_error, value_wei, tx_hash),
            )

        # Credit only once, only if successful + enough confirmations
        row = db.execute(
            "SELECT is_credited, value_wei, is_error FROM deposits WHERE tx_hash = ?",
            (tx_hash,),
        ).fetchone()
        if not row or int(row["is_credited"]) == 1: continue
        if int(row["is_error"]) == 1: continue
        if conf < MIN_CONFIRMATIONS: continue

        credits = int(row["value_wei"]) // WEI_PER_CREDIT
        if credits <= 0:
            # record as credited=1 with 0 credits to avoid repeated work
            db.execute(
                "UPDATE deposits SET is_credited = 1, credited_credits = 0, credited_at = CURRENT_TIMESTAMP WHERE tx_hash = ?",
                (tx_hash,),
            )
            continue

        # Atomic credit to prevent double-credit on concurrent calls
        updated = db.execute(
            """
            UPDATE deposits
            SET is_credited = 1, credited_credits = ?, credited_at = CURRENT_TIMESTAMP
            WHERE tx_hash = ? AND is_credited = 0
            """,
            (credits, tx_hash),
        ).rowcount
        if updated == 1:
            db.execute(
                "UPDATE users SET credits = credits + ? WHERE address = ?",
                (credits, usr),
            )
            newly_credited += credits
        db.commit()

    return newly_credited

@app.route("/api/topup/address", methods=["GET"])
def api_topup_address():
    user_addr = require_login()
    if not user_addr: return jsonify({"ok": False, "error": "not_logged_in"}), 401

    try:
        deposit_addr = get_or_assign_deposit_address(user_addr)
    except Exception as e:
        app.logger.exception("topup_check failed")
        return jsonify({"ok": False, "error": str(e)}), 500

    # Provide ERC-681 payment URIs (value in WEI)
    basic_wei = 10**16   # 0.01 ETH
    pro_wei = 5 * 10**16 # 0.05 ETH

    def eip681(value_wei: int) -> str: return f"ethereum:{deposit_addr}@{PAY_CHAIN_ID}?value={value_wei}"

    return jsonify({
        "ok": True,
        "chain_id": PAY_CHAIN_ID,
        "min_confirmations": MIN_CONFIRMATIONS,
        "wei_per_credit": WEI_PER_CREDIT,
        "deposit_address": deposit_addr,
        "tiers": {
            "basic": {"eth": "0.01", "credits": 100, "value_wei": basic_wei, "uri": eip681(basic_wei)},
            "pro": {"eth": "0.05", "credits": 500, "value_wei": pro_wei, "uri": eip681(pro_wei)},
            #"enterprise": {"max_eth": "1.0", "max_credits": (10**18)//WEI_PER_CREDIT, "max_value_wei": 10**18, "uri_prefix": f"ethereum:{deposit_addr}@{PAY_CHAIN_ID}?value="},
        }
    })

@app.route("/api/topup/check", methods=["POST"])
def api_topup_check():
    user_addr = require_login()
    if not user_addr: return jsonify({"ok": False, "error": "not_logged_in"}), 401

    try:
        deposit_addr = get_or_assign_deposit_address(user_addr)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    try:
        newly = sync_and_credit(user_addr, deposit_addr)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

    user = get_user(user_addr) or get_or_create_user(user_addr)
    return jsonify({
        "ok": True,
        "deposit_address": deposit_addr,
        "newly_credited": newly,
        "credits": int(user["credits"]),
        "min_confirmations": MIN_CONFIRMATIONS
    })

# --------- Beta ----------

@app.route("/beta/")
def beta(): return render_template("beta.html")

# --------- Analyzer ----------

# walks extracted project, finds sol files, and returns summary with report
def analyze_project(root: str):
    sol_files = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".sol"):
                full = os.path.join(dirpath, name)
                rel = os.path.relpath(full, root)
                sol_files.append(rel)
    sol_files.sort()
    sol_count = len(sol_files)
    summary = { "critical": 0, "high": 0, "medium": 0, "low": 0 }
    lines = []
    lines.append("# Thrum scan report")
    lines.append("")
    lines.append(f"- project root: `{os.path.basename(root)}`")
    lines.append(f"- solidity files detected: **{sol_count}**")
    lines.append("")
    if sol_files:
        lines.append("## Solidity files")
        lines.append("")
        for rel in sol_files: lines.append(f"- `{rel}`")
        lines.append("")
    else:
        lines.append("No `.sol` files were detected in this archive.")
        lines.append("")
    lines.append("## Findings")
    lines.append("")
    lines.append("> This is a placeholder report. No real detectors have run yet.")
    lines.append("> Once the engine is wired, this section will contain real findings.")
    lines.append("")
    report_markdown = "\n".join(lines)
    return summary, report_markdown

def get_docs():
    posts = [] # list available markdown posts
    for path in DOCS_DIR.glob("*.md"): posts.append({ "slug": path.stem, "title": path.stem.replace("-", " ").title() })
    posts.sort(key=lambda p: p["slug"], reverse=True)
    return posts

@app.route("/docs/")
def docs_index():
    posts = get_docs()
    return render_template("docs_index.html", posts=posts)

@app.route("/docs/<slug>/")
def docs_post(slug):
    md_path = DOCS_DIR / f"{slug}.md"
    if not md_path.exists(): abort(404)
    md_text = md_path.read_text(encoding="utf-8")
    html = markdown.markdown( md_text, extensions=["fenced_code", "tables", "toc"] )
    return render_template("docs_post.html", content=html, slug=slug)

# ---- Vlad's blog ----

def get_vlad_blog():
    posts = [] # list available markdown posts
    for path in VLAD_DIR.glob("*.md"): posts.append({ "slug": path.stem, "title": path.stem.replace("-", " ").title() })
    posts.sort(key=lambda p: p["slug"], reverse=True)
    return posts

@app.route("/vlad/")
def vlad_index():
    posts = get_vlad_blog()
    return render_template("vlad_index.html", posts=posts)

@app.route("/vlad/<slug>/")
def vlad_post(slug):
    md_path = VLAD_DIR / f"{slug}.md"
    if not md_path.exists(): abort(404)
    md_text = md_path.read_text(encoding="utf-8")
    html = markdown.markdown( md_text, extensions=["fenced_code", "tables", "toc"] )
    return render_template("vlad_post.html", content=html, slug=slug)

# ----------------

def get_posts():
    posts = [] # list available markdown posts
    for path in BLOG_DIR.glob("*.md"): posts.append({ "slug": path.stem, "title": path.stem.replace("-", " ").title() })
    posts.sort(key=lambda p: p["slug"], reverse=True)
    return posts

@app.route("/blog/")
def blog_index():
    posts = get_posts()
    return render_template("blog_index.html", posts=posts)

@app.route("/blog/<slug>/")
def blog_post(slug):
    md_path = BLOG_DIR / f"{slug}.md"
    if not md_path.exists(): abort(404)
    md_text = md_path.read_text(encoding="utf-8")
    html = markdown.markdown( md_text, extensions=["fenced_code", "tables", "toc"] )
    return render_template("blog_post.html", content=html, slug=slug)

# ---------- DB HELPERS ----------

def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            address    TEXT PRIMARY KEY,
            credits    INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Pool of merchant-owned deposit addresses (public addresses only).
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS deposit_pool (
            address     TEXT PRIMARY KEY,
            assigned_to TEXT,           -- user wallet address (lowercased)
            assigned_at DATETIME,
            is_active   INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    # Track deposits to avoid double-crediting
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS deposits (
            tx_hash         TEXT PRIMARY KEY,
            user_address    TEXT NOT NULL,
            deposit_address TEXT NOT NULL,
            value_wei       INTEGER NOT NULL,
            block_number    INTEGER,
            confirmations   INTEGER NOT NULL DEFAULT 0,
            is_error        INTEGER NOT NULL DEFAULT 0,
            is_credited     INTEGER NOT NULL DEFAULT 0,
            credited_credits INTEGER NOT NULL DEFAULT 0,
            credited_at     DATETIME,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    db.commit()
    db.close()

@app.before_request
def setup_db():
    init_db()

# get the db method
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# close the db
@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None: db.close()

# get the user
def get_user(address: str):
    db = get_db()
    cur = db.execute("SELECT address, credits FROM users WHERE address = ?", (address.lower(),))
    return cur.fetchone()

# return user row, creating it with 0 credits if missing
def get_or_create_user(address: str):
    db = get_db()
    cur = db.execute("SELECT address, credits FROM users WHERE address = ?", (address.lower(),))
    row = cur.fetchone()
    if row: return row
    db.execute("INSERT INTO users (address, credits) VALUES (?, 0)", (address.lower(),))
    db.commit()
    cur = db.execute("SELECT address, credits FROM users WHERE address = ?", (address.lower(),))
    return cur.fetchone()

# get top users by credits
def get_top_users(limit: int = 20):
    db = get_db()
    cur = db.execute(
        "SELECT address, credits FROM users ORDER BY credits DESC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()

# ---------- Leaderboard ---------- #

@app.route("/leaderboard/")
def leaderboard():
    users = get_top_users(10)
    return render_template("leaderboard.html", users=users)

# ---------- Wallet connection and top-ups ---------- #

@app.route("/wallet/")
def wallet(): return render_template("wallet.html")

# accept tar.gz archive of project from CLI, extract to tmp, runs analysis, returns JSON payload the CLI expects
@app.route("/api/scan", methods=["POST"])
def api_scan():
    upload = request.files.get("file")
    if not upload: return jsonify({"ok": False, "error": "missing_file"}), 400
    project_type = (request.form.get("project_type") or "unknown").strip()
    skip_compile_flag = (request.form.get("skip_compile") or "false").strip().lower()
    skip_compile = skip_compile_flag in ("1", "true", "yes")
    tmp_dir = tempfile.mkdtemp(prefix="thrum-scan-")
    archive_path = os.path.join(tmp_dir, upload.filename or "project.tar.gz")
    try:
        # save and extract archive
        upload.save(archive_path)
        extract_dir = os.path.join(tmp_dir, "project")
        os.makedirs(extract_dir, exist_ok=True)
        try:
            with tarfile.open(archive_path, "r:gz") as tf: tf.extractall(extract_dir)
        except tarfile.ReadError:
            with tarfile.open(archive_path, "r:") as tf: tf.extractall(extract_dir)
        print(f"[thrum] scan received. project_type={project_type}, skip_compile={skip_compile}")
        print(f"[thrum] extracted to {extract_dir}")

        # Run dummy analysis [replace soon]
        summary, report_markdown = analyze_project(extract_dir)

        # Ensure summary has needed keys
        crit = int(summary.get("critical", 0))
        high = int(summary.get("high", 0))
        med = int(summary.get("medium", 0))
        low = int(summary.get("low", 0))

        resp = {
            "ok": True,
            "summary": {
                "critical": crit,
                "high": high,
                "medium": med,
                "low": low,
            },
            "report_markdown": report_markdown,
            "report_path_hint": "thrum-report.md",
        }
        return jsonify(resp), 200
    except Exception as e:
        print(f"[thrum] scan error: {e}")
        return jsonify({"ok": False, "error": f"scan_failed: {e}"}), 500
    finally:
        try: shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception: pass

# frontend passes address, backend returns message to sign, we store nonce+addr in session for verification later
@app.route("/api/wallet/nonce", methods=["GET"])
def api_wallet_nonce():
    addr = request.args.get("address", "", type=str).strip()
    if not addr or not addr.startswith("0x") or len(addr) != 42: return jsonify({"ok": False, "error": "invalid address"}), 400

    nonce = secrets.token_hex(16)
    session["siwe_nonce"] = nonce
    session["siwe_address"] = addr.lower()
    msg = f"thrum login\n\naddress: {addr}\nnonce: {nonce}"
    return jsonify({
        "ok": True,
        "message": msg,
        "address": addr
    })

# frontend sends {addr, msg, sig}, we recover the addr from the sig and compare
@app.route("/api/wallet/verify", methods=["POST"])
def api_wallet_verify():
    data = request.get_json(silent=True) or {}
    address = (data.get("address") or "").strip()
    message = data.get("message") or ""
    signature = data.get("signature") or ""

    if not address or not message or not signature: return jsonify({"ok": False, "error": "missing_fields"}), 400

    expected_nonce = session.get("siwe_nonce")
    expected_addr = (session.get("siwe_address") or "").lower()

    if not expected_nonce or not expected_addr: return jsonify({"ok": False, "error": "no_nonce_in_session"}), 400

    if expected_nonce not in message: return jsonify({"ok": False, "error": "nonce_mismatch"}), 400

    try:
        encoded = encode_defunct(text=message)
        recovered = Account.recover_message(encoded, signature=signature)
    except Exception as e:
        return jsonify({"ok": False, "error": f"recover_failed: {e}"}), 400

    if recovered.lower() != expected_addr or recovered.lower() != address.lower(): return jsonify({"ok": False, "error": "address_mismatch"}), 400

    session["wallet_logged_in"] = True
    session["wallet_address"] = recovered.lower()
    # create / fetch user and credits
    user = get_or_create_user(recovered.lower())
    short = recovered[:6] + "..." + recovered[-4:]
    return jsonify({ "ok": True, "address": recovered, "display": short, "credits": user["credits"] })

# return current logged-in wallet + credits
# @app.route("/api/me", methods=["GET"])
# def api_me():
#     addr = session.get("wallet_address")
#     if not addr: return jsonify({"ok": False, "error": "not_logged_in"}), 401
#     user = get_user(addr)
#     if not user: user = get_or_create_user(addr)
#     return jsonify({ "ok": True, "address": user["address"], "credits": user["credits"] })
@app.route("/api/me", methods=["GET"])
def api_me():
    addr = auth_addr_from_request()
    if not addr: return jsonify({"ok": False, "error": "not_logged_in"}), 401
    user = get_user(addr)
    if not user: user = get_or_create_user(addr)
    return jsonify({"ok": True, "address": user["address"], "credits": int(user["credits"])})

# ------ Graphs ------

def generate_graph_data():
    # Time labels for Thrum Index (like -29d, -24d, ..., today)
    labels = ["-29d", "-24d", "-19d", "-14d", "-9d", "-4d", "today"]

    # Random walk around 0.8 for "bug density"
    base = 0.8
    steps = np.random.normal(loc=0.0, scale=0.05, size=len(labels))
    series = []
    current = base
    for step in steps:
        current = max(0.2, min(1.5, current + step))  # clamp to [0.2, 1.5]
        series.append(round(float(current), 3))

    # Severity counts as random-ish small integers
    crit = int(np.random.poisson(lam=10))
    high = int(np.random.poisson(lam=35))
    med = int(np.random.poisson(lam=80))
    low = int(np.random.poisson(lam=140))

    # KPIs – fake but coherent
    total_scans = int(np.random.randint(1000, 1500))
    contracts_analyzed = int(total_scans * np.random.uniform(4.5, 6.5))
    crit_scan_rate = round(
        100.0 * np.random.uniform(0.15, 0.22), 1
    )  # 15–22%
    avg_verdict_secs = int(np.random.uniform(35, 65))

    # Ecosystem "tape"
    ecosystems = [
        {"name": "eth", "crit_per_scan": round(float(np.random.uniform(0.15, 0.25)), 2),
         "volume": int(np.random.randint(400, 600))},
        {"name": "arb", "crit_per_scan": round(float(np.random.uniform(0.10, 0.18)), 2),
         "volume": int(np.random.randint(150, 260))},
        {"name": "op", "crit_per_scan": round(float(np.random.uniform(0.12, 0.2)), 2),
         "volume": int(np.random.randint(120, 220))},
        {"name": "base", "crit_per_scan": round(float(np.random.uniform(0.06, 0.14)), 2),
         "volume": int(np.random.randint(90, 170))},
        {"name": "other", "crit_per_scan": round(float(np.random.uniform(0.08, 0.16)), 2),
         "volume": int(np.random.randint(180, 260))},
    ]

    # Vuln families
    vuln_families = [
        {"family": "mv-si", "findings": int(np.random.randint(40, 80)),
         "crit_rate": int(np.random.randint(20, 35)), "ttd_secs": int(np.random.randint(30, 55))},
        {"family": "reentrancy", "findings": int(np.random.randint(30, 60)),
         "crit_rate": int(np.random.randint(15, 28)), "ttd_secs": int(np.random.randint(40, 65))},
        {"family": "upgrade-safety", "findings": int(np.random.randint(25, 55)),
         "crit_rate": int(np.random.randint(12, 24)), "ttd_secs": int(np.random.randint(38, 60))},
        {"family": "oracle", "findings": int(np.random.randint(15, 35)),
         "crit_rate": int(np.random.randint(10, 20)), "ttd_secs": int(np.random.randint(45, 70))},
        {"family": "access-control", "findings": int(np.random.randint(10, 30)),
         "crit_rate": int(np.random.randint(5, 15)), "ttd_secs": int(np.random.randint(25, 45))},
    ]

    # "tape" – recent scans
    # just synthesize a few timestamps going back
    now = int(time.time())
    tape_rows = []
    networks = ["eth", "arb", "base", "op", "other"]
    severities = ["none", "low", "medium", "high", "crit"]
    for i in range(10):
        t = now - i * np.random.randint(300, 900)
        ts = time.strftime("%H:%M:%S utc", time.gmtime(t))
        net = np.random.choice(networks)
        sev = np.random.choice(severities, p=[0.2, 0.3, 0.25, 0.15, 0.1])
        if sev == "none":
            findings_str = "0 findings"
        else:
            findings_str = f"{int(np.random.randint(1, 8))} findings · {sev}"
        tape_rows.append({"timestamp": ts, "network": net, "summary": findings_str})

    return {
        "index_labels": labels,
        "index_series": series,
        "total_scans": total_scans,
        "contracts_analyzed": contracts_analyzed,
        "crit_scan_rate": crit_scan_rate,
        "avg_verdict_secs": avg_verdict_secs,
        "severity_counts": {
            "critical": crit,
            "high": high,
            "medium": med,
            "low": low,
        },
        "ecosystems": ecosystems,
        "vuln_families": vuln_families,
        "tape": tape_rows,
    }

@app.route("/graphs/")
def graphs():
    data = generate_graph_data()
    return render_template("graphs.html", graph_data=data)

@app.route("/api/graphs/random")
def graphs_random():
    data = generate_graph_data()
    return jsonify(data)

@app.route("/", methods=["GET"])
def index():
    host = (request.host or "").split(":")[0]
    if host.startswith("get."):
        return app.send_static_file("install.sh")
    else:
        top = get_top_users(3)
        return render_template("index.html", top_users=top)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5028, debug=True)