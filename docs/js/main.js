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
const CHARTS = {
  m1: { spec: "vega/m1_world_choropleth.json" },
  c1: { spec: "vega/c1_ridgeline.json", facetWidth: true },
  c2: { spec: "vega/c2_genre_heatmap.json" }
  // add new charts here as they are built
};

// background: null lets the page colour show through instead of Vega's default
// white box. It merges under each spec's own config, so the spec files are unchanged.
const EMBED_OPTIONS = { actions: false, renderer: "svg", config: { background: null } };
const FACET_LABEL_ROOM = 110; // px kept free for a facet chart's row labels
const RESIZE_DEBOUNCE_MS = 200;

const specs = {};       // id -> fetched spec, reused on re-embed
const views = {};       // id -> current vega View, finalized before re-embed
const facetWidths = {}; // id -> width last embedded, to skip no-op resizes

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

function withFacetWidth(spec, width) {
  const copy = structuredClone(spec);
  copy.width = width;
  if (copy.spec) copy.spec.width = width;
  return copy;
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

    let spec = specs[id];
    if (cfg.facetWidth) {
      const width = Math.max(120, Math.floor(contentWidth(el) - FACET_LABEL_ROOM));
      if (views[id] && facetWidths[id] === width) return;
      facetWidths[id] = width;
      spec = withFacetWidth(spec, width);
    }

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
      for (const [id, cfg] of Object.entries(CHARTS)) {
        if (cfg.facetWidth && views[id]) render(id);
      }
    }, RESIZE_DEBOUNCE_MS);
  });
}

init();
