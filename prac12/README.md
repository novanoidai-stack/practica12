# Práctica 12: Despliegue y Visualización Interactiva

Reconocedor de dígitos MNIST (0-9) con API serverless en Vercel + Frontend interactivo.

## 🎯 Objetivos

- ✅ Crear una aplicación web interactiva
- ✅ Desplegar un modelo MNIST en producción (API serverless)
- ✅ Publicar en la nube (Vercel)
- ✅ Gestionar confianza y UX mediante métricas de predicción

## 📋 Requisitos

- Python 3.9+
- scikit-learn, joblib, opencv, numpy
- Cuenta en Vercel (vercel.com)
- GitHub repository

## 🚀 Instalación local

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Entrenar el modelo (si necesitas reentrenar)
```bash
python train_model_sklearn.py
```

### 3. Probar API localmente
```bash
# Instalar Vercel CLI
npm install -g vercel

# Ejecutar localmente
vercel dev
```

Se abrirá en `http://localhost:3000`

## 📁 Estructura para Vercel

```
prac12/
├── api/
│   └── predict.py              # 🚀 API serverless (Python)
├── public/
│   └── index.html              # 🎨 Frontend interactivo
├── modelo_mnist.pkl            # 🤖 Modelo entrenado
├── scaler.pkl                  # Normalizador
├── requirements.txt            # Dependencias
├── vercel.json                 # Configuración Vercel
├── train_model_sklearn.py      # Entrenamiento
└── README.md                   # Este archivo
```

## 🌐 Deploy en Vercel

### Paso 1: Crear repositorio GitHub
```bash
git remote add origin https://github.com/carlos432ew/practica12.git
git branch -M main
git push -u origin main
```

### Paso 2: Deploy en Vercel
**Opción A: CLI**
```bash
npm install -g vercel
vercel
```
Sigue las instrucciones y conecta con GitHub.

**Opción B: Web**
1. Ve a https://vercel.com
2. Click "New Project"
3. Importa tu repo GitHub
4. Vercel detectará `vercel.json` automáticamente
5. Click "Deploy" ✅

### URL Final
Será algo como: `https://practica12.vercel.app`

## 🎮 Características

- 🎨 Canvas interactivo 280x280px
- ⚡ Predicción en tiempo real (<1 segundo)
- 📊 Visualización de confianza
- ⚠️ Umbral de seguridad (80%)
- 📈 Gráficos de probabilidades por dígito
- 📱 Responsive (funciona en móvil)

## 🏗️ Cómo funciona

### Frontend (HTML/JS)
1. Usuario dibuja en canvas
2. Se convierte a Base64
3. Envía POST a `/api/predict`
4. Recibe predicción + probabilidades
5. Muestra resultado interactivamente

### Backend (API Python)
1. Recibe imagen Base64
2. Redimensiona a 8x8 píxeles
3. Normaliza y aplica scaler
4. Ejecuta modelo scikit-learn
5. Retorna dígito + confianza

## 📊 Modelo

- **Tipo**: Red Neuronal (MLP - Multi-Layer Perceptron)
- **Dataset**: Digits dataset de scikit-learn (1,797 imágenes 8x8)
- **Accuracy**: 97.22% en test
- **Layers**: [input(64) → 128 → 64 → output(10)]
- **Regularización**: Dropout 0.5

## ⚙️ Configuración Vercel

El archivo `vercel.json` configura:
- Runtime: Python 3.11
- Build: Instala `requirements.txt`
- Rewrites: Sirve `public/index.html` como inicio
- API: Route `/api/predict` → `api/predict.py`

```json
{
  "buildCommand": "pip install -r requirements.txt",
  "functions": {
    "api/predict.py": {
      "runtime": "python3.11"
    }
  }
}
```

## 🧪 Testing

### Local
```bash
curl -X POST http://localhost:3000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,..."}'
```

### Producción
Usa el formulario interactivo en la web

## 📝 Respuestas a Preguntas

### ¿Por qué guardar el modelo en archivo?

**No tiene sentido entrenar cada visita porque:**
- Entrenamiento = 5-10 minutos (muy lento)
- Predicción desde archivo = <50ms (instantáneo)
- Datos etiquetados = recurso costoso
- Usuario espera respuesta inmediata

**Conclusión**: Guardar es **obligatorio** en producción.

### ¿Cómo afectan "datos del mundo real"?

**El modelo funciona mejor/peor según:**
- Tamaño/grosor del trazo
- Posición en el canvas
- Ángulo de escritura
- Claridad del dígito

**Observación**: Si compartes con compañeros, sus letras pueden dar resultados diferentes.

**Solución**: Reentrenar con datos reales de usuarios (data augmentation) para mejorar robustez.

## 🔧 Troubleshooting

| Error | Solución |
|-------|----------|
| Modelo no encontrado | Verifica que `modelo_mnist.pkl` está en root |
| Port 3000 en uso | `vercel dev --port 3001` |
| Build falla | Revisa `requirements.txt` |
| Predicción lenta | Check logs: `vercel logs` |

## 📚 Recursos

- [Vercel Python Runtime](https://vercel.com/docs/functions/python)
- [scikit-learn MLP](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
- [MNIST Dataset](https://en.wikipedia.org/wiki/MNIST_database)

## 👤 Autor

Carlos Ocaña - Práctica 12 PIIA UPV 2026

---

**Última actualización**: 2026-05-05
