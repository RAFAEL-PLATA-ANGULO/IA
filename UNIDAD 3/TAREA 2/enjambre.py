import random
import matplotlib.pyplot as plt
import pandas as pd

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

    def __repr__(self):
        return f"Partícula {self.id}: Pos={self.posicion}, Vel={self.velocidad}"

class Enjambre:
    def __init__(self, cantidad, x_min, x_max, y_min, y_max):
        self.particulas = []
        for i in range(cantidad):
            p = Particula(i + 1, x_min, x_max, y_min, y_max)
            self.particulas.append(p)

    def mostrar_grafica(self):
        x_vals = [p.posicion[0] for p in self.particulas]
        y_vals = [p.posicion[1] for p in self.particulas]
        plt.figure(figsize=(8, 6))
        plt.scatter(x_vals, y_vals, c='blue', label='Posición de partículas')
        for p in self.particulas:
            plt.text(p.posicion[0], p.posicion[1], str(p.id))
        plt.title('Posición inicial de las partículas')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.legend()
        plt.show()

    def mostrar_tabla(self):
        data = {
            'ID': [],
            'Posición X': [],
            'Posición Y': [],
            'Velocidad': [],
            'Memoria': [],
            'Coef. Cognitivo': [],
            'Coef. Social': []
        }
        for p in self.particulas:
            data['ID'].append(p.id)
            data['Posición X'].append(round(p.posicion[0], 2))
            data['Posición Y'].append(round(p.posicion[1], 2))
            data['Velocidad'].append(p.velocidad)
            data['Memoria'].append(p.memoria)
            data['Coef. Cognitivo'].append(p.coef_cognitivo)
            data['Coef. Social'].append(p.coef_social)

        df = pd.DataFrame(data)
        print(df)

# Uso de ejemplo
enjambre = Enjambre(cantidad=4, x_min=0, x_max=20, y_min=0, y_max=20)
enjambre.mostrar_grafica()
enjambre.mostrar_tabla()
