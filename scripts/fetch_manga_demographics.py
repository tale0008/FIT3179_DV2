"""
C4 and C5 data: who manga is written for.

Downloads the 5,000 most popular manga on MyAnimeList through the free
Jikan API (no key needed), and records each title's demographic
(shounen, shoujo, seinen, josei, kids), start year and status.
Writes two small summary CSVs into data/.

Run from the repo root:   python scripts/fetch_manga_demographics.py
Needs: Python 3.8+, internet access. No extra packages.
Takes about 4 to 5 minutes because Jikan allows about one request a second.
Cite as "MyAnimeList via the Jikan API (jikan.moe)".
"""

import csv
import json
import os
import time
import urllib.request
from collections import Counter

PAGES = 200          # 25 titles per page, so 5,000 titles
OUT = os.path.join(os.path.dirname(__file__), "..", "data")
URL = "https://api.jikan.moe/v4/manga?type=manga&order_by=members&sort=desc&limit=25&page={}"
NAMES = {"Shounen": "Shōnen", "Shoujo": "Shōjo", "Seinen": "Seinen", "Josei": "Josei", "Kids": "Kids"}


def get(url, tries=6):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FIT3179-DV2-student-project/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            wait = 3 * (attempt + 1)
            print(f"  page failed ({e}), retrying in {wait}s")
            time.sleep(wait)
    return None


def main():
    titles = []
    for page in range(1, PAGES + 1):
        data = get(URL.format(page))
        if not data or not data.get("data"):
            print(f"  stopped at page {page}")
            break
        for m in data["data"]:
            demos = [d["name"] for d in m.get("demographics", [])]
            demo = NAMES.get(demos[0], "Not stated") if demos else "Not stated"
            year = (((m.get("published") or {}).get("prop") or {}).get("from") or {}).get("year")
            titles.append((m["mal_id"], year, m.get("status", ""), demo))
        if page % 20 == 0:
            print(f"  {page}/{PAGES} pages, {len(titles)} titles so far")
        if not data.get("pagination", {}).get("has_next_page"):
            break
        time.sleep(1.1)

    unique = {t[0]: t for t in titles}.values()
    by_year = Counter()
    current = Counter()
    for _, year, status, demo in unique:
        if year and 1960 <= year <= 2026:
            by_year[(year, demo)] += 1
        if status == "Publishing":
            current[demo] += 1

    demos = ["Shōnen", "Shōjo", "Seinen", "Josei", "Kids", "Not stated"]
    with open(os.path.join(OUT, "manga_demo_by_year.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "demographic", "titles"])
        for year in range(1960, 2027):
            for d in demos:
                w.writerow([year, d, by_year.get((year, d), 0)])
    with open(os.path.join(OUT, "manga_demo_current.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["demographic", "titles"])
        for d in demos:
            w.writerow([d, current.get(d, 0)])

    print(f"\nDone. {len(list(unique))} unique titles, {sum(current.values())} still publishing.")


if __name__ == "__main__":
    main()
