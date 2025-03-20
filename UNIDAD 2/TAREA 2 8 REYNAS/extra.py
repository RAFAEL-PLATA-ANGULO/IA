import tkinter as tk
from tkinter import ttk

def es_valida(tablero, fila, col):
    """
    Verifica si se puede colocar una reina en la posición (fila, col) sin conflictos.
    """
    for i in range(fila):
        if (tablero[i] == col or  # Misma columna
            tablero[i] - i == col - fila or  # Misma diagonal (
            tablero[i] + i == col + fila):  # Misma diagonal )
            return False
    return True

def resolver_8_reinas(fila=0, tablero=[], soluciones=[]):
    """
    Encuentra todas las soluciones del problema de las 8 reinas.
    """
    if fila == 8:
        soluciones.append(tablero[:])  # Se almacena una copia de la solución
        return
    
    for col in range(8):
        if es_valida(tablero, fila, col):
            tablero.append(col)  # Colocar reina
            resolver_8_reinas(fila + 1, tablero, soluciones)
            tablero.pop()  # Retirar reina para probar siguiente opción

def encontrar_todas_las_soluciones():
    soluciones = []
    resolver_8_reinas(tablero=[], soluciones=soluciones)
    return soluciones

def mostrar_soluciones():
    soluciones = encontrar_todas_las_soluciones()
    for i, solucion in enumerate(soluciones, 1):
        tabla.insert("", "end", values=[i] + solucion)

# Crear la ventana principal
root = tk.Tk()
root.title("92 Soluciones del Problema de las 8 Reinas")

# Crear el Treeview para la tabla
tabla = ttk.Treeview(root, columns=("No.", "Fila 1", "Fila 2", "Fila 3", "Fila 4", "Fila 5", "Fila 6", "Fila 7", "Fila 8"), show="headings")

# Configurar encabezados
encabezados = ["No.", "Fila 1", "Fila 2", "Fila 3", "Fila 4", "Fila 5", "Fila 6", "Fila 7", "Fila 8"]
for col in encabezados:
    tabla.heading(col, text=col)
    tabla.column(col, width=80)

tabla.pack(expand=True, fill="both")

# Botón para mostrar las soluciones
boton = tk.Button(root, text="Mostrar Soluciones", command=mostrar_soluciones)
boton.pack()

# Ejecutar la interfaz gráfica
root.mainloop()