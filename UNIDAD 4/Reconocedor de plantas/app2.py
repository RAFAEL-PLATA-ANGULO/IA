import tkinter as tk
from tkinter import filedialog, Label, Button
import numpy as np
import cv2
from PIL import Image, ImageTk
import tensorflow as tf
import keras_cv  # Asegúrate de tenerlo instalado

# Lista de clases
CLASES = [
    'aloevera', 'banana', 'bilimbi', 'cantaloupe', 'cassava', 'coconut',
    'corn', 'cucumber', 'curcuma', 'eggplant', 'galangal', 'ginger',
    'guava', 'kale', 'longbeans', 'mango', 'melon', 'orange', 'paddy',
    'papaya', 'peper chili', 'pineapple', 'pomelo', 'shallot', 'soybeans',
    'spinach', 'sweet potatoes', 'tobacco', 'waterapple', 'watermelon'
]

# Cargar el modelo con soporte para capas personalizadas
modelo = tf.keras.models.load_model(
    "modelos/aprendiendomachin.h5",
    custom_objects={"ImageClassifier": keras_cv.models.ImageClassifier}
)

# Preprocesar imagen
def preparar_imagen(img):
    img = cv2.resize(img, (28, 28))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype('float32') / 255.0
    return np.expand_dims(img, axis=0)

# Hacer predicción y obtener probabilidad
def predecir(img):
    procesada = preparar_imagen(img)
    predicciones = modelo.predict(procesada)[0]
    indice = np.argmax(predicciones)
    clase = CLASES[indice]
    probabilidad = predicciones[indice] * 100
    return clase, probabilidad

# Cargar imagen desde archivo
def cargar_imagen():
    archivo = filedialog.askopenfilename()
    if archivo:
        img = cv2.imread(archivo)
        mostrar_resultado(img)

# Capturar imagen desde la cámara
def capturar_imagen():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        resultado_label.config(text="Error al abrir la cámara.")
        return

    ret, frame = cam.read()
    cam.release()
    if ret:
        mostrar_resultado(frame)

# Mostrar imagen y resultado
def mostrar_resultado(img):
    clase, prob = predecir(img)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize((140, 140))
    img_tk = ImageTk.PhotoImage(img_pil)
    imagen_label.config(image=img_tk)
    imagen_label.image = img_tk
    resultado_label.config(text=f"Predicción: {clase} ({prob:.2f}%)")

# Interfaz
ventana = tk.Tk()
ventana.title("Identificador de Plantas")
ventana.geometry("400x420")

btn_cargar = Button(ventana, text="Cargar Imagen", command=cargar_imagen)
btn_capturar = Button(ventana, text="Capturar desde Cámara", command=capturar_imagen)
resultado_label = Label(ventana, text="Resultado aparecerá aquí", font=("Arial", 12))
imagen_label = Label(ventana)

btn_cargar.pack(pady=10)
btn_capturar.pack(pady=10)
imagen_label.pack(pady=10)
resultado_label.pack(pady=10)

ventana.mainloop()
