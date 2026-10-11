"""
M2 data: where Japan's manga artists were born.

Queries Wikidata for every person with occupation "manga artist" (Q191633)
whose place of birth lies inside a Japanese prefecture, plus each
prefecture's latest population. Writes two small CSVs into data/.

Run from the repo root:   python scripts/fetch_mangaka_wikidata.py
Needs: Python 3.8+, internet access. No extra packages.
Takes about a minute. Wikidata is CC0, cite as "Wikidata".
"""

import csv
import json
import os
import time
import urllib.parse
import urllib.request
from collections import Counter

ENDPOINT = "https://query.wikidata.org/sparql"
HEADERS = {
    "User-Agent": "FIT3179-DV2-student-project/1.0 (Monash University coursework)",
    "Accept": "application/sparql-results+json",
}
OUT = os.path.join(os.path.dirname(__file__), "..", "data")

BINS = [
    ("Born before 1950", 0, 1949),
    ("1950s", 1950, 1959),
    ("1960s", 1960, 1969),
    ("1970s", 1970, 1979),
    ("1980s", 1980, 1989),
    ("1990 or later", 1990, 2100),
]

Q_MANGAKA = """
SELECT DISTINCT ?person ?birth ?code WHERE {
  ?person wdt:P106 wd:Q191633 ;
          wdt:P19 ?place .
  ?place wdt:P131* ?pref .
  ?pref wdt:P31 wd:Q50337 ;
        wdt:P300 ?code .
  OPTIONAL { ?person wdt:P569 ?birth . }
}
"""

Q_POP = """
SELECT ?code ?prefLabel ?pop ?when WHERE {
  ?pref wdt:P31 wd:Q50337 ;
        wdt:P300 ?code ;
        p:P1082 ?st .
  ?st ps:P1082 ?pop .
  OPTIONAL { ?st pq:P585 ?when . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". ?pref rdfs:label ?prefLabel . }
}
"""


def run(query, tries=4):
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": query, "format": "json"})
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)["results"]["bindings"]
        except Exception as e:
            print(f"  query failed ({e}), retrying in {10 * (attempt + 1)}s")
            time.sleep(10 * (attempt + 1))
    raise SystemExit("Wikidata query kept failing. Try again in a few minutes.")


def pref_id(code):
    # "JP-13" -> 13, matching the id in japan_prefectures.topojson
    return int(code.split("-")[1])


def main():
    print("Querying Wikidata for manga artists' birthplaces...")
    rows = run(Q_MANGAKA)
    seen = {}
    for r in rows:
        p = r["person"]["value"]
        if p in seen:
            continue
        year = None
        if "birth" in r:
            try:
                year = int(r["birth"]["value"][:5].lstrip("+")[:4])
            except ValueError:
                year = None
        seen[p] = (pref_id(r["code"]["value"]), year)
    print(f"  {len(seen)} manga artists with a birthplace in a Japanese prefecture")

    counts = Counter()
    no_year = 0
    for pid, year in seen.values():
        if year is None:
            no_year += 1
            continue
        for label, lo, hi in BINS:
            if lo <= year <= hi:
                counts[(pid, label)] += 1
                break
    print(f"  {no_year} have no birth year and are left out of the decade maps")

    with open(os.path.join(OUT, "mangaka_prefecture_decade.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pref_id", "generation", "generation_order", "mangaka"])
        for pid in range(1, 48):
            for i, (label, _, _) in enumerate(BINS):
                w.writerow([pid, label, i, counts.get((pid, label), 0)])

    print("Querying Wikidata for prefecture populations...")
    best = {}
    for r in run(Q_POP):
        pid = pref_id(r["code"]["value"])
        when = r.get("when", {}).get("value", "")
        pop = int(float(r["pop"]["value"]))
        name = r["prefLabel"]["value"]
        if pid not in best or when > best[pid][0]:
            best[pid] = (when, pop, name)
    with open(os.path.join(OUT, "japan_prefecture_population.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pref_id", "prefecture", "population", "population_date"])
        for pid in sorted(best):
            when, pop, name = best[pid]
            w.writerow([pid, name, pop, when[:10]])
    print(f"  populations for {len(best)} of 47 prefectures")

    total = sum(counts.values())
    print(f"\nDone. {total} artists mapped. Files written to data/.")
    if len(best) < 47:
        print("WARNING: some prefectures have no population. Tell Claude which ones are missing.")


if __name__ == "__main__":
    main()
