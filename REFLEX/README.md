# Aplicación Reflex + Gemini

Una aplicación simple que demuestra la integración de Reflex (frontend) con Google Gemini API.

## 🚀 Cómo ejecutar la aplicación

### 1. Dirígete al directorio REFLEX
```bash
cd Reflex
```

### 2. Crea un entorno virtual
```bash
python -m venv venv
```

### 3. Activa el entorno virtual
```bash
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 4. Instala los requerimientos
```bash
pip install -r requirements.txt
```

### 5. Crea un archivo .env
Crea un archivo `.env` en el directorio REFLEX con el siguiente contenido:

```env
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
```

**Nota:** Necesitas obtener una API key de Google Gemini desde [Google AI Studio](https://makersuite.google.com/app/apikey).

### 6. Ejecuta la aplicación
```bash
reflex run
```

La aplicación estará disponible en: `http://localhost:3000`

## 📝 Descripción

Esta aplicación permite:
- Hacer preguntas a Gemini AI
- Interfaz web simple con Reflex
- Integración con Google ADK

## 🔧 Requisitos

- Python 3.8+
- API Key de Google Gemini
- Entorno virtual activado