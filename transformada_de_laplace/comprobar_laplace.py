import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import scipy

t = sp.symbols('t', positive=True)
s = sp.symbols('s')
F, limite, condicion = sp.laplace_transform(t * sp.exp(-2*t), t, s)
y1 = sp.simplify(sp.inverse_laplace_transform(4/(s*(s+2)), s, t))
y2 = sp.simplify(sp.inverse_laplace_transform((s+2)/(s**2+2*s+5), s, t))
print('Versiones: SymPy', sp.__version__, '; SciPy', scipy.__version__)
print('L{t exp(-2t)} =', F, '; Re(s) >', limite, '; condición adicional:', condicion)
print('y1(t) =', y1)
print('y2(t) =', y2)
print('Residuo EDO 1:', sp.simplify(sp.diff(y1,t)+2*y1-4))
print('Residuo EDO 2:', sp.simplify(sp.diff(y2,t,2)+2*sp.diff(y2,t)+5*y2))
print('Condiciones iniciales:', y1.subs(t,0), y2.subs(t,0), sp.diff(y2,t).subs(t,0))

tiempos = np.linspace(0, 5, 1001)
sol1 = solve_ivp(lambda t,z: [4-2*z[0]], (0,5), [0],
                 t_eval=tiempos, rtol=1e-10, atol=1e-12)
sol2 = solve_ivp(lambda t,z: [z[1], -2*z[1]-5*z[0]], (0,5), [1,0],
                 t_eval=tiempos, rtol=1e-10, atol=1e-12)
exacta1 = 2*(1-np.exp(-2*tiempos))
exacta2 = np.exp(-tiempos)*(np.cos(2*tiempos)+np.sin(2*tiempos)/2)
assert sol1.success and sol2.success
print('Error máximo absoluto EDO 1:', f'{np.max(np.abs(sol1.y[0]-exacta1)):.3e}')
print('Error máximo absoluto EDO 2:', f'{np.max(np.abs(sol2.y[0]-exacta2)):.3e}')
print('t | y1 exacta | y1 numérica | y2 exacta | y2 numérica')
for valor in [0, 0.5, 1, 2, 3, 5]:
    i = int(valor*200)
    print(f'{valor:.1f} | {exacta1[i]:.9f} | {sol1.y[0,i]:.9f} | '
          f'{exacta2[i]:.9f} | {sol2.y[0,i]:.9f}')
