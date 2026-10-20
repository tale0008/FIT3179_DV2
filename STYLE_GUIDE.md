# Style Guide: text, colour and type

This guide sets the writing, colour and typography rules for the FIT3179 DV2 page. It is based on the style of the author's DV1 dashboard ("Housing Tenure Over The Ages"). It overrides any draft text or colour choice in BUILD_BRIEF.md where the two disagree.

## 1. The page voice

* Written for a curious adult with no background in comics or statistics.
* Plain words, short sentences, short paragraphs. Most paragraphs are one or two sentences.
* Every claim is concrete. Prefer "17 of every 100 issues" or "about 10,600 issues per million people" over "a high share".
* Never more than a few numbers per paragraph. Pick the one that carries the point.
* Confident and direct, never hedging in the main text. Uncertainty goes in the italic caveat (see section 3), not in the takeaway.

## 2. Headings carry the argument

Section headings are claims or questions, never topic labels. Read in order, the headings alone should tell the story.

| Section | Heading |
| :- | :- |
| Page title | Australia reads comics. Australia doesn't make them. |
| Page subtitle | Who makes the world's comics, and who only reads them, 1930 to 2026 |
| §1 | Comics are everywhere. They are not made everywhere. |
| §2 | Japan makes its own comics, and keeps them. |
| §3 | America reprints itself. |
| §4 | Australia's comics are mostly someone else's. |
| §5 | Can we grow them at home? |

Chart titles are plain descriptions of what is shown, with a subtitle line giving the unit, the period and the source in short form. Where a title names a country or category, that word is coloured to act as the legend (see section 5).
Headings must be center aligned.

## 3. The per-chart text pattern

Every chart follows the same five-part pattern. Parts marked optional can be dropped when they add nothing.

1. **Lead-in** (1 to 3 short paragraphs, about 30 to 60 words). Sets up the question the chart answers, or explains why it matters. Often continues from the previous chart's transition.
2. **Reading guide** (optional, only where the chart cannot be read without one). Most charts need none: the title, axes, legend and direct labels already say how to read them, and repeating that in text clutters the page. Never describe a legend, an axis or what a dot or bar is. When a guide is genuinely needed (for example the horizon chart's folded bands, or a key the chart has no legend for), it is one short line in the chart subtitle, not a paragraph in the text. There is no "Reading the ..." paragraph in the text column.
3. **The chart**, with its title and subtitle.
4. **Takeaway** (1 or 2 short paragraphs, about 20 to 40 words). States the single finding with one or two specific numbers. Never just describes the chart.
5. **Caveat** (optional, italic, in brackets, about 15 to 40 words). Data limits, definitions, exclusions. Example: "(The database is built by volunteers, so it records how thoroughly each country's comics have been catalogued as well as how many were made.)"
6. **Transition** (one sentence, often a question). Hands over to the next chart or section. Example: "So who makes comics depends on how you count. The next question is when."

Total per chart: about 100 to 150 words. Per section intro: about 40 to 70 words.

Placement: the page reads left to right, row by row. A chart in one column has all of its text directly beside it in the other column, and chart rows alternate sides. A chart spanning both columns has its lead-in in a merged text row directly above it, and the rest directly below it. Text with no chart is one merged cell across both columns, never two columns of text. A merged text cell starts at the left edge of the left column and ends at the right edge of the right column, like a merged table cell. It is never a narrower centred block. A chart never appears without its lead-in and takeaway.

## 4. Page-level structure

* **Header band:** title, subtitle, then a short intro paragraph that defines the key terms, with the three country names coloured so the intro doubles as the page legend.
* **Scope note** directly under the intro, one or two sentences, stating what the figures count. Draft: "Unless a chart says otherwise, these figures count comic issues, not copies sold. They come from the Grand Comics Database, a volunteer catalogue of over two million issues."
* **Sections** each open with a heading band, then a short intro, then charts in the pattern above.
* **Conclusion** ("Can we grow them at home?") recaps in short, punchy single-sentence paragraphs and ends on one memorable line.
* **Footer, "About this visualisation":** author, date, unit, a Generative AI acknowledgement, data sources grouped and linked, then "Notes on the data". This is required and marked.

## 5. Colour rules

Colour is semantic. Each colour means one thing, and it means that thing everywhere on the page.

| Colour | Hex (charts) | Hex (inline text) | Means |
| :- | :- | :- | :- |
| Gold | `#B07A00` | `#8A5F00` | Australia |
| Red | `#C8102E` | `#C8102E` | Japan |
| Blue | `#1F4E9A` | `#1F4E9A` | United States |
| Light grey | `#C9C9C4` | not used for text | Every other country, the past, context |
| Dark grey | `#6F6D66` | not used for text | The country the reader is following, when it is not one of the three (see section 8) |
| Cyan | `#00B4D8` | not used for text | Outline of the followed country on the world maps (M1, M4). An outline only, never a fill, so the map's own colours still show |
| Purple ramp, light to dark | Vega `purples` scheme | not used for text | "How much" on maps and heatmaps |

Rules:

* **Coloured words are the legend.** Only the names of the three countries (and the matching words in chart titles) are coloured in text, always bold. Nothing else in the text is coloured, so the colour always means the same thing.
* Use the **inline text hex** for coloured words. The chart gold fails text contrast on the cream background, so text uses the darker `#8A5F00`.
* **Grey is context.** Countries outside the story, and "before" values in before-and-after charts, are grey. The country being discussed is coloured.
* **Purple is only for amounts.** A single-hue ramp, light means less, dark means more. Never used for categories.
* A new category that is not a country (for example "foreign reprints" vs "domestic reprints" in the waffle) uses shades of the relevant country's colour plus grey, not a new hue. Add a new hue only when no existing one fits, and say what it means in the chart title.
* No rainbow or multi-hue scales anywhere.
* **Manga audiences (C4 and C5 only).** Greens for manga written for teenagers (shōnen dark green `#2D6A1F`, shōjo light green `#A9CF7F`), teals for manga written for adults (seinen dark teal `#0E8C8C`, josei light teal `#86D3CE`), greys for kids and not stated. No reds, so red only ever means Japan. This palette appears nowhere else.
* **M6 (state search shares) uses the purple ramp**, like every other amount on the page. Red is kept for Japan and manga lines, never for an amount.

## 6. Typography

Four typefaces, each with one job. All load from Google Fonts in `index.html`, and each CSS stack falls back to a similar system font.

| Typeface | Used for | Where it is set |
| :- | :- | :- |
| Bangers | The page title only. Comic-book lettering ties the page to its topic. | `--font-comic` in `style.css` |
| Bebas Neue | Section headings and the footer title, uppercase. | `--font-display` |
| Source Serif 4 | All reading text: leads, takeaways, caveats, transitions. | `--font-body` |
| Inter | Small text (scope note, byline, footer) and all chart text. | `--font-ui`, and `config.font` in `main.js` |

Rules:

* **Display fonts stay big.** Bangers and Bebas Neue are only used at 32px and above, never for sentences.
* **Body text** is 18px with a line height of 1.6. Text beside a chart is held to about 68 characters a line.
* **Caveats** are 16px italic in the muted grey.
* **Chart text** is never smaller than 11px. Chart titles are 16px bold, subtitles 12px in `#555`.
* **Bold** is for country names and key numbers only. No underlines except links, no all-caps in body text.
* All text is left-aligned, except headings and the title, which are centred.

## 7. Example: §1 written in this style

Draft text for §1. Lines marked [verify] contain a finding that must be checked against the rendered chart before it is used.

**Intro (header band)**

> A comic can be made in Australia, or made somewhere else and printed here. This page follows both: comics made in **Australia**, comics made in **Japan** and **the United States**, and the reprints that carry them around the world.

**§1 heading:** Comics are everywhere. They are not made everywhere.

**M1, world map**

* Lead-in: "Start with where comics come from. Counted in total, a handful of large countries publish most of the world's comics. Counted per person, the map changes."
* Takeaway: "Norway publishes about 10,600 comic issues for every million people, around six times the rate of **the United States**. **Australia**, at about 1,300 per million, sits just below it."
* Caveat: "(The database is built by volunteers, so this map also measures how thoroughly each country's comics have been catalogued. **Japan**, the world's largest comics market, looks small here for that reason.)"
* Transition: "So who makes comics depends on how you count. The next question is when."

**C1, ridgeline**

* Lead-in: "Comic industries did not grow at the same time. Some countries had their boom before television arrived, others are still in theirs."
* Takeaway [verify]: "**Australia**'s busiest years came early, in the 1950s, and its strip all but disappears after the mid-1980s. **Japan** and **the United States** are still publishing."
* Caveat: "(Series with an uncertain start year are left out, so the earliest decades are undercounted.)"
* Transition: "Countries did not only publish at different times. They published different kinds of comics."

**C2, genre heatmap**

* Lead-in: "Each country built its comics around different stories."
* Takeaway [verify]: "Superheroes dominate **American** comics, but most other countries built their industries on humour, adventure and stories for children."
* Caveat: "(A story can carry more than one genre, so shares count genre tags rather than whole stories. Smaller genres are grouped together and not shown.)"
* Transition: "**Japan** is the clearest case of a country that built its own kind of comics, and then kept them for itself."

## 8. Interactivity

The spec asks for interactivity "where it makes sense", not for its own sake. Each interaction on the page answers a question the text raises.

| Interaction | Charts | The question it answers |
| :- | :- | :- |
| Follow a country | M1, C1, C2, C10, C7, C7b, M4 | "Where does my country (or this one) sit in each of these?" |
| Count per million or in total | M1 | The M1 lead-in says the map changes depending on how you count. |
| Zoom to Europe | M1, M4 | Europe's countries are small and its flow lines overlap. |
| Click an audience in the legend | C4 | The middle layers of a streamgraph are hard to read on their own. |

Rules:

* **Follow a country.** Picking a country in the header dropdown, or clicking one in any of the linked charts, highlights it in every linked chart and fades the others. The followed country keeps its own colour if it is Australia, Japan or the United States, and turns dark grey otherwise. On the choropleth (M1) it is outlined instead, because fading would hide the amounts. The waffle (C7) adds it as a fourth panel. A chart that does not include that country stays as it is.
* **Every chart reads correctly with nothing selected.** Interactions add detail. The takeaway text never depends on the reader clicking anything.
* **Buttons are labelled with what they do** ("Zoom to Europe", "Count per million people"), in Inter at 14px, directly under the chart.
* **No sliders or extra dropdowns** unless a chart asks a question that one answers better than the static chart.
* **No new libraries.** Everything uses Vega-Lite params and Vega's view API in `main.js`.
