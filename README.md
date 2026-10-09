# Australia reads comics. Australia doesn't make them.

A single-page data story about eighty years of comic publishing around the world, and why so few of the comics Australians read are made in Australia.

**Author:** Thisum Patabadige · **Date:** October 2026 · FIT3179 Data Visualisation 2, Monash University

All charts and maps are built with [Vega-Lite](https://vega.github.io/vega-lite/).

## Preview locally

The page loads its chart specs and data with `fetch`, which does not work when `index.html` is opened directly from disk (`file://`). Serve the `docs/` folder instead. From the repo root:

```
python -m http.server 8000 --directory docs
```

Then open <http://localhost:8000>.

## Structure

Everything the website needs lives in `docs/`. GitHub Pages is set to publish from the `/docs` folder of `main` (Settings → Pages → Branch: `main`, folder: `/docs`).

```
docs/                 the website (published by GitHub Pages)
  index.html          the page
  css/style.css       layout and typography (two-column grid, colour tokens)
  js/main.js          chart loader: CHARTS registry -> vegaEmbed
  vega/               one pretty-printed Vega-Lite spec per chart
  data/               small aggregated CSVs (about 80 KB in total)
scripts/              data preparation, never loaded by the page
notes/                planning notes
specs/                assignment specification
```

## Adding a chart

1. Save the spec as `docs/vega/<id>_<name>.json` with data paths relative to the page (`data/...`).
2. Add one line to `CHARTS` in `docs/js/main.js`, for example `c3: { spec: "vega/c3_manga_market.json" }`. Add `facetWidth: true` for faceted specs, which cannot use `"width": "container"`.
3. Delete the placeholder content inside the element with that ID in `docs/index.html`.

## Data

All files below are in `docs/data/`.

| File | Built by | Used by |
| --- | --- | --- |
| `country_output.csv`, `country_year.csv`, `country_genre.csv`, `reprint_shares.csv`, `reprint_flows.csv`, `au_series_by_year.csv`, `us_creators_by_state.csv`, `creators_by_country.csv` | `scripts/export.py` (from a local copy of the GCD database, not in this repo) | C1, C2, later charts |
| `country_meta.csv` | hand-compiled ISO codes and World Bank populations | `build_country_map.py` |
| `country_map.csv` | `scripts/build_country_map.py` (joins the two above) | M1 |

The Grand Comics Database dump (`gcd.db`) is several gigabytes and is git-ignored. Never commit it.

## Data sources

- [Grand Comics Database](https://www.comics.org/) (comics.org), licensed [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- [World Bank, population, total](https://data.worldbank.org/indicator/SP.POP.TOTL)
- Research Institute for Publications / [AJPEA](https://www.ajpea.or.jp/), Japanese publishing market 2025
- [ICv2](https://icv2.com/) / [Circana BookScan](https://www.circana.com/), US graphic novel market 2025
- [Australian Publishers Association](https://publishers.asn.au/), "Graphic Novels: Can We Grow Them at Home?" (Splatt, 2024)
- World boundaries: [Natural Earth](https://www.naturalearthdata.com/) via [vega-datasets](https://github.com/vega/vega-datasets)
- Still to add: Wikidata, AniList / Jikan, Google Trends, ABS, US Census, convention attendance figures

Figures from the Grand Comics Database reflect volunteer indexing and are a lower bound. Series with uncertain start years are excluded from year-by-year charts.
