import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os
import torch
from torchvision import transforms
from facenet_pytorch import MTCNN, InceptionResnetV1

# Cargar el modelo de detección de rostros y clasificación de género
mtcnn = MTCNN()
model = InceptionResnetV1(pretrained='vggface2').eval()
transform = transforms.Compose([transforms.Resize((160, 160)), transforms.ToTensor()])

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
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img = img.resize((300, 200), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk
        root.after(10, update_frame)

def take_photo():
    if cap:
        ret, frame = cap.read()
        if ret:
            filename = "captured_image.jpg"
            cv2.imwrite(filename, frame)
            print(f"Imagen guardada como {filename}")
            detect_gender(filename)

def detect_gender(image_path):
    img = Image.open(image_path)
    img_cropped = mtcnn(img)
    if img_cropped is not None:
        img_cropped = transform(img_cropped).unsqueeze(0)
        with torch.no_grad():
            embedding = model(img_cropped)
        gender = "Hombre" if embedding.mean().item() > 0 else "Mujer"
        result_label.config(text=f"Género detectado: {gender}")
    else:
        result_label.config(text="No se detectó un rostro")

def close_camera():
    if cap:
        cap.release()

def on_closing():
    close_camera()
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title("Captura de Imagen")
root.geometry("400x500")

# Botón para activar la cámara
start_button = Button(root, text="Activar Cámara", command=start_camera)
start_button.pack(pady=10)

# Botón para capturar imagen
take_photo_button = Button(root, text="Tomar Foto", command=take_photo)
take_photo_button.pack(pady=10)

# Label para mostrar la imagen en tiempo real
image_label = Label(root)
image_label.pack()

# Label para mostrar el resultado de la detección de género
result_label = Label(root, text="Género detectado: ")
result_label.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
