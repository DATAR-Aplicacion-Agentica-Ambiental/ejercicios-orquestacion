"""
Sistema de Agentes con MCP - AGENTE BIÓLOGO ACTIVO
Versión sin warnings - Salida limpia
"""

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

# ========================================
# SUPRESIÓN DE WARNINGS
# ========================================

# Método 1: Suprimir todos los ResourceWarning
warnings.filterwarnings("ignore", category=ResourceWarning)

# Método 2: Suprimir warnings específicos de aiohttp
warnings.filterwarnings("ignore", message=".*Unclosed client session.*")
warnings.filterwarnings("ignore", message=".*Unclosed connector.*")

# Método 3: Configurar logging para ignorar warnings
logging.getLogger("google_genai").setLevel(logging.ERROR)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

# Método 4: Configurar asyncio para no mostrar warnings de recursos
import sys

if sys.version_info >= (3, 8):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass

# Cargar variables de entorno
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("⚠️  ERROR: GOOGLE_API_KEY no encontrada en el archivo .env")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

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

    Retorna el total de observaciones y especies registradas.
    """
    try:
        return ejecutar_async_en_thread(_ejecutar_consulta_mcp("estadisticas", {}))
    except Exception as e:
        return f"⚠️  Error al consultar MCP: {str(e)}"


def buscar_especie_info(nombre_especie: str) -> str:
    """
    Busca información detallada sobre una especie.

    Args:
        nombre_especie: Nombre común o científico de la especie

    Retorna información taxonómica y número de observaciones.
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

    Args:
        nombre_especie: Nombre de la especie

    Retorna lista de observaciones con fecha y ubicación.
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

    Args:
        nombre_usuario: Nombre de usuario en iNaturalist

    Retorna historial de observaciones del usuario.
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
        return "⚠️  Error: No se encontró servidor_mcp.py"
    except Exception as e:
        return f"⚠️  Error al conectar con servidor MCP: {str(e)}"


def _procesar_estadisticas(result) -> str:
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

agente_biologo = Agent(
    name="biologo",
    model="gemini-2.0-flash",
    instruction="""Eres un biólogo experto en biodiversidad colombiana, apasionado por la naturaleza.

HERRAMIENTAS DISPONIBLES:
1. consultar_estadisticas_colombia() - Estadísticas generales de Colombia
2. buscar_especie_info(nombre) - Información detallada de una especie
3. buscar_observaciones_especie(nombre) - Observaciones recientes de una especie
4. consultar_observaciones_usuario(usuario) - Historial de un observador

CÓMO USARLAS:
- Si preguntan por estadísticas generales → usa consultar_estadisticas_colombia()
- Si preguntan sobre UNA especie específica → usa buscar_especie_info()
- Si quieren ver observaciones de una especie → usa buscar_observaciones_especie()
- Si preguntan por un usuario → usa consultar_observaciones_usuario()

IMPORTANTE:
- Siempre usa la herramienta apropiada antes de responder
- Después de obtener los datos, compártelos de forma educativa y entusiasta
- Agrega contexto ecológico interesante sobre las especies
- Inspira amor y respeto por la biodiversidad colombiana

Tu forma de hablar es apasionada, educativa y busca despertar el interés por la naturaleza.""",
    tools=[
        consultar_estadisticas_colombia,
        buscar_especie_info,
        buscar_observaciones_especie,
        consultar_observaciones_usuario,
    ],
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
        app_name=APP_NAME, user_id=USER_ID, session_id="sesion_biologo"
    )


runner_biologo = Runner(
    agent=agente_biologo, app_name=APP_NAME, session_service=session_service
)


# ========================================
# INTERACCIÓN
# ========================================


async def preguntar_a_agente(pregunta: str, reintentos=2):
    """Pregunta al agente biólogo con reintentos"""
    for intento in range(reintentos):
        try:
            contenido = types.Content(role="user", parts=[types.Part(text=pregunta)])

            respuesta_completa = ""
            async for evento in runner_biologo.run_async(
                user_id=USER_ID, session_id="sesion_biologo", new_message=contenido
            ):
                if evento.is_final_response() and evento.content:
                    respuesta_completa = " ".join(
                        p.text
                        for p in evento.content.parts
                        if hasattr(p, "text") and p.text
                    )

            return respuesta_completa

        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                if intento < reintentos - 1:
                    espera = (intento + 1) * 3
                    print(f"\n⚠️  Modelo saturado. Reintentando en {espera}s...\n")
                    await asyncio.sleep(espera)
                    continue
                else:
                    return "❌ El servicio de Gemini está saturado. Intenta más tarde o usa la prueba directa."
            else:
                return f"❌ Error: {error_msg}"

    return "❌ No se pudo completar la consulta."


# ========================================
# EJEMPLOS DE USO
# ========================================


async def ejemplos_interactivos():
    """Ejemplos de preguntas que el agente puede responder"""

    ejemplos = [
        {
            "titulo": "📊 Estadísticas generales",
            "pregunta": "¿Cuántas especies y observaciones hay registradas en Colombia?",
        },
        {
            "titulo": "🦜 Información de especie",
            "pregunta": "Cuéntame sobre el Colibrí Chillón",
        },
        {
            "titulo": "🔎 Observaciones recientes",
            "pregunta": "Muéstrame las últimas observaciones de Tucanes en Colombia",
        },
    ]

    print("\n" + "=" * 70)
    print("🤖 AGENTE BIÓLOGO ACTIVO - Ejemplos de uso")
    print("=" * 70)
    print("\nEl agente elegirá automáticamente la herramienta correcta\n")

    for i, ejemplo in enumerate(ejemplos, 1):
        print("\n" + "-" * 70)
        print(f"\n{ejemplo['titulo']}")
        print(f"Pregunta: \"{ejemplo['pregunta']}\"")
        print("\nRespuesta del agente:")
        print("-" * 70)

        respuesta = await preguntar_a_agente(ejemplo["pregunta"])
        print(f"\n{respuesta}\n")

        if i < len(ejemplos):
            print("⏳ Esperando 3 segundos antes de la siguiente pregunta...\n")
            await asyncio.sleep(3)


async def modo_conversacion():
    """Modo de conversación interactiva"""
    print("\n" + "=" * 70)
    print("💬 MODO CONVERSACIÓN CON EL BIÓLOGO")
    print("=" * 70)
    print("\nHaz preguntas sobre biodiversidad colombiana")
    print("El agente usará las herramientas automáticamente")
    print("Escribe 'salir' para terminar\n")

    while True:
        try:
            pregunta = input("\n🌿 Tu pregunta: ").strip()

            if pregunta.lower() in ["salir", "exit", "quit"]:
                print(
                    "\n👋 ¡Hasta luego! Gracias por explorar la biodiversidad colombiana.\n"
                )
                break

            if not pregunta:
                continue

            print("\n🤖 Biólogo está pensando y usando herramientas...\n")
            respuesta = await preguntar_a_agente(pregunta)
            print(f"\n{respuesta}\n")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!\n")
            break


# ========================================
# MAIN
# ========================================


async def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("🌿 Sistema de Agentes - BIÓLOGO ACTIVO (Sin Warnings)")
    print("=" * 70)

    print("\n📋 Inicializando agente biólogo...")
    await inicializar_sesiones()
    print("✅ ¡Agente listo!\n")

    # Elegir modo
    print("Selecciona un modo:\n")
    print("1. Ejemplos automáticos (3 preguntas predefinidas)")
    print("2. Conversación interactiva (haz tus propias preguntas)")

    try:
        opcion = input("\nOpción (1 o 2): ").strip()

        if opcion == "1":
            await ejemplos_interactivos()
        elif opcion == "2":
            await modo_conversacion()
        else:
            print("\n⚠️  Opción no válida. Ejecutando ejemplos automáticos...\n")
            await ejemplos_interactivos()

    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!\n")

    print("\n" + "=" * 70)
    print("✅ Sesión finalizada")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
