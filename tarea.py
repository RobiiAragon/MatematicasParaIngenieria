import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1.2, 100)
y1 = x**2
y2 = x

plt.figure(figsize=(6, 4))
plt.plot(x, y1, label='$y = x^2$ (Límite inferior)')
plt.plot(x, y2, label='$y = x$ (Límite superior)')
plt.fill_between(x, y1, y2, where=(x <= 1), color='skyblue', alpha=0.4, label='Región R')
plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
plt.axvline(x=1, color='red', linestyle='--', alpha=0.5)
plt.title('Región Tipo I: $0 \leq x \leq 1$')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()

y = np.linspace(-1.5, 2.5, 100)
x1 = y**2
x2 = y + 2

plt.figure(figsize=(6, 4))
plt.plot(x1, y, label='$x = y^2$ (Izquierda)')
plt.plot(x2, y, label='$x = y + 2$ (Derecha)')
plt.fill_betweenx(y, x1, x2, where=(y >= -1) & (y <= 2), color='salmon', alpha=0.4, label='Región R')
plt.axhline(y=-1, color='green', linestyle='--', alpha=0.5)
plt.axhline(y=2, color='green', linestyle='--', alpha=0.5)
plt.title('Región Tipo II: $-1 \leq y \leq 2$')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()