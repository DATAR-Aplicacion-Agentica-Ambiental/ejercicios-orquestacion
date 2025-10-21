import asyncio
import logging
import os
import warnings

import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Cargar variables de entorno desde .env
load_dotenv()

# Suprimir warnings específicos
warnings.filterwarnings("ignore")
logging.getLogger("google_genai").setLevel(logging.ERROR)

# Configurar API Key de Google desde .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("⚠️  ERROR: GOOGLE_API_KEY no encontrada en el archivo .env")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# URL de la API de iNaturalist (local)
API_INATURALIST_URL = os.getenv("API_INATURALIST_URL", "http://localhost:8000")


# ========================================
# DEFINICIÓN DE HERRAMIENTAS
# ========================================


def consultar_clima(ciudad: str) -> str:
    """Consulta el clima actual de una ciudad usando wttr.in

    Args:
        ciudad: Nombre de la ciudad a consultar

    Returns:
        Reporte de clima en formato texto
    """
    try:
        url = f"https://wttr.in/{ciudad}?format=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        return "No se pudo obtener información del clima"
    except Exception as e:
        return f"Error al consultar clima: {str(e)}"


def calcular_peso_total(
    peso1: float, peso2: float, peso3: float, peso4: float
) -> float:
    """Calcula el peso total sumando cuatro valores

    Args:
        peso1: Primer peso en kilogramos
        peso2: Segundo peso en kilogramos
        peso3: Tercer peso en kilogramos
        peso4: Cuarto peso en kilogramos

    Returns:
        Peso total en kilogramos
    """
    return peso1 + peso2 + peso3 + peso4


def calcular_distancia_estimada(
    velocidad_promedio: float, tiempo_horas: float
) -> float:
    """Calcula distancia estimada según velocidad y tiempo

    Args:
        velocidad_promedio: Velocidad en km/h
        tiempo_horas: Tiempo de viaje en horas

    Returns:
        Distancia en kilómetros
    """
    return velocidad_promedio * tiempo_horas


def calcular_raiz_cuadrada(numero: float) -> float:
    """Calcula la raíz cuadrada de un número

    Args:
        numero: Número del cual calcular la raíz

    Returns:
        Raíz cuadrada del número
    """
    return numero**0.5


def consultar_biodiversidad(
    lugar: str = "Humedal La Conejera", ciudad: str = "Bogotá"
) -> str:
    """Consulta observaciones de biodiversidad en un lugar específico usando la API de iNaturalist

    Args:
        lugar: Nombre del lugar a consultar (default: Humedal La Conejera)
        ciudad: Nombre de la ciudad (default: Bogotá)

    Returns:
        Información sobre una observación aleatoria de biodiversidad en formato texto
    """
    try:
        url = f"{API_INATURALIST_URL}/observaciones/aleatoria"
        params = {"lugar": lugar, "ciudad": ciudad}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            datos = response.json()
            if datos.get("exitoso"):
                return (
                    f"Observación en {datos['lugar']}, {datos['ciudad']}:\n"
                    f"Especie: {datos['especie']} ({datos['nombre_comun']})\n"
                    f"Fecha: {datos['fecha_observacion']}\n"
                    f"Observador: {datos['usuario']}"
                )
            else:
                return f"No se encontraron observaciones para {lugar}"
        else:
            return f"Error al consultar biodiversidad: código {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "⚠️  Error: No se pudo conectar a la API de iNaturalist. Asegúrate de que el servidor esté corriendo en http://localhost:8000"
    except Exception as e:
        return f"Error al consultar biodiversidad: {str(e)}"


# ========================================
# CREACIÓN DE AGENTES
# ========================================

# Subagente Meteorólogo
agente_meteorologo = Agent(
    name="meteorologo",
    model="gemini-2.0-flash",
    instruction="""Eres un meteorólogo especializado.
    Tu tarea es consultar el clima de la ciudad solicitada usando la herramienta disponible.
    Analiza la información y proporciona un reporte claro sobre temperatura, condiciones y viento.
    Se preciso y profesional en tu análisis. Tu forma de hablar es muy adornada y como un teólogo medieval y usas español antiguo""",
    tools=[consultar_clima],
)

# Subagente Matemático
agente_matematico = Agent(
    name="matematico",
    model="gemini-2.0-flash",
    instruction="""Eres un experto en cálculos logísticos.
    Tu tarea es realizar cálculos precisos sobre peso de carga, distancias y otros valores numéricos.
    Siempre usa las herramientas disponibles para garantizar precisión absoluta.
    Presenta los resultados de forma clara y concisa. Tu forma de hablar es demasiado técnica y puntual""",
    tools=[calcular_peso_total, calcular_distancia_estimada, calcular_raiz_cuadrada],
)

# Subagente Biólogo
agente_biologo = Agent(
    name="biologo",
    model="gemini-2.0-flash",
    instruction="""Eres un biólogo especializado en biodiversidad colombiana.
    Tu tarea es consultar información sobre especies observadas en diferentes lugares.
    Usa la herramienta disponible para obtener datos de observaciones reales de iNaturalist.
    Proporciona contexto sobre las especies encontradas y su importancia ecológica.
    Tu forma de hablar es apasionada y educativa, tratando de despertar el interés por la naturaleza.""",
    tools=[consultar_biodiversidad],
)

# Agente Principal Coordinador
agente_principal = Agent(
    name="coordinador_expedicion",
    model="gemini-2.0-flash",
    instruction="""Eres el Coordinador del Asistente del Explorador.
    Tu trabajo es analizar las preguntas sobre expediciones y determinar qué información necesitas.

    Cuando recibas una pregunta sobre una expedición:
    1. Identifica si necesitas información meteorológica
    2. Identifica si necesitas cálculos logísticos
    3. Identifica si necesitas información sobre biodiversidad del lugar
    4. Solicita esta información a los agentes especializados
    5. Integra todas las respuestas en una recomendación final clara

    Tu respuesta final debe ser concisa y directa, indicando si es buen momento para la expedición.
    Basa tu recomendación en los datos proporcionados por los subagentes.""",
)


# ========================================
# CONFIGURACIÓN DE SESIONES Y RUNNERS
# ========================================

# Servicio de sesiones en memoria para mantener el contexto
session_service = InMemorySessionService()

# Parámetros de la aplicación
APP_NAME = "asistente-explorador"
USER_ID = "explorador_01"


# Crear sesiones independientes para cada agente
async def inicializar_sesiones():
    """Inicializa las sesiones para todos los agentes"""
    session_principal = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_principal"
    )

    session_meteorologo = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_meteorologo"
    )

    session_matematico = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_matematico"
    )

    session_biologo = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_biologo"
    )

    return session_principal, session_meteorologo, session_matematico, session_biologo


# Crear runners para cada agente
runner_principal = Runner(
    agent=agente_principal, app_name=APP_NAME, session_service=session_service
)

runner_meteorologo = Runner(
    agent=agente_meteorologo, app_name=APP_NAME, session_service=session_service
)

runner_matematico = Runner(
    agent=agente_matematico, app_name=APP_NAME, session_service=session_service
)

runner_biologo = Runner(
    agent=agente_biologo, app_name=APP_NAME, session_service=session_service
)


# ========================================
# FUNCIONES DE INTERACCIÓN
# ========================================


async def preguntar_a_agente(runner, session_id, pregunta):
    """
    Función simple para hacer una pregunta a cualquier agente

    Args:
        runner: El runner del agente (ej: runner_meteorologo)
        session_id: ID de la sesión (ej: "sesion_meteorologo")
        pregunta: La pregunta en texto simple

    Returns:
        Respuesta del agente en texto
    """
    contenido = types.Content(role="user", parts=[types.Part(text=pregunta)])

    async for evento in runner.run_async(
        user_id=USER_ID, session_id=session_id, new_message=contenido
    ):
        if evento.is_final_response() and evento.content:
            return " ".join(
                p.text for p in evento.content.parts if hasattr(p, "text") and p.text
            )
    return ""


# ========================================
# EJEMPLOS DE USO
# ========================================


async def ejemplo_1_agente_individual():
    """
    EJEMPLO 1: Consultar un solo agente
    Muestra cómo hacer preguntas individuales a cada agente
    """
    print("\n" + "=" * 70)
    print("📚 EJEMPLO 1: Usando agentes individuales")
    print("=" * 70 + "\n")

    # Pregunta al meteorólogo
    print("🌤️  Preguntando al Meteorólogo...")
    clima = await preguntar_a_agente(
        runner_meteorologo, "sesion_meteorologo", "¿Cómo está el clima en Bogotá?"
    )
    print(f"Respuesta: {clima}\n")

    # Pregunta al matemático
    print("📊 Preguntando al Matemático...")
    calculo = await preguntar_a_agente(
        runner_matematico,
        "sesion_matematico",
        "Calcula el peso total de 10, 20, 30 y 40 kilogramos",
    )
    print(f"Respuesta: {calculo}\n")

    # Pregunta al biólogo
    print("🌿 Preguntando al Biólogo...")
    biodiversidad = await preguntar_a_agente(
        runner_biologo, "sesion_biologo", "¿Qué especies hay en el Humedal La Conejera?"
    )
    print(f"Respuesta: {biodiversidad}\n")


async def ejemplo_2_coordinacion_simple():
    """
    EJEMPLO 2: Coordinación simple
    El agente principal coordina a los demás
    """
    print("\n" + "=" * 70)
    print("📚 EJEMPLO 2: Coordinación simple de agentes")
    print("=" * 70 + "\n")

    # Hacemos UNA pregunta al coordinador, y él se encarga de todo
    pregunta_completa = """
    Quiero hacer una expedición al Humedal La Conejera en Bogotá.
    Necesito saber:
    1. ¿Cómo está el clima?
    2. Si llevo equipaje de 15, 20, 10 y 5 kg, ¿cuánto peso total cargo?
    3. ¿Qué biodiversidad puedo encontrar allí?

    Dame una recomendación sobre si es buen momento para la expedición.
    """

    print("🎯 Coordinador analizando la expedición...\n")
    recomendacion = await preguntar_a_agente(
        runner_principal, "sesion_principal", pregunta_completa
    )
    print(f"✅ RECOMENDACIÓN:\n{recomendacion}\n")


async def ejemplo_3_uso_libre():
    """
    EJEMPLO 3: Uso libre
    ¡Experimenta aquí con tus propias preguntas!
    """
    print("\n" + "=" * 70)
    print("📚 EJEMPLO 3: ¡Tu turno de experimentar!")
    print("=" * 70 + "\n")

    # Cambia estas preguntas por las que quieras probar
    print("💡 Prueba tus propias preguntas aquí...\n")

    # Ejemplo: Pregunta personalizada al meteorólogo
    mi_ciudad = "Medellín"  # Cambia la ciudad aquí
    respuesta = await preguntar_a_agente(
        runner_meteorologo, "sesion_meteorologo", f"¿Qué clima hay en {mi_ciudad}?"
    )
    print(f"🌤️  Clima en {mi_ciudad}:\n{respuesta}\n")


# ========================================
# EJECUCIÓN PRINCIPAL
# ========================================


async def main():
    """
    Función principal - Ejecuta los ejemplos
    Puedes comentar/descomentar los ejemplos que quieras probar
    """
    print("\n" + "=" * 70)
    print("Sistema de Agentes")
    print("=" * 70)

    # Inicializar sesiones (necesario siempre)
    print("\n📋 Inicializando agentes...")
    await inicializar_sesiones()
    print("✅ ¡Agentes listos!\n")

    # Ejecuta los ejemplos que quieras (comenta los que no necesites)

    # await ejemplo_1_agente_individual()      # Consultas individuales
    await ejemplo_2_coordinacion_simple()  # Coordinación automática
    # await ejemplo_3_uso_libre()              # Tus propias pruebas

    print("\n" + "=" * 70)
    print("✅ Ejemplos completados")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
    warnings.filterwarnings('ignore', category=ResourceWarning)
    asyncio.run(main())
