# UPDATE_08: class critique fixes (colour, M1 legend, text size, C7a)

This update acts on four points from the 12 October class critique (`notes/critique.txt`). Every changed file is supplied in `files/`, already tested by rendering the whole page headlessly at 1366x768. Your job is to copy them in, check the diff matches the list below, and preview.

Base commit: `f05fdab`. If the repo has moved on since then, apply `UPDATE_08.patch` with `git apply --3way` instead of copying, and report any conflicts rather than guessing.

## What changes, and why

### 1. Colour clash: red now only means Japan

* **C4 and C5 (manga audiences):** the reds are replaced. Red already means Japan, and the class flagged the clash.
  * shōnen `#B50F2A` becomes dark green `#2D6A1F`
  * shōjo `#F0849A` becomes light green `#A9CF7F`
  * seinen `#00829E` becomes dark teal `#0E8C8C` (moved away from the US blue)
  * josei `#45C6D1` becomes light teal `#86D3CE`
  * Kids and "Not stated" stay grey.
  * The palette was checked with a colour-vision validator. Neighbouring bands pass for normal vision and for colour blindness, and the dark teal is clearly separated from the US blue.
* **M6 (state searches):** the `reds` scheme becomes `purples`. It shows an amount, and the style guide says purple is the only colour for amounts. It also stops a red Australia map reading as "Japan". The subtitle now says "Darker purple".
* **C3 and C6 keep their reds** on purpose: C3 is Japan's own market, and C6's red line is manga. Both mean Japan.
* **C4 reading guide text** in `index.html` now says "Greens are manga written for teenagers" instead of "Reds".
* **STYLE_GUIDE.md section 5** records the new audience palette and the M6 rule.

### 2. M1: the legend no longer overlaps the globe

* The legend moves from inside the map (bottom left) to a horizontal bar above it, under the subtitle.
* `main.js` gives M1 `aspect: 0.5`, the same mechanism M4 uses, so the map height follows the globe's shape and there is no empty band.

### 3. Small grey text is larger and darker

* **Every spec:** any chart text under 11px is raised to 11px. This covers legend labels (some were 9px), axis labels and annotations. Subtitles go from 11px to 12px, and their colour from `#666` to `#555`. The grey annotation text in C10 and C11 goes from `#77766F` to `#5F5E58`.
* **`main.js`:** `EMBED_OPTIONS.config` now sets 11px axis and legend labels, 12px titles and darker label ink for any chart that doesn't set its own. A size set inside a spec still wins.
* **Subtitles re-wrapped** at about 62 characters for the half-width charts, so the larger text doesn't widen the charts. The wording is unchanged except in C7a and M6, which are covered in their own sections.
* **`style.css`:** `.caption` goes from 14px to 15px, and `.meta h4` from 12px to 13px.

### 4. C7a: two units, now two clearly separate panels

* **The problem:** copies sold (in millions) and new series (a count) shared one chart and one legend, so it read as one measure.
* **The fix:** two stacked panels, each with its own bold title and source line.
  * "Graphic novels sold in Australian shops": grey bars with value labels. The y axis is removed because every bar is labelled.
  * "New comic series made in Australia": one gold square per series, with a count label under each year.
  * The shared colour legend is gone, because the panel titles do its job.
* **Bug fix:** the old spec shared one `xOffset` scale across both panels, which set the sales bars to a fixed 18px width (the console warned "Cannot use the relative band size with linear scale"). The scales are now resolved independently.
* **Text in `index.html`:**
  * The C7a reading guide is removed, since the chart now explains itself. This also follows your note about moving reading guides into the charts.
  * The takeaway now explains how the two counts link: "The two panels count different things, copies bought and series made, but together they show the gap: demand nearly tripled while local supply stayed in single figures each year."
  * The C7a `<!-- VERIFY -->` comment is deleted, because the figure was checked.
* **Numbers checked against the CSVs:**
  * Sales total 495,083 in 2020 and 1,380,854 in 2023, which is 2.79 times. That fits "nearly tripled", "about 500,000" and "1.38 million".
  * `au_series_by_year.csv` has 2, 7 and 5 new series for 2020 to 2022 and no 2023 row (imputed as 0). That makes 14 in total, single figures each year.

## Instructions for Claude Code

1. Confirm `git log -1` is `f05fdab` and the working tree is clean. If it isn't, stop and use `git apply --3way UPDATE_08.patch` instead of step 2.
2. Copy every file from `files/` over the repo, keeping paths. For example, `files/docs/vega/c7a_gap.json` goes to `docs/vega/c7a_gap.json`. There are 22 files:
   * `STYLE_GUIDE.md`
   * `docs/index.html`, `docs/js/main.js` and `docs/css/style.css`
   * all 18 specs in `docs/vega/`
3. Run `git diff --stat` and check that only those 22 files changed. In the 17 specs other than C7a, the diff should only touch font sizes, subtitle colour and wording, subtitle line breaks, the M1 legend block, and the C4, C5 and M6 colours.
4. Check every spec still parses: `python -c "import json,glob;[json.load(open(f,encoding='utf-8')) for f in glob.glob('docs/vega/*.json')]"`.
5. Preview with `python -m http.server 8000 --directory docs`, then check:
   * The console shows no errors, and no "relative band size" warning.
   * There is no horizontal scroll at 1366 wide.
   * The M1 legend sits above the globe and doesn't touch it.
   * C4 and C5 show greens and teals, with no red.
   * M6 is purple.
   * C7a shows two titled panels, with the bars centred on their year labels.
6. Don't change anything else. If something renders differently from the previews in `preview/`, report it instead of redesigning it.
7. Suggested commit message: `Update 08: critique fixes (audience palette, M1 legend, text sizes, C7a split)`.

## Not in this update (next steps)

* Cutting the footnotes and merging caveats, plus moving the other reading guides into the charts (the waffle first).
* Adding more "why" and story to the text.
* Interactivity (UPDATE_09): M4 zoom, a flat projection and arrowheads, plus linked filters.
* Web fonts, which are still waiting on approval.
