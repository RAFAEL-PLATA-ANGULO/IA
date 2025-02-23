import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se pudo acceder a la cámara.")
        return
    update_frame()

def update_frame():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = img.resize((300, 200), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
        root.after(10, update_frame)
    
def take_photo():
    if cap:
        ret, frame = cap.read()
        if ret:
            filename = "captured_image.jpg"
            cv2.imwrite(filename, frame)
            print(f"Imagen guardada como {filename}")

def close_camera():
    if cap:
        cap.release()

def on_closing():
    close_camera()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Captura de Imagen")
root.geometry("400x400")

# Botón para activar la cámara
start_button = Button(root, text="Activar Cámara", command=start_camera)
start_button.pack(pady=10)

# Botón para capturar imagen
take_photo_button = Button(root, text="Tomar Foto", command=take_photo)
take_photo_button.pack(pady=10)

# Label para mostrar la imagen en tiempo real
image_label = Label(root)
image_label.pack()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
