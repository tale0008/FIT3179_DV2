"""
FIT3179 DV2 - GCD data export
Aggregates the Grand Comics Database SQLite dump down to small CSVs for Vega-Lite.
"""

import sqlite3
import csv
import os
from collections import defaultdict

DB_PATH = r"C:\Personal\Code\UNI\Sem 7\FIT3179 Data Visualisation\A2\Repo\FIT3179_DV2\gcd.db"
OUT_DIR = r"C:\Personal\Code\UNI\Sem 7\FIT3179 Data Visualisation\A2\Repo\FIT3179_DV2\gcd export"

os.makedirs(OUT_DIR, exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()


def write_csv(filename, header, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    size_kb = os.path.getsize(path) / 1024
    print(f"  {filename:<34} {len(rows):>6} rows  {size_kb:>7.1f} KB")


print("Creating indexes (one-off, slow the first time)...")
for stmt in [
    "CREATE INDEX IF NOT EXISTS ix_series_country ON gcd_series(country_id)",
    "CREATE INDEX IF NOT EXISTS ix_issue_series   ON gcd_issue(series_id)",
    "CREATE INDEX IF NOT EXISTS ix_story_issue    ON gcd_story(issue_id)",
    "CREATE INDEX IF NOT EXISTS ix_reprint_target ON gcd_reprint(target_issue_id)",
    "CREATE INDEX IF NOT EXISTS ix_reprint_origin ON gcd_reprint(origin_issue_id)",
    "CREATE INDEX IF NOT EXISTS ix_creator_birth  ON gcd_creator(birth_country_id)",
]:
    cur.execute(stmt)
conn.commit()
print("Indexes ready.\n")

# Shared filter: live, comics-only series
LIVE = "s.deleted = 0 AND s.is_comics_publication = 1"

print("Exporting...")


# ---------------------------------------------------------------
# 1. country_output.csv   ->  M1 world choropleth
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT c.code, c.name,
           COUNT(DISTINCT s.id) AS series_count,
           COUNT(DISTINCT i.id) AS issue_count
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    LEFT JOIN gcd_issue i ON i.series_id = s.id AND i.deleted = 0
    WHERE {LIVE} AND c.code NOT IN ('zz', 'xx')
    GROUP BY c.id
    HAVING issue_count > 0
    ORDER BY issue_count DESC
""")
rows = cur.fetchall()
# issues per series is the bonus chart, computed here so the CSV carries it
rows = [(code, name, sc, ic, round(ic / sc, 2) if sc else 0)
        for code, name, sc, ic in rows]
write_csv("country_output.csv",
          ["code", "country", "series", "issues", "issues_per_series"], rows)


# ---------------------------------------------------------------
# 2. country_year.csv   ->  C1 ridgeline
#    Top 15 countries only, certain years only
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT c.code
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    WHERE {LIVE} AND c.code NOT IN ('zz', 'xx')
    GROUP BY c.id ORDER BY COUNT(*) DESC LIMIT 15
""")
top15 = [r[0] for r in cur.fetchall()]
placeholders = ",".join("?" * len(top15))

cur.execute(f"""
    SELECT c.code, c.name, s.year_began, COUNT(*) AS n
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    WHERE {LIVE}
      AND s.year_began_uncertain = 0
      AND s.year_began BETWEEN 1930 AND 2026
      AND c.code IN ({placeholders})
    GROUP BY c.id, s.year_began
    ORDER BY c.name, s.year_began
""", top15)
write_csv("country_year.csv", ["code", "country", "year", "series"], cur.fetchall())


# ---------------------------------------------------------------
# 3. country_genre.csv   ->  C2 heatmap matrix
#    genre is semicolon-delimited free text; aggregate in SQL first,
#    then split in Python so we never pull 4.5m rows into memory
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT c.code, c.name, st.genre, COUNT(*) AS n
    FROM gcd_story st
    JOIN gcd_issue i  ON i.id = st.issue_id
    JOIN gcd_series s ON s.id = i.series_id
    JOIN stddata_country c ON c.id = s.country_id
    WHERE st.deleted = 0 AND i.deleted = 0 AND {LIVE}
      AND st.genre IS NOT NULL AND st.genre != ''
      AND c.code IN ({placeholders})
    GROUP BY c.id, st.genre
""", top15)

split_counts = defaultdict(int)
country_names = {}
for code, name, genre_raw, n in cur.fetchall():
    country_names[code] = name
    for g in genre_raw.split(";"):
        g = g.strip().lower()
        if g:
            split_counts[(code, g)] += n

# keep the 15 largest genres overall, bucket the rest
genre_totals = defaultdict(int)
for (code, g), n in split_counts.items():
    genre_totals[g] += n
top_genres = {g for g, _ in sorted(genre_totals.items(),
                                   key=lambda kv: -kv[1])[:15]}

final = defaultdict(int)
for (code, g), n in split_counts.items():
    final[(code, g if g in top_genres else "other")] += n

rows = [(code, country_names[code], g, n) for (code, g), n in sorted(final.items())]
write_csv("country_genre.csv", ["code", "country", "genre", "stories"], rows)


# ---------------------------------------------------------------
# 4. reprint_shares.csv   ->  C7 waffle
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT tc.code, tc.name,
           COUNT(DISTINCT i.id) AS total_issues,
           COUNT(DISTINCT CASE WHEN oc.id != tc.id THEN r.target_issue_id END) AS foreign_reprints,
           COUNT(DISTINCT CASE WHEN oc.id  = tc.id THEN r.target_issue_id END) AS domestic_reprints
    FROM gcd_issue i
    JOIN gcd_series s ON s.id = i.series_id
    JOIN stddata_country tc ON tc.id = s.country_id
    LEFT JOIN gcd_reprint r ON r.target_issue_id = i.id
    LEFT JOIN gcd_issue oi ON oi.id = r.origin_issue_id
    LEFT JOIN gcd_series os ON os.id = oi.series_id
    LEFT JOIN stddata_country oc ON oc.id = os.country_id
    WHERE i.deleted = 0 AND {LIVE}
    GROUP BY tc.id
    HAVING total_issues > 5000
    ORDER BY (CAST(foreign_reprints AS FLOAT) / total_issues) DESC
""")
rows = []
for code, name, total, foreign, domestic in cur.fetchall():
    rows.append((code, name, total, foreign, domestic,
                 total - foreign - domestic,
                 round(100.0 * foreign / total, 2),
                 round(100.0 * domestic / total, 2)))
write_csv("reprint_shares.csv",
          ["code", "country", "total_issues", "foreign_reprints",
           "domestic_reprints", "original", "pct_foreign", "pct_domestic"], rows)


# ---------------------------------------------------------------
# 5. reprint_flows.csv   ->  M4 flow map
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT oc.code, oc.name, tc.code, tc.name, COUNT(*) AS n
    FROM gcd_reprint r
    JOIN gcd_issue oi ON oi.id = r.origin_issue_id
    JOIN gcd_series os ON os.id = oi.series_id
    JOIN stddata_country oc ON oc.id = os.country_id
    JOIN gcd_issue ti ON ti.id = r.target_issue_id
    JOIN gcd_series ts ON ts.id = ti.series_id
    JOIN stddata_country tc ON tc.id = ts.country_id
    WHERE oc.id != tc.id
    GROUP BY oc.id, tc.id
    HAVING n >= 100
    ORDER BY n DESC
""")
write_csv("reprint_flows.csv",
          ["origin_code", "origin", "target_code", "target", "reprints"],
          cur.fetchall())


# ---------------------------------------------------------------
# 6. au_series_by_year.csv   ->  C8 horizon chart
# ---------------------------------------------------------------
cur.execute(f"""
    SELECT s.year_began,
           COUNT(DISTINCT s.id) AS series,
           COUNT(DISTINCT i.id) AS issues
    FROM gcd_series s
    JOIN stddata_country c ON c.id = s.country_id
    LEFT JOIN gcd_issue i ON i.series_id = s.id AND i.deleted = 0
    WHERE {LIVE} AND c.code = 'au'
      AND s.year_began_uncertain = 0
      AND s.year_began BETWEEN 1930 AND 2026
    GROUP BY s.year_began ORDER BY s.year_began
""")
write_csv("au_series_by_year.csv", ["year", "series", "issues"], cur.fetchall())


# ---------------------------------------------------------------
# 7. us_creators_by_state.csv   ->  M3 state choropleth
# ---------------------------------------------------------------
cur.execute("""
    SELECT cr.birth_province, COUNT(*) AS n
    FROM gcd_creator cr
    JOIN stddata_country c ON c.id = cr.birth_country_id
    WHERE cr.deleted = 0 AND c.code = 'us'
      AND cr.birth_province IS NOT NULL AND cr.birth_province != ''
    GROUP BY cr.birth_province ORDER BY n DESC
""")
write_csv("us_creators_by_state.csv", ["state", "creators"], cur.fetchall())


# ---------------------------------------------------------------
# 8. creators_by_country.csv   ->  supporting stat
# ---------------------------------------------------------------
cur.execute("""
    SELECT c.code, c.name, COUNT(*) AS n
    FROM gcd_creator cr
    JOIN stddata_country c ON c.id = cr.birth_country_id
    WHERE cr.deleted = 0
    GROUP BY c.id HAVING n >= 20 ORDER BY n DESC
""")
write_csv("creators_by_country.csv", ["code", "country", "creators"], cur.fetchall())


conn.close()
print("\nDone. Commit the CSVs in /data, never gcd.db.")