# Tarea 19-02-2026: Gráficas de Máximos, Mínimos y Multiplicadores de Lagrange
#Aragon Lopez Jesus Roberto, Lopez Martinez Diana Carolina

import numpy as np
import matplotlib.pyplot as plt

# 1. Gráfica 2D de Máximos, Mínimos y Valores Críticos
x = np.linspace(-2.5, 2.5, 400)
y = x**3 - 3*x

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='f(x) = x³ - 3x', color='royalblue', linewidth=2)

# Puntos críticos
plt.scatter([-1, 1], [2, -2], color='crimson', zorder=5, s=60)
plt.text(-1, 2.4, 'Máximo Local\nf\'(-1) = 0', ha='center', color='darkred', fontweight='bold')
plt.text(1, -2.8, 'Mínimo Local\nf\'(1) = 0', ha='center', color='darkred', fontweight='bold')

# Líneas tangentes (derivada cero)
plt.hlines(y=2, xmin=-1.5, xmax=-0.5, color='green', linestyle='--', label='Tangente Horizontal (f\'(x)=0)')
plt.hlines(y=-2, xmin=0.5, xmax=1.5, color='green', linestyle='--')

plt.title('Valores Críticos, Máximos y Mínimos Locales', fontsize=14)
plt.xlabel('Eje X', fontsize=12)
plt.ylabel('Eje Y ( f(x) )', fontsize=12)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('maximos_minimos_2d.png', dpi=300)
plt.close()

# 2. Gráfica 2D (Curvas de Nivel) para Multiplicadores de Lagrange
x = np.linspace(-1, 3, 400)
y = np.linspace(-1, 3, 400)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2  # Función objetivo f(x,y)

plt.figure(figsize=(8, 6))
# Curvas de nivel
contour = plt.contour(X, Y, Z, levels=[0.2, 0.8, 2, 4, 6.5], cmap='Blues_r', linewidths=2)
plt.clabel(contour, inline=True, fontsize=10, fmt='f(x,y)=%1.1f')

# Restricción: x + y = 2  => y = 2 - x
y_const = 2 - x
plt.plot(x, y_const, color='crimson', label='Restricción: g(x,y) = x + y - 2 = 0', linewidth=2.5)

# Punto óptimo en (1, 1) donde f(x,y) = 2
plt.scatter([1], [1], color='black', zorder=5, s=80, label='Punto Extremo Restringido')

# Vectores gradiente
plt.quiver(1, 1, 2, 2, color='navy', scale=15, label='∇f (Gradiente Función)')
plt.quiver(1, 1, 1, 1, color='darkred', scale=15, width=0.005, label='∇g (Gradiente Restricción)')

plt.text(0.1, 1.1, 'Tangencia:\n∇f = λ∇g', fontsize=11, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

plt.title('Interpretación Geométrica: Multiplicadores de Lagrange', fontsize=14)
plt.xlabel('Eje X', fontsize=12)
plt.ylabel('Eje Y', fontsize=12)
plt.xlim(-0.5, 2.5)
plt.ylim(-0.5, 2.5)
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig('lagrange_curvas_nivel.png', dpi=300)
plt.close()