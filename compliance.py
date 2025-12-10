import json, re, time, hashlib, requests
from dataclasses import dataclass
from typing import Optional, Set, Tuple

ETH_ADDR_RE = re.compile(rb"0x[a-fA-F0-9]{40}")

# Dedicated exception for sanction list failures
class SanctionsDataUnavailable(RuntimeError): pass

@dataclass
class ComplianceConfig:
    enforce_sanctions: bool = True
    sanctions_cache_ttl_seconds: int = 24 * 60 * 60

    # OFAC list URLs
    ofac_sdn_advanced_url: str = "https://www.treasury.gov/ofac/downloads/sanctions/1.0/sdn_advanced.xml"
    ofac_cons_advanced_url: str = "https://www.treasury.gov/ofac/downloads/sanctions/1.0/cons_advanced.xml"

    # Evidence/versioning
    terms_version: str = "v1"
    privacy_version: str = "v1"
    disclosures_version: str = "v1"

class ComplianceEngine(object):
    def __init__(self, cfg: ComplianceConfig): self.cfg = cfg

    def _ensure_column(self, db, table: str, col: str, coltype: str):
        try: db.execute(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}")
        except Exception: pass

    def _download_extract_eth_addrs(self):
        addrs, h = set(), hashlib.sha256()

        # If someone configured the deprecated path, try the modern one first
        def candidates(url: str):
            if url.endswith("/ofac/downloads/sdn_advanced.xml"): return [ "https://www.treasury.gov/ofac/downloads/sanctions/1.0/sdn_advanced.xml", url ]
            if url.endswith("/ofac/downloads/cons_advanced.xml"): return [ "https://www.treasury.gov/ofac/downloads/sanctions/1.0/cons_advanced.xml", url ]
            return [url]

        urls = []
        for u in (self.cfg.ofac_sdn_advanced_url, self.cfg.ofac_cons_advanced_url): urls.extend(candidates(u))

        last_err = None
        for url in urls:
            try:
                r = requests.get( url, timeout=60, headers={"User-Agent": "ThrumCompliance/1.0"} )
                r.raise_for_status()
                content = r.content
                h.update(content)
                for m in ETH_ADDR_RE.finditer(content): addrs.add(m.group(0).decode("ascii").lower())
            except Exception as e:
                last_err = e
                continue

        if not addrs: raise SanctionsDataUnavailable(f"Could not fetch any OFAC advanced XML: {last_err}")
        return addrs, h.hexdigest()

    def _load_cached_addrs(self, db, allow_stale: bool) -> Optional[Set[str]]:
        row = db.execute("SELECT updated_at, addrs_json FROM ofac_eth_cache WHERE id = 1").fetchone()
        if not row: return None
        updated_at = int(row["updated_at"])
        expired = (int(time.time()) - updated_at) > int(self.cfg.sanctions_cache_ttl_seconds)
        if expired and not allow_stale: return None
        try: return set(json.loads(row["addrs_json"]) or [])
        except Exception: return None

    def _refresh_cache_if_needed(self, db) -> Set[str]:
        fresh = self._load_cached_addrs(db, allow_stale=False)
        if fresh is not None: return fresh

        # Keep stale as emergency fallback
        stale = self._load_cached_addrs(db, allow_stale=True)
        try: addrs, digest = self._download_extract_eth_addrs()
        except Exception as e:
            if stale is not None: return stale
            raise SanctionsDataUnavailable(str(e))

        now = int(time.time())
        db.execute(
            """
            INSERT INTO ofac_eth_cache (id, updated_at, sha256, addrs_json)
            VALUES (1, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
            updated_at=excluded.updated_at,
            sha256=excluded.sha256,
            addrs_json=excluded.addrs_json
            """,
            (now, digest, json.dumps(sorted(addrs))),
        )
        db.commit()
        return addrs

    # Schema
    def ensure_schema(self, db):
        # (1) Consent log
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS consent_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_address TEXT NOT NULL,
                kind TEXT NOT NULL,              -- e.g., "purchase"
                value_wei INTEGER,               -- intended purchase amount (optional but recommended)
                tier TEXT,                       -- "basic"/"pro"/"enterprise"/custom
                terms_version TEXT,
                privacy_version TEXT,
                disclosures_version TEXT,
                ip TEXT,
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # (2) Sanctions cache to store extracted ETH addresses only (manual OFAC review)
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS ofac_eth_cache (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                updated_at INTEGER NOT NULL,
                sha256 TEXT NOT NULL,
                addrs_json TEXT NOT NULL
            )
            """
        )

        # (3) Trail of screening events
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS screening_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_type TEXT NOT NULL,      -- "wallet" | "tx_from"
                subject_value TEXT NOT NULL,
                matched INTEGER NOT NULL,        -- 0/1
                source TEXT NOT NULL,            -- "ofac"
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        self._ensure_column(db, "deposits", "from_address", "TEXT")
        self._ensure_column(db, "deposits", "compliance_status", "TEXT")
        self._ensure_column(db, "deposits", "compliance_reason", "TEXT")
        db.commit()

    def is_sanctioned_eth(self, db, addr: str) -> bool:
        if not addr: return False
        a = addr.lower()
        if not a.startswith("0x") or len(a) != 42: return False
        try: addrs = self._refresh_cache_if_needed(db)
        except SanctionsDataUnavailable: raise
        return a in addrs

    def record_screening(self, db, subject_type: str, subject_value: str, matched: bool):
        db.execute(
            """
            INSERT INTO screening_events (subject_type, subject_value, matched, source)
            VALUES (?, ?, ?, 'ofac')
            """,
            (subject_type, (subject_value or "").lower(), 1 if matched else 0),
        )
        db.commit()

    def guard_not_sanctioned(self, db, addr: str, subject_type: str):
        try: matched = self.is_sanctioned_eth(db, addr)
        except SanctionsDataUnavailable as e: raise PermissionError("sanctions_unavailable") from e
        self.record_screening(db, subject_type, addr, matched)
        if self.cfg.enforce_sanctions and matched: raise PermissionError("sanctions_match")

    # Consent (clickwrap) logging
    def record_consent(
        self,
        db,
        user_address: str,
        kind: str,
        value_wei: Optional[int],
        tier: Optional[str],
        ip: Optional[str],
        user_agent: Optional[str],
    ):
        db.execute(
            """
            INSERT INTO consent_events
              (user_address, kind, value_wei, tier, terms_version, privacy_version, disclosures_version, ip, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_address.lower(),
                kind,
                int(value_wei) if value_wei is not None else None,
                tier,
                self.cfg.terms_version,
                self.cfg.privacy_version,
                self.cfg.disclosures_version,
                ip,
                user_agent,
            ),
        )
        db.commit()

    # “Minimum viable evidence”
    def has_matching_purchase_consent(self, db, user_address: str, value_wei: int, lookback_seconds: int = 2 * 60 * 60) -> bool:
        cutoff = int(time.time()) - int(lookback_seconds)
        row = db.execute(
            """
            SELECT 1
            FROM consent_events
            WHERE user_address = ?
              AND kind = 'purchase'
              AND value_wei = ?
              AND strftime('%s', created_at) >= ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_address.lower(), int(value_wei), cutoff),
        ).fetchone()
        return row is not None

    # Deposit compliance decision
    def apply_deposit_compliance(self, db, user_address: str, tx_hash: str, from_address: str, value_wei: int) -> Tuple[bool, str]:
        ua = (user_address or "").lower()
        txh = (tx_hash or "").lower()
        fa = (from_address or "").lower()

        # Sanctions screening (robust + honors enforce_sanctions)
        try: matched = self.is_sanctioned_eth(db, fa)
        except Exception as e:
            status = "held_screening_unavailable" if self.cfg.enforce_sanctions else "ok"
            reason = f"Sanctions screening unavailable: {type(e).__name__}"
            self.record_screening(db, "tx_from", fa, False)
            self._mark_deposit(db, txh, fa, status, reason)
            return (False, status) if self.cfg.enforce_sanctions else (True, "ok")

        self.record_screening(db, "tx_from", fa, bool(matched))

        if matched:
            if self.cfg.enforce_sanctions:
                self._mark_deposit(db, txh, fa, "blocked_sanctions", "OFAC match on tx.from")
                return False, "blocked_sanctions"
            # Screening match, but enforcement disabled -> allow crediting while preserving evidence
            self._mark_deposit(db, txh, fa, "ok", "OFAC match on tx.from (enforcement disabled)")
            return True, "ok"

        # Consent gate
        try: v = int(value_wei)
        except Exception: v = 0

        if v <= 0:
            self._mark_deposit(db, txh, fa, "held_no_consent", "Invalid value_wei")
            return False, "held_no_consent"
        if not self.has_matching_purchase_consent(db, ua, v):
            self._mark_deposit(db, txh, fa, "held_no_consent", "No matching purchase consent for value_wei")
            return False, "held_no_consent"
        self._mark_deposit(db, txh, fa, "ok", "")
        return True, "ok"

    def _mark_deposit(self, db, tx_hash: str, from_address: str, status: str, reason: str):
        db.execute(
            """
            UPDATE deposits
            SET from_address = COALESCE(?, from_address),
                compliance_status = ?,
                compliance_reason = ?
            WHERE tx_hash = ?
            """,
            ((from_address or "").lower(), status, reason, (tx_hash or "").lower()),
        )
        db.commit()