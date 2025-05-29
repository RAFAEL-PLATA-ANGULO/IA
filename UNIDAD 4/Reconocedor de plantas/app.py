import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cámara o Imagen")
        self.root.geometry("800x600")

        self.panel = tk.Label(root)
        self.panel.pack()

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.btn_camara = tk.Button(btn_frame, text="Activar Cámara", command=self.activar_camara)
        self.btn_camara.grid(row=0, column=0, padx=10)

        self.btn_imagen = tk.Button(btn_frame, text="Cargar Imagen", command=self.cargar_imagen)
        self.btn_imagen.grid(row=0, column=1, padx=10)

        self.cap = None  # Captura de la cámara
        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def activar_camara(self):
        self.cap = cv2.VideoCapture(0)
        self.mostrar_frame()

    def mostrar_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.panel.imgtk = imgtk
                self.panel.config(image=imgtk)
            self.panel.after(10, self.mostrar_frame)

    def cargar_imagen(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imagenes", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((640, 480))
            imgtk = ImageTk.PhotoImage(image=image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            if self.cap:  # Detener la cámara si estaba activa
                self.cap.release()
                self.cap = None

    def salir(self):
        if self.cap:
            self.cap.release()
        self.root.destroy()

# Ejecutar la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
