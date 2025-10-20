# Sistema de Agentes Multi-Especializados para Expediciones

Sistema inteligente de asistencia para expediciones que integra consultas meteorológicas, cálculos logísticos y datos de biodiversidad mediante agentes especializados basados en Google Gemini.

## Características

- **Agentes Especializados**: Sistema multi-agente con personalidades únicas
  - **Meteorólogo**: Consulta clima en tiempo real con estilo teológico medieval
  - **Matemático**: Cálculos logísticos precisos con lenguaje técnico
  - **Biólogo**: Información sobre biodiversidad con estilo apasionado y educativo
  - **Coordinador**: Integra información de todos los agentes para recomendaciones finales

- **API REST de iNaturalist**: Consulta observaciones reales de biodiversidad del Humedal La Conejera en Bogotá
- **Arquitectura Asíncrona**: Procesamiento eficiente con asyncio
- **Integración con APIs Externas**:
  - wttr.in para datos meteorológicos
  - iNaturalist para observaciones de biodiversidad

## Requisitos Previos

- Python 3.8 o superior
- Cuenta de Google Cloud con acceso a Gemini API
- Conexión a internet para consultas en tiempo real

## Instalación

### 1. Clonar el repositorio

```bash
cd DATAR
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GOOGLE_API_KEY="tu_api_key_aqui"
API_INATURALIST_URL="http://localhost:8000"
```

> **Importante**: Obtén tu API key de Google en [Google AI Studio](https://makersuite.google.com/app/apikey)

## Uso

### Paso 1: Iniciar la API de iNaturalist

En una terminal, ejecuta:

```bash
python api_inaturalist.py
```

Esto iniciará el servidor FastAPI en `http://localhost:8000`

Puedes acceder a la documentación interactiva en: `http://localhost:8000/docs`

### Paso 2: Ejecutar el Sistema de Agentes

En otra terminal (manteniendo la primera activa), ejecuta:

```bash
python sistema_agentes.py
```

## Ejemplos de Uso

### Ejemplo 1: Consultar Agentes Individuales

```python
# Consultar clima
clima = await preguntar_a_agente(
    runner_meteorologo,
    "sesion_meteorologo",
    "¿Cómo está el clima en Bogotá?"
)

# Realizar cálculos
peso = await preguntar_a_agente(
    runner_matematico,
    "sesion_matematico",
    "Calcula el peso total de 10, 20, 30 y 40 kilogramos"
)

# Consultar biodiversidad
biodiversidad = await preguntar_a_agente(
    runner_biologo,
    "sesion_biologo",
    "¿Qué especies hay en el Humedal La Conejera?"
)
```

### Ejemplo 2: Coordinación Automática

```python
pregunta = """
Quiero hacer una expedición al Humedal La Conejera en Bogotá.
Necesito saber:
1. ¿Cómo está el clima?
2. Si llevo equipaje de 15, 20, 10 y 5 kg, ¿cuánto peso total cargo?
3. ¿Qué biodiversidad puedo encontrar allí?

Dame una recomendación sobre si es buen momento para la expedición.
"""

recomendacion = await preguntar_a_agente(
    runner_principal,
    "sesion_principal",
    pregunta
)
```

## Estructura del Proyecto

```
DATAR/
├── api_inaturalist.py      # API REST para consultas de biodiversidad
├── sistema_agentes.py      # Sistema multi-agente coordinado
├── requirements.txt        # Dependencias del proyecto
├── .env                    # Variables de entorno (no incluir en git)
└── README.md              # Este archivo
```

## API Endpoints

### iNaturalist API

- `GET /` - Información de la API
- `GET /observaciones/aleatoria` - Obtiene una observación aleatoria
  - Parámetros:
    - `lugar` (opcional): Nombre del lugar (default: "Humedal La Conejera")
    - `ciudad` (opcional): Nombre de la ciudad (default: "Bogotá")
- `GET /health` - Verificar estado del servidor
- `GET /docs` - Documentación interactiva Swagger

### Ejemplo de respuesta

```json
{
  "exitoso": true,
  "lugar": "Humedal La Conejera",
  "ciudad": "Bogotá",
  "especie": "Ardea alba",
  "nombre_comun": "Garza Real",
  "fecha_observacion": "2025-01-15",
  "usuario": "naturalista123"
}
```

## Herramientas Disponibles

### Agente Meteorólogo
- `consultar_clima(ciudad: str)` - Consulta clima en tiempo real

### Agente Matemático
- `calcular_peso_total(peso1, peso2, peso3, peso4)` - Suma de pesos
- `calcular_distancia_estimada(velocidad, tiempo)` - Cálculo de distancia
- `calcular_raiz_cuadrada(numero)` - Raíz cuadrada

### Agente Biólogo
- `consultar_biodiversidad(lugar, ciudad)` - Observaciones de iNaturalist

## Configuración de Agentes

Cada agente tiene una personalidad única definida en sus instrucciones:

- **Meteorólogo**: Estilo teológico medieval con español antiguo
- **Matemático**: Técnico y puntual
- **Biólogo**: Apasionado y educativo
- **Coordinador**: Profesional y directo

Puedes modificar estas personalidades editando el campo `instruction` de cada agente en [sistema_agentes.py](sistema_agentes.py).

## Troubleshooting

### Error: "GOOGLE_API_KEY no encontrada"
- Verifica que el archivo `.env` existe en la raíz del proyecto
- Asegúrate de que la API key es válida

### Error: "No se pudo conectar a la API de iNaturalist"
- Verifica que `api_inaturalist.py` está ejecutándose en otra terminal
- Comprueba que el puerto 8000 no está siendo usado por otro proceso

### Error: "No se encontraron observaciones"
- El Humedal La Conejera puede no tener observaciones recientes
- Verifica tu conexión a internet

## Personalización

### Agregar nuevos lugares

Edita [api_inaturalist.py](api_inaturalist.py#L70-L72):

```python
coordenadas = {
    "Humedal La Conejera": {"lat": 4.7519, "lon": -74.0841, "radio": 1000},
    "Tu Nuevo Lugar": {"lat": LAT, "lon": LON, "radio": RADIO_METROS}
}
```

### Agregar nuevas herramientas

1. Define la función en [sistema_agentes.py](sistema_agentes.py)
2. Agrégala al array `tools` del agente correspondiente
3. Actualiza las instrucciones del agente

## Tecnologías Utilizadas

- **Google ADK**: Framework para agentes de IA
- **Google Gemini 2.0 Flash**: Modelo de lenguaje
- **FastAPI**: Framework web asíncrono
- **Uvicorn**: Servidor ASGI
- **Pydantic**: Validación de datos
- **Requests**: Cliente HTTP
- **python-dotenv**: Gestión de variables de entorno

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Autor

Sistema de Agentes Multi-Especializados - Proyecto DATAR

## Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio.

---

**Nota de Seguridad**: Nunca compartas tu `GOOGLE_API_KEY` públicamente. Asegúrate de agregar `.env` a tu `.gitignore`.
