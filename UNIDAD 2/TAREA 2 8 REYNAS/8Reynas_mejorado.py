import random

# Parámetro de la búsqueda tabú
TENURE = 5  # Número de iteraciones que un movimiento permanecerá en la lista tabú

# Función para calcular el número de conflictos en una solución dada
def calcular_conflictos(solucion):
    """
    Calcula el número de pares de reinas en conflicto (ataques diagonales).
    :param solucion: Lista que representa la posición de las reinas en cada fila.
    :return: Número de conflictos.
    """
    conflictos = 0
    n = len(solucion)
    for i in range(n):
        for j in range(i + 1, n):
            # Si dos reinas están en la misma diagonal, hay conflicto
            if abs(solucion[i] - solucion[j]) == abs(i - j):
                conflictos += 1
    return conflictos

# Función para generar vecinos intercambiando dos reinas
def generar_vecinos(solucion):
    """
    Genera todos los vecinos de una solución intercambiando dos reinas.
    :param solucion: Lista que representa la posición de las reinas en cada fila.
    :return: Lista de tuplas (movimiento, nueva solución).
    """
    vecinos = []
    n = len(solucion)
    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = solucion.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]  # Intercambia dos reinas
            vecinos.append(((i, j), vecino))  # Guarda el movimiento y la nueva solución
    return vecinos

# Función principal de búsqueda tabú
def busqueda_tabu(n, max_iter):
    """
    Implementa la búsqueda tabú para el problema de las N-Reinas.
    :param n: Número de reinas.
    :param max_iter: Número máximo de iteraciones.
    :return: Mejor solución encontrada.
    """
    # Generamos una solución inicial aleatoria
    solucion_actual = list(range(n))  # Se crea una lista con valores del 0 al n-1
    random.shuffle(solucion_actual)  # Mezcla la lista para tener una configuración aleatoria
    
    # Calculamos conflictos en la solución inicial
    mejor_solucion = solucion_actual[:]
    mejor_conflictos = calcular_conflictos(mejor_solucion)
    
    # Lista tabú para registrar movimientos recientes
    lista_tabu = {}
    
    iteracion = 0
    while iteracion < max_iter and mejor_conflictos > 0:
        vecinos = generar_vecinos(solucion_actual)  # Generamos todos los posibles vecinos
        mejor_vecino = None
        mejor_movimiento = None
        mejor_vecino_conflictos = float('inf')  # Inicializamos con un número alto
        
        # Evaluamos cada vecino para seleccionar el mejor
        for movimiento, vecino in vecinos:
            if movimiento in lista_tabu and lista_tabu[movimiento] > iteracion:
                continue  # Se omite si está en la lista tabú
            
            conflictos = calcular_conflictos(vecino)
            if conflictos < mejor_vecino_conflictos:
                mejor_vecino = vecino
                mejor_movimiento = movimiento
                mejor_vecino_conflictos = conflictos
        
        # Si no encontramos un mejor vecino, terminamos
        if mejor_vecino is None:
            break
        
        # Actualizamos la solución actual con el mejor vecino encontrado
        solucion_actual = mejor_vecino[:]
        
        # Si la nueva solución es mejor que la mejor registrada, la guardamos
        if mejor_vecino_conflictos < mejor_conflictos:
            mejor_solucion = mejor_vecino[:]
            mejor_conflictos = mejor_vecino_conflictos
        
        # Agregamos el movimiento a la lista tabú con su tiempo de permanencia
        lista_tabu[mejor_movimiento] = iteracion + TENURE
        
        iteracion += 1  # Avanzamos a la siguiente iteración
    
    return mejor_solucion  # Retornamos la mejor solución encontrada

# Parámetros del problema
n_reinas = 8  # Número de reinas en el tablero (N)
max_iteraciones = 1000  # Número máximo de iteraciones permitidas

# Ejecutamos la búsqueda tabú para encontrar una solución
solucion_final = busqueda_tabu(n_reinas, max_iteraciones)

# Imprimimos la solución final y la cantidad de conflictos
print("Solución encontrada:", solucion_final)
print("Conflictos finales:", calcular_conflictos(solucion_final))
