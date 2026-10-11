"""
C4 and C5 data, manual route: use this instead of fetch_manga_demographics.py
if the Jikan API cannot be reached.

1. Download a MyAnimeList manga export from Kaggle. Recommended:
   https://www.kaggle.com/datasets/andreuvallhernndez/myanimelist
   (free Kaggle account needed). Unzip it and find the manga file
   (usually manga.csv).
2. Save it as  data/raw/manga.csv
3. Run from the repo root:   python scripts/process_manga_kaggle.py

The file needs columns for: type, members (or popularity), demographics,
start date, and status. The script finds them by name and tells you if any
are missing. It keeps the 5,000 manga with the most members, the same rule
as the API script, and writes the same two CSVs into data/.
Cite as "MyAnimeList data via Kaggle (<dataset name and author>), downloaded <date>".
"""

import ast
import csv
import os
import re
import sys
from collections import Counter

csv.field_size_limit(10_000_000)
HERE = os.path.dirname(__file__)
RAW = os.path.join(HERE, "..", "data", "raw", "manga.csv")
OUT = os.path.join(HERE, "..", "data")
TOP_N = 5000
NAMES = {"shounen": "Shōnen", "shonen": "Shōnen", "shoujo": "Shōjo", "shojo": "Shōjo",
         "seinen": "Seinen", "josei": "Josei", "kids": "Kids"}
DEMOS = ["Shōnen", "Shōjo", "Seinen", "Josei", "Kids", "Not stated"]


def find(cols, *options):
    low = {c.lower().strip(): c for c in cols}
    for o in options:
        if o in low:
            return low[o]
    for o in options:
        for k, c in low.items():
            if o in k:
                return c
    return None


def parse_list(v):
    v = (v or "").strip()
    if not v or v.lower() in ("[]", "nan", "none"):
        return []
    try:
        x = ast.literal_eval(v)
        if isinstance(x, (list, tuple)):
            return [str(i) for i in x]
    except (ValueError, SyntaxError):
        pass
    return [p.strip(" '\"[]") for p in re.split(r"[,|;]", v) if p.strip(" '\"[]")]


def num(v):
    try:
        return float(re.sub(r"[^0-9.]", "", v or "") or 0)
    except ValueError:
        return 0.0


def main():
    if not os.path.exists(RAW):
        sys.exit("Put the Kaggle manga file at data/raw/manga.csv first.")
    with open(RAW, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames
        rows = list(reader)
    c_type = find(cols, "type", "media_type")
    c_mem = find(cols, "members", "member", "num_list_users", "popularity")
    c_demo = find(cols, "demographics", "demographic")
    c_start = find(cols, "start_date", "real_start_date", "published_from", "published", "start")
    c_status = find(cols, "status")
    print("Columns used:", {"type": c_type, "members": c_mem, "demographics": c_demo,
                            "start": c_start, "status": c_status})
    missing = [n for n, c in [("members", c_mem), ("demographics", c_demo), ("start date", c_start), ("status", c_status)] if not c]
    if missing:
        sys.exit(f"Could not find columns for: {', '.join(missing)}. Send Claude the header line of the file.")

    if c_type:
        rows = [r for r in rows if (r.get(c_type) or "").strip().lower() == "manga"]
    popularity_is_rank = c_mem.lower() == "popularity"
    rows.sort(key=lambda r: num(r[c_mem]), reverse=not popularity_is_rank)
    rows = rows[:TOP_N]

    by_year, current = Counter(), Counter()
    for r in rows:
        demos = parse_list(r.get(c_demo))
        demo = NAMES.get(demos[0].lower(), "Not stated") if demos else "Not stated"
        m = re.search(r"(19|20)\d\d", r.get(c_start) or "")
        year = int(m.group(0)) if m else None
        status = (r.get(c_status) or "").lower()
        if year and 1960 <= year <= 2026:
            by_year[(year, demo)] += 1
        if "publishing" in status and "finish" not in status:
            current[demo] += 1

    with open(os.path.join(OUT, "manga_demo_by_year.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "demographic", "titles"])
        for year in range(1960, 2027):
            for d in DEMOS:
                w.writerow([year, d, by_year.get((year, d), 0)])
    with open(os.path.join(OUT, "manga_demo_current.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["demographic", "titles"])
        for d in DEMOS:
            w.writerow([d, current.get(d, 0)])
    print(f"Done. {len(rows)} titles used, {sum(current.values())} still publishing.")
    print("Still publishing by audience:", dict(current))


if __name__ == "__main__":
    main()
