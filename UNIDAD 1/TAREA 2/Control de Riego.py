import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Definir las variables del sistema difuso
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
temperatura = ctrl.Antecedent(np.arange(0, 51, 1), 'temperatura')
riego = ctrl.Consequent(np.arange(0, 101, 1), 'riego')

# Definir conjuntos difusos para humedad
humedad['baja'] = fuzz.trimf(humedad.universe, [0, 0, 50])
humedad['media'] = fuzz.trimf(humedad.universe, [20, 50, 80])
humedad['alta'] = fuzz.trimf(humedad.universe, [50, 100, 100])

# Definir conjuntos difusos para temperatura
temperatura['fria'] = fuzz.trimf(temperatura.universe, [0, 0, 20])
temperatura['templada'] = fuzz.trimf(temperatura.universe, [10, 25, 40])
temperatura['calida'] = fuzz.trimf(temperatura.universe, [30, 50, 50])

# Definir conjuntos difusos para riego
riego['bajo'] = fuzz.trimf(riego.universe, [0, 0, 50])
riego['medio'] = fuzz.trimf(riego.universe, [20, 50, 80])
riego['alto'] = fuzz.trimf(riego.universe, [50, 100, 100])

# Definir reglas difusas
regla1 = ctrl.Rule(humedad['baja'] & temperatura['calida'], riego['alto'])
regla2 = ctrl.Rule(humedad['baja'] & temperatura['templada'], riego['medio'])
regla3 = ctrl.Rule(humedad['media'] & temperatura['calida'], riego['medio'])
regla4 = ctrl.Rule(humedad['alta'] | temperatura['fria'], riego['bajo'])

# Crear el sistema de control
sistema_riego_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4])
sistema_riego = ctrl.ControlSystemSimulation(sistema_riego_ctrl)

# Interfaz interactiva
def evaluar_riego():
    try:
        humedad_usuario = float(input("Ingrese la humedad del suelo (0-100): "))
        temperatura_usuario = float(input("Ingrese la temperatura ambiental (0-50°C): "))

        if 0 <= humedad_usuario <= 100 and 0 <= temperatura_usuario <= 50:
            sistema_riego.input['humedad'] = humedad_usuario
            sistema_riego.input['temperatura'] = temperatura_usuario
            sistema_riego.compute()

            print("\n--- Resultado del sistema de riego ---")
            print(f"Humedad ingresada: {humedad_usuario}%")
            print(f"Temperatura ingresada: {temperatura_usuario}°C")
            print(f"Nivel de riego recomendado: {sistema_riego.output['riego']:.2f}%\n")
        else:
            print("Error: Los valores deben estar dentro del rango especificado.")
    except ValueError:
        print("Error: Ingrese un valor numérico válido.")

# Menú principal
while True:
    print("\n--- Sistema Experto de Riego Inteligente ---")
    print("1. Evaluar riego")
    print("2. Salir")
    
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        evaluar_riego()
    elif opcion == "2":
        print("Saliendo del sistema. ¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
