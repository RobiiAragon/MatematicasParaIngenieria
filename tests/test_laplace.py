"""Re-run the Laplace checks and compare the exact (symbolic) results with the recorded output."""
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("sympy")
pytest.importorskip("scipy")

DIR = Path(__file__).resolve().parents[1] / "transformada_de_laplace"
EXACT_PREFIXES = ("L{", "y1(t)", "y2(t)", "Residuo", "Condiciones")


def test_laplace_symbolic_results_match_recorded_output():
    out = subprocess.run([sys.executable, "comprobar_laplace.py"], cwd=DIR, check=True,
                         capture_output=True, text=True, timeout=600).stdout
    expected = (DIR / "resultados_esperados.txt").read_text(encoding="utf-8")
    pick = lambda text: [l for l in text.splitlines() if l.startswith(EXACT_PREFIXES)]
    assert pick(out) == pick(expected)
    for line in out.splitlines():
        if line.startswith("Error máximo absoluto"):
            assert float(line.rsplit(":", 1)[1]) < 1e-8
