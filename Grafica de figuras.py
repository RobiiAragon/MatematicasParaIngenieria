import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


def cicloide_esferica(t, r=2.0, c=6.0):
	x = r * np.cos(t) * (1 - np.cos(c * t))
	y = r * np.sin(t) * (1 - np.cos(c * t))
	z = r * np.sin(c * t)
	return x, y, z


def anillos_sinusoidales(t, R=3.5, r=1.0, n=8.0, a=1.2):
	x = (R + r * np.cos(n * t)) * np.cos(t)
	y = (R + r * np.cos(n * t)) * np.sin(t)
	z = a * np.sin(n * t)
	return x, y, z


def helice_esferica(t, r=2.5, c=10.0):
	x = r * np.sin(c * t) * np.cos(t)
	y = r * np.sin(c * t) * np.sin(t)
	z = r * np.cos(c * t)
	return x, y, z


def rosa_conica(t, a=0.18, k=7.0, c=0.06):
	x = a * t * np.cos(k * t) * np.cos(t)
	y = a * t * np.cos(k * t) * np.sin(t)
	z = c * t
	return x, y, z


def configurar_ejes(ax, titulo):
	ax.set_title(titulo)
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	ax.set_zlabel("z")
	ax.grid(True, alpha=0.25)


def graficar_todo():
	t_base = np.linspace(0, 2 * np.pi, 3000)
	t_rosa = np.linspace(0, 16 * np.pi, 4000)

	figuras = [
		("Cicloide Esferica", cicloide_esferica(t_base), "#ff6b35"),
		("Anillos Sinusoidales", anillos_sinusoidales(t_base), "#0ea5e9"),
		("Helice Esferica", helice_esferica(t_base), "#16a34a"),
		("Rosa Conica", rosa_conica(t_rosa), "#a855f7"),
	]

	fig = plt.figure(figsize=(11, 8))
	fig.suptitle("Ecuaciones Parametricas Representativas", fontsize=15, y=0.98)
	ax = fig.add_subplot(1, 1, 1, projection="3d")
	plt.subplots_adjust(bottom=0.14, top=0.92)

	estado = {"indice": 0}

	def mostrar_figura(indice):
		titulo, (x, y, z), color = figuras[indice]
		ax.clear()
		ax.plot(x, y, z, color=color, linewidth=1.6)
		configurar_ejes(ax, f"{titulo} ({indice + 1}/{len(figuras)})")
		ax.set_box_aspect([1, 1, 1])

		# Ajusta limites para que cada curva se vea centrada y con margen.
		margen = 0.1
		x_min, x_max = np.min(x), np.max(x)
		y_min, y_max = np.min(y), np.max(y)
		z_min, z_max = np.min(z), np.max(z)
		dx = x_max - x_min
		dy = y_max - y_min
		dz = z_max - z_min
		ax.set_xlim(x_min - dx * margen, x_max + dx * margen)
		ax.set_ylim(y_min - dy * margen, y_max + dy * margen)
		ax.set_zlim(z_min - dz * margen, z_max + dz * margen)
		fig.canvas.draw_idle()

	def siguiente(_evento):
		estado["indice"] = (estado["indice"] + 1) % len(figuras)
		mostrar_figura(estado["indice"])

	def anterior(_evento):
		estado["indice"] = (estado["indice"] - 1) % len(figuras)
		mostrar_figura(estado["indice"])

	ax_anterior = plt.axes([0.28, 0.03, 0.18, 0.06])
	ax_siguiente = plt.axes([0.54, 0.03, 0.18, 0.06])
	boton_anterior = Button(ax_anterior, "<- Anterior")
	boton_siguiente = Button(ax_siguiente, "Siguiente ->")
	boton_anterior.on_clicked(anterior)
	boton_siguiente.on_clicked(siguiente)

	mostrar_figura(estado["indice"])
	plt.show()


if __name__ == "__main__":
	graficar_todo()
