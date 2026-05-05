"""
Script para entrenar y guardar el modelo MNIST con scikit-learn
Versión compatible con Python 3.14
"""
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
import joblib
import numpy as np

print("Cargando dataset MNIST...")
digits = load_digits()
X, y = digits.data, digits.target

print(f"Dataset: {X.shape[0]} imágenes de 8x8 píxeles")

# Dividir en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Normalizar
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nEntrenando modelo MLP (Red Neuronal)...")
model = MLPClassifier(
    hidden_layer_sizes=(128, 64),
    max_iter=500,
    random_state=42,
    verbose=1,
    learning_rate_init=0.001
)

model.fit(X_train, y_train)

# Evaluar
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"\nAccuracy en train: {train_score:.4f}")
print(f"Accuracy en test: {test_score:.4f}")

# Guardar modelo y scaler
joblib.dump(model, 'modelo_mnist.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\nModelo guardado como 'modelo_mnist.pkl'")
print("Scaler guardado como 'scaler.pkl'")
