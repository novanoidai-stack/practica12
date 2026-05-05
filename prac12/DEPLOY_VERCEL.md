# 🚀 Guía Paso a Paso: Deploy en Vercel

## Estructura lista para Vercel

✅ API serverless Python: `api/predict.py`  
✅ Frontend HTML/JS: `public/index.html`  
✅ Modelo MNIST: `modelo_mnist.pkl`  
✅ Configuración: `vercel.json`  

---

## 📋 PASO 1: Crear Repositorio GitHub

### Opción A: Desde GitHub.com
1. Ve a https://github.com/new
2. **Repository name**: `practica12`
3. **Owner**: Tu usuario (carlos432ew)
4. **Public**: ✅ Sí
5. **Initialize with README**: No (ya tenemos uno)
6. Click "Create repository"

### Opción B: Desde terminal
```bash
gh repo create practica12 --public --source=. --remote=origin --push
```

---

## 📤 PASO 2: Push a GitHub

```bash
cd C:/Users/carli/OneDrive/Escritorio/practicas_ia/prac12

# Configurar remoto
git remote add origin https://github.com/carlos432ew/practica12.git
git branch -M main
git push -u origin main
```

**Resultado esperado**: ✅ Todos los archivos en GitHub

Verifica en: https://github.com/carlos432ew/practica12

---

## 🚀 PASO 3: Deploy en Vercel

### OPCIÓN A: Desde Vercel.com (Recomendado - GUI)

1. **Login**: Ve a https://vercel.com
2. **Cuenta**: 
   - Crea cuenta si no tienes
   - O login con GitHub

3. **New Project**:
   - Click "Add New..." → "Project"
   - Click "Continue with GitHub"
   - Busca `practica12`
   - Click "Import"

4. **Configuración**:
   - Framework Preset: `Other` (Python)
   - Root Directory: `./` (automático)
   - Build Command: `pip install -r requirements.txt` (automático)
   - Install Command: `pip install -r requirements.txt`
   - Output Directory: (dejar vacío)

5. **Deploy**:
   - Click "Deploy"
   - Espera 1-2 minutos
   - ✅ **¡Listo!**

### OPCIÓN B: Desde Terminal (CLI)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Desde la carpeta del proyecto
cd prac12

# Deploy
vercel

# Sigue las instrucciones interactivas
```

---

## ✅ PASO 4: Probar la Aplicación

### URL de tu app
```
https://practica12.vercel.app
```
(o similar con tu nombre/ID)

### Checklist
- [ ] Puedo acceder a la URL
- [ ] Veo el canvas negro para dibujar
- [ ] Puedo dibujar números con el ratón
- [ ] Botón "Predecir" funciona
- [ ] Aparece el resultado con confianza
- [ ] Se muestran las probabilidades

---

## 🔍 PASO 5: Verificar Logs

Si hay problemas:

```bash
# Ver logs en tiempo real
vercel logs https://practica12.vercel.app --follow

# Ver último deploy
vercel logs [URL] --since 1h
```

O desde Vercel.com:
1. Dashboard → tu proyecto
2. "Deployments" → último
3. "Functions" → ver logs

---

## 🧪 PASO 6: Testing

### Test 1: Canvas
✅ Dibuja un "5" grande en el canvas  
✅ Click "Predecir"  
✅ Debería reconocer como 5

### Test 2: Confianza
✅ Dibuja un número confuso  
✅ Si confianza < 80%, aparece ⚠️ warning

### Test 3: Compatibilidad
✅ Abre en móvil/tablet
✅ Funciona el canvas táctil

---

## ❌ Troubleshooting

### Error: "Model not loaded"
**Causa**: `modelo_mnist.pkl` no está en el repo  
**Solución**:
```bash
git add -f modelo_mnist.pkl scaler.pkl
git commit -m "add: modelos entrenados"
git push
```
Luego redeploy en Vercel.

### Error: "ModuleNotFoundError: joblib"
**Causa**: requirements.txt no instalado  
**Solución**: Verifica `requirements.txt` tiene `joblib>=1.3.0`

### Error 500 en `/api/predict`
**Causa**: Problema en Python  
**Solución**: 
```bash
vercel logs [URL] --follow
# Ver error específico y corregir
```

### Predicción muy lenta
**Causa**: Cold start de Vercel  
**Solución**: Normal primera vez. Vercel cache después.

---

## 📝 Después del Deploy: Respuestas a Preguntas

### Pregunta 1: ¿Por qué guardar modelo en archivo?

**Respuesta:**
- Entrenar MNIST = 5-10 minutos
- Predicción desde archivo = 50-100ms
- En web, usuario espera <1 segundo
- **No tiene sentido** entrenar cada visita
- Guardar en archivo es **obligatorio** en producción

### Pregunta 2: ¿Funciona igual con diferentes letras?

**Experiment:**
1. Dibuja un "7" normal → Probablemente reconozca bien
2. Dibuja un "7" extraño → Posiblemente falle
3. Comparte URL con amigo
4. Pídele que dibuje números
5. Compara resultados

**Observación esperada:**
- Funciona bien con estilos similares al entrenamiento
- Falla con escritura muy diferente
- Esto es **normal** y esperado

**Conclusión:**
- Modelo es sensible a **variabilidad real**
- Para mejorar: reentrenar con datos diversos (data augmentation)
- Este es el problema principal en ML en producción

---

## 📊 Entrega Final (PDF)

Crea un PDF con:

1. **Captura 1**: Canvas con un número dibujado
2. **Captura 2**: Resultado de predicción (confianza alta)
3. **Captura 3**: Resultado de predicción (confianza baja)
4. **Captura 4**: URL de Vercel funcionando
5. **Texto**:
   - ¿Por qué guardar el modelo?
   - ¿Cómo afectan los datos reales?
   - Tus conclusiones

---

## ✨ Resumen

```
Local Development:
  ✅ Modelo entrenado (97.22% accuracy)
  ✅ API Python serverless (api/predict.py)
  ✅ Frontend HTML/JS (public/index.html)
  ✅ Configuración Vercel (vercel.json)

GitHub:
  ✅ Repository creado
  ✅ Push a main

Vercel:
  ✅ Deploy automático
  ✅ Live en https://practica12.vercel.app
  
Resultados:
  ✅ IA funcionando en producción
  ✅ Accesible públicamente
  ✅ Responde en <1 segundo
```

---

## 📚 Recursos

- Documentación Vercel: https://vercel.com/docs
- scikit-learn: https://scikit-learn.org
- Vercel Python: https://vercel.com/docs/functions/python
- Git & GitHub: https://github.com

---

**¡Listo para conquistar el mundo con tu IA! 🚀**
