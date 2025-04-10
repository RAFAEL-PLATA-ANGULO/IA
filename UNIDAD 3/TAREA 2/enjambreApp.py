import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# -------------------- Clase Partícula --------------------
class Particula:
    def __init__(self, id, x_min, x_max, y_min, y_max):
        # Identificador de la partícula
        self.id = id

        # Posición aleatoria inicial dentro de los límites dados
        self.posicion = (
            random.uniform(x_min, x_max),
            random.uniform(y_min, y_max)
        )

        # Velocidad aleatoria positiva
        self.velocidad = round(random.uniform(0.1, 1.0), 2)

        # Memoria: lista de posiciones por donde ha pasado
        self.memoria = [self.posicion]

        # Coeficientes aleatorios
        self.coef_cognitivo = round(random.uniform(0.5, 2.0), 2)
        self.coef_social = round(random.uniform(0.5, 2.0), 2)

# -------------------- Clase Enjambre (colección de partículas) --------------------
class Enjambre:
    def __init__(self, cantidad, x_min, x_max, y_min, y_max):
        self.particulas = []

        # Crear la cantidad de partículas solicitadas
        for i in range(cantidad):
            p = Particula(i + 1, x_min, x_max, y_min, y_max)
            self.particulas.append(p)

    # Generar DataFrame con los datos de las partículas para mostrar en tabla
    def obtener_dataframe(self):
        data = {
            'ID': [],
            'Posición X': [],
            'Posición Y': [],
            'Velocidad': [],
            'Memoria': [],
            'Coef. Cognitivo': [],
            'Coef. Social': []
        }

        # Extraer los datos de cada partícula
        for p in self.particulas:
            data['ID'].append(p.id)
            data['Posición X'].append(round(p.posicion[0], 2))
            data['Posición Y'].append(round(p.posicion[1], 2))
            data['Velocidad'].append(p.velocidad)
            data['Memoria'].append(p.memoria)
            data['Coef. Cognitivo'].append(p.coef_cognitivo)
            data['Coef. Social'].append(p.coef_social)

        return pd.DataFrame(data)

# -------------------- Interfaz gráfica --------------------
class AplicacionEnjambre:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Enjambre de Partículas")
        self.root.geometry("1000x700")

        # Hacer que las filas y columnas puedan redimensionarse
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(6, weight=1)  # Tabla
        self.root.rowconfigure(7, weight=3)  # Gráfica

        # Crear campos de entrada para parámetros
        self.parametros = {}
        for i, label in enumerate(["Cantidad", "X Min", "X Max", "Y Min", "Y Max"]):
            ttk.Label(root, text=label).grid(row=i, column=0, sticky='w', padx=10, pady=2)
            entry = ttk.Entry(root)
            entry.grid(row=i, column=1, sticky='ew', padx=10, pady=2)
            self.parametros[label] = entry

        # Botón para generar el enjambre
        ttk.Button(root, text="Crear Enjambre", command=self.generar_enjambre).grid(row=5, column=0, columnspan=2, pady=10)

        # Frame para contener la tabla con scroll
        self.tree_frame = ttk.Frame(root)
        self.tree_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        # Tabla con datos de las partículas
        self.tree = ttk.Treeview(self.tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scroll vertical para la tabla
        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Frame para contener la gráfica
        self.canvas_frame = ttk.Frame(root)
        self.canvas_frame.grid(row=7, column=0, columnspan=2, sticky="nsew")
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)

    # Función que se ejecuta al hacer clic en "Crear Enjambre"
    def generar_enjambre(self):
        try:
            # Leer parámetros de entrada
            cantidad = int(self.parametros["Cantidad"].get())
            x_min = float(self.parametros["X Min"].get())
            x_max = float(self.parametros["X Max"].get())
            y_min = float(self.parametros["Y Min"].get())
            y_max = float(self.parametros["Y Max"].get())

            # Crear el enjambre y obtener los datos
            enjambre = Enjambre(cantidad, x_min, x_max, y_min, y_max)
            df = enjambre.obtener_dataframe()

            # Mostrar en tabla y gráfica
            self.mostrar_tabla(df)
            self.mostrar_grafica(enjambre)

        except Exception as e:
            print("Error:", e)

    # Mostrar los datos del enjambre en la tabla
    def mostrar_tabla(self, df):
        # Limpiar contenido anterior
        self.tree.delete(*self.tree.get_children())

        # Configurar columnas de la tabla
        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Insertar cada fila
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    # Mostrar una gráfica con la posición de las partículas
    def mostrar_grafica(self, enjambre):
        # Eliminar gráfica anterior si existe
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        # Obtener coordenadas X e Y
        x_vals = [p.posicion[0] for p in enjambre.particulas]
        y_vals = [p.posicion[1] for p in enjambre.particulas]

        # Crear figura y ejes
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(x_vals, y_vals, c='blue')

        # Etiquetar cada partícula con su ID
        for p in enjambre.particulas:
            ax.text(p.posicion[0], p.posicion[1], str(p.id), fontsize=9)

        ax.set_title("Posición de Partículas")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.grid(True)

        # Mostrar la gráfica dentro del canvas de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# -------------------- Ejecutar la aplicación --------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionEnjambre(root)
    root.mainloop()
