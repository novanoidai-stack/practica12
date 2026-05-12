from http.server import BaseHTTPRequestHandler
import json
import base64
import os
from io import BytesIO

import joblib
import numpy as np
import cv2
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo_mnist.pkl')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    model = None
    scaler = None
    _load_error = str(e)
else:
    _load_error = None


def _predict(image_b64: str) -> dict:
    if ',' in image_b64:
        image_b64 = image_b64.split(',', 1)[1]

    img_bytes = base64.b64decode(image_b64)
    img = Image.open(BytesIO(img_bytes)).convert('RGB')
    img_array = np.array(img)

    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    img_8x8 = cv2.resize(img_gray, (8, 8), interpolation=cv2.INTER_AREA)

    img_normalized = (255 - img_8x8) / 255.0
    img_flat = img_normalized.flatten().reshape(1, -1)
    img_scaled = scaler.transform(img_flat)

    pred_digit = int(model.predict(img_scaled)[0])
    pred_proba = model.predict_proba(img_scaled)[0]
    confidence = float(np.max(pred_proba))

    return {
        'digit': pred_digit,
        'confidence': round(confidence, 4),
        'probabilities': [round(float(p), 4) for p in pred_proba],
    }


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self._send_json(200, {
            'status': 'ok',
            'model_loaded': model is not None and scaler is not None,
            'load_error': _load_error,
            'cwd': os.getcwd(),
            'file_dir': os.path.dirname(__file__),
            'dir_contents': os.listdir(os.path.dirname(__file__)),
            'usage': 'POST JSON {"image": "<base64>"} to this endpoint',
        })

    def do_POST(self):
        if model is None or scaler is None:
            self._send_json(500, {'error': f'Model not loaded: {_load_error}'})
            return

        try:
            length = int(self.headers.get('Content-Length', '0'))
            raw = self.rfile.read(length).decode('utf-8') if length > 0 else ''
            data = json.loads(raw) if raw else {}
        except Exception as e:
            self._send_json(400, {'error': f'Invalid JSON: {e}'})
            return

        image_b64 = data.get('image')
        if not image_b64:
            self._send_json(400, {'error': 'No image provided'})
            return

        try:
            result = _predict(image_b64)
        except Exception as e:
            self._send_json(500, {'error': f'Prediction failed: {e}'})
            return

        self._send_json(200, result)
