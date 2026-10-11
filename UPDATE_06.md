# Update 06: the remaining nine charts

This update adds every remaining chart and its text, so no chart placeholders are left on the page. Follow the layout rules in UPDATE_04.md and STYLE_GUIDE.md exactly (chart rows with text beside, wide chart rows with text above and below, merged text rows, alternating sides). Do not edit the chart specs.

Files supplied with this update:

* `UPDATE_06.md` (this file)
* `vega/`: `c3_japan_market.json`, `m2_japan_mangaka.json`, `c4_manga_streamgraph.json`, `c5_manga_radial.json`, `m3_us_creators.json`, `c6_us_bookscan.json`, `c11_smash_attendance.json`, `m6_au_trends.json`, `c9_au_categories.json`
* `data/`: `japan_manga_market.csv`, `us_bookscan_categories.csv`, `smash_attendance.csv`, `japan_prefectures.topojson`, `au_states.topojson`
* `scripts/`: `fetch_mangaka_wikidata.py`, `fetch_manga_demographics.py`, `build_us_creators_state.py`, `build_au_trends.py`

**Paths:** this repo serves the site from `docs/`. Everywhere this update says `vega/`, `data/` or `index.html`, it means `docs/vega/`, `docs/data/` and `docs/index.html`. Scripts go in `scripts/` at the repo root. The scripts already read from and write to `docs/data/`. Never commit `docs/data/raw/` (add it to `.gitignore`), because it holds large downloads such as the 54 MB Kaggle file.

## 0. Layout fixes (do these first)

### Merged text rows span both columns exactly

The page is a two-column table. Every row either has two cells (left column, right column) or one merged cell that spans both. A merged cell starts at the left edge of the left column and ends at the right edge of the right column, exactly like merging two cells in a table. Its edges line up with the column edges of every other row on the page.

Currently, merged text rows are a narrower block centred in the middle of the row (capped by `--measure-wide`). That is wrong and must be removed:

* Merged text rows use `grid-column: 1 / -1` with no `max-width`, no auto margins and no centring of the text block.
* Delete the `--measure-wide` variable and every rule that uses it.
* Text inside a merged row is left-aligned and starts at the left edge of the left column.
* This applies to every merged text row: header intro, scope note and byline, section intros, the text rows above and below wide charts, and the closing text.
* Check: draw a vertical line down the left edge of the left column and the right edge of the right column. Every row's content, text or chart, must start and end on those two lines.

Update the "Placement" paragraph in STYLE_GUIDE.md section 3 to add: "A merged text cell starts at the left edge of the left column and ends at the right edge of the right column, like a merged table cell. It is never a narrower centred block."

### Headings are centre aligned

The student has added "Headings must be center aligned" to STYLE_GUIDE.md section 2. Apply it to the page title, page subtitle and all five section headings, including the accent bar above each section heading, which should sit centred too. Chart titles inside the Vega specs stay left-aligned, since they belong to their charts. Do not change the specs.

## 1. Data the student must generate first

Five charts need data that has to be downloaded on the student's machine. The student runs these before you build (or you run them, if you can reach the internet). Each script writes its CSV into `data/`.

| Script | Creates | Used by | Notes |
| :- | :- | :- | :- |
| `python scripts/fetch_mangaka_wikidata.py` | `mangaka_prefecture_decade.csv`, `japan_prefecture_population.csv` | M2 | Waits out Wikidata's one-query-a-minute limit, or uses two CSVs downloaded by hand into `data/raw/` (see the top of the script) |
| `python scripts/fetch_manga_demographics.py` | `manga_demo_by_year.csv`, `manga_demo_current.csv` | C4, C5 | About 4 to 5 minutes |
| or `python scripts/process_manga_kaggle.py` | same two files | C4, C5 | Manual route if the Jikan API is unreachable: uses a MyAnimeList export from Kaggle saved as `data/raw/manga.csv` |
| `python scripts/build_us_creators_state.py` | `us_creators_state_pc.csv` | M3 | Prints any birth states it could not match |
| `python scripts/build_au_trends.py` | `au_trends_states.csv` | M6 | Needs a manual Google Trends download first, see the top of the script |

If a CSV is missing when you build, embed the chart anyway (it will show its error box) and list it in your summary. Do not invent data.

## 2. Chart registry

Copy the nine specs into `/vega/`, the data files into `/data/`, the scripts into `/scripts/`, and add to `CHARTS`:

```js
c3:  { spec: "vega/c3_japan_market.json" },
m2:  { spec: "vega/m2_japan_mangaka.json" },
c4:  { spec: "vega/c4_manga_streamgraph.json" },
c5:  { spec: "vega/c5_manga_radial.json" },
m3:  { spec: "vega/m3_us_creators.json" },
c6:  { spec: "vega/c6_us_bookscan.json" },
c11: { spec: "vega/c11_smash_attendance.json" },
m6:  { spec: "vega/m6_au_trends.json" },
c9:  { spec: "vega/c9_au_categories.json" }
```

Width notes:

* `m2` is a 3 by 2 grid of fixed 300 px maps, about 950 px wide. It goes in a wide chart row. Do not apply any width fix to it.
* `c5` has a fixed 300 px chart plus its legend, about 430 px. It fits a half column.
* All other new charts use `"width": "container"`.

## 3. M5 is replaced by C11

There is not enough attendance data to map Australian conventions city by city. M5 is replaced by **C11**, a chart of attendance at SMASH!, Sydney's manga and anime convention, from 2007 to 2026. Remove the M5 placeholder and put C11 in its row. The page still has five maps (M1, M2, M3, M4, M6), well above the minimum of three.

## 4. Colour note: manga demographics

C4 and C5 introduce one new set of colours, used only for manga audiences. Add this to STYLE_GUIDE.md section 5:

> **Manga audiences (C4 and C5 only).** Reds for manga written for teenagers (shōnen dark red `#B50F2A`, shōjo pink `#F0849A`), teals for manga written for adults (seinen dark teal `#00829E`, josei light teal `#45C6D1`), greys for kids and not stated. The reds tie to Japan. This palette appears nowhere else.

## 5. Placement and text, section by section

Bold country names use the colour classes. Lines marked VERIFY must get an HTML comment `<!-- VERIFY: ... -->` beside them, because they depend on data the student has not generated yet.

### §2 Japan makes its own comics, and keeps them.

1. Text row: existing section intro (unchanged).
2. **Chart row, text left, C3 right.**
   * `.lead` "In 2025, Japanese readers spent ¥692.5 billion on manga, about US$4.4 billion. Almost all of it was written and drawn in **Japan**."
   * `.reading-guide` "(Each band is one format. The top edge of the chart is the whole market.)"
   * `.takeaway` "Digital manga grew three and a half times in ten years, from ¥149 billion in 2016 to ¥527 billion in 2025. It is now about three quarters of the market, while printed volumes and magazines have both shrunk."
   * `.caveat` "(Print figures cover books and magazines sold through wholesalers. Digital figures are estimates of reader spending.)"
   * `.transition` "**Japan** does not only read its own comics. It grows the people who draw them, all over the country."
3. Text row (above M2):
   * `.lead` "Tokyo is the centre of Japanese publishing, but manga artists come from every corner of the country."
   * `.reading-guide` "(Each map is one generation, grouped by the decade an artist was born. Darker purple means more manga artists for every million people living in that prefecture today.)"
4. Wide chart row: **M2**.
5. Text row (below M2):
   * `.takeaway` VERIFY "Per person, several rural prefectures have produced as many manga artists as Tokyo, in every generation." Rewrite once the real map is visible: name the two or three prefectures that stand out, and say whether Tokyo leads.
   * `.caveat` "(Only artists with a recorded birthplace and birth year on Wikidata are counted, so famous artists are over-represented. Rates use today's population, not the population when each artist was born.)"
   * `.transition` "What those artists draw, and who for, has changed too."
6. **Chart row, C4 left, text right.**
   * `.lead` "Manga is not one genre. It is sold by the reader it is written for."
   * `.reading-guide` "(Reading the streamgraph: each band is one audience, and its thickness shows how many popular series started that year. Reds are manga written for teenagers, teals manga written for adults.)"
   * `.takeaway` VERIFY "Manga written for adult men, seinen, has grown fastest among popular titles, and now rivals shōnen, the boys' adventure manga most Western readers know." Check against the rendered C4 and rewrite if the pattern is different.
   * `.caveat` "(Based on the 5,000 manga with the most members on MyAnimeList, an English-language site. It shows what international fans follow, not everything published in Japan.)"
   * `.transition` "So who is manga written for right now?"
7. **Chart row, text left, C5 right.**
   * `.lead` "Look only at the series that were still being published in 2023."
   * `.reading-guide` "(Each slice is one audience. The wider and longer the slice, the more series.)"
   * `.takeaway` "Manga for adult men, seinen, now slightly outnumbers manga for teenage boys, shōnen: 218 running series against 211. Almost half of all popular running manga are written for adults."
   * `.caveat` "(Same 5,000 MyAnimeList titles as the chart above, counting the 492 still being published in August 2023 that have a stated audience. Another 520 running series list no audience and are left out.)"
   * `.transition` "Japan makes comics for every age group. **America**'s comics industry grew up differently."

### §3 America reprints itself.

1. Text row: existing section intro (unchanged).
2. **Chart row, text left, M3 right.**
   * `.lead` "American comics have been made all over the country, but not evenly."
   * `.reading-guide` "(Darker purple means more comic creators born in that state for every million people living there today.)"
   * `.takeaway` VERIFY "Per person, [state] and [state] have produced the most comic creators." Fill in from the rendered M3.
   * `.caveat` "(Counts only creators in the Grand Comics Database with a recorded birth state. Rates use 2024 Census Bureau population estimates.)"
   * `.transition` "Those creators work in an industry that now sells far more than superheroes."
3. **Chart row, C6 left, text right.**
   * `.lead` "Superhero comic books are what most people picture when they think of American comics. They are not what Americans buy most."
   * `.reading-guide` "(Each line is one kind of graphic novel sold in US bookshops and online. Red marks adult fiction, which is mostly manga.)"
   * `.takeaway` "Adult fiction nearly doubled, from 15.2 million copies in 2020 to 28.2 million in 2023, after peaking at 35.4 million in 2022. In 2023, manga made up 21.8 million of the 44.7 million graphic novels sold, almost half."
   * `.caveat` "(BookScan covers bookshops and online retailers, about 85 per cent of the book market, but not comic shops, libraries or school book fairs.)"
   * `.transition` "**America**'s bookshops are now full of comics from **Japan**. So are Australia's."

### §4 changes

* The M5 row becomes a **chart row, C11 left, text right.**
   * `.lead` "The appetite for manga and anime shows up in person, too."
   * `.reading-guide` "(Each point is one year's attendance at SMASH!, Sydney's manga and anime convention. Hollow points are minimum figures.)"
   * `.takeaway` "SMASH! grew from 1,435 visitors in 2007 to 53,071 in 2026, about 37 times bigger, and it has grown every year since it returned after the pandemic."
   * `.caveat` "(Attendance as reported by the convention and collected on Wikipedia. Some years are reported only as 'more than' a figure, and none were published for 2016 and 2017.)"
   * `.transition` "Those fans are not spread evenly across the country."
* The M6 row stays a **chart row, text left, M6 right**, with this text:
   * `.lead` "Which comics Australians look for depends on where they live."
   * `.reading-guide` "(Each state is coloured by the share of Google searches for 'manga', compared with searches for 'comics'. The colour scale runs from 60 to 80 per cent, so even the palest state still searches mostly for manga.)"
   * `.takeaway` "In every state and territory, Australians search for manga more than twice as often as for comics. The Northern Territory leans furthest towards manga, at 76 per cent of searches, and Tasmania the least, at 67 per cent."
   * `.caveat` "(Google Trends shows relative interest, not the number of searches, over the past five years.)"
   * `.transition` "The readers are here. The question is who will make comics for them."

### §5 Can we grow them at home?

1. **Chart row, text left, C9 right.**
   * `.lead` "The fastest-growing comic readers in **Australia** are the youngest."
   * `.reading-guide` "(Grey dots are sales in 2020, gold dots sales in 2023. The longer the line, the bigger the growth.)"
   * `.takeaway` "Sales of children's graphic novels in **Australia** grew 3.3 times in three years, to almost 1.1 million copies in 2023. Adult fiction grew 1.8 times."
   * `.caveat` "(Excludes manga and superhero titles, which BookScan counts separately. Most of the best-selling children's titles are imported, such as Dog Man.)"
   * `.transition` none. The closing text row follows.
2. Text row: the existing closing text (unchanged).

## 6. Footer sources

Add these to the data sources list, each with its link:

* All Japan Magazine and Book Publishers' and Editors' Association, Research Institute for Publications, annual comic market reports 2016 to 2025 (shuppankagaku.com, as reported by hon.jp and nippon.com)
* Wikidata, manga artists' birthplaces and prefecture populations, CC0 (wikidata.org)
* MyAnimeList, top 5,000 manga by members, via a Kaggle export: 'MyAnimeList Anime and Manga Datasets' by Andreu Vall Hernàndez (kaggle.com/datasets/andreuvallhernndez/myanimelist), data as of August 2023
* U.S. Census Bureau, Vintage 2024 state population estimates, NST-EST2024 (census.gov)
* Circana BookScan, US graphic novel sales by category 2020 to 2023, and Brian Hibbs's 2023 BookScan analysis, both as published in Splatt (2024)
* Google Trends, Australia, 'manga' compared with 'comics', past five years (trends.google.com), with the download date
* SMASH! convention attendance, Wikipedia (en.wikipedia.org/wiki/SMASH!_(convention))
* Japan prefecture boundaries: Global Map Japan (Geospatial Information Authority of Japan), via the dataofjapan/land GitHub repository
* Australian state boundaries: tonywr71/GeoJson-Data GitHub repository
* US state boundaries: vega-datasets (us-10m)

## 7. Checklist

* [ ] Every merged text row starts at the left column's left edge and ends at the right column's right edge. `--measure-wide` is gone.
* [ ] Page title, subtitle, section headings and their accent bars are centred. Chart titles are unchanged.
* [ ] All nine charts are embedded. Any whose CSV is missing are listed in your summary.
* [ ] No chart placeholders remain. M5 is gone and C11 is in its place.
* [ ] Every new chart follows the row rules and has its full five-part text.
* [ ] Every VERIFY sentence has an HTML comment beside it.
* [ ] The demographic palette note is added to STYLE_GUIDE.md.
* [ ] Footer sources are added.
* [ ] No horizontal scroll at 1366 x 768. M2 fits in its wide row.

When done, list the three remaining VERIFY sentences (M2, C4, M3) and any missing data files.
