const TWO_PI = 2 * Math.PI;

function linspace(start, end, count) {
  const step = (end - start) / (count - 1);
  return Array.from({ length: count }, (_, i) => start + i * step);
}

function cicloideEsferica(t, r = 2.0, c = 6.0) {
  const x = t.map((v) => r * Math.cos(v) * (1 - Math.cos(c * v)));
  const y = t.map((v, i) => r * Math.sin(v) * (1 - Math.cos(c * t[i])));
  const z = t.map((v) => r * Math.sin(c * v));
  return { x, y, z };
}

function anillosSinusoidales(t, R = 3.5, r = 1.0, n = 8.0, a = 1.2) {
  const x = t.map((v) => (R + r * Math.cos(n * v)) * Math.cos(v));
  const y = t.map((v) => (R + r * Math.cos(n * v)) * Math.sin(v));
  const z = t.map((v) => a * Math.sin(n * v));
  return { x, y, z };
}

function heliceEsferica(t, r = 2.5, c = 10.0) {
  const x = t.map((v) => r * Math.sin(c * v) * Math.cos(v));
  const y = t.map((v) => r * Math.sin(c * v) * Math.sin(v));
  const z = t.map((v) => r * Math.cos(c * v));
  return { x, y, z };
}

function rosaConica(t, a = 0.18, k = 7.0, c = 0.06) {
  const x = t.map((v) => a * v * Math.cos(k * v) * Math.cos(v));
  const y = t.map((v) => a * v * Math.cos(k * v) * Math.sin(v));
  const z = t.map((v) => c * v);
  return { x, y, z };
}

const tBase = linspace(0, TWO_PI, 3000);
const tRosa = linspace(0, 16 * Math.PI, 4000);

const curves = [
  {
    name: "Cicloide Esferica",
    equation: "x = r cos(t)(1 - cos(ct)),  y = r sin(t)(1 - cos(ct)),  z = r sin(ct)",
    color: "#ff6b35",
    data: cicloideEsferica(tBase),
  },
  {
    name: "Anillos Sinusoidales",
    equation: "x = (R + r cos(nt)) cos(t),  y = (R + r cos(nt)) sin(t),  z = a sin(nt)",
    color: "#0ea5e9",
    data: anillosSinusoidales(tBase),
  },
  {
    name: "Helice Esferica",
    equation: "x = r sin(ct) cos(t),  y = r sin(ct) sin(t),  z = r cos(ct)",
    color: "#16a34a",
    data: heliceEsferica(tBase),
  },
  {
    name: "Rosa Conica",
    equation: "x = a t cos(kt) cos(t),  y = a t cos(kt) sin(t),  z = c t",
    color: "#a855f7",
    data: rosaConica(tRosa),
  },
];

let currentIndex = 0;

const plotEl = document.getElementById("plot");
const titleEl = document.getElementById("curveTitle");
const eqEl = document.getElementById("curveEquation");
const countEl = document.getElementById("curveCounter");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

function withMargin(values, margin = 0.1) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  return [min - span * margin, max + span * margin];
}

function renderCurve(index) {
  const curve = curves[index];
  const { x, y, z } = curve.data;

  titleEl.textContent = curve.name;
  eqEl.textContent = curve.equation;
  countEl.textContent = `${index + 1} / ${curves.length}`;

  const trace = {
    x,
    y,
    z,
    mode: "lines",
    type: "scatter3d",
    line: {
      width: 5,
      color: curve.color,
    },
    hoverinfo: "skip",
  };

  const layout = {
    margin: { l: 0, r: 0, t: 0, b: 0 },
    scene: {
      xaxis: { title: "x", range: withMargin(x), gridcolor: "rgba(0,0,0,0.1)" },
      yaxis: { title: "y", range: withMargin(y), gridcolor: "rgba(0,0,0,0.1)" },
      zaxis: { title: "z", range: withMargin(z), gridcolor: "rgba(0,0,0,0.1)" },
      aspectmode: "cube",
      camera: {
        eye: { x: 1.4, y: 1.4, z: 1.2 },
      },
    },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    showlegend: false,
  };

  const config = {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ["lasso2d", "select2d"],
  };

  Plotly.react(plotEl, [trace], layout, config);
}

function nextCurve() {
  currentIndex = (currentIndex + 1) % curves.length;
  renderCurve(currentIndex);
}

function prevCurve() {
  currentIndex = (currentIndex - 1 + curves.length) % curves.length;
  renderCurve(currentIndex);
}

prevBtn.addEventListener("click", prevCurve);
nextBtn.addEventListener("click", nextCurve);

window.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") {
    nextCurve();
  }
  if (event.key === "ArrowLeft") {
    prevCurve();
  }
});

window.addEventListener("resize", () => {
  Plotly.Plots.resize(plotEl);
});

renderCurve(currentIndex);
