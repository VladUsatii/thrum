# scripts/import_deposit_pool.py
import sqlite3, sys

DB = "thrum.db"

def main(path: str):
    addrs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            a = line.strip()
            if not a: continue
            addrs.append(a.lower())

    db = sqlite3.connect(DB)
    db.execute("CREATE TABLE IF NOT EXISTS deposit_pool (address TEXT PRIMARY KEY, assigned_to TEXT, assigned_at DATETIME, is_active INTEGER NOT NULL DEFAULT 1)")
    inserted = 0
    for a in addrs:
        try:
            db.execute("INSERT OR IGNORE INTO deposit_pool (address, assigned_to, assigned_at, is_active) VALUES (?, NULL, NULL, 1)", (a,))
            inserted += db.total_changes
        except Exception as e:
            print("skip", a, e)
    db.commit()
    db.close()
    print(f"done. inserted={inserted}, total_lines={len(addrs)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python scripts/import_deposit_pool.py deposit_addresses.txt")
        sys.exit(2)
    main(sys.argv[1])