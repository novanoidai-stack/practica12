import json
import base64
import joblib
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import os

# Cargar modelo y scaler
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'modelo_mnist.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    print(f"Error cargando modelo: {e}")
    model = None
    scaler = None

def handler(request):
    """
    Endpoint para predicción MNIST
    Espera: POST con JSON { "image": "base64_encoded_image" }
    Retorna: { "digit": int, "confidence": float, "probabilities": [array] }
    """

    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Only POST allowed'})
        }

    if model is None or scaler is None:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Model not loaded'})
        }

    try:
        # Parsear request
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
        img_base64 = body.get('image')

        if not img_base64:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No image provided'})
            }

        # Decodificar imagen base64
        img_bytes = base64.b64decode(img_base64)
        img = Image.open(BytesIO(img_bytes)).convert('RGB')
        img_array = np.array(img)

        # Convertir a escala de grises
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Redimensionar a 8x8
        img_8x8 = cv2.resize(img_gray, (8, 8))

        # Normalizar (invertir: negro=0, blanco=1)
        img_normalized = 255 - img_8x8
        img_normalized = img_normalized / 255.0

        # Aplanar
        img_flat = img_normalized.flatten().reshape(1, -1)

        # Aplicar scaler
        img_scaled = scaler.transform(img_flat)

        # Predicción
        pred_digit = int(model.predict(img_scaled)[0])
        pred_proba = model.predict_proba(img_scaled)[0]
        confidence = float(np.max(pred_proba))

        # Respuesta
        response = {
            'digit': pred_digit,
            'confidence': round(confidence, 4),
            'probabilities': [round(float(p), 4) for p in pred_proba]
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(response)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
