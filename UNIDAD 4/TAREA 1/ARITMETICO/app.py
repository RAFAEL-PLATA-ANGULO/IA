import numpy as np
import tkinter as tk
from tkinter import messagebox
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import re

# -------------------------------
# 1. Cargar modelo
# -------------------------------
modelo = load_model("modelo_aritmetico.h5")

# -------------------------------
# 2. Configurar codificador
# -------------------------------
operaciones = ['+', '-', '*', '/']
le = LabelEncoder()
le.fit(operaciones)

# -------------------------------
# 3. Función de predicción
# -------------------------------
def predecir_operacion(entrada):
    try:
        match = re.match(r"^\s*(\d)\s*([+\-*/])\s*(\d)\s*$", entrada)
        if not match:
            return "Formato inválido. Usa: 3 + 4"

        a = int(match.group(1))
        op = match.group(2)
        b = int(match.group(3))

        if op == '/' and b == 0:
            return "Error: división por cero"

        op_encoded = le.transform([op])[0]
        entrada_modelo = np.array([[a, op_encoded, b]]) / 9.0
        resultado = modelo.predict(entrada_modelo)[0][0] * 81
        return f"{a} {op} {b} = {resultado:.2f} (estimado por IA)"
    
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------------------
# 4. Crear interfaz gráfica
# -------------------------------
def calcular():
    operacion = entrada.get()
    resultado = predecir_operacion(operacion)
    salida.config(text=resultado)

# Ventana principal
ventana = tk.Tk()
ventana.title("Calculadora IA - Aritmética básica")
ventana.geometry("400x200")
ventana.resizable(False, False)

# Widgets
tk.Label(ventana, text="Ingresa operación (ej. 3 + 4):", font=("Arial", 12)).pack(pady=10)
entrada = tk.Entry(ventana, font=("Arial", 14), justify="center")
entrada.pack(pady=5)

tk.Button(ventana, text="Calcular", command=calcular, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
entrada.bind("<Return>", lambda event: calcular()) # Permitir calcular con Enter

salida = tk.Label(ventana, text="", font=("Arial", 14), fg="blue")
salida.pack()

# Iniciar GUI
ventana.mainloop()
