import os, tempfile, tarfile, shutil, secrets
from flask import Flask, render_template, abort, request, jsonify, session, g
from pathlib import Path
import markdown
import sqlite3
from eth_account import Account
from eth_account.messages import encode_defunct
app = Flask(__name__)
app.secret_key = "1c5da44f5c278ac7f41f666501347d7572a18ae6"
BLOG_DIR = Path("templates/blog")
DATABASE = "thrum.db"

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

@app.route("/docs/")
def docs(): return render_template("docs.html")

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

# create users table if not existing
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
@app.route("/api/me", methods=["GET"])
def api_me():
    addr = session.get("wallet_address")
    if not addr: return jsonify({"ok": False, "error": "not_logged_in"}), 401
    user = get_user(addr)
    if not user: user = get_or_create_user(addr)
    return jsonify({ "ok": True, "address": user["address"], "credits": user["credits"] })

@app.route("/")
def index():
    top = get_top_users(3)
    return render_template("index.html", top_users=top)

if __name__ == "__main__": app.run(host="0.0.0.0", port=5028, debug=True)