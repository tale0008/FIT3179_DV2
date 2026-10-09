"""
FIT3179 DV2 - build data/country_map.csv for M1 (world choropleth).

Joins the GCD output counts (country_output.csv) with World Bank population
(country_meta.csv) and adds issues per million people. M1 looks this file up
by ISO 3166 numeric code, which matches the ids in world-110m.json.

Run from anywhere: python scripts/build_country_map.py
"""

import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "data")


def read(name):
    with open(os.path.join(DATA_DIR, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


output = {r["code"]: r for r in read("country_output.csv")}

rows = []
for m in read("country_meta.csv"):
    o = output.get(m["code"])
    if o is None:
        print(f"  skipped {m['country']}: no GCD output row")
        continue
    issues = int(o["issues"])
    population = int(m["population"])
    rows.append([
        m["iso_n3"], m["code"], m["country"],
        issues, int(o["series"]), population,
        round(issues / population * 1_000_000, 1),
    ])

path = os.path.join(DATA_DIR, "country_map.csv")
with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["iso_n3", "code", "country", "issues", "series", "population", "issues_per_million"])
    w.writerows(rows)

print(f"  country_map.csv  {len(rows)} rows")
