import cv2
import numpy as np

# Iniciar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para reducir ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detectar bordes con Canny
    edges = cv2.Canny(gray, 50, 150)

    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Aproximar la forma del contorno
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Obtener el número de lados de la figura
        sides = len(approx)
        x, y, w, h = cv2.boundingRect(approx)

        # Clasificación de la figura según el número de lados
        if sides == 3:
            shape = "Triangulo"
        elif sides == 4:
            aspect_ratio = float(w) / h
            shape = "Cuadrado" if 0.95 <= aspect_ratio <= 1.05 else "Rectangulo"
        elif sides > 6:
            shape = "Circulo"
        else:
            shape = "Otro"

        # Dibujar el contorno y la etiqueta de la figura
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
        cv2.putText(frame, shape, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Mostrar la imagen procesada
    cv2.imshow("Detección de Figuras Geométricas", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
