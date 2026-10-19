# UPDATE_09: typography, number checks and page clean-up

This update does the typography critique point and the loose ends from `TODO.md` that needed no decision from you. Every changed file is in `files/`, tested by rendering the whole page headlessly at 1366x768 and at phone width (390px). No horizontal scroll at either width, all 18 charts load, and the console shows no new warnings.

Base commit: `2e32296` ("Delete notes directory"). If the repo has moved on, apply `UPDATE_09.patch` with `git apply --3way` instead of copying, and report any conflicts rather than guessing.

## What changes, and why

### 1. Typography (critique: "the main heading can use an interesting typography, balanced with readability")

* **Web fonts are switched on.** The commented-out Google Fonts block in `<head>` is now live. The spec allows any CSS library, and this is a font file, not a code library.
* **Page title in Bangers**, a comic-book lettering font, with a flat pale offset shadow like a printed panel title. Only the title uses it, so the reading text stays easy to read. Preview: `preview/title_before.png`, `preview/title_after.png`, `preview/title_phone.png`.
* **"Australia" in the title is gold**, like every other mention of Australia on the page, so the title also acts as the legend.
* **Section headings** keep Bebas Neue, **body text** Source Serif 4, and **small text** Inter. These were already named in the CSS but never loaded, so until now the page showed system fallbacks.
* **Charts now use Inter too** (`config.font` in `main.js`), so chart text matches the page's small text instead of Vega's default Helvetica or Arial.
* **`main.js` waits for the fonts** (`document.fonts.ready`) before drawing charts. Vega measures text once at layout, so drawing before Inter loads would size titles and labels for the wrong font.
* **Bold weight 700 of Source Serif 4** is now loaded, so the bold country names are a real bold, not one faked by the browser.
* **Line breaks:** headings use `text-wrap: balance` so wrapped headings have even lines, and paragraphs use `text-wrap: pretty` to avoid one word alone on the last line.
* **STYLE_GUIDE.md** has a new section 6, Typography: which font does which job, sizes, weights and alignment. The old section 6 (the example) is now section 7.

### 2. The nine `<!-- VERIFY -->` comments are checked and removed

Each figure was checked against the CSV and the rendered chart. Four were wrong and are fixed:

* **C8 (horizon chart), wrong.** The text said new series "jumped from 2 in 1939 to 83 in 1940" and peaked in the mid-1950s. `au_series_by_year.csv` has 2 in 1939, 4 in 1940, 15 in 1941 and 29 in 1944. The 1950s peak is 85 in 1955, and the busiest single year is 1982 (109), in the second wave. New takeaway: "New series grew from 2 in 1939 to 29 in 1944, and reached 85 in 1955. When American comics returned in 1959, local output fell. A second wave, Australian editions of American comics, peaked at 109 new series in 1982. After that, output almost disappeared."
  * The C8 caveat now says the chart shows three-year averages, so the single-year counts in the text sit higher than the strip.
  * The C8 lead "filled the gap almost overnight" becomes "rushed to fill the gap", and the conclusion's "appeared almost overnight" becomes "grew within a few years", since the climb took about four years.
* **C10 (scatter), wrong.** The US averages 6.7 issues per series, not 4, and Mexico 121, not 119 (`country_output.csv`). Japan (37) and Australia (10) were right.
* **C2 (genre heatmap), misleading.** "Superheroes dominate American comics" is true (26% of US stories), but superheroes are an even bigger share in Brazil (63%) and Germany (44%), which print large numbers of American comics. The new takeaway says so, and names Norway, the Netherlands and Sweden as the humour countries (humour is their top genre).
* **M2 (Japan maps), rewritten as the comment asked.** Across all generations Kōchi leads with about 38 manga artists per million people, ahead of Tokyo (34), with Akita and Iwate close behind (34 and 33). Tokyo tops only the 1960s map.
* **C4 (streamgraph), sharpened.** Seinen became the biggest band in the 1990s and kept pace with shōnen (566 series started in the 2010s against 537). Shōjo shrank most. The old "grown fastest" was not quite what the chart shows.
* **Checked and correct, comment just removed:**
  * M1: Norway 10,640 per million, about 6.0 times the US (1,786). Australia 1,273, Japan 1,119. If you later switch to World Bank populations (decision 7), these need checking again.
  * C1: both Australian humps are visible, and the 1980s one is slightly taller.
  * M4: France 70,899 stories, Australia 22,645, second outside Europe after Brazil (23,471).
  * Footer: Google Trends date 11 October 2026 matches the day `geoMap.csv` was first committed.
* **C7a, small consistency fix:** the lead said sales "nearly tripled in four years" while C9 says "three years" for the same 2020 to 2023 figures. Both now say three years, and the takeaway says "Over the same years, 2020 to 2023".

### 3. Waffle reading guide removed

Your own critique note: the waffle's reading guide repeated what the chart subtitle already says (100 issues per grid, dark, light and grey squares). It is deleted. Other reading guides are untouched, since merging footnotes is still your decision.

### 4. Clean-up

* **Unused CSS deleted** from `style.css`: `.placeholder`, all `.ph-*`, `.todo`, `.stat` and `.caption`. Nothing on the page used them, so nothing looks different.
* `--ph-bg` is deleted and `--ph-border` is renamed `--link-line`, since its only remaining use is the link underline.
* **`main.js`**: the comment about deleting placeholder content and the leftover `classList.remove("placeholder")` are tidied.
* **Footer Generative AI line**: your own wording is kept. Only `class="pending"` is removed, so it no longer shows as grey italic placeholder text.

## Instructions for Claude Code

1. Confirm `git log -1` is `2e32296` and the working tree is clean. If it isn't, stop and use `git apply --3way UPDATE_09.patch` instead of step 2.
2. Copy these 4 files from `files/` over the repo, keeping paths:
   * `STYLE_GUIDE.md`
   * `docs/index.html`
   * `docs/css/style.css`
   * `docs/js/main.js`
3. Run `git diff --stat` and check only those 4 files changed. No spec in `docs/vega/` changes.
4. Check that `docs/index.html` has no `VERIFY` left: `grep -n VERIFY docs/index.html` should print nothing.
5. Preview with `python -m http.server 8000 --directory docs`, then check:
   * the title is in comic lettering with "Australia" in gold, on desktop and on a narrow window
   * section headings are tall condensed capitals, and body text is a serif
   * chart text matches the small grey text on the page (Inter)
   * all 18 charts load, and the browser console has no errors
   * no horizontal scroll at 1366x768
6. Commit with the message `Update 9: typography, number checks and clean-up`, then push.

## Optional steps, only if you decide to

These are decisions 2 and 3 in `TODO.md`. Skip them if you haven't decided.

* **Pin the chart libraries (decision 3).** In `docs/index.html`, change the three script tags to the exact versions the live site loads today:
  * `https://cdn.jsdelivr.net/npm/vega@5.33.1`
  * `https://cdn.jsdelivr.net/npm/vega-lite@5.23.0`
  * `https://cdn.jsdelivr.net/npm/vega-embed@6.29.0`
* **Page licence (decision 2).** In the footer `Licence` line, either delete the grey `<span class="pending">[Licence for the rest of the page ...]</span>`, or replace it with "The rest of this page is shared under CC BY-SA 4.0 too." (my recommendation, matching the GCD data).
