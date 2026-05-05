"""
Script para entrenar y guardar el modelo MNIST
Se ejecuta una sola vez para generar modelo_mnist.keras
"""
import tensorflow as tf
from tensorflow import keras
import numpy as np

# Cargar dataset MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalizar los datos
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0

# Añadir dimensión de canal
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# Crear el modelo
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(10, activation='softmax')
])

# Compilar
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar
print("Entrenando modelo...")
model.fit(x_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=1)

# Evaluar
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\nAccuracy en test: {test_acc:.4f}")

# Guardar el modelo
model.save('modelo_mnist.keras')
print("\nModelo guardado como 'modelo_mnist.keras'")
