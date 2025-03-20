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

# Ejecutar el código para obtener todas las soluciones
soluciones = encontrar_todas_las_soluciones()

# Mostrar todas las soluciones
print(f"Se encontraron {len(soluciones)} soluciones válidas.")
for i, solucion in enumerate(soluciones, 1):
    print(f"Solución {i}: {solucion}")
