import asyncio
import json
import logging
import os
import warnings
from concurrent.futures import ThreadPoolExecutor

import requests
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Cargar variables de entorno
load_dotenv()

# Configuración de logging y warnings
warnings.filterwarnings("ignore", category=ResourceWarning)
logging.getLogger("google_genai").setLevel(logging.ERROR)

# API Key de Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("⚠️  ERROR: GOOGLE_API_KEY no encontrada en el archivo .env")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# Executor para tareas asíncronas
executor = ThreadPoolExecutor(max_workers=3)


# ========================================
# HERRAMIENTAS BÁSICAS
# ========================================


def consultar_clima(ciudad: str) -> str:
    """Consulta el clima actual de una ciudad"""
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
    """Calcula el peso total sumando cuatro valores"""
    return peso1 + peso2 + peso3 + peso4


def calcular_distancia_estimada(
    velocidad_promedio: float, tiempo_horas: float
) -> float:
    """Calcula distancia según velocidad y tiempo"""
    return velocidad_promedio * tiempo_horas


def calcular_raiz_cuadrada(numero: float) -> float:
    """Calcula la raíz cuadrada"""
    return numero**0.5


# ========================================
# HELPER PARA EJECUTAR CÓDIGO ASÍNCRONO
# ========================================


def ejecutar_async_en_thread(coro):
    """Ejecuta una coroutine en un nuevo event loop en un thread separado"""

    def run_in_thread():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(coro)
        finally:
            new_loop.close()

    future = executor.submit(run_in_thread)
    return future.result(timeout=30)


# ========================================
# HERRAMIENTAS MCP
# ========================================


def consultar_estadisticas_colombia() -> str:
    """
    Consulta estadísticas generales de biodiversidad en Colombia.
    Usa el servidor MCP de iNaturalist.
    """
    try:
        return ejecutar_async_en_thread(_ejecutar_consulta_mcp("estadisticas", {}))
    except Exception as e:
        return f"⚠️  Error al consultar MCP: {str(e)}"


def buscar_especie_info(nombre_especie: str) -> str:
    """
    Busca información detallada sobre una especie.
    Usa el servidor MCP de iNaturalist.
    """
    try:
        return ejecutar_async_en_thread(
            _ejecutar_consulta_mcp("buscar_especie", {"nombre": nombre_especie})
        )
    except Exception as e:
        return f"⚠️  Error al consultar MCP: {str(e)}"


def buscar_observaciones_especie(nombre_especie: str) -> str:
    """
    Busca observaciones recientes de una especie en Colombia.
    Usa el servidor MCP de iNaturalist.
    """
    try:
        return ejecutar_async_en_thread(
            _ejecutar_consulta_mcp("buscar_observaciones", {"nombre": nombre_especie})
        )
    except Exception as e:
        return f"⚠️  Error al consultar MCP: {str(e)}"


def consultar_observaciones_usuario(nombre_usuario: str) -> str:
    """
    Consulta observaciones de un usuario en iNaturalist Colombia.
    Usa el servidor MCP.
    """
    try:
        return ejecutar_async_en_thread(
            _ejecutar_consulta_mcp("usuario", {"nombre": nombre_usuario})
        )
    except Exception as e:
        return f"⚠️  Error al consultar MCP: {str(e)}"


# ========================================
# FUNCIONES INTERNAS MCP
# ========================================


async def _ejecutar_consulta_mcp(tipo: str, parametros: dict) -> str:
    """Ejecuta la consulta MCP según el tipo"""
    server_params = StdioServerParameters(
        command="python", args=["servidor_mcp.py"], env=None
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                if tipo == "estadisticas":
                    result = await session.call_tool(
                        "estadisticas_biodiversidad_colombia", arguments={}
                    )
                    return _procesar_estadisticas(result)

                elif tipo == "buscar_especie":
                    result = await session.call_tool(
                        "buscar_especies", arguments={"nombre": parametros["nombre"]}
                    )
                    return _procesar_especies(result, parametros["nombre"])

                elif tipo == "buscar_observaciones":
                    result = await session.call_tool(
                        "buscar_observaciones",
                        arguments={"taxon_name": parametros["nombre"], "per_page": 5},
                    )
                    return _procesar_observaciones(result, parametros["nombre"])

                elif tipo == "usuario":
                    result = await session.call_tool(
                        "observaciones_por_usuario",
                        arguments={"username": parametros["nombre"], "per_page": 5},
                    )
                    return _procesar_usuario(result, parametros["nombre"])

                else:
                    return f"⚠️  Tipo de consulta '{tipo}' no reconocido"

    except FileNotFoundError:
        return "⚠️  Error: No se encontró servidor_mcp.py. Asegúrate de que esté en el mismo directorio."
    except Exception as e:
        return f"⚠️  Error al conectar con servidor MCP: {str(e)}"


def _procesar_estadisticas(result) -> str:
    """Procesa resultado de estadísticas"""
    try:
        data = json.loads(result.content[0].text)
        if "error" in data:
            return f"Error: {data['error']}"
        return (
            f"📊 Estadísticas de Biodiversidad en Colombia:\n"
            f"• Total de observaciones: {data.get('total_observaciones', 'N/A'):,}\n"
            f"• Total de especies: {data.get('total_especies', 'N/A'):,}"
        )
    except Exception as e:
        return f"Error procesando estadísticas: {str(e)}"


def _procesar_especies(result, nombre: str) -> str:
    """Procesa resultado de búsqueda de especies"""
    try:
        data = json.loads(result.content[0].text)
        if "error" in data:
            return f"Error: {data['error']}"
        if not data.get("especies"):
            return f"No se encontraron especies con '{nombre}'"

        resultado = f"🔍 Búsqueda de '{nombre}':\n\n"
        for i, esp in enumerate(data["especies"][:3], 1):
            resultado += f"{i}. {esp.get('nombre_cientifico', 'N/A')}\n"
            if esp.get("nombre_comun"):
                resultado += f"   Común: {esp['nombre_comun']}\n"
            resultado += f"   Rango: {esp.get('rango', 'N/A')}\n"
            resultado += (
                f"   Observaciones: {esp.get('observaciones_totales', 0):,}\n\n"
            )
        return resultado
    except Exception as e:
        return f"Error procesando especies: {str(e)}"


def _procesar_observaciones(result, nombre: str) -> str:
    """Procesa resultado de observaciones"""
    try:
        data = json.loads(result.content[0].text)
        if "error" in data:
            return f"Error: {data['error']}"
        if not data.get("observaciones"):
            return f"No se encontraron observaciones de '{nombre}'"

        resultado = f"🔎 Observaciones de '{nombre}':\n"
        resultado += f"Total: {data.get('total', 0):,}\n\n"
        for i, obs in enumerate(data["observaciones"][:3], 1):
            resultado += f"{i}. {obs.get('especie', 'No identificado')}\n"
            resultado += f"   Fecha: {obs.get('fecha_observacion', 'N/A')}\n"
            resultado += f"   Lugar: {obs.get('lugar', 'N/A')}\n\n"
        return resultado
    except Exception as e:
        return f"Error procesando observaciones: {str(e)}"


def _procesar_usuario(result, nombre: str) -> str:
    """Procesa resultado de usuario"""
    try:
        data = json.loads(result.content[0].text)
        if "error" in data:
            return f"Error: {data['error']}"

        resultado = f"👤 Usuario '{nombre}':\n"
        resultado += f"Total observaciones: {data.get('total_observaciones', 0):,}\n\n"
        if data.get("observaciones"):
            for i, obs in enumerate(data["observaciones"][:3], 1):
                resultado += f"{i}. {obs.get('especie', 'No identificado')}\n"
                resultado += f"   Fecha: {obs.get('fecha', 'N/A')}\n"
                resultado += f"   Lugar: {obs.get('lugar', 'N/A')}\n\n"
        return resultado
    except Exception as e:
        return f"Error procesando usuario: {str(e)}"


# ========================================
# AGENTES
# ========================================

agente_meteorologo = Agent(
    name="meteorologo",
    model="gemini-2.0-flash",
    instruction="Eres un meteorólogo. Consulta el clima y proporciona reportes claros. Hablas con estilo medieval.",
    tools=[consultar_clima],
)

agente_matematico = Agent(
    name="matematico",
    model="gemini-2.0-flash",
    instruction="Eres un experto en cálculos. Usa las herramientas para garantizar precisión. Eres muy técnico.",
    tools=[calcular_peso_total, calcular_distancia_estimada, calcular_raiz_cuadrada],
)

agente_biologo = Agent(
    name="biologo",
    model="gemini-2.0-flash",
    instruction="""Eres un biólogo especializado en biodiversidad colombiana.

Herramientas disponibles:
- consultar_estadisticas_colombia: Estadísticas generales
- buscar_especie_info: Información de especies
- buscar_observaciones_especie: Observaciones recientes
- consultar_observaciones_usuario: Historial de usuarios

Usa la herramienta apropiada según la pregunta. Eres apasionado y educativo.""",
    tools=[
        consultar_estadisticas_colombia,
        buscar_especie_info,
        buscar_observaciones_especie,
        consultar_observaciones_usuario,
    ],
)

agente_principal = Agent(
    name="coordinador",
    model="gemini-2.0-flash",
    instruction="""Coordinas expediciones. Analiza preguntas y delega a los agentes especializados.
    Integra respuestas en recomendaciones claras.""",
)


# ========================================
# CONFIGURACIÓN
# ========================================

session_service = InMemorySessionService()
APP_NAME = "asistente-explorador"
USER_ID = "explorador_01"


async def inicializar_sesiones():
    """Inicializa sesiones"""
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_principal"
    )
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_meteorologo"
    )
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_matematico"
    )
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_biologo"
    )


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
# INTERACCIÓN
# ========================================


async def preguntar_a_agente(runner, session_id, pregunta, reintentos=3):
    """Pregunta a un agente con reintentos en caso de error 503"""
    for intento in range(reintentos):
        try:
            contenido = types.Content(role="user", parts=[types.Part(text=pregunta)])

            async for evento in runner.run_async(
                user_id=USER_ID, session_id=session_id, new_message=contenido
            ):
                if evento.is_final_response() and evento.content:
                    return " ".join(
                        p.text
                        for p in evento.content.parts
                        if hasattr(p, "text") and p.text
                    )
            return ""

        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                if intento < reintentos - 1:
                    espera = (intento + 1) * 3
                    print(
                        f"   ⚠️  Modelo saturado. Reintentando en {espera}s... ({intento + 1}/{reintentos})"
                    )
                    await asyncio.sleep(espera)
                    continue
                else:
                    return "❌ El servicio de Gemini está temporalmente saturado. Por favor intenta más tarde."
            else:
                return f"❌ Error: {error_msg}"

    return "❌ No se pudo completar la consulta después de varios intentos."


# ========================================
# EJEMPLOS
# ========================================


def ejemplo_consulta_directa_mcp_sync():
    """Ejemplo: Prueba directa de herramientas MCP (versión síncrona)"""
    print("\n" + "=" * 70)
    print("🧪 PRUEBA DIRECTA: Herramientas MCP")
    print("=" * 70 + "\n")

    print("1️⃣ Probando estadísticas de Colombia...")
    resultado = consultar_estadisticas_colombia()
    print(f"{resultado}\n")

    print("2️⃣ Probando búsqueda de especie: Oso de anteojos...")
    resultado = buscar_especie_info("Tremarctos ornatus")
    print(f"{resultado}\n")

    print("3️⃣ Probando observaciones de Colibrí...")
    resultado = buscar_observaciones_especie("Colibrí")
    print(f"{resultado}\n")


async def ejemplo_con_agente():
    """Ejemplo: Consulta a través del agente biólogo"""
    print("\n" + "=" * 70)
    print("🤖 EJEMPLO: Consulta con agente biólogo")
    print("=" * 70 + "\n")

    print("Preguntando al biólogo sobre estadísticas...\n")
    respuesta = await preguntar_a_agente(
        runner_biologo,
        "sesion_biologo",
        "Dame las estadísticas de biodiversidad en Colombia",
    )
    print(f"Respuesta:\n{respuesta}\n")


# ========================================
# MAIN
# ========================================


async def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🌿 Sistema de Agentes - Versión Final")
    print("=" * 70)

    print("\n📋 Inicializando agentes...")
    await inicializar_sesiones()
    print("✅ ¡Agentes listos!\n")

    # Ejecutar prueba directa
    print("💡 Ejecutando prueba directa de MCP...\n")
    ejemplo_consulta_directa_mcp_sync()

    # Si quieres probar con el agente (descomenta):
    # print("\n💡 Ahora probando con el agente...\n")
    # await ejemplo_con_agente()

    print("\n" + "=" * 70)
    print("✅ Pruebas completadas")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
