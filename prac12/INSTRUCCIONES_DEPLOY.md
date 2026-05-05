# Instrucciones para Deploy - Práctica 12

## 🚀 Opción 1: Deploy en Streamlit Cloud (Recomendado)

### Paso 1: Subir a GitHub
```bash
cd prac12
git remote add origin https://github.com/tu_usuario/practica12.git
git branch -M main
git push -u origin main
```

### Paso 2: Ir a Streamlit Cloud
1. Visita https://share.streamlit.io
2. Haz login con tu cuenta de GitHub
3. Click en "New app"
4. Selecciona:
   - Repository: `tu_usuario/practica12`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy" ✅

**Resultado**: Tu app estará disponible en una URL como:
```
https://practica12-xxxxx.streamlit.app
```

---

## 🌐 Opción 2: Deploy en Vercel (Requiere refactor)

Para Vercel se necesita una API en Node.js/Python ya que Vercel ejecuta serverless functions, no apps de Streamlit directamente.

### Paso 1: Crear estructura para Vercel

```
practica12/
├── api/
│   └── predict.py          # API endpoint
├── public/
│   └── index.html          # Frontend
├── vercel.json
└── requirements.txt
```

### Paso 2: Crear `api/predict.py`

```python
from http.server import BaseHTTPRequestHandler
import pickle
import json
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import cv2

# Cargar modelo
with open('modelo_mnist.pkl', 'rb') as f:
    model = pickle.load(f)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        
        data = json.loads(body)
        img_base64 = data['image']
        
        # Decodificar imagen
        img_bytes = base64.b64decode(img_base64)
        img = Image.open(BytesIO(img_bytes))
        img_array = np.array(img)
        
        # Procesar
        img_8x8 = cv2.resize(img_array, (8, 8))
        img_normalized = (255 - img_8x8) / 255.0
        img_flat = img_normalized.flatten().reshape(1, -1)
        
        # Predecir
        prediction = model.predict(img_flat)[0]
        probability = model.predict_proba(img_flat)[0]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'digit': int(prediction),
            'confidence': float(probability[int(prediction)]),
            'probabilities': probability.tolist()
        }
        
        self.wfile.write(json.dumps(response).encode())
```

### Paso 3: Crear `vercel.json`

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api/*.py": {
      "runtime": "python3.11"
    }
  }
}
```

### Paso 4: Push a GitHub y Deploy en Vercel

```bash
git push origin main
```

Luego en https://vercel.com:
1. Import del proyecto GitHub
2. Deploy automático ✅

---

## 📝 Respuestas a Preguntas Conceptuales

### ¿Por qué guardar el modelo en archivo?

**No tiene sentido entrenar cada vez que alguien entra a la página porque:**
- Entrenamiento = **5-10 minutos** (muy lento para usuarios)
- El modelo ya está optimizado
- Entrenamiento requiere datos etiquetados (costoso)
- La web debe ser **rápida y responsiva** (<1 segundo)

### ¿Cómo afectan "datos del mundo real"?

**El modelo funciona mejor/peor según la entrada porque:**
- Entrenado con caracteres estándar 8x8 del dataset MNIST
- Varía significativamente con diferentes estilos de letra
- Usuarios escriben más inclinado, impreciso o irregular
- **Solución**: Reentrenar con datos de usuarios reales (data augmentation)

---

## ✅ Checklist Final

- [ ] Crear repo en GitHub (público)
- [ ] Subir archivos con `git push`
- [ ] Hacer login en https://share.streamlit.io
- [ ] Conectar GitHub y hacer deploy
- [ ] Probar escribiendo números en la app
- [ ] Compartir URL con un compañero
- [ ] Documentar diferencias en reconocimiento
- [ ] Crear PDF con capturas + conclusiones

