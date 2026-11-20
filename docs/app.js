const TWO_PI = 2 * Math.PI;

function linspace(start, end, count) {
  const step = (end - start) / (count - 1);
  return Array.from({ length: count }, (_, i) => start + i * step);
}

function cicloideEsferica(t, { r, c }) {
  const x = t.map((v) => r * Math.cos(v) * (1 - Math.cos(c * v)));
  const y = t.map((v) => r * Math.sin(v) * (1 - Math.cos(c * v)));
  const z = t.map((v) => r * Math.sin(c * v));
  return { x, y, z };
}

function anillosSinusoidales(t, { R, r, n, a }) {
  const x = t.map((v) => (R + r * Math.cos(n * v)) * Math.cos(v));
  const y = t.map((v) => (R + r * Math.cos(n * v)) * Math.sin(v));
  const z = t.map((v) => a * Math.sin(n * v));
  return { x, y, z };
}

function heliceEsferica(t, { r, c }) {
  const x = t.map((v) => r * Math.sin(c * v) * Math.cos(v));
  const y = t.map((v) => r * Math.sin(c * v) * Math.sin(v));
  const z = t.map((v) => r * Math.cos(c * v));
  return { x, y, z };
}

function rosaConica(t, { a, k, c }) {
  const x = t.map((v) => a * v * Math.cos(k * v) * Math.cos(v));
  const y = t.map((v) => a * v * Math.cos(k * v) * Math.sin(v));
  const z = t.map((v) => c * v);
  return { x, y, z };
}

const tBase = linspace(0, TWO_PI, 3000);
const tRosa = linspace(0, 16 * Math.PI, 4000);

// Each parameter: [default, min, max, step]. Defaults match scripts/parametric_curves_3d.py.
const curves = [
  {
    id: "cicloide",
    name: "Cicloide Esférica",
    equation: "x = r cos(t)(1 - cos(ct)),  y = r sin(t)(1 - cos(ct)),  z = r sin(ct)",
    color: "#ff6b35",
    t: tBase,
    fn: cicloideEsferica,
    params: { r: [2.0, 0.5, 5, 0.1], c: [6, 1, 20, 1] },
  },
  {
    id: "anillos",
    name: "Anillos Sinusoidales",
    equation: "x = (R + r cos(nt)) cos(t),  y = (R + r cos(nt)) sin(t),  z = a sin(nt)",
    color: "#0ea5e9",
    t: tBase,
    fn: anillosSinusoidales,
    params: { R: [3.5, 1, 6, 0.1], r: [1.0, 0, 3, 0.1], n: [8, 1, 20, 1], a: [1.2, 0, 3, 0.1] },
  },
  {
    id: "helice",
    name: "Hélice Esférica",
    equation: "x = r sin(ct) cos(t),  y = r sin(ct) sin(t),  z = r cos(ct)",
    color: "#16a34a",
    t: tBase,
    fn: heliceEsferica,
    params: { r: [2.5, 0.5, 5, 0.1], c: [10, 1, 30, 1] },
  },
  {
    id: "rosa",
    name: "Rosa Cónica",
    equation: "x = a t cos(kt) cos(t),  y = a t cos(kt) sin(t),  z = c t",
    color: "#a855f7",
    t: tRosa,
    fn: rosaConica,
    params: { a: [0.18, 0.02, 0.5, 0.01], k: [7, 1, 15, 1], c: [0.06, 0, 0.3, 0.01] },
  },
];

const plotEl = document.getElementById("plot");
const titleEl = document.getElementById("curveTitle");
const eqEl = document.getElementById("curveEquation");
const countEl = document.getElementById("curveCounter");
const paramsEl = document.getElementById("params");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const resetBtn = document.getElementById("resetBtn");

const values = curves.map((c) =>
  Object.fromEntries(Object.entries(c.params).map(([k, [def]]) => [k, def]))
);

const indexFromHash = () => Math.max(0, curves.findIndex((c) => `#${c.id}` === location.hash));
let currentIndex = indexFromHash();

function withMargin(arr, margin = 0.1) {
  let min = Infinity;
  let max = -Infinity;
  for (const v of arr) {
    if (v < min) min = v;
    if (v > max) max = v;
  }
  const span = max - min || 1;
  return [min - span * margin, max + span * margin];
}

function drawPlot() {
  const curve = curves[currentIndex];
  const { x, y, z } = curve.fn(curve.t, values[currentIndex]);
  plotEl.setAttribute("aria-label", `Gráfica 3D de la curva ${curve.name}`);

  const trace = {
    x, y, z,
    mode: "lines",
    type: "scatter3d",
    line: { width: 5, color: curve.color },
    hoverinfo: "skip",
  };

  const layout = {
    margin: { l: 0, r: 0, t: 0, b: 0 },
    scene: {
      xaxis: { title: "x", range: withMargin(x), gridcolor: "rgba(0,0,0,0.1)" },
      yaxis: { title: "y", range: withMargin(y), gridcolor: "rgba(0,0,0,0.1)" },
      zaxis: { title: "z", range: withMargin(z), gridcolor: "rgba(0,0,0,0.1)" },
      aspectmode: "cube",
      camera: { eye: { x: 1.4, y: 1.4, z: 1.2 } },
    },
    // Keep the camera where the user left it while dragging sliders.
    uirevision: curve.id,
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    showlegend: false,
  };

  Plotly.react(plotEl, [trace], layout, {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  });
}

function renderParams() {
  const curve = curves[currentIndex];
  paramsEl.replaceChildren();
  for (const [key, [, min, max, step]] of Object.entries(curve.params)) {
    const id = `param-${curve.id}-${key}`;
    const label = document.createElement("label");
    label.className = "param";
    label.htmlFor = id;

    const name = document.createElement("span");
    name.className = "param-name";
    name.textContent = key;

    const input = document.createElement("input");
    Object.assign(input, { type: "range", id, min, max, step, value: values[currentIndex][key] });

    const out = document.createElement("output");
    out.htmlFor = id;
    out.textContent = input.value;

    input.addEventListener("input", () => {
      values[currentIndex][key] = Number(input.value);
      out.textContent = input.value;
      drawPlot();
    });

    label.append(name, input, out);
    paramsEl.append(label);
  }
}

function renderCurve(index) {
  currentIndex = index;
  const curve = curves[index];
  titleEl.textContent = curve.name;
  eqEl.textContent = curve.equation;
  countEl.textContent = `${index + 1} / ${curves.length}`;
  if (location.hash !== `#${curve.id}`) history.replaceState(null, "", `#${curve.id}`);
  renderParams();
  drawPlot();
}

const step = (delta) => renderCurve((currentIndex + delta + curves.length) % curves.length);

prevBtn.addEventListener("click", () => step(-1));
nextBtn.addEventListener("click", () => step(1));
resetBtn.addEventListener("click", () => {
  const curve = curves[currentIndex];
  for (const [k, [def]] of Object.entries(curve.params)) values[currentIndex][k] = def;
  renderParams();
  drawPlot();
});

window.addEventListener("keydown", (event) => {
  // Don't hijack arrows while a slider or other control has focus.
  if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest("input, select, textarea")) return;
  if (event.key === "ArrowRight") step(1);
  if (event.key === "ArrowLeft") step(-1);
});

window.addEventListener("hashchange", () => renderCurve(indexFromHash()));

if (window.Plotly) {
  renderCurve(currentIndex);
} else {
  titleEl.textContent = "No se pudo cargar Plotly";
  eqEl.textContent = "Revisa tu conexión a internet y recarga la página.";
}
