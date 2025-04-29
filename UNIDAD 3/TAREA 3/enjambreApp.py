import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# -------------------- Clase Partícula --------------------
class Particula:
    def __init__(self, id, x_min, x_max, y_min, y_max):
        self.id = id
        self.posicion = (
            random.uniform(x_min, x_max),
            random.uniform(y_min, y_max)
        )
        self.velocidad = round(random.uniform(0.1, 1.0), 2)
        self.memoria = [self.posicion]
        self.coef_cognitivo = round(random.uniform(0.5, 2.0), 2)
        self.coef_social = round(random.uniform(0.5, 2.0), 2)

        # Inicializar mejor posición personal y mejor valor
        self.mejor_posicion = self.posicion
        self.mejor_valor = self.evaluar(self.posicion)

    # Función objetivo: minimizar x^2 + y^2
    def evaluar(self, posicion):
        x, y = posicion
        return x**2 + y**2
    # Actualizar posición y velocidad
    def actualizar(self, mejor_global):
        # Actualizar la velocidad con componentes cognitiva y social
        r1 = random.random()
        r2 = random.random()

        nueva_velocidad_x = (self.velocidad * r1 * self.coef_cognitivo +
                            (mejor_global[0] - self.posicion[0]) * r2 * self.coef_social)
        nueva_velocidad_y = (self.velocidad * r1 * self.coef_cognitivo +
                            (mejor_global[1] - self.posicion[1]) * r2 * self.coef_social)

        # Nueva posición
        nueva_x = self.posicion[0] + nueva_velocidad_x
        nueva_y = self.posicion[1] + nueva_velocidad_y
        self.posicion = (nueva_x, nueva_y)

        # ➡️ Guardar la nueva posición en la memoria
        self.memoria.append(self.posicion)

        # ➡️ Actualizar mejor posición personal
        valor_actual = self.evaluar(self.posicion)
        if valor_actual < self.mejor_valor:
            self.mejor_valor = valor_actual
            self.mejor_posicion = self.posicion

# -------------------- Clase Enjambre --------------------
class Enjambre:
    def __init__(self, cantidad, x_min, x_max, y_min, y_max):
        self.particulas = []

        for i in range(cantidad):
            p = Particula(i + 1, x_min, x_max, y_min, y_max)
            self.particulas.append(p)

    def obtener_dataframe(self):
        data = {
            'ID': [],
            'Posición X': [],
            'Posición Y': [],
            'Velocidad': [],
            'Memoria': [],
            'Coef. Cognitivo': [],
            'Coef. Social': [],
            'Mejor Valor': []
        }

        for p in self.particulas:
            data['ID'].append(p.id)
            data['Posición X'].append(round(p.posicion[0], 2))
            data['Posición Y'].append(round(p.posicion[1], 2))
            data['Velocidad'].append(p.velocidad)
            data['Memoria'].append(len(p.memoria))  # Mostrar cuántas posiciones ha guardado
            data['Coef. Cognitivo'].append(p.coef_cognitivo)
            data['Coef. Social'].append(p.coef_social)
            data['Mejor Valor'].append(round(p.mejor_valor, 4))

        return pd.DataFrame(data)

    def obtener_mejor_global(self):
        mejor_particula = min(self.particulas, key=lambda p: p.mejor_valor)
        return mejor_particula.mejor_posicion

    def mover_particulas(self):
        mejor_global = self.obtener_mejor_global()
        for particula in self.particulas:
            particula.actualizar(mejor_global)

# -------------------- Interfaz gráfica --------------------
class AplicacionEnjambre:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Enjambre de Partículas")
        self.root.geometry("1000x750")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(7, weight=3)

        self.parametros = {}
        for i, label in enumerate(["Cantidad", "X Min", "X Max", "Y Min", "Y Max"]):
            ttk.Label(root, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=2)
            entry = ttk.Entry(root)
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=2)
            self.parametros[label] = entry

        ttk.Button(root, text="Crear Enjambre", command=self.generar_enjambre).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(root, text="Mover Enjambre", command=self.mover_enjambre).grid(row=8, column=0, columnspan=2, pady=10)

        self.tree_frame = ttk.Frame(root)
        self.tree_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.grid(row=7, column=0, columnspan=2, sticky="nsew")
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

    def generar_enjambre(self):
        try:
            cantidad = int(self.parametros["Cantidad"].get())
            x_min = float(self.parametros["X Min"].get())
            x_max = float(self.parametros["X Max"].get())
            y_min = float(self.parametros["Y Min"].get())
            y_max = float(self.parametros["Y Max"].get())

            self.enjambre = Enjambre(cantidad, x_min, x_max, y_min, y_max)
            df = self.enjambre.obtener_dataframe()

            self.mostrar_tabla(df)
            self.mostrar_grafica(self.enjambre)

        except Exception as e:
            print("Error:", e)

    def mover_enjambre(self):
        try:
            if hasattr(self, 'enjambre'):
                self.enjambre.mover_particulas()
                df = self.enjambre.obtener_dataframe()
                self.mostrar_tabla(df)
                self.mostrar_grafica(self.enjambre)
        except Exception as e:
            print("Error en mover enjambre:", e)

    def mostrar_tabla(self, df):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def mostrar_grafica(self, enjambre):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        x_vals = [p.posicion[0] for p in enjambre.particulas]
        y_vals = [p.posicion[1] for p in enjambre.particulas]

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(x_vals, y_vals, c='blue')

        for p in enjambre.particulas:
            ax.text(p.posicion[0], p.posicion[1], str(p.id), fontsize=9)

        ax.set_title("Posición de Partículas")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# -------------------- Ejecutar la aplicación --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionEnjambre(root)
    root.mainloop()
