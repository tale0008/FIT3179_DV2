"""
M6 data: which Australian states search for manga versus comics.

Google Trends has no free API, so download the file by hand first:

  1. Open https://trends.google.com/trends/explore?geo=AU&date=today%205-y&q=manga,comics
  2. Scroll to "Compared breakdown by sub-region" (or "Interest by sub-region").
  3. Make sure the view is "Region", then click the download icon (arrow) for that panel.
  4. Save the file as  data/raw/geoMap.csv  (create the raw folder if needed).

Then run from the repo root:   python scripts/build_au_trends.py
Writes data/au_trends_states.csv. Cite as "Google Trends, Australia, past five years, downloaded <date>".
"""

import csv
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# The site lives in docs/ (GitHub Pages), so data is in docs/data. Fall back to data/ at the repo root.
DATA_DIR = os.path.join(ROOT, "docs", "data") if os.path.isdir(os.path.join(ROOT, "docs", "data")) else os.path.join(ROOT, "data")
RAW = os.path.join(DATA_DIR, "raw", "geoMap.csv")
OUT = os.path.join(DATA_DIR, "au_trends_states.csv")
STATES = {"New South Wales", "Victoria", "Queensland", "South Australia", "Western Australia",
          "Tasmania", "Northern Territory", "Australian Capital Territory"}


def num(s):
    s = re.sub(r"[^0-9.]", "", s or "")
    return float(s) if s else 0.0


def main():
    with open(RAW, encoding="utf-8-sig") as f:
        lines = [l for l in csv.reader(f) if l]
    header_i = next(i for i, l in enumerate(lines) if l[0].strip().lower() in ("region", "sub-region", "subregion"))
    header = [h.lower() for h in lines[header_i]]
    mi = next(i for i, h in enumerate(header) if "manga" in h)
    ci = next(i for i, h in enumerate(header) if "comic" in h)

    rows = []
    for l in lines[header_i + 1:]:
        state = l[0].strip()
        if state not in STATES:
            continue
        m, c = num(l[mi]), num(l[ci])
        share = round(100 * m / (m + c), 1) if (m + c) else None
        rows.append((state, m, c, share))

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["state", "manga", "comics", "manga_share"])
        w.writerows(rows)
    print(f"Wrote {len(rows)} states to data/au_trends_states.csv")
    for r in rows:
        print(f"  {r[0]:<30} manga {r[1]:>5}  comics {r[2]:>5}  manga share {r[3]}%")
    if len(rows) < 8:
        print("WARNING: fewer than 8 states found. Check the downloaded file is the sub-region breakdown.")


if __name__ == "__main__":
    main()
