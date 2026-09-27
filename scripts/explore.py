import sqlite3

conn = sqlite3.connect("gcd.db")
cur = conn.cursor()

tables = [
    "gcd_series", "gcd_issue", "gcd_story", "gcd_publisher",
    "gcd_creator", "gcd_reprint", "stddata_country", "stddata_language",
]

for t in tables:
    print(f"\n=== {t} ===")
    cur.execute(f"PRAGMA table_info({t})")
    for cid, name, coltype, notnull, default, pk in cur.fetchall():
        print(f"  {name}  ({coltype})")

conn.close()