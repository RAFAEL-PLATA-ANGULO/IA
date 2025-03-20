import random
import math

def calcular_conflictos(tablero):
    """
    Calcula el número de conflictos en el tablero, donde un conflicto 
    ocurre si dos reinas se atacan. Esto sucede cuando están en la misma fila, 
    columna o diagonal.
    
    - El parámetro 'tablero' es una lista de enteros que representa la
      posición de las reinas en cada fila. El valor de la lista indica 
      la columna donde se encuentra cada reina.
    """
    n = len(tablero)  # El tamaño del tablero, que es el número de filas/columnas (8 en este caso).
    conflictos = 0  # Contador de conflictos entre reinas.
    
    # Iteramos sobre todos los pares de reinas en el tablero.
    for i in range(n):
        for j in range(i + 1, n):
            # Comprobamos si las reinas se encuentran en la misma columna o si se atacan en una diagonal
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1  # Si se atacan, incrementamos el contador de conflictos.
    
    return conflictos  # Devolvemos el número total de conflictos.

def generar_vecino(tablero):
    """
    Genera un vecino del tablero cambiando la posición de una reina de forma aleatoria.
    
    - El parámetro 'tablero' es la configuración actual del tablero.
    - Devuelve una nueva configuración de tablero con una reina movida.
    """
    vecino = tablero[:]  # Creamos una copia del tablero actual para modificarla sin afectar el original.
    
    fila = random.randint(0, len(tablero) - 1)  # Elegimos aleatoriamente una fila.
    columna = random.randint(0, len(tablero) - 1)  # Elegimos aleatoriamente una columna para esa fila.
    
    vecino[fila] = columna  # Movemos la reina en la fila seleccionada a la nueva columna.
    
    return vecino  # Devolvemos el nuevo tablero vecino.

def recocido_simulado(tablero_inicial, temperatura_inicial=1000, factor_enfriamiento=0.99, iteraciones=10000):
    """
    Algoritmo de Recocido Simulado para resolver el problema de las 8 reinas.
    
    - 'tablero_inicial' es el estado inicial del tablero.
    - 'temperatura_inicial' es la temperatura inicial que determina la probabilidad de aceptar movimientos peores.
    - 'factor_enfriamiento' es el factor por el cual la temperatura se reduce en cada iteración.
    - 'iteraciones' es el número máximo de iteraciones que el algoritmo realizará.
    
    Devuelve el mejor tablero encontrado, la cantidad de conflictos en ese tablero y el número de movimientos realizados.
    """
    tablero_actual = tablero_inicial[:]  # Iniciamos con el tablero proporcionado.
    conflictos_actual = calcular_conflictos(tablero_actual)  # Calculamos los conflictos del tablero actual.
    temperatura = temperatura_inicial  # Establecemos la temperatura inicial.
    movimientos = 0  # Contador de movimientos realizados.
    
    # Realizamos iteraciones hasta que se encuentre una solución o se alcance el límite de iteraciones.
    for _ in range(iteraciones):
        if conflictos_actual == 0:
            break  # Si encontramos una solución sin conflictos, terminamos el algoritmo.
        
        vecino = generar_vecino(tablero_actual)  # Generamos un vecino del tablero actual.
        conflictos_vecino = calcular_conflictos(vecino)  # Calculamos los conflictos del vecino.
        
        # Si el vecino tiene menos conflictos, lo aceptamos como el nuevo estado.
        if conflictos_vecino < conflictos_actual:
            tablero_actual, conflictos_actual = vecino, conflictos_vecino
        else:
            
            # Si delta es positivo : El nuevo estado es peor (más conflictos).
            # Si delta es negativo o cero : El nuevo estado es igual o mejor. 
            delta = conflictos_vecino - conflictos_actual  # La diferencia en conflictos.
            probabilidad = math.exp(-delta / temperatura)  # Calculamos la probabilidad de aceptar el peor estado.
            
            # Si un número aleatorio es menor que la probabilidad, aceptamos el vecino.
            if random.random() < probabilidad:
                tablero_actual, conflictos_actual = vecino, conflictos_vecino
        
        # Reducimos la temperatura en cada iteración, lo que hace que sea menos probable aceptar peores soluciones.
        temperatura *= factor_enfriamiento
        movimientos += 1  # Incrementamos el contador de movimientos.
    
    # Devolvemos el mejor tablero encontrado, los conflictos en ese tablero y el número de movimientos realizados.
    return tablero_actual, conflictos_actual, movimientos

if __name__ == "__main__":
    # Solicitar al usuario que ingrese una configuración inicial de las 8 reinas (valores de 0 a 7).
    print("Ingrese una configuración inicial de las 8 reinas (valores 0-7 separados por espacio):")
    estado_inicial = list(map(int, input().strip().split()))
    
    # Validar que el usuario haya ingresado exactamente 8 valores entre 0 y 7.
    if len(estado_inicial) != 8 or not all(0 <= x < 8 for x in estado_inicial):
        print("Error: Debe ingresar exactamente 8 números entre 0 y 7.")
    else:
        # Ejecutar el algoritmo de recocido simulado con la configuración inicial proporcionada.
        solucion, conflictos, movimientos = recocido_simulado(estado_inicial)
        
        # Imprimir el resultado de la ejecución: la solución encontrada, los conflictos y el número de movimientos.
        print("\nSolución encontrada:", solucion)
        print("Número de conflictos en la solución:", conflictos)
        print("Cantidad de movimientos realizados:", movimientos)
