# Transformada de Laplace

Código Python utilizado para comprobar los ejemplos de la investigación mediante cálculo simbólico con SymPy e integración numérica con SciPy.

## Archivos

- `comprobar_laplace.py`: programa original de las comprobaciones.
- `requirements.txt`: versiones de las dependencias utilizadas.
- `resultados_esperados.txt`: salida registrada durante la ejecución original.

## Ejecución

Desde esta carpeta, usando Python 3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python comprobar_laplace.py
```

Para guardar una nueva salida:

```bash
python comprobar_laplace.py > resultados_nueva_ejecucion.txt
```

## Ejemplos comprobados

1. **Transformada directa:** calcula la transformada de `t·exp(−2t)`, cuyo resultado es `1/(s + 2)²`, con `Re(s) > −2`.
2. **Ecuación de primer orden:** obtiene `y(t) = 2(1 − exp(−2t))` para `y′ + 2y = 4`, con `y(0) = 0`.
3. **Ecuación de segundo orden:** obtiene `y(t) = exp(−t)[cos(2t) + sin(2t)/2]` para `y″ + 2y′ + 5y = 0`, con `y(0) = 1` y `y′(0) = 0`.

El programa sustituye ambas soluciones en sus ecuaciones y verifica que los residuos simbólicos sean cero. También comprueba las condiciones iniciales y compara las soluciones analíticas con `solve_ivp` en 1001 puntos entre `t = 0` y `t = 5`, con tolerancias relativas de `1e-10` y absolutas de `1e-12`.

## Resultados registrados

La ejecución original utilizó Python 3.12.14, NumPy 2.5.3, SymPy 1.14.0 y SciPy 1.18.1. Las diferencias máximas absolutas observadas fueron:

- Primera ecuación: `3.948 × 10⁻¹¹`.
- Segunda ecuación: `1.749 × 10⁻¹¹`.

Son resultados de esa ejecución y de los puntos evaluados; no representan límites garantizados para otros entornos. La salida completa está en `resultados_esperados.txt`.
