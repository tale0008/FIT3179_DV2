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

# 0. country code format (need this to join to TopoJSON later)
q("0. Sample country codes", """
    SELECT id, code, name FROM stddata_country ORDER BY name LIMIT 15
""")

# 1. Country coverage
q("1. Series per country (top 30)", """
    SELECT c.name, c.code, COUNT(*) AS series_ct, SUM(s.issue_count) AS issue_ct
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    WHERE s.deleted = 0 AND s.is_comics_publication = 1
    GROUP BY c.id ORDER BY series_ct DESC LIMIT 30
""", limit=30)

# 2. THE BIG ONE: Australian output by year
q("2. Australian series started per year (1930-2026)", """
    SELECT s.year_began, COUNT(*) AS series_ct, SUM(s.issue_count) AS issue_ct
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    WHERE c.name LIKE '%Australia%'
      AND s.deleted = 0 AND s.is_comics_publication = 1
      AND s.year_began BETWEEN 1930 AND 2026
    GROUP BY s.year_began ORDER BY s.year_began
""", limit=100)

# 3. Reprint coverage - issue level
q("3a. Reprint rows: fill rate of the two link types", """
    SELECT
      COUNT(*) AS total_rows,
      SUM(CASE WHEN origin_issue_id IS NOT NULL THEN 1 ELSE 0 END) AS has_issue_link,
      SUM(CASE WHEN origin_id IS NOT NULL THEN 1 ELSE 0 END) AS has_story_link
    FROM gcd_reprint
""")

q("3b. Cross-country reprint flows (top 25)", """
    SELECT oc.name AS origin_country, tc.name AS target_country, COUNT(*) AS n
    FROM gcd_reprint r
    JOIN gcd_issue oi ON oi.id = r.origin_issue_id
    JOIN gcd_series os ON os.id = oi.series_id
    JOIN stddata_country oc ON oc.id = os.country_id
    JOIN gcd_issue ti ON ti.id = r.target_issue_id
    JOIN gcd_series ts ON ts.id = ti.series_id
    JOIN stddata_country tc ON tc.id = ts.country_id
    WHERE oc.id != tc.id
    GROUP BY oc.id, tc.id ORDER BY n DESC LIMIT 25
""", limit=25)

q("3c. Reprints landing in Australia, by origin", """
    SELECT oc.name AS origin_country, COUNT(*) AS n
    FROM gcd_reprint r
    JOIN gcd_issue oi ON oi.id = r.origin_issue_id
    JOIN gcd_series os ON os.id = oi.series_id
    JOIN stddata_country oc ON oc.id = os.country_id
    JOIN gcd_issue ti ON ti.id = r.target_issue_id
    JOIN gcd_series ts ON ts.id = ti.series_id
    JOIN stddata_country tc ON tc.id = ts.country_id
    WHERE tc.name LIKE '%Australia%'
    GROUP BY oc.id ORDER BY n DESC LIMIT 20
""", limit=20)

# 4. Creator birthplace fill rate
q("4. Creator birthplace fill rate", """
    SELECT
      COUNT(*) AS total,
      SUM(CASE WHEN birth_country_id IS NOT NULL THEN 1 ELSE 0 END) AS has_country,
      SUM(CASE WHEN birth_province IS NOT NULL AND birth_province != '' THEN 1 ELSE 0 END) AS has_province,
      SUM(CASE WHEN birth_city IS NOT NULL AND birth_city != '' THEN 1 ELSE 0 END) AS has_city
    FROM gcd_creator WHERE deleted = 0
""")

q("4b. Creators by birth country (top 20)", """
    SELECT c.name, COUNT(*) AS n
    FROM gcd_creator cr
    JOIN stddata_country c ON c.id = cr.birth_country_id
    WHERE cr.deleted = 0
    GROUP BY c.id ORDER BY n DESC LIMIT 20
""", limit=20)

# 5. Genre mess
q("5. Raw genre values (top 40)", """
    SELECT genre, COUNT(*) AS n
    FROM gcd_story
    WHERE deleted = 0 AND genre IS NOT NULL AND genre != ''
    GROUP BY genre ORDER BY n DESC LIMIT 40
""", limit=40)

# 6. Scale check
q("6. Row counts", """
    SELECT 'series' AS t, COUNT(*) FROM gcd_series WHERE deleted = 0
    UNION ALL SELECT 'issues', COUNT(*) FROM gcd_issue WHERE deleted = 0
    UNION ALL SELECT 'stories', COUNT(*) FROM gcd_story WHERE deleted = 0
    UNION ALL SELECT 'creators', COUNT(*) FROM gcd_creator WHERE deleted = 0
    UNION ALL SELECT 'reprints', COUNT(*) FROM gcd_reprint
""")

conn.close()