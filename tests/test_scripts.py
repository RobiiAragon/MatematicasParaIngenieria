"""Smoke tests: every script runs headless, and the curves match the web viewer."""
import importlib.util
import os
import re
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = sorted((ROOT / "scripts").glob("*.py"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_script_compiles_without_warnings(script):
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # invalid escape sequences, etc.
        compile(script.read_text(encoding="utf-8"), str(script), "exec")


@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.name)
def test_script_runs_headless(script, tmp_path):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    # parametric_curves_3d only builds the figure inside its __main__ guard, which runs here too.
    r = subprocess.run([sys.executable, str(script)], cwd=tmp_path, env=env,
                       capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, r.stderr


def test_assignment_saves_both_figures(tmp_path):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    subprocess.run([sys.executable, str(ROOT / "scripts" / "assignment_2026-02-19.py")],
                   cwd=tmp_path, env=env, check=True, timeout=300)
    assert (tmp_path / "maximos_minimos_2d.png").stat().st_size > 0
    assert (tmp_path / "lagrange_curvas_nivel.png").stat().st_size > 0


def test_curves_have_expected_geometry():
    m = load("parametric_curves_3d")
    t = np.linspace(0, 2 * np.pi, 2001)
    # Spherical helix lies on a sphere of radius r.
    x, y, z = m.helice_esferica(t, r=2.5)
    assert np.allclose(np.sqrt(x**2 + y**2 + z**2), 2.5)
    # Sinusoidal rings: distance from the z axis stays within R ± r.
    x, y, _ = m.anillos_sinusoidales(t, R=3.5, r=1.0)
    rho = np.hypot(x, y)
    assert rho.min() >= 2.5 - 1e-9 and rho.max() <= 4.5 + 1e-9
    # Conic rose rises linearly in z.
    _, _, z = m.rosa_conica(t, c=0.06)
    assert np.allclose(z, 0.06 * t)


def test_web_viewer_defaults_match_python():
    """docs/app.js must draw the same curves as scripts/parametric_curves_3d.py."""
    import inspect

    m = load("parametric_curves_3d")
    js = (ROOT / "docs" / "app.js").read_text(encoding="utf-8")
    pairs = {
        "cicloide": m.cicloide_esferica,
        "anillos": m.anillos_sinusoidales,
        "helice": m.helice_esferica,
        "rosa": m.rosa_conica,
    }
    for cid, fn in pairs.items():
        block = re.search(rf'id: "{cid}".*?params: \{{(.*?)\}},\n', js, re.S)
        assert block, cid
        js_defaults = {k: float(v) for k, v in re.findall(r"(\w+): \[([\d.]+),", block.group(1))}
        py_defaults = {k: p.default for k, p in inspect.signature(fn).parameters.items() if k != "t"}
        assert js_defaults == py_defaults, cid


def test_source_link_points_to_existing_file():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    for path in re.findall(r"RobiiAragon/MatematicasParaIngenieria/blob/main/([^\"]+)", html):
        assert (ROOT / path).is_file(), path
