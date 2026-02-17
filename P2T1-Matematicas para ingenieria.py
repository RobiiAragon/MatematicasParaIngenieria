import numpy as np
import matplotlib.pyplot as plt
# ==========================================
#Aragón Lopez Jesus Roberto, Lopez Martinez Diana Carolina
# ==========================================
# Gráfica 1: Razón de Cambio (Vista 2D)
# ==========================================
def grafica_razon_cambio():
    x = np.linspace(0, 5, 100)
    y = x**2 # Función de ejemplo f(x) (representando un corte y=constante)
    
    # Punto de análisis
    x0 = 2
    y0 = x0**2
    
    # Derivada (pendiente) en x0 = 2x = 4
    m = 2 * x0
    tangente = m * (x - x0) + y0

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label='Curva $z = f(x, y_0)$', color='blue')
    plt.plot(x, tangente, '--', color='red', label='Recta Tangente (Razón de cambio)')
    plt.scatter([x0], [y0], color='black', zorder=5)
    
    # Anotaciones
    plt.text(x0 - 0.5, y0 + 2, f'Pendiente = Razón de cambio = {m}', fontsize=10, bbox=dict(facecolor='white', alpha=0.6))
    plt.title('1. Derivada parcial como Razón de Cambio (Corte 2D)')
    plt.xlabel('Variable $x$')
    plt.ylabel('Magnitud $z$')
    plt.legend()
    plt.grid(True)
    plt.show()

# ==========================================
# Gráfica 2: Pendiente en una Superficie 3D
# ==========================================
def grafica_pendiente_3d():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Crear superficie z = x^2 + y^2
    X = np.linspace(-3, 3, 30)
    Y = np.linspace(-3, 3, 30)
    X, Y = np.meshgrid(X, Y)
    Z = X**2 + Y**2

    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none')

    # Punto de análisis (1, 1, 2)
    x0, y0 = 1, 1
    z0 = x0**2 + y0**2

    # Vector que representa la pendiente en la dirección x (derivada parcial respecto a x)
    # dz/dx = 2x -> en x=1 es 2
    t = np.linspace(-1, 1, 10)
    x_tan = x0 + t
    y_tan = np.full_like(t, y0) # y se mantiene constante
    z_tan = z0 + 2 * t          # pendiente es 2

    ax.plot(x_tan, y_tan, z_tan, color='red', linewidth=3, label='Pendiente en dir. $x$ ($\partial f/\partial x$)')
    ax.scatter([x0], [y0], [z0], color='black', s=50)

    ax.set_title('2. Derivada parcial como Pendiente en 3D')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.legend()
    plt.show()

# ==========================================
# Gráfica 3: Recta Tangente a la Curva de Intersección
# ==========================================
def grafica_recta_tangente_curva():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Superficie z = -(x^2 + y^2) + 10 (un paraboloide invertido)
    x = np.linspace(-3, 3, 30)
    y = np.linspace(-3, 3, 30)
    X, Y = np.meshgrid(x, y)
    Z = -(X**2 + Y**2) + 10

    # Dibujar la superficie principal
    ax.plot_surface(X, Y, Z, color='cyan', alpha=0.3)

    # Plano constante y = 1
    Y_plano = np.ones_like(X)
    ax.plot_surface(X, Y_plano, Z, color='gray', alpha=0.4) # Plano de corte

    # Curva de intersección (donde y=1) -> z = -x^2 - 1 + 10 = -x^2 + 9
    x_curva = np.linspace(-3, 3, 50)
    y_curva = np.ones_like(x_curva)
    z_curva = -(x_curva**2) + 9
    ax.plot(x_curva, y_curva, z_curva, color='blue', linewidth=3, label='Curva de intersección $f(x, 1)$')

    # Recta tangente a la curva en x = 1
    x0, y0 = 1, 1
    z0 = 8 # -(1^2) + 9 = 8
    # Derivada dz/dx = -2x -> en x=1 es -2
    t = np.linspace(-1.5, 1.5, 10)
    x_tan = x0 + t
    y_tan = np.ones_like(t)
    z_tan = z0 - 2 * t

    ax.plot(x_tan, y_tan, z_tan, color='red', linewidth=3, label='Recta tangente a la curva')
    ax.scatter([x0], [y0], [z0], color='black', s=60)

    ax.set_title('3. Recta Tangente a la Curva (Intersección con plano $y=b$)')
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.legend()
    plt.show()

# Llamar a las funciones una por una (cierra la ventana de una para ver la siguiente)
if __name__ == '__main__':
    grafica_razon_cambio()
    grafica_pendiente_3d()
    grafica_recta_tangente_curva()