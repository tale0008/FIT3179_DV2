# Style Guide: text and colour

This guide sets the writing and colour rules for the FIT3179 DV2 page. It is based on the style of the author's DV1 dashboard ("Housing Tenure Over The Ages"). It overrides any draft text or colour choice in BUILD_BRIEF.md where the two disagree.

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

## 3. The per-chart text pattern

Every chart follows the same five-part pattern. Parts marked optional can be dropped when they add nothing.

1. **Lead-in** (1 to 3 short paragraphs, about 30 to 60 words). Sets up the question the chart answers, or explains why it matters. Often continues from the previous chart's transition.
2. **Reading guide** (optional, required for unusual idioms, about 20 to 40 words). Starts with "Reading the ... :" in brackets, or sits as short side notes next to the chart. Required for: ridgeline, horizon chart, waffle, flow map, radial arc, streamgraph, small multiples. Not needed for bars, lines or a plain choropleth.
3. **The chart**, with its title and subtitle.
4. **Takeaway** (1 or 2 short paragraphs, about 20 to 40 words). States the single finding with one or two specific numbers. Never just describes the chart.
5. **Caveat** (optional, italic, in brackets, about 15 to 40 words). Data limits, definitions, exclusions. Example: "(The database is built by volunteers, so it records how thoroughly each country's comics have been catalogued as well as how many were made.)"
6. **Transition** (one sentence, often a question). Hands over to the next chart or section. Example: "So who makes comics depends on how you count. The next question is when."

Total per chart: about 100 to 150 words. Per section intro: about 40 to 70 words.

Placement: the page reads left to right, row by row. A chart in one column has all of its text directly beside it in the other column, and chart rows alternate sides. A chart spanning both columns has its lead-in and reading guide in a merged text row directly above it, and the rest directly below it. Text with no chart is one merged cell across both columns, never two columns of text. A chart never appears without its lead-in and takeaway.

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
| Purple ramp, light to dark | Vega `purples` scheme | not used for text | "How much" on maps and heatmaps |

Rules:

* **Coloured words are the legend.** Only the names of the three countries (and the matching words in chart titles) are coloured in text, always bold. Nothing else in the text is coloured, so the colour always means the same thing.
* Use the **inline text hex** for coloured words. The chart gold fails text contrast on the cream background, so text uses the darker `#8A5F00`.
* **Grey is context.** Countries outside the story, and "before" values in before-and-after charts, are grey. The country being discussed is coloured.
* **Purple is only for amounts.** A single-hue ramp, light means less, dark means more. Never used for categories.
* A new category that is not a country (for example "foreign reprints" vs "domestic reprints" in the waffle) uses shades of the relevant country's colour plus grey, not a new hue. Add a new hue only when no existing one fits, and say what it means in the chart title.
* No rainbow or multi-hue scales anywhere.

## 6. Example: §1 written in this style

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
* Reading guide: "(Reading the ridgeline: each strip is one country's new series per year. A taller strip means that year was closer to the country's busiest. Countries run from the earliest publishers at the top to the latest at the bottom.)"
* Takeaway [verify]: "**Australia**'s busiest years came early, in the 1950s, and its strip all but disappears after the mid-1980s. **Japan** and **the United States** are still publishing."
* Caveat: "(Series with an uncertain start year are left out, so the earliest decades are undercounted.)"
* Transition: "Countries did not only publish at different times. They published different kinds of comics."

**C2, genre heatmap**

* Lead-in: "Each country built its comics around different stories."
* Reading guide: "(Each row is one country and each column one genre. Darker purple means a larger share of that country's stories.)"
* Takeaway [verify]: "Superheroes dominate **American** comics, but most other countries built their industries on humour, adventure and stories for children."
* Caveat: "(A story can carry more than one genre, so shares count genre tags rather than whole stories. Smaller genres are grouped together and not shown.)"
* Transition: "**Japan** is the clearest case of a country that built its own kind of comics, and then kept them for itself."
