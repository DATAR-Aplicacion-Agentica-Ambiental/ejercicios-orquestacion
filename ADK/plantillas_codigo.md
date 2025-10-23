# 🌿 Plantillas de Código para el Asistente de Expediciones

Este archivo contiene plantillas de código limpias y reutilizables que muestran las estructuras esenciales del proyecto. Están diseñadas para ser didácticas, con comentarios claros y mínima complejidad, facilitando su uso y ampliación.

## 1. Base del Proyecto

Esta sección cubre la configuración inicial y la estructura fundamental para cualquier proyecto de agentes con ADK.

### 1.1. `requirements.txt` (Dependencias)

Define las librerías de Python necesarias. Una versión mínima y esencial sería:

```txt
# --- Plantilla de requirements.txt ---

# Google ADK y Gemini para los agentes de IA
google-adk
google-genai

# Servidor web para APIs REST (si es necesario)
fastapi
uvicorn

# Para realizar llamadas a APIs externas
requests

# Para gestionar variables de entorno (como API keys)
python-dotenv

# Para el protocolo MCP (si se usa)
mcp
httpx
```

> **Nota Explicativa:** Mantener este archivo limpio asegura que solo se instalen las dependencias necesarias, haciendo el proyecto más ligero y fácil de gestionar.

### 1.2. `.env` (Variables de Entorno)

Un archivo para almacenar claves secretas de forma segura, separado del código.

```env
# --- Plantilla de .env ---

# Clave de API de Google para usar los modelos Gemini
# Obtenla en: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY="TU_CLAVE_SECRETA_DE_GOOGLE_AQUI"

# (Opcional) URL del servidor de API local si estás usando uno
API_INATURALIST_URL="http://localhost:8000"
```

> **Nota Explicativa:** Nunca compartas este archivo ni incluyas tus claves secretas directamente en el código. Añade `.env` a tu `.gitignore` para evitar subirlo a repositorios públicos.

### 1.3. Script Principal Básico

Estructura de un script de Python para inicializar el entorno de forma segura.

```python
# --- Plantilla de Script Principal ---

import os
from dotenv import load_dotenv

def inicializar_entorno():
    """
    Carga las variables de entorno y configura la API Key de Google.
    
    Retorna:
        bool: True si la configuración fue exitosa, False en caso contrario.
    """
    print("🔌 Cargando configuración...")
    
    # Carga las variables desde el archivo .env
    load_dotenv()
    
    # Obtiene la API Key de Google
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: La variable GOOGLE_API_KEY no se encontró.")
        print("   Asegúrate de crear un archivo .env con tu clave.")
        return False
        
    # Configura la API Key para que las librerías de Google la usen
    os.environ["GOOGLE_API_KEY"] = api_key
    
    # Importante para usar los modelos de Gemini directamente
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
    
    print("✅ Entorno configurado correctamente.")
    return True

if __name__ == "__main__":
    if inicializar_entorno():
        # Aquí iría la lógica principal de tu aplicación
        print("🚀 Aplicación lista para iniciar.")
        # Ejemplo: asyncio.run(main())
    else:
        print("🛑 La aplicación no puede continuar sin la configuración correcta.")

```

> **Nota Explicativa:** Esta estructura centraliza la configuración, valida que las claves existan antes de ejecutar el resto del código y previene errores comunes.

---

## 2. Integración de Herramientas

Las herramientas son funciones de Python que los agentes pueden llamar para realizar tareas específicas.

### 2.1. Herramienta Simple (Cálculo Local)

Una función que no depende de servicios externos.

```python
# --- Plantilla de Herramienta Simple ---

def calcular_promedio(numeros: list[float]) -> float:
    """
    Calcula el promedio de una lista de números.
    
    Args:
        numeros: Una lista de números para promediar.
        
    Returns:
        El promedio calculado.
    """
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

# Ejemplo de uso (para pruebas)
# print(f"El promedio es: {calcular_promedio([10, 20, 30])}")
```

> **Nota Explicativa:** Las herramientas deben ser simples, con una única responsabilidad. Los `docstrings` son cruciales, ya que el modelo de IA los usa para entender qué hace la herramienta y cómo llamarla.

### 2.2. Herramienta de API Externa (Llamada Web)

Una función que se conecta a una API externa para obtener datos.

```python
# --- Plantilla de Herramienta de API Externa ---

import requests

def obtener_chiste_aleatorio() -> str:
    """
    Obtiene un chiste aleatorio de una API pública.
    
    Returns:
        Un chiste en formato de texto.
    """
    API_URL = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # Realiza la llamada a la API con un tiempo de espera
        response = requests.get(API_URL, timeout=5)
        
        # Lanza un error si la respuesta no fue exitosa (ej. 404, 500)
        response.raise_for_status()
        
        # Convierte la respuesta JSON en un diccionario de Python
        datos = response.json()
        
        # Formatea la salida para que sea fácil de entender
        return f"{datos['setup']} - {datos['punchline']}"
        
    except requests.exceptions.Timeout:
        return "Lo siento, la API de chistes tardó mucho en responder."
    except requests.exceptions.RequestException as e:
        return f"Error al contactar la API de chistes: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

# Ejemplo de uso (para pruebas)
# print(obtener_chiste_aleatorio())
```

> **Nota Explicativa:** Es fundamental incluir un manejo de errores robusto (timeouts, errores de conexión, etc.) para que el agente pueda gestionar fallos en servicios externos y no se bloquee.

---

## 3. Lógica de Agentes (ADK)

Define el "cerebro" de los agentes, sus personalidades y las herramientas que pueden usar.

### 3.1. Agente Especializado

Un agente diseñado para una tarea específica, con acceso a herramientas relevantes.

```python
# --- Plantilla de Agente Especializado ---

from google.adk.agents import Agent

# Asume que las funciones `calcular_promedio` y `obtener_chiste_aleatorio` ya existen
# from .herramientas import calcular_promedio, obtener_chiste_aleatorio

# Creación del agente
agente_analista = Agent(
    name="analista_de_datos",
    model="gemini-2.0-flash",  # Modelo de IA a utilizar
    
    # Instrucciones que definen la personalidad y el comportamiento del agente
    instruction="""
    Eres un analista de datos y también tienes un gran sentido del humor.
    - Para cualquier cálculo numérico, DEBES usar la herramienta `calcular_promedio`.
    - Si te piden algo divertido o un chiste, DEBES usar la herramienta `obtener_chiste_aleatorio`.
    - Responde de forma clara, precisa y con un toque amigable.
    """,
    
    # Lista de herramientas que este agente puede utilizar
    tools=[
        calcular_promedio,
        obtener_chiste_aleatorio
    ]
)
```

> **Nota Explicativa:** La `instruction` (o "prompt del sistema") es la parte más importante. Debe ser muy clara sobre las responsabilidades del agente y cuándo debe usar cada herramienta.

### 3.2. Agente Coordinador

Un agente que no usa herramientas directamente, sino que delega tareas a otros agentes.

```python
# --- Plantilla de Agente Coordinador ---

from google.adk.agents import Agent

agente_coordinador = Agent(
    name="jefe_de_proyecto",
    model="gemini-2.0-flash",
    
    instruction="""
    Eres el coordinador general. Tu única tarea es analizar la solicitud del usuario
    y delegar las subtareas a los agentes especializados correspondientes.
    
    - Si la solicitud implica números o cálculos, delega al 'analista_de_datos'.
    - Si la solicitud es sobre planificación o estrategia, formula un plan.
    
    No respondas directamente a la solicitud final. Tu trabajo es dirigir.
    """,
    
    # Un coordinador generalmente no tiene herramientas propias
    tools=[]
)
```

> **Nota Exlicativa:** La clave de un buen coordinador es su capacidad para descomponer un problema complejo en partes más pequeñas y saber a quién asignárselas. Sus instrucciones deben enfocarse en la delegación.

### 3.3. Configuración de `Runner` y `Session`

El `Runner` ejecuta el agente y la `Session` mantiene el historial de la conversación.

```python
# --- Plantilla de Runner y Session ---

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# 1. Crear un servicio de sesiones (en memoria para simplicidad)
session_service = InMemorySessionService()

# 2. Definir identificadores únicos
APP_NAME = "mi_aplicacion_de_agentes"
USER_ID = "usuario_001"
SESSION_ID = "sesion_analista_1"

# 3. Crear el Runner para un agente específico
# (asume que `agente_analista` ya fue creado)
runner_analista = Runner(
    agent=agente_analista,
    app_name=APP_NAME,
    session_service=session_service,
)

async def ejecutar_agente():
    """Función para inicializar y ejecutar una consulta al agente."""
    # Crear la sesión en el servicio
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # La pregunta del usuario
    pregunta = "Calcula el promedio de 5, 10 y 15, y luego cuéntame un chiste."
    
    # Crear el objeto de contenido para el runner
    contenido_pregunta = Content(role="user", parts=[Part(text=pregunta)])
    
    print(f"Pregunta: {pregunta}")
    print("\n🤖 Agente pensando...")
    
    # Ejecutar el agente de forma asíncrona
    respuesta_final = ""
    async for evento in runner_analista.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=contenido_pregunta
    ):
        if evento.is_final_response() and evento.content:
            # Acumular el texto de la respuesta final
            respuesta_final = " ".join(p.text for p in evento.content.parts if hasattr(p, "text"))

    print(f"\nRespuesta del Agente:\n{respuesta_final}")

# Para ejecutar la función asíncrona
# if __name__ == "__main__":
#     asyncio.run(ejecutar_agente())
```

> **Nota Explicativa:** Esta estructura es el motor que pone en marcha a los agentes. El `Runner` se encarga de la lógica de ejecución (llamar al modelo, ejecutar herramientas), mientras que la `Session` asegura que el agente recuerde las conversaciones anteriores.

---

## 4. Servidor FastAPI (API REST)

Para exponer funcionalidades a través de una API web simple y rápida.

### 4.1. Servidor Básico con Endpoint

```python
# --- Plantilla de Servidor FastAPI ---

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Mi API Personalizada",
    description="Una API de ejemplo para proyectos de agentes.",
    version="1.0"
)

# --- Modelos de Datos (Pydantic) ---
# Ayudan a validar los datos de entrada y salida.

class Entrada(BaseModel):
    nombre: str
    edad: int

class Salida(BaseModel):
    mensaje: str
    datos_recibidos: Entrada

# --- Endpoints de la API ---

@app.get("/")
def endpoint_raiz():
    """Endpoint principal que da la bienvenida."""
    return {"mensaje": "Bienvenido a mi API personalizada"}

@app.post("/saludar", response_model=Salida)
def endpoint_saludar(entrada: Entrada):
    """Recibe datos, los procesa y devuelve un saludo."""
    if entrada.edad < 18:
        # Ejemplo de manejo de errores
        raise HTTPException(status_code=400, detail="La edad debe ser mayor de 18.")
        
    mensaje_salida = f"¡Hola, {entrada.nombre}! Tienes {entrada.edad} años."
    
    return Salida(
        mensaje=mensaje_salida,
        datos_recibidos=entrada
    )

# --- Ejecución del Servidor ---
# Para ejecutar, guarda este código como `mi_api.py` y corre en la terminal:
# uvicorn mi_api:app --reload
```

> **Nota Explicativa:** FastAPI es ideal para crear APIs rápidas que los agentes pueden consumir. Usar modelos Pydantic (`BaseModel`) es una buena práctica porque garantiza que los datos que entran y salen de tu API tengan la estructura correcta, previniendo errores.

---

## 5. Servidor MCP (FastMCP)

Para exponer herramientas más complejas o que requieren un estado, usando el Protocolo de Contexto de Modelo (MCP).

### 5.1. Servidor Básico con una Herramienta

```python
# --- Plantilla de Servidor FastMCP ---

from mcp.server.fastmcp import FastMCP
import httpx  # Recomendado para llamadas asíncronas a APIs

# Inicializar el servidor MCP con un nombre descriptivo
mcp = FastMCP("ServidorDeHerramientasAvanzadas")

# URL base de una API externa que usaremos
BASE_URL = "https://api.publicapis.org"

@mcp.tool()
async def buscar_apis_publicas(categoria: str) -> dict:
    """
    Busca APIs públicas por categoría.
    
    Args:
        categoria: La categoría a buscar (ej: 'Animals', 'Weather').
        
    Returns:
        Un diccionario con la lista de APIs encontradas.
    """
    try:
        # Usar un cliente asíncrono para no bloquear el servidor
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {"category": categoria}
            response = await client.get(f"{BASE_URL}/entries", params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['count'] == 0:
                return {"mensaje": f"No se encontraron APIs para la categoría '{categoria}'."}
            
            # Formatear una respuesta útil
            nombres_apis = [entry['API'] for entry in data['entries'][:5]] # Limitar a 5
            return {
                "total_encontrado": data['count'],
                "primeros_resultados": nombres_apis
            }
            
    except httpx.HTTPStatusError as e:
        return {"error": f"Error de la API externa: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Error inesperado en el servidor MCP: {str(e)}"}

# --- Ejecución del Servidor ---
# Para ejecutar, guarda este código como `mi_servidor_mcp.py` y corre en la terminal:
# python mi_servidor_mcp.py
if __name__ == "__main__":
    print("🚀 Servidor MCP iniciado. Esperando conexiones...")
    mcp.run()

```

> **Nota Explicativa:** MCP es más adecuado para herramientas complejas que pueden ser lentas o requerir un estado persistente. El decorador `@mcp.tool()` expone la función al cliente MCP (en este caso, el agente). Usar `httpx.AsyncClient` es crucial para mantener el servidor receptivo mientras espera respuestas de APIs externas.
