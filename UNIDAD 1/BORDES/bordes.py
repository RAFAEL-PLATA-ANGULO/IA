import cv2

def detectar_bordes():
    # Iniciar la cámara (0 para la cámara principal)
    cap = cv2.VideoCapture(0)

    while True:
        # Capturar fotograma
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar detector de bordes Canny
        bordes = cv2.Canny(gris, 100, 2000)

        # Mostrar el resultado
        cv2.imshow('Bordes detectados', bordes)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

# Ejecutar la función
detectar_bordes()
