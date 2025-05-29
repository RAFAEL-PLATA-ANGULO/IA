import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score
import random
import matplotlib.pyplot as plt

# ====== CONFIGURACIÓN GENERAL ======
IMG_SIZE = 28
CLASES = [
    'aloevera', 'banana', 'bilimbi', 'cantaloupe', 'cassava', 'coconut',
    'corn', 'cucumber', 'curcuma', 'eggplant', 'galangal', 'ginger',
    'guava', 'kale', 'longbeans', 'mango', 'melon', 'orange', 'paddy',
    'papaya', 'peper chili', 'pineapple', 'pomelo', 'shallot', 'soybeans',
    'spinach', 'sweet potatoes', 'tobacco', 'waterapple', 'watermelon'
]

model_paths = {
    "Modelo 1": "model_1_savedmodel.h5",
    "Modelo 2": "model_2_savedmodel.h5",
    "Modelo 3": "model_3_savedmodel.h5",
    "Modelo 4": "model_4_savedmodel.h5"
}

def pred_label(vector):
    return CLASES[np.argmax(vector)]

def preprocess_image(img):
    img = img.resize((IMG_SIZE, IMG_SIZE)).convert("RGB")
    img_array = np.array(img) / 255.0
    return img_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)

# ====== INTERFAZ GRÁFICA ======
class PlantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocedor de Plantas")
        self.selected_model = None
        self.image = None
        self.tk_image = None

        # Dropdown para elegir modelo
        self.model_var = tk.StringVar(value="Modelo 1")
        model_menu = ttk.OptionMenu(root, self.model_var, "Modelo 1", *model_paths.keys())
        model_menu.pack(pady=5)

        # Botones
        tk.Button(root, text="Cargar Imagen", command=self.load_image).pack(pady=5)
        tk.Button(root, text="Activar Cámara", command=self.capture_image).pack(pady=5)
        tk.Button(root, text="Predecir", command=self.predict).pack(pady=5)
        tk.Button(root, text="Validar Todos los Modelos", command=self.validate_models).pack(pady=5)

        # Área de imagen
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Resultado
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=5)

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = Image.open(path)
            self.display_image(self.image)

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.result_label.config(text="No se pudo acceder a la cámara.")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.image = Image.fromarray(frame)
            self.display_image(self.image)

    def display_image(self, pil_img):
        resized = pil_img.resize((200, 200))
        self.tk_image = ImageTk.PhotoImage(resized)
        self.image_label.config(image=self.tk_image)

    def predict(self):
        model_name = self.model_var.get()
        model_path = model_paths[model_name]
        model = load_model(model_path)

        if not self.image:
            self.result_label.config(text="Primero selecciona o captura una imagen.")
            return

        input_data = preprocess_image(self.image)
        prediction = model.predict(input_data)
        label = pred_label(prediction[0])
        self.result_label.config(text=f"Predicción: {label}")

    def validate_models(self):
        # Ruta a carpeta de prueba con subcarpetas por clase
        test_folder = "./dataset_prueba"
        X_test, y_test = [], []

        for clase in CLASES:
            folder = os.path.join(test_folder, clase)
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder)[:5]:  # Solo 5 imágenes por clase
                try:
                    img = Image.open(os.path.join(folder, fname))
                    X_test.append(preprocess_image(img)[0])
                    label = np.zeros(len(CLASES))
                    label[CLASES.index(clase)] = 1
                    y_test.append(label)
                except:
                    continue

        X_test = np.array(X_test)
        y_test = np.array(y_test)
        index = random.randint(0, len(y_test) - 1)

        for name, path in model_paths.items():
            model = load_model(path)
            y_pred = model.predict(X_test)
            pred_labels_list = [pred_label(p) for p in y_pred]
            true_labels_list = [pred_label(t) for t in y_test]

            pred_index_label = pred_labels_list[index]
            true_index_label = true_labels_list[index]
            acc = round(accuracy_score(true_labels_list, pred_labels_list), 2)

            print(f"{name}:")
            print(f" - Predicción muestra aleatoria: {pred_index_label}")
            print(f" - Real: {true_index_label}")
            print(f" - ¿Correcto? {pred_index_label == true_index_label}")
            print(f" - Accuracy total: {acc}")
            print("-" * 30)

        # Mostrar imagen aleatoria usada
        img_np = (X_test[index] * 255).astype(np.uint8)
        img_pil = Image.fromarray(img_np)
        img_pil = img_pil.resize((150, 150))
        self.tk_image = ImageTk.PhotoImage(img_pil)
        self.image_label.config(image=self.tk_image)
        self.result_label.config(text=f"Ejemplo: {true_labels_list[index]}")

# ====== EJECUTAR APP ======
if __name__ == "__main__":
    root = tk.Tk()
    app = PlantApp(root)
    root.mainloop()
