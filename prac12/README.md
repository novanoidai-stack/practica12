# Práctica 12: Despliegue y Visualización Interactiva

Reconocedor de dígitos MNIST (0-9) con interfaz interactiva usando Streamlit y TensorFlow.

## 🎯 Objetivos

- Crear una aplicación web interactiva con Streamlit
- Desplegar un modelo MNIST en producción
- Publicar en la nube (Streamlit Cloud y Vercel)
- Gestionar confianza y UX mediante métricas de predicción

## 📋 Requisitos

- Python 3.8+
- TensorFlow 2.13+
- Streamlit 1.28+

## 🚀 Instalación y uso

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Entrenar el modelo (primera vez)
```bash
python train_model.py
```
Esto genera `modelo_mnist.keras` (~50MB)

### 3. Ejecutar la aplicación localmente
```bash
streamlit run app.py
```
Se abrirá en `http://localhost:8501`

## 📁 Estructura

```
prac12/
├── app.py                 # Aplicación Streamlit
├── train_model.py         # Script de entrenamiento
├── modelo_mnist.keras     # Modelo entrenado (generado)
├── requirements.txt       # Dependencias
├── README.md             # Este archivo
└── .gitignore            # Ignorar archivos grandes
```

## 🌐 Despliegue

### Streamlit Cloud
1. Push a GitHub (sin el modelo)
2. Ir a https://share.streamlit.io
3. Conectar con GitHub
4. Seleccionar: `repo/prac12/app.py`
5. Deploy automático ✅

### Vercel (API + Frontend)
Para Vercel se necesita refactorizar con Next.js/API routes:
- API en `/api/predict.js` → TensorFlow.js o Python backend
- Frontend en React/Next.js

## 🎮 Características

- Canvas interactivo 280x280px
- Predicción en tiempo real
- Visualización de confianza
- Umbral de seguridad (80%)
- Tabla de probabilidades por dígito

## ⚠️ Notas

- El modelo **no se commitea** (muy pesado)
- Streamlit Cloud lo entrenará la primera vez (tarda ~2min)
- Para producción, considera usar TensorFlow.js

## 📊 Modelo

- **Arquitectura**: CNN (3 capas convolucionales)
- **Dataset**: MNIST (70,000 imágenes 28x28)
- **Accuracy**: ~99%
- **Epochs**: 10
- **Batch size**: 32

## 👤 Autor

Carlos Ocaña - Práctica 12 PIIA UPV

---

**Preguntas clave**:
- ¿Por qué guardar el modelo en archivo? No tiene sentido entrenarlo en cada visita (tiempo/recursos)
- ¿Cómo afectan "datos reales"? El modelo es sensible a estilos de escritura diferentes
