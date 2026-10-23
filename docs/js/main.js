/*
 * Chart loader for the FIT3179 DV2 page.
 *
 * Preview through a local web server, not by opening index.html directly.
 * fetch() does not work over file://, so no chart will load that way.
 *   From the repo root:  python -m http.server 8000 --directory docs
 *   Then open:           http://localhost:8000
 */

// Element ID -> Vega-Lite spec. To add a chart: put its spec in vega/, add one
// line here, and add an element with that ID to index.html.
// facetWidth: faceted specs cannot use "container" width, so the loader sets a
// pixel width from the element before embedding and again on window resize.
// aspect: the loader sets the spec's height to its drawing width times this
// ratio, so a fixed-shape chart (a world map) has no empty band when narrower.
//
// Chart scale: each chart is drawn at 1/CHART_SCALE of its box width and the SVG
// is then scaled up to fill the box, so chart text and marks read larger next to
// the body text. "container" specs get that drawing width in pixels (their
// fit-x autosize keeps the same fit); fixed-width specs are scaled up as far as
// their box allows.
const CHARTS = {
  m1: { spec: "vega/m1_world_choropleth.json", aspect: 0.5 },
  c1: { spec: "vega/c1_ridgeline.json", facetWidth: true },
  c2: { spec: "vega/c2_genre_heatmap.json" },
  c10: { spec: "vega/c10_publishing_models.json" },
  c7a: { spec: "vega/c7a_gap.json" },
  c7:  { spec: "vega/c7_waffle.json" },
  c7b: { spec: "vega/c7b_reprint_butterfly.json" },
  c8:  { spec: "vega/c8_au_horizon.json" },
  m4:  { spec: "vega/m4_flow_map.json", aspect: 0.46 },
  c3:  { spec: "vega/c3_japan_market.json" },
  m2:  { spec: "vega/m2_japan_mangaka.json" },
  c4:  { spec: "vega/c4_manga_streamgraph.json" },
  c5:  { spec: "vega/c5_manga_radial.json" },
  m3:  { spec: "vega/m3_us_creators.json" },
  c6:  { spec: "vega/c6_us_bookscan.json" },
  c11: { spec: "vega/c11_smash_attendance.json" },
  m6:  { spec: "vega/m6_au_trends.json" },
  c9:  { spec: "vega/c9_au_categories.json" }
  // add new charts here as they are built
};

// background: null lets the page colour show through instead of Vega's default
// white box. font sets every chart's text to Inter, the page's small-text font. The axis and legend sizes lift Vega's 10px defaults so small chart
// text stays readable. Both merge under each spec's own config, so any size set
// in a spec still wins.
const EMBED_OPTIONS = {
  actions: false,
  renderer: "svg",
  config: {
    background: null,
    font: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    axis: { labelFontSize: 12, titleFontSize: 12, labelColor: "#3a3833", titleColor: "#3a3833" },
    legend: { labelFontSize: 12, titleFontSize: 12, labelColor: "#3a3833" }
  }
};
const FACET_LABEL_ROOM = 110; // px kept free for a facet chart's row labels
const CHART_SCALE = 1.2;      // how much larger charts are drawn than their natural size
const MIN_DRAW_WIDTH = 360;   // px; on narrow screens the scale shrinks so charts are never drawn narrower
const RESIZE_DEBOUNCE_MS = 200;

const specs = {};       // id -> fetched spec, reused on re-embed
const views = {};       // id -> current vega View, finalized before re-embed
const boxWidths = {};   // id -> box width last embedded at, to skip no-op resizes

function showError(el, id, err) {
  console.error(`Chart "${id}" failed to load:`, err);
  el.classList.remove("is-loading");
  el.innerHTML = "";
  const msg = document.createElement("p");
  msg.className = "chart-error";
  msg.textContent = `This chart could not be loaded (${CHARTS[id].spec}).`;
  el.appendChild(msg);
}

function contentWidth(el) {
  const style = getComputedStyle(el);
  return el.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight);
}

function withWidth(spec, width) {
  const copy = structuredClone(spec);
  // A facet operator spec takes its width on the inner spec only.
  if (copy.spec) copy.spec.width = width;
  else copy.width = width;
  return copy;
}

function chartScale(boxWidth) {
  return Math.max(1, Math.min(CHART_SCALE, boxWidth / MIN_DRAW_WIDTH));
}

// Width Vega drew the SVG at, before any scaling.
function svgWidth(el) {
  const svg = el.querySelector("svg");
  return svg ? parseFloat(svg.getAttribute("width")) : 0;
}

// Scale the rendered SVG up by `scale`, but never past its box.
function scaleSvg(el, scale, boxWidth) {
  const svg = el.querySelector("svg");
  if (svg) svg.style.width = `${Math.min(svgWidth(el) * scale, boxWidth)}px`;
}

// A Vega loader that records data-file failures, which Vega otherwise only logs.
function trackingLoader(onError) {
  const loader = vega.loader();
  const load = loader.load.bind(loader);
  loader.load = (uri, options) =>
    load(uri, options).catch((err) => {
      onError(new Error(`Could not load data "${uri}": ${err.message}`));
      throw err;
    });
  return loader;
}

// Embed `spec` into `el`, replacing any earlier view. Throws if a data file failed.
async function embed(id, el, spec) {
  let dataError = null;
  const loader = trackingLoader((err) => { dataError = dataError || err; });

  // A resize re-embeds the chart, which would reset its buttons. Keep their values.
  const kept = views[id] ? boundParams(views[id], spec) : {};
  if (views[id]) views[id].finalize();
  const result = await vegaEmbed(el, spec, { ...EMBED_OPTIONS, loader });
  views[id] = result.view;
  for (const [name, value] of Object.entries(kept)) result.view.signal(name, value);
  linkFocus(result.view);
  linkZoom(id, el, result.view, spec);
  await result.view.runAsync();

  if (dataError) {
    result.view.finalize();
    delete views[id];
    throw dataError;
  }
}

// Current values of the params a spec binds to buttons (zoom, count).
function boundParams(view, spec) {
  const values = {};
  for (const p of spec.params || []) {
    if (p.bind && !p.select) values[p.name] = view.signal(p.name);
  }
  return values;
}

/*
 * Follow a country. Every chart whose spec declares a "focus" param highlights
 * the country whose code is in that param, and fades the rest. This code keeps
 * that param the same in all of them: the dropdown in the header and a click on
 * a country in any linked chart both call setFocus, which pushes the code into
 * every linked view. An empty string means no country is followed.
 */
let focus = "";

function hasSignal(view, name) {
  try {
    view.signal(name);
    return true;
  } catch (err) {
    return false; // this chart has no such param
  }
}

function hasFocus(view) {
  return hasSignal(view, "focus");
}

function setFocus(code, name) {
  focus = code;
  for (const [id, view] of Object.entries(views)) {
    if (!hasFocus(view)) continue;
    // resize() lets a chart grow when it gains a panel (the waffle adds one for
    // the followed country); the SVG is then fitted to its box again.
    view.signal("focus", focus).resize().runAsync().then(() => {
      const el = document.getElementById(id);
      scaleSvg(el, chartScale(boxWidths[id]), boxWidths[id]);
    });
  }

  // The header picker, the floating one and the waffle's always show the same country.
  for (const id of ["focus-select", "focus-float", "focus-waffle"]) {
    const select = document.getElementById(id);
    if (code && !select.querySelector(`option[value="${code}"]`)) {
      select.add(new Option(name || code, code)); // a country clicked in a chart but not in the list
    }
    select.value = code;
  }
  updateChip();
}

// The floating picker in the corner appears once the header picker scrolls out
// of view, so the reader can switch country without scrolling back up. It also
// stays while a country is followed, so it can be cleared from anywhere.
let headerPickerVisible = true;

function updateChip() {
  document.getElementById("focus-chip").hidden = !focus && headerPickerVisible;
  document.getElementById("focus-clear").hidden = !focus;
}

// Give a newly embedded chart the current focus, and let a click on one of its
// countries change it. Clicking the followed country again stops following it.
function linkFocus(view) {
  if (!hasFocus(view)) return;
  view.signal("focus", focus);
  view.addEventListener("click", (event, item) => {
    const d = item && item.datum;
    const code = d && (d.code || d.target_code);
    if (!code) return;
    setFocus(code === focus ? "" : code, d.name || d.country || d.target);
  });
}

/*
 * Zoom and pan a map (M1, M4). A spec opts in by declaring the params zoomK
 * (zoom on top of the preset), panX and panY (shift of the map in drawing
 * pixels), zoomUnit (the projection scale that fits the whole world across the
 * width), plus zoomBase and zoomCentre, which its "Zoom to" preset sets. Its
 * projection uses scale zoomBase * zoomK * zoomUnit, center zoomCentre and
 * translate [width / 2 + panX, height / 2 + panY]. Dragging pans; pinching, or
 * Ctrl + scroll, zooms about the pointer. Picking a preset starts again from it.
 * Plain scrolling still scrolls the page.
 */
const ZOOM_MIN = 1;        // never smaller than the whole world across the width
const ZOOM_MAX = 16;       // times the world view
const ZOOM_STEP = 1.6;     // per press of a zoom button
const WHEEL_RATE = 0.004;  // doublings of zoom per pixel of Ctrl + scroll
const DRAG_THRESHOLD = 4;  // screen px a pointer moves before a press counts as a drag
// Latitudes the map can be panned within. Mercator runs to infinity at the poles,
// so it stops at Antarctica's coast and above Greenland.
const PAN_LATITUDES = { mercator: [-60, 84] };

const clamp = (v, lo, hi) => (lo > hi ? (lo + hi) / 2 : Math.min(hi, Math.max(lo, v)));
const zoomMaps = new WeakMap();  // view -> { type: projection type, controls: its buttons }
const mapBoundsCache = {};

// The whole map's extent [x0, x1, y0, y1] at projection scale 1, measured from
// the projected centre, found by projecting points along the map's edges.
// zoomCentre is in the projection's rotated frame, so no rotation is needed here.
function mapBounds(type, centre) {
  const key = `${type} ${centre}`;
  if (mapBoundsCache[key]) return mapBoundsCache[key];
  const proj = vega.projection(type)().scale(1).center(centre).translate([0, 0]);
  const [bottom, top] = PAN_LATITUDES[type] || [-90, 90];
  const edge = [];
  for (let lat = bottom; lat <= top; lat += 2) edge.push([-179.9, lat], [179.9, lat]);
  for (let lon = -179.9; lon <= 179.9; lon += 5) edge.push([lon, bottom], [lon, top]);
  const xs = [], ys = [];
  for (const [x, y] of edge.map(proj)) {
    xs.push(x);
    ys.push(y);
  }
  return (mapBoundsCache[key] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)]);
}

// Set zoom and pan, kept inside the map so it cannot be dragged off the edge.
function setView(view, k, panX, panY) {
  const base = view.signal("zoomBase");
  const w = view.width(), h = view.height();
  k = clamp(k, ZOOM_MIN / base, ZOOM_MAX / base);
  const s = base * k * view.signal("zoomUnit"); // projection scale
  const [x0, x1, y0, y1] = mapBounds(zoomMaps.get(view).type, view.signal("zoomCentre")).map((v) => v * s);
  // The map spans translate + [x0, x1] across; keep it covering the plot.
  panX = clamp(panX, w / 2 - x1, -x0 - w / 2);
  panY = clamp(panY, h / 2 - y1, -y0 - h / 2);
  view.signal("zoomK", k).signal("panX", panX).signal("panY", panY).runAsync();
  updateZoomControls(view);
}

// Zoom by `ratio`, keeping the drawing point p (relative to the plot) fixed.
function zoomAt(view, p, ratio) {
  const k0 = view.signal("zoomK");
  const base = view.signal("zoomBase");
  const k = clamp(k0 * ratio, ZOOM_MIN / base, ZOOM_MAX / base);
  const r = k / k0;
  const tx = view.width() / 2 + view.signal("panX");
  const ty = view.height() / 2 + view.signal("panY");
  setView(view, k, p[0] - (p[0] - tx) * r - view.width() / 2, p[1] - (p[1] - ty) * r - view.height() / 2);
}

function zoomAtCentre(view, ratio) {
  zoomAt(view, [view.width() / 2, view.height() / 2], ratio);
}

function resetZoom(view) {
  setView(view, 1, 0, 0);
}

// Drawing pixels per screen pixel, since scaleSvg draws the SVG larger than its size.
function drawPerScreen(el) {
  const svg = el.querySelector("svg");
  return svg ? svgWidth(el) / svg.getBoundingClientRect().width : 1;
}

// A screen point as drawing pixels relative to the plot's top-left corner.
function plotPoint(view, el, clientX, clientY) {
  const rect = el.querySelector("svg").getBoundingClientRect();
  const f = drawPerScreen(el);
  const pad = view.padding();
  const origin = view.origin();
  return [(clientX - rect.left) * f - pad.left - origin[0], (clientY - rect.top) * f - pad.top - origin[1]];
}

// Zoom buttons, added to the row of buttons Vega draws under the chart.
function addZoomControls(view, el) {
  const row = el.querySelector(".vega-bindings");
  if (!row) return;
  const group = document.createElement("div");
  group.className = "zoom-controls";
  const buttons = [
    ["Zoom in", () => zoomAtCentre(view, ZOOM_STEP)],
    ["Zoom out", () => zoomAtCentre(view, 1 / ZOOM_STEP)],
    ["Reset", () => resetZoom(view)]
  ];
  for (const [label, action] of buttons) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", action);
    group.appendChild(button);
  }
  const hint = document.createElement("span");
  hint.className = "zoom-hint";
  hint.textContent = "Drag to move. Pinch or Ctrl + scroll to zoom.";
  group.appendChild(hint);
  row.appendChild(group);
  zoomMaps.get(view).controls = group;
  updateZoomControls(view);
}

// Reset only shows once the map has moved away from its preset.
function updateZoomControls(view) {
  const group = zoomMaps.get(view).controls;
  if (!group) return;
  const moved = view.signal("zoomK") !== 1 || view.signal("panX") !== 0 || view.signal("panY") !== 0;
  group.querySelector("button:last-of-type").hidden = !moved;
}

// Pointer and wheel handling go on the chart's element once, since it outlives
// each re-embedded view; they act on whichever view is current.
function linkZoom(id, el, view, spec) {
  if (!hasSignal(view, "zoomK")) return;
  zoomMaps.set(view, { type: spec.projection.type });
  addZoomControls(view, el);
  if (hasSignal(view, "zoom")) view.addSignalListener("zoom", () => resetZoom(view)); // a preset starts afresh
  if (el.dataset.zoomPan) return;
  el.dataset.zoomPan = "on";

  const pointers = new Map(); // pointerId -> last [clientX, clientY]
  let travel = 0;             // screen px moved in the current gesture
  let dragged = false;        // the gesture was a drag, so its click should not follow a country

  el.addEventListener("wheel", (e) => {
    const view = views[id];
    if (!view || !(e.ctrlKey || e.metaKey) || !e.target.closest("svg")) return;
    e.preventDefault(); // trackpad pinches arrive as Ctrl + wheel; stop the browser zooming the page
    const px = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
    zoomAt(view, plotPoint(view, el, e.clientX, e.clientY), Math.pow(2, -px * WHEEL_RATE));
  }, { passive: false });

  el.addEventListener("pointerdown", (e) => {
    if (!views[id] || !e.target.closest("svg") || (e.pointerType === "mouse" && e.button !== 0)) return;
    if (pointers.size === 0) {
      travel = 0;
      dragged = false;
    }
    pointers.set(e.pointerId, [e.clientX, e.clientY]);
  });

  el.addEventListener("pointermove", (e) => {
    const last = pointers.get(e.pointerId);
    const view = views[id];
    if (!last || !view) return;
    const before = [...pointers.values()];
    pointers.set(e.pointerId, [e.clientX, e.clientY]);
    travel += Math.hypot(e.clientX - last[0], e.clientY - last[1]);
    if (!dragged) {
      if (travel < DRAG_THRESHOLD) return;
      // Capture only once it is a drag: a captured press would send its click to
      // this element instead of the country under it.
      dragged = true;
      el.classList.add("is-dragging");
      for (const pid of pointers.keys()) el.setPointerCapture(pid);
    }
    const f = drawPerScreen(el);
    const after = [...pointers.values()];
    if (after.length === 1) {
      setView(view, view.signal("zoomK"),
        view.signal("panX") + (e.clientX - last[0]) * f,
        view.signal("panY") + (e.clientY - last[1]) * f);
    } else if (after.length === 2) {
      // Pinch: pan with the midpoint of the two fingers, zoom with their spread.
      const mid = (pts) => [(pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2];
      const spread = (pts) => Math.hypot(pts[0][0] - pts[1][0], pts[0][1] - pts[1][1]);
      const [m0, m1] = [mid(before), mid(after)];
      setView(view, view.signal("zoomK"),
        view.signal("panX") + (m1[0] - m0[0]) * f,
        view.signal("panY") + (m1[1] - m0[1]) * f);
      if (spread(before) > 0) zoomAt(view, plotPoint(view, el, m1[0], m1[1]), spread(after) / spread(before));
    }
  });

  const release = (e) => {
    pointers.delete(e.pointerId);
    if (pointers.size === 0) el.classList.remove("is-dragging");
  };
  el.addEventListener("pointerup", release);
  el.addEventListener("pointercancel", release);

  // A drag ends with a click; stop it before it reaches Vega and changes the focus.
  el.addEventListener("click", (e) => {
    if (dragged && pointers.size === 0) {
      e.stopPropagation();
      dragged = false;
    }
  }, true);
}

async function render(id) {
  const cfg = CHARTS[id];
  const el = document.getElementById(id);
  if (!el) {
    console.error(`Chart "${id}": no element with that ID on the page.`);
    return;
  }

  try {
    if (!specs[id]) {
      // no-cache: check with the server each time, so an edited spec is never
      // paired with a stale cached copy after a normal reload.
      const res = await fetch(cfg.spec, { cache: "no-cache" });
      if (!res.ok) throw new Error(`${cfg.spec}: HTTP ${res.status}`);
      specs[id] = await res.json();
    }

    const boxWidth = Math.floor(contentWidth(el));
    if (views[id] && boxWidths[id] === boxWidth) return;
    boxWidths[id] = boxWidth;
    const scale = chartScale(boxWidth);
    const drawWidth = Math.floor(boxWidth / scale);

    let spec = specs[id];
    if (cfg.facetWidth) {
      spec = withWidth(spec, Math.max(120, drawWidth - FACET_LABEL_ROOM));
    } else if (spec.width === "container") {
      spec = withWidth(spec, drawWidth);
    }
    if (cfg.aspect) {
      spec = structuredClone(spec);
      spec.height = Math.round(drawWidth * cfg.aspect);
    }

    await embed(id, el, spec);

    // A title wider than the drawing width sets the chart's width instead, which
    // leaves a facet chart's plot narrower than its title. Redraw with the plot
    // widened to match; scaleSvg then fits the whole chart to its box.
    const drawn = svgWidth(el);
    if (cfg.facetWidth && drawn > drawWidth + 1) {
      await embed(id, el, withWidth(specs[id], Math.max(120, drawn - FACET_LABEL_ROOM)));
    }

    scaleSvg(el, scale, boxWidth);
    el.classList.remove("is-loading");
  } catch (err) {
    showError(el, id, err);
  }
}

function init() {
  for (const id of Object.keys(CHARTS)) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.add("is-loading");
      el.innerHTML = "";
    }
    render(id);
  }

  const headerSelect = document.getElementById("focus-select");
  const floatSelect = document.getElementById("focus-float");
  const waffleSelect = document.getElementById("focus-waffle");
  floatSelect.innerHTML = headerSelect.innerHTML;
  waffleSelect.innerHTML = headerSelect.innerHTML;
  for (const select of [headerSelect, floatSelect, waffleSelect]) {
    select.addEventListener("change", (e) => setFocus(e.target.value));
  }
  document.getElementById("focus-clear").addEventListener("click", () => setFocus(""));
  new IntersectionObserver(([entry]) => {
    headerPickerVisible = entry.isIntersecting;
    updateChip();
  }).observe(headerSelect.closest(".focus-picker"));

  let timer;
  window.addEventListener("resize", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      for (const id of Object.keys(CHARTS)) {
        if (views[id]) render(id);
      }
    }, RESIZE_DEBOUNCE_MS);
  });
}

// Wait for the web fonts before drawing, because Vega measures text once when it
// lays out a chart. Charts drawn before Inter loads would be laid out for the
// fallback font.
document.fonts.ready.then(init);
