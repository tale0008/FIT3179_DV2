# UPDATE_15: to-do fixes that needed no input

Base commit: `6e92c60` ("Change the text to have more of a story focus"). M4 is not touched, so this update can go in alongside the M4 zoom work.

## What changes

* **Chart text size.** Axis, legend and label text goes from 11px to 12px, and subtitles from 12px to 13px, in every spec except C5 and M4, and in the `main.js` defaults. (Notes 11 p. 6, class critique.)
* **C2 heatmap.**
  * Genre labels are plain English: Humour, Superhero, Funny animals, Sci-fi, Adventure, Teen, Fantasy, Western, Horror, Children, War, Romance, Non-fiction, Mystery, Crime.
  * The two cells the text names are labelled: Brazil superhero 63%, Norway humour 33%.
* **C4 streamgraph.** Shōnen, Shōjo, Seinen and Josei are labelled on their bands, so the chart passes the greyscale test. The legend click still works.
* **M1 map.** Norway is labelled ("Norway 10,600") in the per million, World view. It is hidden in the Total and Europe views.
* **C10 scatter.** Gridlines only at 1k, 10k and 100k. The caveat that repeated the subtitle is deleted.
* **C11 and C9.** The zero label is plain "0", not "0k" or "0M". C11's line is linear instead of smoothed.
* **Headline titles** (decision 10):
  * C1: "Australia's comic boom ended decades ago"
  * C7: "Australia prints other countries' comics. Japan prints its own."
  * C7a: "Australians buy more comics every year. They make almost none."
  * C8: "Australia's comics boomed while American comics were banned"
  * C9: "Children are Australia's fastest-growing comic readers"
* **Caveats** (decision 6). Each chart keeps at most one, and any that repeated the subtitle are cut or trimmed. 18 down to 13:
  * deleted: C1, C10, M3, C11, C9
  * trimmed: M1, C2, C5, C7b, C8, M4, M6
* **"%" everywhere.** C6 caveat and M6 takeaway.
* **Bold numbers.** At most one per paragraph (§3 intro and M3).
* **Text beside charts is top-aligned** (decision 11), so it starts level with the chart title.
* **CDN pinned** (decision 3): vega 5.33.1, vega-lite 5.23.0, vega-embed 6.29.0.
* **Generative AI line** in the footer now covers data, chart design, code and page text.
* **STYLE_GUIDE.md** records the headline-title exception, the one-caveat rule, the 12px and 13px sizes, one bold number per paragraph and top alignment.

Every number in changed text was rechecked against the CSVs (Norway 10,641 per million, Brazil superhero 63.1%, Norway humour 32.7%, AU sales rising every year from 2020 to 2023, 14 new AU series from 2020 to 2023, children's sales 3.30 times).

## Steps for Claude Code

1. Run `git status` and `git log -1`. If the working tree has uncommitted M4 zoom work, commit or stash it first.
2. Apply the patch from the repo root: `git apply --3way UPDATE_15.patch`. If the log is still `6e92c60` and the tree is clean, copying everything in `files/` over the repo (keeping paths) does the same thing. If there are conflicts, report them rather than guessing. The only file both updates are likely to touch is `docs/js/main.js`, and this update changes just two lines there (the `labelFontSize` values in `EMBED_OPTIONS`).
3. Do not change `docs/vega/m4_flow_map.json` or `docs/vega/c5_manga_radial.json`.
4. Serve with `python -m http.server 8000 --directory docs`, open http://localhost:8000 at 1366x768, and check:
   * every chart loads, and the console has no errors
   * there is no horizontal scroll
   * C2 shows plain genre names and the 63% and 33% labels
   * C4 shows the four band labels
   * M1 shows the Norway label, which disappears on Total and on Europe
   * the five new chart titles are there
5. Commit as "UPDATE_15: to-do fixes" and push.

## Previews

`preview/` has before and after renders at 1366px for M1, C1, C2, C10, C4, M3, C7a, C7, C8, C11 and C9, plus M1 in the Europe view.

## Also in this folder

`MOODLE_DESCRIPTION.md` is a first draft of the Moodle description (domain, why, who, then what and how per chart). It is not on the page.
