# Moodle description draft: what, why and how

A first draft for the three parts of the Moodle description (spec, Task 5c). It follows Munzner's what, why, how framework as Notes 1 pp. 6 to 14 lays it out with Gapminder. It is not on the page. Edit freely, and check the word limit in the Moodle template.

## 1. Domain, why and who

* **Domain:** comic book collections. The page asks who makes the world's comics and who only reads them, from 1930 to 2026, with Australia as the focus and Japan and the United States as the two comparisons.
* **Why:** Australians buy more comics every year, yet almost none are made here. The page shows that this is not new. Australia has printed other countries' comics for eighty years, and only made its own while American comics were banned (1940 to 1959). It ends on the open question from the APA report: can we grow them at home?
* **Who:** the average Australian, with no background in comics or statistics. Text is plain and short, terms like manga, shōnen and seinen are explained where they first appear, and log scales are named in the chart subtitles.
* **Genre:** annotated charts read in a fixed order, close to a partitioned poster (Notes 7 pp. 5 to 6). Five sections, each with a claim as its heading, read top to bottom: world, Japan, America, Australia, then the open question.

## 2. What: the data

* **Grand Comics Database** (comics.org, volunteer-built, CC BY-SA 4.0). Comic issues, series, genres, reprint links and creator birthplaces. I exported it from the public SQLite dump, keeping only comic publications with a certain start year. It is the only open catalogue that links reprints to their originals, which the reprint story depends on. It is volunteer-built, so it measures how well each country is catalogued as well as how much it made, and the page says so.
* **Wikidata** (CC0). Manga artists' birthplaces and birth years, and Japanese prefecture populations, queried with SPARQL.
* **MyAnimeList** via a Kaggle export (Vall Hernàndez, data as of August 2023). The 5,000 most popular manga, with start year and intended audience.
* **AJPEA** (All Japan Magazine and Book Publishers' and Editors' Association) annual reports, 2016 to 2025. Japan's print and digital manga sales.
* **Circana BookScan** (US) and **NielsenIQ BookScan** (Australia), as published in Splatt (2024), the Australian Publishers Association's Beatrice Davis Fellowship report. Graphic novel sales by category, 2020 to 2023. These are the most recent public figures.
* **Google Trends**, 'manga' compared with 'comics' by Australian state, past five years, downloaded 11 October 2026.
* **Wikipedia**, SMASH! convention attendance, 2007 to 2026.
* **Population:** World Bank (countries) and US Census Bureau Vintage 2024 (states), for per-person rates.
* **Boundaries:** Natural Earth and us-10m via vega-datasets, Global Map Japan, and a public GeoJSON of Australian states.
* **Combining sources:** GCD counts are divided by World Bank and Census populations (M1, M3), Wikidata counts by Wikidata populations (M2), and sales data sits beside GCD series counts (C7a).

## 3. How: idioms, and why each one fits

Each line gives the data (what), the reader's task as an action and a target (why) and the marks and channels (how). Position is the most accurate channel for quantities, then length, then angle and area, then colour lightness (Notes 1 p. 12), so the most important value goes on position wherever the idiom allows.

### §1 The world

* **M1, choropleth with a sphere.**
  * What: geographic regions (countries), with issues per million (quantitative) as the attribute.
  * Why: locate the countries that publish the most per person, and compare Australia with them.
  * How: area marks, with a single-hue purple ramp on a log scale, because the values span four orders of magnitude. An Equal Earth projection keeps areas fair. A Total toggle and a Europe preset view support the comparison, and Norway is labelled because the text names it.
* **C1, ridgeline.**
  * What: a table of country (categorical), year (ordered) and new series (quantitative).
  * Why: compare when each country's output rose and fell (trends).
  * How: one area per country, each scaled to its own peak, so the shapes compare even though the totals differ by 1,000 times. Grey is context, and the three story countries are coloured.
* **C2, heatmap.**
  * What: a table of country (categorical), genre (categorical) and share (quantitative).
  * Why: find each country's dominant genre, and the outliers (Brazil's superheroes, Norway's humour).
  * How: rect marks on a grid, with purple lightness for share on a square-root scale, so small shares stay visible. Rows and columns are sorted by total. The two cells the text discusses are labelled.
* **C10, scatterplot on log-log axes.**
  * What: country, series published and average issues per series (both quantitative).
  * Why: compare two publishing models, and find the extremes (Mexico, the United States).
  * How: point marks with position on both axes. Log scales spread the countries out. Corner notes name the two models.

### §2 Japan

* **C3, stacked area chart.**
  * What: year (ordered), format (categorical) and sales in yen (quantitative).
  * Why: see the trend in the total, and the shift from print to digital.
  * How: stacked areas, with digital in Japan's red. Annotations mark the 2020 boom and the first fall since 2017.
* **M2, small-multiple choropleths.**
  * What: prefectures (geographic regions), birth decade (ordered) and artists per million (quantitative).
  * Why: compare where artists come from across six generations.
  * How: six maps side by side instead of a slider, so the reader compares with their eyes rather than their memory (Munzner pp. 131 to 133). All six share one purple scale.
* **C4, streamgraph.**
  * What: start year (ordered), intended audience (categorical) and new series (quantitative).
  * Why: see how the mix of audiences changed, and when seinen caught up with shōnen.
  * How: stacked areas around a centre line. Each audience pairs a dark young-reader hue with a light adult hue. Bands are labelled directly, so they still read in greyscale. Clicking a legend entry highlights one band.
* **C5, radial arc chart.**
  * What: intended audience (categorical) and running series (quantitative).
  * Why: compare the share of each audience today.
  * How: arc marks, with angle and radius both showing the count, plus percentage labels. It uses the same palette as C4, so the two read as a pair.

### §3 The United States

* **M3, proportional symbol map.**
  * What: states (geographic regions), creators (quantitative) and creators per million (quantitative).
  * Why: locate where creators were born, in total and per person, at once.
  * How: circles at state centroids. Size shows the count and purple lightness shows the rate, so two attributes share one map. New York and California are labelled.
* **C6, multi-line chart.**
  * What: year (ordered), category (categorical) and copies sold (quantitative).
  * Why: compare the trends of each category, and find the 2021 jump in adult fiction.
  * How: lines with position on both axes. Adult fiction (mostly manga) is in red and the rest are grey, labelled directly instead of with a legend.

### §4 Australia

* **C7a, bar chart over unit squares.**
  * What: year, copies sold and new Australian series.
  * Why: compare demand with local supply over the same four years.
  * How: two panels on one shared year axis, because the units differ. Grey bars show sales, and one gold square stands for each new series, so "almost none" can be counted.
* **C7, waffle chart.**
  * What: country, and the share of issues that are foreign reprints, own reprints or neither.
  * Why: compare part-to-whole shares for Australia, the US and Japan.
  * How: 100 squares per country, which reads as "out of every 100 comics" with no maths. Colour shades of each country's own hue, and grey for the rest.
* **C7b, diverging (butterfly) bar chart.**
  * What: country, with the foreign and own reprint shares.
  * Why: rank countries, and contrast importers with self-reprinters.
  * How: bars on a common zero line, with foreign to the right and own to the left, so both sides use length.
* **C8, horizon chart.**
  * What: year (ordered) and new Australian series (quantitative).
  * Why: find the booms and link them to events (the 1940 ban, 1959, about 1980).
  * How: a two-band horizon chart folds the tall peaks into a short strip, with darker gold for busier years. Event lines are annotated.
* **M4, flow map.**
  * What: a network of origin (US) and destinations, with the number of reprinted stories (quantitative).
  * Why: see where American comics went, and compare Australia with Europe.
  * How: lines with width for the volume and arrowheads for direction. Australia's line is gold. A Europe preset zooms into the busiest region.
* **C11, line chart with an annotated gap.**
  * What: year (ordered) and attendance (quantitative).
  * Why: see the growth trend.
  * How: a linear line with points. Hollow points mark "more than" figures, and a band marks the cancelled years, so the missing data is shown honestly.
* **M6, choropleth of Australian states.**
  * What: states, with manga's share of searches (quantitative).
  * Why: compare states.
  * How: area marks with lightness for the share, and state labels.

### §5 The open question

* **C9, dumbbell chart.**
  * What: category (categorical), with copies sold in 2020 and in 2023 (quantitative).
  * Why: compare growth across reader groups.
  * How: two points joined by a line, using position for both years. The growth multiple is labelled at the end.

### Special features

* **Follow a country:** a dropdown in the header (and a floating copy as you scroll), or a click on a country in any linked chart, highlights that country across seven charts (M1, C1, C2, C10, C7, C7b, M4). It is written in `main.js` on top of a shared Vega-Lite `focus` param, and every chart still reads correctly with nothing selected.
* **Preset views instead of free zoom** on M1 and M4 (World and Europe), as Munzner recommends (pp. 256 to 257).
* **Colour as legend:** Australia, Japan and the US have one colour each across the whole page. Their names are coloured in the text, so the text doubles as the legend. Purple only ever means "how much".
* **Typography:** Bangers for the comic-style title, Bebas Neue for the headings, Source Serif 4 for the reading text and Inter for all chart text.
