# Update 02: six new charts (§1 and §4)

This update adds six finished charts and their text. Make only the changes listed here. STYLE_GUIDE.md still applies to everything. Do not edit the chart specs, and do not change any chart or text not listed.

Files supplied with this update:

* `UPDATE_02.md` (this file)
* `vega/c7a_gap.json`, `vega/c7_waffle.json`, `vega/c7b_reprint_butterfly.json`, `vega/c8_au_horizon.json`, `vega/m4_flow_map.json`, `vega/c10_publishing_models.json` (new)
* `data/au_sales.csv` (new)
* `data/country_meta.csv` (adds `lat` and `lon` columns, see section 1)

## 1. Data files

* Copy `data/au_sales.csv` into `/data/`. It holds Australian graphic novel sales from NielsenIQ BookScan, as published in the Australian Publishers Association report (Splatt, 2024).
* `data/country_meta.csv` now has two extra columns, `lat` and `lon` (country centre points for the flow map), plus one extra row for Yugoslavia. **If the repo's copy already has different population figures** (for example World Bank values the student added), do not overwrite them. Add only the `lat` and `lon` columns and the Yugoslavia row from the supplied file. Otherwise copy the supplied file over the old one.
* No other data files change.

## 2. Chart registry

Copy the six spec files into `/vega/` and add them to the `CHARTS` registry in `main.js`:

```js
c10: { spec: "vega/c10_publishing_models.json" },
c7a: { spec: "vega/c7a_gap.json" },
c7:  { spec: "vega/c7_waffle.json" },
c7b: { spec: "vega/c7b_reprint_butterfly.json" },
c8:  { spec: "vega/c8_au_horizon.json" },
m4:  { spec: "vega/m4_flow_map.json" }
```

Width notes:

* `c10`, `c7b`, `c8` and `m4` use `"width": "container"` and fit their box. No special handling.
* `c7` (waffle) is a faceted chart with three fixed 130 px grids, about 460 px wide in total. `c7a` is a two-part stacked chart with a fixed width of 440 px plus its axis, about 500 px in total. Both fit a single column at full page width. Do not add the facet width fix to them. If either overflows its column at 1366 x 768, report it rather than editing the spec.

Remove the placeholders for C7a, C7, C8 and M4. C7b and C10 are new, so they have no placeholder.

## 3. §1 changes

### Change the C2 transition

Replace the C2 `.transition` text with:

> "Countries did not only publish different stories. They published them in different shapes."

### Add Row 3 to §1: text left, C10 right

Row 3 is a normal two-column row after the C1 and C2 row.

* `.lead` "Some countries launch thousands of short series. Others keep a few running for decades."
* `.reading-guide` "(Each dot is a country. Further right means more series published. Higher up means each series ran for more issues on average.)"
* `.takeaway` "**The United States** publishes the most series, but they average only about 4 issues each. Mexico's average about 119. **Japan** sits in between at about 37 issues per series, and **Australia** at about 10." `<!-- VERIFY: issues per series values against country_output.csv -->`
* `.caveat` "(Both axes use a log scale, so each gridline multiplies the value rather than adding to it. Countries with fewer than 200 series in the database are left out.)"
* `.transition` "**Japan** is the clearest case of a country that built its own kind of comics, and then kept them for itself."

The Japan transition moves here from C2, so §1 still ends by handing over to §2.

## 4. §4 layout and text

§4 is rebuilt as follows. Rows 4 (M5 placeholder) and 5 (M6 placeholder and its text) stay as they are, but M5 now sits in the right column of Row 4 beside M4.

**Section intro** (under the §4 heading, left column, replaces the old §4 lead text):

> "Australia has always read comics. For most of the last eighty years, it has printed other countries' comics to do it."

### Row 1: text left, C7a right

* `.lead` "Start with today. Australians are buying more comics than ever."
* `.lead` "Sales of graphic novels in Australian shops nearly tripled in four years, from about 500,000 copies in 2020 to 1.38 million in 2023."
* `.reading-guide` "(Grey bars are copies sold. Each gold square beneath them is one new comic series published in Australia that year.)"
* `.takeaway` "Over the same four years, the database records just 14 new Australian comic series." `<!-- VERIFY: sum of 2020 to 2023 in au_series_by_year.csv -->`
* `.caveat` "(Sales figures exclude manga and superhero titles, so the true total is higher. The newest years of the database are the least complete, because volunteers tend to catalogue recent comics last.)"
* `.transition` "So if Australians are not reading Australian comics, whose are they reading?"

### Row 2: C7 left, C7b right, text beneath each

**C7 waffle (left column)**

* `.lead` "Look at the comics Australia has published itself, and many of them turn out to be someone else's."
* `.reading-guide` "(Reading the waffle: each grid is 100 comic issues. Dark squares reprint a foreign comic, light squares reprint one of the country's own, and grey squares have no reprint recorded.)"
* chart
* `.takeaway` "About 18 of every 100 **Australian** issues reprint a foreign comic, and fewer than 1 reprints an Australian one. In **Japan**, foreign reprints do not fill a single square: about 7 in every 10,000 issues."
* `.caveat` "(These are only the reprints volunteers have linked to their originals, so the true shares are higher everywhere.)"
* `.transition` "Australia is not the only country that imports its comics, but it is near the top of the list."

**C7b butterfly (right column)**

* `.lead` "Every country reprints comics. What differs is whose."
* `.reading-guide` "(Bars to the right show reprints of foreign comics. Bars to the left show reprints of a country's own older comics.)"
* chart
* `.takeaway` "**Australia** ranks third for foreign reprints, behind only Norway and Canada. **The United States** and **Japan** sit at the bottom: when they reprint, they reprint themselves. Eleven of every 100 American issues bring back an older American comic."
* `.caveat` "(Countries with more than 5,000 issues in the database. Yugoslavia is shown as it existed from 1918 to 1991.)"
* `.transition` "It was not always this way. For a few years, Australia made its own comics because it had no choice."

The two takeaways in this row should line up where possible.

### Row 3: C8 full width, text beneath in the left column only

* `.lead` (above the chart, left column) "In 1940, wartime import controls stopped American comics reaching Australian newsstands. Local publishers filled the gap almost overnight."
* `.reading-guide` (above the chart) "(Reading the horizon chart: the strip shows new Australian series each year. When a year is too busy to fit, the extra folds back over the strip in a darker gold, so darker always means busier.)"
* chart, full width
* `.takeaway` "New series jumped from 2 in 1939 to 83 in 1940, and the industry peaked in the mid-1950s. When American comics returned in 1959, local output began to fall. After a second wave of Australian editions of American comics around 1980, it almost disappeared." `<!-- VERIFY against rendered C8 and au_series_by_year.csv: 1939 and 1940 counts, timing of the peaks -->`
* `.caveat` "(Series with an uncertain start year are left out. Each point is a three-year average.)"
* `.transition` "Where did the replacement comics come from? Almost entirely from one country."

Prose stays one column wide even though the chart spans both.

### Row 4: M4 left (text beneath), M5 placeholder right

**M4 flow map (left column)**

* `.lead` "American comics did not only fill Australian shelves. They filled shelves around the world."
* `.reading-guide` "(Each line runs from the United States to a country that reprinted American stories. The thicker the line, the more stories.)"
* chart
* `.takeaway` "Western Europe took the most, led by France with about 71,000 stories. **Australia** took 22,645, more than any other country outside Europe except Brazil." `<!-- VERIFY against reprint_flows.csv -->`
* `.caveat` "(Counts are reprinted stories rather than issues, and only stories that volunteers have linked to their American original. Flows of under 1,000 stories are not shown.)"
* `.transition` "The readers are still here. The next question is where they gather."

M5 (right column) keeps its existing placeholder.

## 5. Footer sources

Add to the data sources list in the footer, if not already present:

* NielsenIQ BookScan figures as published in: Splatt, S. (2024). *Graphic Novels: Can We Grow Them at Home?* Australian Publishers Association, 2023 to 24 Beatrice Davis Editorial Fellowship Report. Link: https://www.publishers.asn.au/common/Uploaded%20files/APA%20Resources/Research/BDEF/BDEF%202023-24%20Report%20-%20Sophie%20Splatt.pdf

## 6. Checklist

* [ ] All six new charts render with real data and no console errors.
* [ ] The C7a, C7, C8 and M4 placeholders are gone. M5 and M6 placeholders remain.
* [ ] §1 now has three rows, ending with C10 and the Japan transition.
* [ ] §4 rows match section 4 of this update.
* [ ] Every new chart has lead, reading guide, takeaway, caveat and transition.
* [ ] Only the three country names are coloured in the new text.
* [ ] The five `<!-- VERIFY -->` comments are in the HTML next to their sentences.
* [ ] No horizontal scroll at 1366 x 768. C7 and C7a fit their columns.
* [ ] `country_meta.csv` kept any population values the student had already updated.

When done, tell the student what changed, report any chart that did not fit its column, and list the five VERIFY sentences.
