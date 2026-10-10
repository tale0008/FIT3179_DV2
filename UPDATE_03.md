# Update 03: layout and chart fixes after review

This update applies the student's review of the page after Update 02. Make only the changes listed here. STYLE_GUIDE.md still applies.

Files supplied with this update:

* `UPDATE_03.md` (this file)
* `vega/c10_publishing_models.json`, `vega/c7a_gap.json`, `vega/c7b_reprint_butterfly.json`, `vega/c8_au_horizon.json`, `vega/m4_flow_map.json` (replace the existing files)

## 1. Fix first: the flow map (M4) shows no flow lines

On the current page, M4 shows only the United States and Australia shapes. The flow lines and the "Australia: 22,645" label are missing. They all come from one layer that joins `data/reprint_flows.csv` to the `lat` and `lon` columns of `data/country_meta.csv`.

1. Open `data/country_meta.csv` and confirm the header is `code,iso_n3,country,population,lat,lon`, and that rows exist for `us`, `au`, `fr`, `br`, `no`, `mx` and `ca` with numbers in `lat` and `lon`.
2. If the columns are missing, add them from the Update 02 copy of `country_meta.csv`. Keep any population values the student has changed.
3. Open `data/reprint_flows.csv` and confirm the header is `origin_code,origin,target_code,target,reprints`, and that it has rows with `origin_code` equal to `us`.
4. Reload and check the browser console for errors on M4.

Report what was wrong.

## 2. Replace the five specs

Overwrite the five files in `/vega/` with the supplied versions. Do not edit them. What changed:

* **C10:** taller (400 px) with larger dots, for full width.
* **C7a:** now has a legend at the top naming the grey bars and the gold squares.
* **C7b:** taller rows and thicker bars. Yugoslavia's label is shortened so it no longer cuts off.
* **C8:** taller (110 px) and simplified from three gold bands to two, so fewer years appear cut off at the top. The subtitle explains how to read the folded band.
* **M4:** larger labels and thicker lines for full width, Antarctica removed, and fewer overlapping labels in Europe.

## 3. Remove leftover placeholder heights

Charts that have replaced a placeholder must not keep the placeholder's fixed or minimum height. Check that the chart wrappers for every real chart (`m1`, `c1`, `c2`, `c10`, `c7a`, `c7`, `c7b`, `c8`, `m4`) have no `min-height` or fixed `height`, so the box shrinks to fit the chart. Placeholders keep their heights.

## 4. Layout changes

### §1 Row 3: C10 becomes full width

Make Row 3 a full-width row:

* Above the chart, in the left column: the existing C10 `.lead` and `.reading-guide`.
* The chart spans both columns.
* Beneath the chart, in the left column: the existing `.takeaway`, `.caveat` and `.transition`.

No text changes. Prose stays one column wide.

### §4 Row 4: M4 becomes full width, M5 moves down

Make M4 a full-width row:

* Above the chart, in the left column: the existing M4 `.lead` and `.reading-guide`.
* The map spans both columns.
* Beneath the map, in the left column: the existing `.takeaway`, `.caveat` and `.transition`.

Then add a new Row 5 with the M5 placeholder in the left column and its caption placeholder in the right column. The old M6 row becomes Row 6, unchanged.

### M4 height follows its width

A world map has a fixed shape, so a fixed height leaves empty space below it when the page is narrower. Add an `aspect` option to the `CHARTS` registry, handled in the same place as the existing C1 width fix:

```js
m4: { spec: "vega/m4_flow_map.json", aspect: 0.46 },
```

For a chart with `aspect`, fetch the spec, set `spec.height` to the container's inner width multiplied by `aspect` (rounded), then embed. Re-run on window resize with the existing debounce. Keep `"width": "container"` in the spec.

## 5. Text change (C8)

Replace the C8 `.reading-guide` with:

> "(Reading the horizon chart: the strip shows new Australian series each year. Light gold fills up to half the busiest year. When a year is busier than that, the extra folds back over the strip in dark gold, so dark gold always marks the busiest years.)"

## 6. Checklist

* [ ] M4 shows flow lines from the United States, with Australia's line in gold and the "Australia: 22,645 US stories" label.
* [ ] The five specs are the supplied versions.
* [ ] No real chart has leftover empty space from a placeholder height.
* [ ] C10 and M4 span both columns, with their text in one column above and below.
* [ ] M5 is in its own row beneath M4. M6 is unchanged.
* [ ] M4 has no large empty band beneath it at 1366 x 768 or at full width.
* [ ] C7a shows its legend. C8 no longer looks cut off except at its single busiest stretch.
* [ ] No horizontal scroll at 1366 x 768.

When done, tell the student what caused the missing flow lines and what changed.
