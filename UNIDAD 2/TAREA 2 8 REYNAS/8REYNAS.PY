import random

def calcular_conflictos(solucion):
    """
    Calcula el número de conflictos en la solución.
    Dos reinas están en conflicto si se encuentran en la misma diagonal.
    """
    conflictos = 0
    n = len(solucion)
    for i in range(n):
        for j in range(i+1, n):
            if abs(solucion[i] - solucion[j]) == abs(i - j):
                conflictos += 1
    return conflictos

def generar_vecinos(solucion):
    """
    Genera los vecinos de la solución actual intercambiando dos reinas.
    """
    vecinos = []
    n = len(solucion)
    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = solucion.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(((i, j), vecino))
    return vecinos

def tabu_search(n, max_iter, tenure, solucion_inicial=None):
    """
    Implementacion del algoritmo de búsqueda tabu para el problema de las n reinas.
    """
    # Si no se proporciona una solución inicial válida, se genera una aleatoria.
    if solucion_inicial is None:
        solucion_actual = list(range(n))
        random.shuffle(solucion_actual)
    else:
        solucion_actual = solucion_inicial.copy()

    mejor_solucion = solucion_actual.copy()
    mejor_conflicto = calcular_conflictos(solucion_actual)
    
    # Lista tabu: diccionario que guarda el movimiento y la iteración hasta la cual es prohibido.
    lista_tabu = {}
    
    iteracion = 0
    #Este ciclo repetira la busqueda hasta encontrar el menor numero de conflictos en el rango de iteraciones
    while iteracion < max_iter and mejor_conflicto > 0:
        iteracion += 1
        vecinos = generar_vecinos(solucion_actual)
        mejor_vecino = None
        mejor_vecino_conflictos = float('inf')
        mejor_movimiento = None
        
        for movimiento, vecino in vecinos:
            conflictos = calcular_conflictos(vecino)
            
            # Se verifica si el movimiento está en la lista tabu.
            # Se permite si mejora la mejor solución encontrada (criterio de aspiración).
            if movimiento in lista_tabu and lista_tabu[movimiento] > iteracion and conflictos >= mejor_conflicto:
                continue
            
            # si el numero de conflictos es menor a los conflictos del mejor vecino , actualiza la heuristica del problema para la siguiente iteracion
            if conflictos < mejor_vecino_conflictos:  
                mejor_vecino_conflictos = conflictos
                mejor_vecino = vecino
                mejor_movimiento = movimiento
        
        # Si no se encontró ningún vecino, se interrumpe el ciclo.
        if mejor_vecino is None:
            break
        
        solucion_actual = mejor_vecino
        lista_tabu[mejor_movimiento] = iteracion + tenure
        
        if mejor_vecino_conflictos < mejor_conflicto:
            mejor_conflicto = mejor_vecino_conflictos
            mejor_solucion = mejor_vecino.copy()
        
        # Muestra el progreso en cada iteración y la mejor heuristica encontrada.
        print(f"#Iteración {iteracion}: #Conflictos = {mejor_vecino_conflictos} y  Solución: {solucion_actual}")
        
    return mejor_solucion, mejor_conflicto, iteracion

def obtener_configuracion_usuario(n):
    """
    Solicita al usuario que ingrese una configuración inicial válida para las reinas.
    """
    entrada = input(f"Ingrese la configuración inicial de las reinas como una lista separada por comas (ejemplo: 3,1,7,5,0,2,4,6): ")
    try:
        configuracion = [int(x.strip()) for x in entrada.split(',')]
        # Verificar que se ingresen exactamente n números y que sean una permutación de 0 a n-1.
        if len(configuracion) != n or sorted(configuracion) != list(range(n)):
            print("La configuración ingresada no es válida.")
            return None
        return configuracion
    except ValueError:
        print("Error al convertir la entrada a números enteros.")
        return None

if __name__ == '__main__':
    N = 8             # Número de reinas.
    MAX_ITER = 10000  # Número máximo de iteraciones.
    TENURE = 5        # Duración en la lista tabu.
    
    # Menú para que el usuario elija la configuración inicial.
    print("Seleccione una opción para la configuración inicial:")
    print("1. Generar configuración random")
    print("2. Ingresar una  configuración manual ")
    
    opcion = input("Ingrese 1 o 2: ").strip()
    
    if opcion == "2":
        configuracion = obtener_configuracion_usuario(N)
        if configuracion is None:
            print("Se utilizará una configuración aleatoria por defecto.")
            configuracion = None
    else:
        configuracion = None
    
    # Ejecutar la búsqueda tabu con la configuración inicial elegida.
    solucion, conflictos, iteraciones = tabu_search(N, MAX_ITER, TENURE, solucion_inicial=configuracion)
    
    print("\nResultado final:")
    print("Solución final:", solucion)
    print("cantidad de conflictos:", conflictos)
    print("cantidad de iteraciones:", iteraciones)
