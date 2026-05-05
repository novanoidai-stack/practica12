import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
import joblib

# Configuración de la página
st.set_page_config(page_title="IA Digit Recognizer", layout="centered")
st.title("🎨 Reconocedor de Dígitos en Tiempo Real")
st.write("Dibuja un número del 0 al 9 en el recuadro negro y la IA lo reconocerá.")

# 1. Cargar el modelo guardado
@st.cache_resource
def load_model():
    try:
        model = joblib.load('modelo_mnist.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except FileNotFoundError:
        return None, None

model, scaler = load_model()

if model is None or scaler is None:
    st.error("❌ Modelo no encontrado")
    st.info("Por favor, ejecuta primero:\n```bash\npython train_model_sklearn.py\n```")
    st.stop()

# 2. Crear el lienzo (Canvas) para dibujar
st.subheader("Dibuja aquí:")
canvas_result = st_canvas(
    fill_color="white",
    stroke_width=15,
    stroke_color="white",
    background_color="black",
    height=280,
    width=280,
    drawing_mode="freedraw",
    key="canvas",
)

# 3. Procesar el dibujo y predecir
if canvas_result.image_data is not None:
    # Convertir a escala de grises
    img = cv2.cvtColor(canvas_result.image_data.astype('uint8'), cv2.COLOR_RGBA2GRAY)

    # Redimensionar a 8x8 (tamaño del dataset de sklearn)
    img_8x8 = cv2.resize(img, (8, 8))

    # Normalizar (invertir: negro=0, blanco=1)
    img_normalized = 255 - img_8x8
    img_normalized = img_normalized / 255.0

    # Aplanar para el modelo
    img_flat = img_normalized.flatten().reshape(1, -1)

    # Aplicar scaler
    img_scaled = scaler.transform(img_flat)

    # Predicción
    pred_class = model.predict(img_scaled)[0]
    pred_proba = model.predict_proba(img_scaled)[0]
    confianza = np.max(pred_proba)

    # 4. Mostrar resultados con Umbral de Seguridad
    st.subheader(f"📊 Resultado: {pred_class}")

    if confianza < 0.80:
        st.warning(f"⚠️ Confianza baja ({confianza:.2%}). ¿Podrías dibujar más claro?")
    else:
        st.success(f"✅ Confianza alta: {confianza:.2%}")

    # Visualización de probabilidades
    st.subheader("Probabilidades por dígito:")
    st.bar_chart(
        data={str(i): pred_proba[i] for i in range(10)},
        use_container_width=True
    )

    # Tabla con probabilidades
    st.subheader("Detalle de predicciones:")
    import pandas as pd
    df = pd.DataFrame({
        'Dígito': [str(i) for i in range(10)],
        'Probabilidad': [f"{pred_proba[i]:.4f}" for i in range(10)],
        'Porcentaje': [f"{pred_proba[i]*100:.2f}%" for i in range(10)]
    })
    st.table(df)

st.divider()
st.info("💡 **Tip**: Intenta dibujar números claros y centrados para mejores resultados.")
