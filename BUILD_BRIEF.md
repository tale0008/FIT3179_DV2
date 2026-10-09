# Build Brief: FIT3179 DV2 Dashboard (MVP shell)

You are building the first version of a single-page data visualisation website for a university assignment (FIT3179 Data Visualisation 2, Monash University). Read this whole brief before writing any code.

The goal of this pass is an **MVP shell**: the full page layout, typography, section structure and narrative text, with three finished Vega-Lite charts embedded and clearly labelled placeholders for every other chart. The remaining charts will be added one at a time later, so swapping a placeholder for a real chart must be a one-line change.

## 1. Hard constraints from the assignment

These are marked requirements. Breaking any of them costs marks or zeroes the assignment.

* **One single scrolling web page** (`index.html`). No routing, no multiple pages, no tabs or buttons that swap major sections in and out.
* **No horizontal scrolling on a small laptop.** Test at 1366 x 768.
* **All charts and maps must be Vega-Lite (or Vega).** Nothing drawn with D3, Chart.js, canvas or hand-written SVG counts toward the mark.
* **Every chart spec lives as its own pretty-printed `.json` file in `/vega/`.** Never inline specs into HTML or JS, never minify them.
* **Hosted on GitHub Pages**, so every path must be relative (`vega/c1_ridgeline.json`, `data/country_output.csv`). No absolute local paths, no build step, no bundler.
* **Total downloadable data under a few megabytes.** Current data is about 50 KB. Keep it that way.
* **Never touch, move, read into the page, or commit `gcd.db`.** It is a 6 GB local source database and must stay git-ignored.

## 2. Tech stack and dependencies

Plain HTML, CSS and vanilla JavaScript. No frameworks, no CSS frameworks, no build tools.

**Allowed without asking (required by the assignment):**

* `https://cdn.jsdelivr.net/npm/vega@5`
* `https://cdn.jsdelivr.net/npm/vega-lite@5`
* `https://cdn.jsdelivr.net/npm/vega-embed@6`

**Needs the student's approval before use (propose it, do not add it silently):**

* A Google Fonts web font. The HD typography criterion asks for a "non-standard typeface matching the topic". Suggested pairing: **Bebas Neue** or **Anton** for headings (comic-cover masthead feel) with **Source Serif 4** or **Inter** for body text. Build the page so it looks fine on a system-font fallback stack, and put the font `<link>` in one clearly commented spot in `<head>` so it can be removed in a single edit.

No other external libraries. If you believe one is needed, stop and explain why instead of adding it.

## 3. Repository structure

Create or confirm this structure. Do not rename existing CSV files.

```
index.html
css/style.css
js/main.js
vega/                     one pretty-printed .json per chart
  m1_world_choropleth.json
  c1_ridgeline.json
  c2_genre_heatmap.json
data/                     small aggregated CSVs
  country_meta.csv
  country_output.csv
  country_year.csv
  country_genre.csv
  reprint_shares.csv
  reprint_flows.csv
  au_series_by_year.csv
  us_creators_by_state.csv
  creators_by_country.csv
scripts/
  export.py               data export script, never loaded by the page
  explore.py, validate.py, check2.py   (exploration scripts, keep for reference)
sketch/
  sketch.pdf              hand-drawn sketch, added by the student
README.md
.gitignore
```

Housekeeping to do first:

* The CSVs currently sit in a folder called `gcd export` (with a space). Move them into `data/` and delete the empty folder.
* Move `export.py` and the other `.py` scripts into `scripts/`. In `export.py`, change `OUT_DIR` so it points at the repo's `data/` folder (use a path relative to the script, for example `os.path.join(os.path.dirname(__file__), "..", "data")`).
* Move `cmd output.txt` and `sketch_outline.txt` into a `notes/` folder or delete them if the student agrees.
* Make sure `.gitignore` contains at least: `gcd.db`, `gcd.db-journal`, `*.sqlite3`, `*.dll`, `*.def`, `__pycache__/`. Run `git check-ignore gcd.db` and confirm it prints `gcd.db`.

## 4. The three finished charts

The files `vega/m1_world_choropleth.json`, `vega/c1_ridgeline.json`, `vega/c2_genre_heatmap.json` and `data/country_meta.csv` are supplied alongside this brief. They already use relative data paths.

* **M1 and C2** use `"width": "container"` with `"autosize": {"type": "fit-x", "contains": "padding"}`. Their wrapper element needs a real width in CSS (`width: 100%`), otherwise they collapse to zero.
* **C1 is a faceted (row) chart.** Vega-Lite does not support `"container"` width on facets, so the file has a fixed `"width": 420`. In `main.js`, fetch this spec, set `spec.width` to the chart container's inner width minus about 110 px (room for the row labels), then embed. Re-embed on window resize, debounced to about 200 ms.

Do not change encodings, colours, titles or transforms inside the specs. Those are the student's design decisions. If something looks broken, report it rather than redesigning it.

## 5. Chart loading (`js/main.js`)

One small, readable loader. Requirements:

* Use `vegaEmbed` with `{actions: false, renderer: "svg"}`.
* Keep a single registry object mapping element IDs to spec paths, so adding a chart later means adding one line.
* Mark facet charts that need the width fix with a flag in the registry rather than hard-coding the C1 ID in the logic.
* If a spec or its data fails to load, show a short error message inside that chart's box instead of breaking the rest of the page, and log the error to the console.
* `fetch` does not work over `file://`. Put a comment at the top of `main.js` and a line in the README saying to preview with `python -m http.server 8000` from the repo root.

Suggested registry shape:

```js
const CHARTS = {
  m1: { spec: "vega/m1_world_choropleth.json" },
  c1: { spec: "vega/c1_ridgeline.json", facetWidth: true },
  c2: { spec: "vega/c2_genre_heatmap.json" }
  // add new charts here as they are built
};
```

## 6. Placeholder component

Every chart not built yet gets a placeholder box that makes the planned design obvious. Each placeholder shows:

* The chart ID (for example `C8`)
* The chart title
* The idiom (for example "Horizon chart")
* The data source or sources
* One line describing the planned key annotation or insight

Style: light grey dashed border, subtle tinted background, left-aligned small text, and a fixed minimum height matching the real chart's expected height (given per chart in section 9) so the layout is realistic now.

Use one CSS class (for example `.placeholder`) and keep the markup consistent, so turning a placeholder into a real chart only means adding its ID to `CHARTS` and deleting the placeholder's inner content. Give each placeholder the same element ID the real chart will use (`c3`, `m2`, and so on).

## 7. Layout system

The student's tutor gave two explicit pieces of feedback on the sketch. Both are requirements:

* **Strict two-column grid everywhere.** Never mix a three-column row with two-column rows. A row is either two equal columns or one full-width row spanning both.
* **Every chart has text beside or below it.** No chart sits alone without narrative or caption text.

Grid details:

* Content max width about 1120 px, centred, with side padding of at least 24 px.
* Two equal columns with a gutter of about 48 px. Every box on the page aligns to the same two column edges, giving one consistent set of vertical sight lines from top to bottom.
* **Body text never runs full width.** Even in a full-width row, paragraphs are capped at one column's width (roughly 60 to 75 characters per line). Charts and maps may span the full width, prose may not.
* One spacing scale (for example 8, 16, 24, 48, 96 px) used throughout for consistent vertical rhythm.
* Sections separated by generous white space and a thin rule or subtle background change, not heavy borders.
* Below about 820 px viewport width, collapse to one column.

Use CSS Grid with reusable row classes, for example `.row-2` (two columns) and `.row-full` (spanning both), rather than one-off layout rules per section.

## 8. Typography and colour

* Body text 17 to 18 px, line height about 1.6, left-aligned. Never centred or justified text blocks.
* Clear hierarchy: page title, section heading, chart title, caption. Each level visibly distinct by size and weight.
* Section headings include the section number (§1 to §5).
* Captions about 14 px, muted colour, directly under or beside their chart.
* Off-white page background with near-black text.
* Define colours as CSS custom properties on `:root`, including three **country accent colours** reused across the page and later in the charts:
  * `--au` Australia, warm gold, for example `#D99A00`
  * `--jp` Japan, red, for example `#C8102E`
  * `--us` United States, blue, for example `#1F4E9A`
* Use accents sparingly: key numbers in lead paragraphs and a thin coloured bar on each country's section heading. The rubric penalises overuse of highlighting.

## 9. Page structure, section by section

Follow this order exactly. "L" is the left column, "R" the right column, "FULL" spans both. Placeholder heights are approximate. All draft text below can be used as written.

### Header

* FULL: page title **"Australia reads comics. Australia doesn't make them."**
* L only: standfirst, then author and date line.
  * Standfirst: "Australians buy millions of comics and graphic novels every year. Almost none of them are made here. This page follows eighty years of comic publishing around the world to show how that happened, and what it would take to change it."
  * Author line: "By Thisum Patabadige · October 2026 · Sources listed at the end of the page"

### §1 Who makes comics?

* Row 1, L: lead text. "Comics are a global medium, but they are not made evenly. The Grand Comics Database, a volunteer catalogue of over two million comic issues, shows that a handful of countries produce most of the world's comics. Per person the picture changes: small countries like Norway and Belgium publish far more than their size suggests. One caution applies to every chart built on this database. It is compiled by volunteers, so it measures how thoroughly each country's comics have been catalogued as well as how many were made."
* Row 1, R: **M1 world choropleth** (real chart, ID `m1`)
* Row 2, L: **C1 ridgeline** (real chart, ID `c1`), caption beneath: "Each country's publishing over time, scaled to its own peak. The centre of gravity of comics has moved across the world since the 1930s."
* Row 2, R: **C2 genre heatmap** (real chart, ID `c2`), caption beneath: "Superheroes dominate American comics, but most other countries built their industries on humour, adventure and stories for children."

### §2 Japan: a country that feeds itself

* Row 1, L: lead text. "Japan has the largest comics industry in the world, and almost all of it is homegrown. Just 0.07% of the Japanese comic issues in the database are reprints of foreign work. In 2025 the Japanese manga market was worth ¥692.5 billion, even as print sales fell and more readers moved to digital."
* Row 1, R: placeholder **C3** "Japan's manga market, print vs digital" · Line chart · Source: Research Institute for Publications (AJPEA) · Annotation: "2025: first market contraction since 2017" · 320 px
* Row 2, FULL: placeholder **M2** "Where Japan's manga artists come from" · Small-multiples choropleth of prefectures, one map per decade (six maps) · Sources: Wikidata manga artist birthplaces plus Japanese prefecture populations · Annotation: "Most famous mangaka were not born in Tokyo" · 280 px. Add a one-column caption placeholder beneath it.
* Row 3, L: placeholder **C4** "Who manga is written for" · Streamgraph · Source: AniList / Jikan (MyAnimeList) API · Annotation: "Shōnen's share over time" · 300 px, with caption placeholder beneath
* Row 3, R: placeholder **C5** "Manga's audience today" · Radial arc chart · Source: AniList / Jikan API · Annotation: "Demographic mix of currently running series" · 300 px, with caption placeholder beneath

### §3 The United States

Text alternates to the right in this section.

* Row 1, L: placeholder **M3** "Where American comic creators were born" · State choropleth, per capita · Sources: Grand Comics Database plus US Census state populations · Annotation: "Creators per million residents by birth state" · 320 px
* Row 1, R: lead text. "The United States is the world's other comics superpower, and like Japan it mostly reprints itself. Only about 1% of American comic issues in the database are reprints of foreign work, while 11% are reprints of older American comics sold again as collected editions."
* Row 2, L: placeholder **C6** "Who sells America's comics" · Slope graph, publisher rank 2015 vs 2025 · Source: ICv2 / Circana BookScan · Annotation: "Children's graphic novel publishers overtake the superhero giants" · 320 px
* Row 2, R: annotation text placeholder with two or three short callout notes about C6.

### §4 Australia (the tallest section, visually the centre of the page)

* Row 1, L: lead text. "Australia is one of the world's great importers of comics. Of the Australian comic issues in the database, 17.5% are reprints of foreign comics and just 0.7% are reprints of Australian ones: twenty-five imported reprints for every local one. Only Norway and Canada import a larger share. Meanwhile Australian sales of graphic novels more than doubled between 2020 and 2023."
* Row 1, L (continued): comparison figure beneath the lead text. "Australia vs Japan: 250 times the share of imported reprints."
* Row 1, R: placeholder **C7** "Whose comics are Australia's comics?" · Waffle chart · Source: Grand Comics Database · Annotation: "17.5% foreign reprints vs 0.7% domestic" · 320 px, with caption placeholder beneath. (Matches the sketch: the waffle is the section's main chart.)
* Row 2, L: placeholder **C7a** "The gap: what Australia buys vs what it makes" · Indexed two-series chart, 2020 = 100 · Sources: NielsenIQ BookScan via Australian Publishers Association report (Splatt, 2024) plus Grand Comics Database · Annotation: "Sales up about 2.5 times, local output flat" · 320 px. Not in the sketch; an extra row added after it.
* Row 2, R: text placeholder for C7a.
* Row 3, FULL: placeholder **C8** "Eighty years of Australian comics" · Horizon chart · Source: Grand Comics Database · Annotations: "1940: wartime import ban, new series jump from 2 to 83", "1959: American comics return", "1980: second reprint boom" · 220 px. Add a one-column caption placeholder beneath it.
* Row 4, L: placeholder **M4** "How American comics reached Australia" · Flow map · Source: Grand Comics Database reprint records · Annotation: "22,645 documented US to Australia reprint links" · 320 px
* Row 4, R: placeholder **M5** "Where Australian fans gather" · Proportional symbol map of conventions and comic festivals by city · Sources: convention attendance figures plus city coordinates · Annotation: "SMASH! Sydney: 53,071 attendees in 2026" · 320 px
* Row 5, L: placeholder **M6** "Which states search for comics" · State choropleth, per capita · Sources: Google Trends plus ABS state populations · Annotation: "Interest in manga vs superhero comics by state" · 320 px
* Row 5, R: text and caption placeholder for M4, M5 and M6.

### §5 Can we grow them at home?

* Row 1, L: placeholder **C9** "Hits and misses" · Jittered strip plot of title sales · Source: Circana BookScan / ICv2 · 280 px
* Row 1, R: closing text. "Australia has made comics before. In the 1940s, when imports were banned, a local industry appeared almost overnight. The readers are here now in greater numbers than ever. The open question is whether Australian comics can find them without a ban to clear the shelves."

### Footer: metadata bar (FULL)

This is marked under the storytelling criterion, so make it complete and well formatted.

* **Author:** Thisum Patabadige
* **Date:** October 2026
* **Unit:** FIT3179 Data Visualisation, Monash University
* **Licence:** GCD-derived data under CC BY-SA 4.0; licence for the rest of the page is the student's choice (the sketch lists a licence in the metadata bar).
* **Data sources**, each with a link:
  * Grand Comics Database (comics.org), licensed CC BY-SA 4.0. The credit must name "Grand Comics Database" and link to comics.org.
  * World Bank population data (used in M1)
  * Research Institute for Publications / AJPEA, Japanese publishing market 2025
  * ICv2 / Circana BookScan, US graphic novel market 2025
  * Australian Publishers Association, "Graphic Novels: Can We Grow Them at Home?" (Splatt, 2024)
  * Placeholder lines for Wikidata, AniList / Jikan, Google Trends, ABS, US Census and convention attendance sources
* **Data note:** "Figures from the Grand Comics Database reflect volunteer indexing and are a lower bound. Series with uncertain start years are excluded from year-by-year charts."
* **AI acknowledgement:** placeholder line for the student to complete.
* **Tools:** "Built with Vega-Lite."

## 10. Out of scope for this pass

* No interactivity beyond the tooltips already in the three specs. No toggles, filters, linked selections or scroll animations.
* No new charts. Everything except M1, C1 and C2 is a placeholder.
* No design changes inside the three existing specs.

## 11. Acceptance checklist

Confirm every item before finishing:

* [ ] `python -m http.server 8000` from the repo root serves the page with no console errors.
* [ ] M1, C1 and C2 render with real data.
* [ ] Every other chart shows a placeholder with ID, title, idiom, source and planned annotation.
* [ ] At 1366 x 768 there is no horizontal scrollbar.
* [ ] Every row is either two equal columns or full width. No three-column rows anywhere.
* [ ] Every box aligns to the same two column edges.
* [ ] No paragraph is wider than one column.
* [ ] Every chart has text beside or beneath it.
* [ ] All paths are relative. Specs in `/vega/` are pretty-printed.
* [ ] `gcd.db` is git-ignored and not staged.
* [ ] Adding a new chart only needs a spec in `/vega/`, one line in `CHARTS`, and removal of its placeholder content.
* [ ] The README explains how to preview locally, lists the data sources and names the author.

When done, give the student a short summary of what was built, any decisions you made that were not specified here, and anything you could not do.
