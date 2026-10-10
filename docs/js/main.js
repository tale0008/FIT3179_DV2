/*
 * Chart loader for the FIT3179 DV2 page.
 *
 * Preview through a local web server, not by opening index.html directly.
 * fetch() does not work over file://, so no chart will load that way.
 *   From the repo root:  python -m http.server 8000 --directory docs
 *   Then open:           http://localhost:8000
 */

// Element ID -> Vega-Lite spec. To add a chart: put its spec in vega/, add one
// line here, and delete the placeholder content inside the element with that ID.
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
  m1: { spec: "vega/m1_world_choropleth.json" },
  c1: { spec: "vega/c1_ridgeline.json", facetWidth: true },
  c2: { spec: "vega/c2_genre_heatmap.json" },
  c10: { spec: "vega/c10_publishing_models.json" },
  c7a: { spec: "vega/c7a_gap.json" },
  c7:  { spec: "vega/c7_waffle.json" },
  c7b: { spec: "vega/c7b_reprint_butterfly.json" },
  c8:  { spec: "vega/c8_au_horizon.json" },
  m4:  { spec: "vega/m4_flow_map.json", aspect: 0.46 }
  // add new charts here as they are built
};

// background: null lets the page colour show through instead of Vega's default
// white box. It merges under each spec's own config, so the spec files are unchanged.
const EMBED_OPTIONS = { actions: false, renderer: "svg", config: { background: null } };
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
  copy.width = width;
  if (copy.spec) copy.spec.width = width;
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

  if (views[id]) views[id].finalize();
  const result = await vegaEmbed(el, spec, { ...EMBED_OPTIONS, loader });
  views[id] = result.view;

  if (dataError) {
    result.view.finalize();
    delete views[id];
    throw dataError;
  }
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
      const res = await fetch(cfg.spec);
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
    el.classList.remove("placeholder", "is-loading");
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

init();
