# API REST iNaturalist Colombia

Una API REST construida con **FastAPI** que consulta observaciones de iNaturalist en tiempo real desde el Humedal La Conejera en Bogotá, Colombia.

## 🚀 Características

- **Endpoint GET** para obtener observaciones aleatorias
- **Consulta en tiempo real** a la API de iNaturalist
- **Documentación automática** Swagger/OpenAPI en `/docs`
- **Manejo de errores** robusto con códigos HTTP apropiados
- **Validación de datos** con Pydantic

## 📋 Instalación

### 1. Navega al directorio del proyecto

```bash
cd MCP/API
```

### 2. Crea un entorno virtual

Con `pip`:
```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate     # En Windows
```

Con `uv`:
```bash
uv venv
source .venv/bin/activate
```

### 3. Instala las dependencias

Con `pip`:
```bash
pip install -r requirements.txt
```

Con `uv`:
```bash
uv sync
```

## 🎯 Uso

### 1. Inicia el servidor

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

### 2. Accede a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Consulta los endpoints

#### Endpoint raíz - Información de la API

```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "nombre": "iNaturalist API",
  "version": "1.0.0",
  "descripcion": "API REST para consultar observaciones de iNaturalist Colombia",
  "endpoints": {
    "info": "/",
    "observaciones_aleatorias": "/observaciones/aleatoria",
    "documentacion": "/docs"
  }
}
```

#### Health Check

```bash
curl http://localhost:8000/health
```

**Respuesta:**
```json
{
  "status": "OK",
  "servicio": "iNaturalist API"
}
```

#### Obtener observación aleatoria

```bash
curl "http://localhost:8000/observaciones/aleatoria"
```

Con parámetros personalizados:
```bash
curl "http://localhost:8000/observaciones/aleatoria?lugar=Humedal%20La%20Conejera&ciudad=Bogotá"
```

**Respuesta exitosa (200):**
```json
{
  "exitoso": true,
  "lugar": "Humedal La Conejera",
  "ciudad": "Bogotá",
  "especie": "Cacicus chrysonotus",
  "nombre_comun": "Mountain Cacique",
  "fecha_observacion": "2025-10-20",
  "usuario": "Angela V."
}
```

**Respuesta con error (404):**
```json
{
  "detail": "No se encontraron observaciones en Humedal La Conejera"
}
```

## 📚 Endpoints Disponibles

| Método | Ruta | Descripción | Parámetros |
|--------|------|-------------|-----------|
| GET | `/` | Información de la API | - |
| GET | `/health` | Verificar que el servidor funciona | - |
| GET | `/observaciones/aleatoria` | Obtener observación aleatoria | `lugar`, `ciudad` |

## 🔍 Parámetros de Consulta

### `/observaciones/aleatoria`

- **lugar** (string, default: "Humedal La Conejera"): Lugar a consultar
- **ciudad** (string, default: "Bogotá"): Ciudad del lugar

## 📊 Estructura de Respuestas

### Observación Exitosa

```json
{
  "exitoso": boolean,
  "lugar": string,
  "ciudad": string,
  "especie": string,
  "nombre_comun": string,
  "fecha_observacion": string,
  "usuario": string
}
```

### Códigos de Error

- **400**: Lugar no configurado
- **404**: No se encontraron observaciones
- **503**: Error de conexión a iNaturalist
- **504**: Tiempo de espera agotado
- **502**: Error general en consulta a iNaturalist
- **500**: Error inesperado del servidor

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno
- **Uvicorn** - Servidor ASGI
- **Requests** - Cliente HTTP
- **Pydantic** - Validación de datos
- **iNaturalist API** - Fuente de datos de biodiversidad

## 📝 Notas

- La API consulta iNaturalist en **tiempo real** sin almacenamiento local
- Solo retorna observaciones de **calidad de investigación** (quality_grade: "research")
- Selecciona una observación al azar de las últimas 20 más recientes
- Soporta solo el Humedal La Conejera (extensible a otros lugares)

## 🚀 Próximas Mejoras

- Agregar más lugares configurables
- Implementar filtros adicionales (especie, rango de fechas, etc.)
- Agregar autenticación
- Implementar rate limiting
- Cachear resultados (opcional)

## 📚 Recursos

- [iNaturalist API Documentation](https://api.inaturalist.org/v1/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
