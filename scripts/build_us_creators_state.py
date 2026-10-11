"""
M3 data: American comic creators per million residents, by birth state.

Reads data/us_creators_by_state.csv (from export.py, Grand Comics Database)
and joins it to 2020 US Census state populations, downloaded from the
Census Bureau API (no key needed). Writes data/us_creators_state_pc.csv.

Run from the repo root:   python scripts/build_us_creators_state.py
Needs: Python 3.8+, internet access. No extra packages.
Cite as "U.S. Census Bureau, 2020 Census, P.L. 94-171 Redistricting Data".
"""

import csv
import json
import os
import re
import urllib.request
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# The site lives in docs/ (GitHub Pages), so data is in docs/data. Fall back to data/ at the repo root.
DATA_DIR = os.path.join(ROOT, "docs", "data") if os.path.isdir(os.path.join(ROOT, "docs", "data")) else os.path.join(ROOT, "data")
DATA = DATA_DIR
CENSUS = "https://api.census.gov/data/2020/dec/pl?get=NAME,P1_001N&for=state:*"

ABBR = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}
EXTRA = {"washington dc": "District of Columbia", "washington d c": "District of Columbia",
         "d c": "District of Columbia", "calif": "California", "mass": "Massachusetts",
         "penn": "Pennsylvania", "penna": "Pennsylvania", "wash": "Washington", "ill": "Illinois",
         "mich": "Michigan", "conn": "Connecticut", "fla": "Florida", "tex": "Texas", "minn": "Minnesota",
         "wis": "Wisconsin", "okla": "Oklahoma", "ariz": "Arizona", "colo": "Colorado", "tenn": "Tennessee"}


def norm(s):
    """Lower-case, drop punctuation, collapse spaces: "N.Y." -> "n y", "California " -> "california"."""
    return " ".join(re.sub(r"[^a-z ]", " ", s.lower()).split())


def main():
    raw = os.path.join(DATA, "raw", "census_2020.json")
    if os.path.exists(raw):
        print("Using downloaded file raw/census_2020.json")
        with open(raw, encoding="utf-8-sig") as f:
            census = json.load(f)[1:]
    else:
        try:
            req = urllib.request.Request(CENSUS, headers={"User-Agent": "FIT3179-DV2-student-project/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                census = json.loads(r.read().decode("utf-8"))[1:]
        except Exception as e:
            raise SystemExit(f"Census download failed ({e}).\nOpen this link in your browser, save the page as "
                             f"{raw}, and run again:\n{CENSUS}")
    pop = {name: (int(p), int(fips)) for name, p, fips in census}
    lookup = {norm(n): n for n in pop}
    lookup.update({a.lower(): n for a, n in ABBR.items()})
    lookup.update(EXTRA)

    creators = Counter()
    unmatched = Counter()
    with open(os.path.join(DATA, "us_creators_by_state.csv"), encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            raw, n = row["state"], int(row["creators"])
            key = norm(raw) or ""
            name = lookup.get(key) or lookup.get(key.replace(" ", ""))
            if name and name in pop:
                creators[name] += n
            else:
                unmatched[raw] += n

    with open(os.path.join(DATA, "us_creators_state_pc.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["fips", "state", "creators", "population", "per_million"])
        for name, (p, fips) in sorted(pop.items()):
            if name == "Puerto Rico":
                continue
            c = creators.get(name, 0)
            w.writerow([fips, name, c, p, round(c / (p / 1_000_000), 2)])

    matched = sum(creators.values())
    lost = sum(unmatched.values())
    print(f"Matched {matched} creators to a state, {lost} could not be matched.")
    if unmatched:
        print("Unmatched values (most common first). Send these to Claude if many are real states:")
        for raw, n in unmatched.most_common(25):
            print(f"  {raw!r}: {n}")


if __name__ == "__main__":
    main()
