import sqlite3

conn = sqlite3.connect("gcd.db")
cur = conn.cursor()

def q(label, sql, limit=25):
    print(f"\n{'='*60}\n{label}\n{'='*60}")
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows[:limit]:
        print("  ", r)
    if len(rows) > limit:
        print(f"   ... ({len(rows)} rows total)")

# check the 1950 spike
q("1950 spike check", """
    SELECT year_began, COUNT(*) AS n,
           SUM(year_began_uncertain) AS uncertain
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    WHERE c.code = 'au' AND s.deleted = 0 AND s.is_comics_publication = 1
      AND year_began BETWEEN 1945 AND 1955
    GROUP BY year_began
""", limit=15)

# distinct AU issues that are reprints
q("AU issues that are reprints (distinct)", """
    SELECT COUNT(DISTINCT r.target_issue_id) AS au_issues_that_are_reprints
    FROM gcd_reprint r
    JOIN gcd_issue ti ON ti.id = r.target_issue_id
    JOIN gcd_series ts ON ts.id = ti.series_id
    JOIN stddata_country tc ON tc.id = ts.country_id
    WHERE tc.code = 'au'
""")

# creator fill rate within US/JP/AU specifically
q("Creator birth-province fill by country", """
    SELECT c.name,
           COUNT(*) AS creators,
           SUM(CASE WHEN cr.birth_province != '' THEN 1 ELSE 0 END) AS has_province
    FROM gcd_creator cr
    JOIN stddata_country c ON c.id = cr.birth_country_id
    WHERE cr.deleted = 0 AND c.code IN ('us','jp','au')
    GROUP BY c.id
""")

conn.close()