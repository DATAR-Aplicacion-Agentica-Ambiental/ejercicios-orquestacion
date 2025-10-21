# Agentes - Agent Development Kit (ADK)

Agentes basados en **Google ADK** que interactúan con servidores MCP para consultar datos de biodiversidad.

## 🚀 Instalación

### Requisitos previos
- Python 3.9 o superior
- pip

### Pasos de instalación

#### 1. Crear entorno virtual

```bash
cd Agentes
python3 -m venv venv
source venv/bin/activate
```

#### 2. Instalar Google ADK

```bash
pip install google-adk
```

#### 3. Configurar API Key

Crea un archivo `.env` en el directorio raíz con tu API Key de Gemini:

```bash
echo 'GOOGLE_API_KEY="tu_api_key_aqui"' > .env
````

Obtén tu API Key en: [Google AI Studio](https://aistudio.google.com/apikey)


## 📁 Estructura

```
Agentes/
├── agent_demo_datar/          # Agente demo para iNaturalist
│   ├── agent.py               # Definición del agente
│   └── __init__.py
├── venv/                       # Entorno virtual
├── README                      # Este archivo
└── .env                        # Variables de entorno (NO compartir)
```

## ▶️ Ejecutar el agente

### Con interfaz de línea de comandos

```bash
adk run agent_demo_datar
```

### Con interfaz web (recomendado)

```bash
adk web
```

Accede a: [http://localhost:8000](http://localhost:8000)

## 🛠️ Herramientas disponibles

El agente `agent_demo_datar` está conectado al servidor MCP **iNaturalist** y tiene acceso a:

- `buscar_observaciones` - Busca observaciones por coordenadas geográficas
- `buscar_especies` - Busca información sobre especies y taxones
- `obtener_lugares` - Obtiene información sobre lugares cercanos
- `estadisticas_biodiversidad` - Estadísticas de biodiversidad por área
- `observaciones_por_usuario` - Observaciones de un usuario específico

**Ubicación por defecto:** Humedal la Conejera, Bogotá (4.8155°N, -74.0750°W)

## 📚 Referencias

- [Google ADK Python Quickstart](https://google.github.io/adk-docs/get-started/python/)
- [Documentación ADK Build](https://google.github.io/adk-docs/build-your-agent/)

## ⚠️ Notas importantes

- No compartir el archivo `.env` con las API keys
- El agente requiere conexión a internet para consultar iNaturalist
- Asegurate de activar el entorno virtual antes de ejecutar comandos
