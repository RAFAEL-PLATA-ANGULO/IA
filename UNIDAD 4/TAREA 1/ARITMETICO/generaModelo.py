import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import os

# -------------------------------
# 1. Cargar dataset
# -------------------------------
file_path = "dataset_operaciones.csv"

if not os.path.exists(file_path):
    raise FileNotFoundError("No se encontró el archivo 'dataset_operaciones.csv'. Genera primero el dataset.")

df = pd.read_csv(file_path)

# -------------------------------
# 2. Preprocesamiento
# -------------------------------
le = LabelEncoder()
df['op_encoded'] = le.fit_transform(df['op'])

X = df[['a', 'op_encoded', 'b']].values
y = df['result'].values

# Normalizar entradas y salida
X = X / 9.0
y = y / 81.0

# División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -------------------------------
# 3. Definición del modelo
# -------------------------------
model = Sequential([
    Dense(64, activation='relu', input_shape=(3,)),
    Dense(64, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# -------------------------------
# 4. Entrenamiento
# -------------------------------
print("Entrenando el modelo...")
model.fit(X_train, y_train, epochs=1000, batch_size=32, validation_split=0.2)

# -------------------------------
# 5. Guardar el modelo
# -------------------------------
model.save("modelo_aritmetico.h5")
print("Modelo guardado como 'modelo_aritmetico.h5'")
