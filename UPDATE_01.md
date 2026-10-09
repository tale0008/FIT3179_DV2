# Update 01: colour system, writing style and §1 text

This update applies changes agreed after the MVP shell was built from BUILD_BRIEF.md. Make only the changes listed here. Do not add new charts, interactivity or redesigns.

Files supplied with this update:

* `UPDATE_01.md` (this file)
* `STYLE_GUIDE.md`, new, goes in the repo root
Where STYLE_GUIDE.md and BUILD_BRIEF.md disagree, STYLE_GUIDE.md wins.

## 1. Chart specs (already updated, do not overwrite)

The student has already replaced the three files in `/vega/` with the updated versions. Do not overwrite or edit them. Only confirm they render. What changed inside them, for reference:

* **M1:** colour ramp changed from yellow-green-blue to the purple ramp (`purples`, log scale).
* **C1:** the multicolour fill is gone. Australia, Japan and the United States are drawn in their country colours, all other countries in light grey. Their row labels are bold. There is no colour legend, because every ridge is labelled by its row.
* **C2:** keeps the purple ramp. Australia, Japan and the United States are bold on the y axis.

C1 is still a faceted chart with a fixed `"width": 420`, so the existing width fix in `main.js` must keep working. Check it still resizes C1 to its column.

## 2. Colour tokens in `css/style.css`

Update `:root` so the page and the charts use the same colours:

```css
:root {
  --au: #B07A00;       /* Australia, chart marks and bars */
  --au-text: #8A5F00;  /* Australia, coloured words in text (passes contrast) */
  --jp: #C8102E;       /* Japan, marks and text */
  --us: #1F4E9A;       /* United States, marks and text */
  --context: #C9C9C4;  /* other countries, the past, context */
}
```

Keep any other existing tokens (background, ink, muted text). Replace the old `--au: #D99A00`.

Add three classes for coloured country words in text. They are always bold:

```css
.c-au { color: var(--au-text); font-weight: 700; }
.c-jp { color: var(--jp);      font-weight: 700; }
.c-us { color: var(--us);      font-weight: 700; }
```

Rules (from STYLE_GUIDE.md section 5):

* Only the three country names, and matching words in chart titles, are ever coloured in text. Nothing else.
* The country accent bar on each country's section heading uses `--au`, `--jp` and `--us`.
* Purple is reserved for "how much" on maps and heatmaps. Do not use purple anywhere in the page chrome.

## 3. Per-chart text components

Add reusable markup and classes for the five-part chart text pattern in STYLE_GUIDE.md section 3:

* `.lead` lead-in paragraphs, normal body text
* `.reading-guide` italic, muted colour, in brackets, slightly smaller than body
* `.takeaway` normal body text, may contain coloured country words
* `.caveat` italic, muted colour, in brackets, slightly smaller than body
* `.transition` normal body text, sits last, a little extra space above it

Keep paragraphs short (one or two sentences each, as separate `<p>` elements). Text blocks still never run wider than one column.

## 4. Header and section headings

Replace the header and every section heading with these:

| Slot | Text |
| :- | :- |
| Page title | Australia reads comics. Australia doesn't make them. |
| Page subtitle | Who makes the world's comics, and who only reads them, 1930 to 2026 |
| §1 heading | Comics are everywhere. They are not made everywhere. |
| §2 heading | Japan makes its own comics, and keeps them. |
| §3 heading | America reprints itself. |
| §4 heading | Australia's comics are mostly someone else's. |
| §5 heading | Can we grow them at home? |

Keep the § numbers if the current design shows them.

**Header intro** (replaces the old standfirst). Country names use the colour classes:

> A comic can be made in Australia, or made somewhere else and printed here. This page follows both: comics made in **Australia**, comics made in **Japan** and **the United States**, and the reprints that carry them around the world.

**Scope note**, directly under the intro, in muted text:

> Unless a chart says otherwise, these figures count comic issues, not copies sold. They come from the Grand Comics Database, a volunteer catalogue of over two million comic issues from around the world.

**Byline** (unchanged): By Thisum Patabadige · October 2026 · Sources listed at the end of the page

## 5. §1 text

Replace all existing §1 text with the following. Bold country names use the matching colour class. Each line in quotes is its own `<p>`.

**Section intro** (under the §1 heading, left column):

> "Almost every country reads comics. Far fewer make them, and the ones that do have made them at different times, in different amounts, and about different things."

### Row 1: text left, M1 right

* `.lead` "Start with where comics come from. Counted in total, a handful of large countries publish most of the world's comics."
* `.lead` "Counted per person, the map changes. Small countries in northern Europe turn the darkest."
* `.takeaway` "Norway has about 10,600 comic issues for every million people, around six times the rate of **the United States**. **Australia** sits at about 1,300 per million." `<!-- VERIFY: recheck figures after World Bank populations are added -->`
* `.caveat` "(The database is built by volunteers, so this map also measures how thoroughly each country's comics have been catalogued. **Japan**, the largest comics market in the world, shows only about 1,100 per million for that reason. Colours use a log scale, so each step is about ten times the last.)"
* `.transition` "So who makes comics depends on how you count. The next question is when."

### Row 2, left column: C1 with text beneath

* `.lead` "Comic industries did not grow at the same time. Some countries had their boom before television arrived, others are still in theirs."
* `.reading-guide` "(Reading the ridgeline: each strip is one country's new comic series per year. The taller the strip, the closer that year was to the country's busiest. Countries run from the earliest publishers at the top to the latest at the bottom.)"
* `.takeaway` "**Australia**'s strip has two humps: one in the 1950s, when local publishers filled the gap left by banned imports, and another around 1980, when Australian editions of American comics boomed. After the mid-1980s it almost disappears." `<!-- VERIFY against rendered C1: are both humps visible, which is taller -->`
* `.caveat` "(Series with an uncertain start year are left out, so the earliest decades are undercounted.)"
* `.transition` "Countries did not only publish at different times. They published different kinds of comics."

Placement note: the lead-in may sit above the chart and the rest beneath it, whichever reads better in the column. Keep the order lead, reading guide, chart, takeaway, caveat, transition.

### Row 2, right column: C2 with text beneath

* `.lead` "Each country built its comics around different kinds of stories."
* `.reading-guide` "(Each row is one country and each column one genre. Darker purple means a larger share of that country's stories.)"
* `.takeaway` "Superheroes dominate **American** comics. Most other countries built their industries on humour, adventure and stories for children." `<!-- VERIFY against rendered C2 -->`
* `.caveat` "(A story can carry more than one genre, so shares count genre tags rather than whole stories. Smaller genres are grouped together and not shown.)"
* `.transition` "**Japan** is the clearest case of a country that built its own kind of comics, and then kept them for itself."

The C1 and C2 text blocks should line up across the row, so their takeaways start at the same height where possible.

## 6. Other sections

Only the headings change in §2 to §5 (section 4 above). Leave their placeholders and draft text as they are. They will be rewritten in this style when their charts are built.

## 7. Footer heading

Rename the footer to **"About this visualisation"** and order it as: author, date and unit, Generative AI acknowledgement placeholder, data sources (grouped, each linked), then a "Notes on the data" sub-heading holding the existing data note. Keep all existing source entries.

## 8. Checklist

* [ ] The three specs in `/vega/` are left untouched and all three render.
* [ ] C1 shows only Australia, Japan and the US in colour, everything else grey, and still fits its column on resize.
* [ ] M1 and C2 both use the purple ramp.
* [ ] `--au` is `#B07A00`, and coloured words in text use `--au-text`.
* [ ] Only the three country names are coloured anywhere in the text.
* [ ] Header, all five section headings and all §1 text match this update.
* [ ] Every chart in §1 has lead, takeaway, caveat and transition, and C1 and C2 have reading guides.
* [ ] The three `<!-- VERIFY -->` comments are in the HTML next to their sentences.
* [ ] No horizontal scroll at 1366 x 768. No paragraph wider than one column.

When done, tell the student what changed, and list the three VERIFY sentences so they can check them against the rendered charts.
