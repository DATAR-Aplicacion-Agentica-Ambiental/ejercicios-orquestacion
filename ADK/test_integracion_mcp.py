"""
Script de prueba para verificar la integración MCP
Ejecuta pruebas simples sin necesidad del sistema completo de agentes
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json


async def probar_servidor_mcp():
    """Prueba la conexión y funcionalidad del servidor MCP"""

    print("\n" + "=" * 70)
    print("🧪 PRUEBAS DE INTEGRACIÓN MCP")
    print("=" * 70 + "\n")

    # Configurar parámetros del servidor
    server_params = StdioServerParameters(
        command="python", args=["servidor_mcp.py"], env=None
    )

    try:
        print("📡 Conectando al servidor MCP...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("✅ Conexión establecida\n")

                # Listar herramientas disponibles
                print("🔧 Herramientas disponibles:")
                tools = await session.list_tools()
                for i, tool in enumerate(tools.tools, 1):
                    print(f"  {i}. {tool.name}")
                    if hasattr(tool, "description"):
                        print(f"     {tool.description[:80]}...")
                print()

                # PRUEBA 1: Estadísticas de biodiversidad
                print("=" * 70)
                print("📊 PRUEBA 1: Estadísticas de Colombia")
                print("=" * 70)
                try:
                    result = await session.call_tool(
                        "estadisticas_biodiversidad_colombia", arguments={}
                    )
                    data = json.loads(result.content[0].text)

                    if "error" in data:
                        print(f"❌ Error: {data['error']}")
                    else:
                        print(
                            f"✅ Total de observaciones: {data.get('total_observaciones', 'N/A'):,}"
                        )
                        print(
                            f"✅ Total de especies: {data.get('total_especies', 'N/A'):,}"
                        )
                except Exception as e:
                    print(f"❌ Error en prueba 1: {str(e)}")
                print()

                # PRUEBA 2: Buscar especie
                print("=" * 70)
                print("🔍 PRUEBA 2: Buscar especie 'Colibrí'")
                print("=" * 70)
                try:
                    result = await session.call_tool(
                        "buscar_especies",
                        arguments={"nombre": "Colibrí", "is_active": True},
                    )
                    data = json.loads(result.content[0].text)

                    if "error" in data:
                        print(f"❌ Error: {data['error']}")
                    elif data.get("especies"):
                        print(f"✅ Encontradas {len(data['especies'])} especies:")
                        for i, esp in enumerate(data["especies"][:3], 1):
                            print(f"\n  {i}. {esp.get('nombre_cientifico', 'N/A')}")
                            if esp.get("nombre_comun"):
                                print(f"     Común: {esp['nombre_comun']}")
                            print(f"     Rango: {esp.get('rango', 'N/A')}")
                            print(
                                f"     Observaciones: {esp.get('observaciones_totales', 0):,}"
                            )
                    else:
                        print("⚠️  No se encontraron especies")
                except Exception as e:
                    print(f"❌ Error en prueba 2: {str(e)}")
                print()

                # PRUEBA 3: Buscar observaciones
                print("=" * 70)
                print("🔎 PRUEBA 3: Observaciones de 'Oso de anteojos'")
                print("=" * 70)
                try:
                    result = await session.call_tool(
                        "buscar_observaciones",
                        arguments={"taxon_name": "Tremarctos ornatus", "per_page": 3},
                    )
                    data = json.loads(result.content[0].text)

                    if "error" in data:
                        print(f"❌ Error: {data['error']}")
                    elif data.get("observaciones"):
                        print(f"✅ Total encontradas: {data.get('total', 0):,}")
                        print(f"✅ Mostrando primeras {len(data['observaciones'])}:\n")
                        for i, obs in enumerate(data["observaciones"], 1):
                            print(f"  {i}. {obs.get('especie', 'No identificado')}")
                            print(f"     Lugar: {obs.get('lugar', 'N/A')}")
                            print(f"     Fecha: {obs.get('fecha_observacion', 'N/A')}")
                            print()
                    else:
                        print("⚠️  No se encontraron observaciones")
                except Exception as e:
                    print(f"❌ Error en prueba 3: {str(e)}")
                print()

                # PRUEBA 4: Lugares de Colombia
                print("=" * 70)
                print("📍 PRUEBA 4: Lugares en Colombia")
                print("=" * 70)
                try:
                    result = await session.call_tool(
                        "obtener_lugares_colombia", arguments={}
                    )
                    data = json.loads(result.content[0].text)

                    if "error" in data:
                        print(f"❌ Error: {data['error']}")
                    elif data.get("lugares"):
                        print(f"✅ Encontrados {len(data['lugares'])} lugares:")
                        for i, lugar in enumerate(data["lugares"][:5], 1):
                            print(f"\n  {i}. {lugar.get('nombre', 'N/A')}")
                            print(f"     ID: {lugar.get('id', 'N/A')}")
                            print(f"     Tipo: {lugar.get('tipo', 'N/A')}")
                            if lugar.get("observaciones"):
                                print(f"     Observaciones: {lugar['observaciones']:,}")
                    else:
                        print("⚠️  No se encontraron lugares")
                except Exception as e:
                    print(f"❌ Error en prueba 4: {str(e)}")
                print()

                print("=" * 70)
                print("✅ TODAS LAS PRUEBAS COMPLETADAS")
                print("=" * 70 + "\n")

    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo servidor_mcp.py")
        print("   Asegúrate de que esté en el mismo directorio.\n")
    except Exception as e:
        print(f"❌ Error al conectar con el servidor MCP: {str(e)}\n")


async def probar_funcion_herramienta():
    """Prueba directa de la función de herramienta sin el servidor completo"""

    print("\n" + "=" * 70)
    print("🧪 PRUEBA DIRECTA DE LA FUNCIÓN HERRAMIENTA")
    print("=" * 70 + "\n")

    # Importar la función desde el sistema de agentes
    import sys

    sys.path.append(".")

    try:
        from sistema_agentes_mejorado import consultar_biodiversidad_avanzada

        print("📊 Probando: estadisticas...")
        resultado = consultar_biodiversidad_avanzada("estadisticas")
        print(resultado)
        print()

        print("🔍 Probando: buscar_especie (Colibrí)...")
        resultado = consultar_biodiversidad_avanzada(
            "buscar_especie", nombre_especie="Colibrí", num_resultados=3
        )
        print(resultado)
        print()

    except ImportError as e:
        print(f"⚠️  No se pudo importar el sistema de agentes: {e}")
        print(
            "   Esta prueba requiere que sistema_agentes_mejorado.py esté disponible.\n"
        )
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")


async def main():
    """Ejecuta todas las pruebas"""

    print("\n" + "🌿" * 35)
    print("Sistema de Pruebas - Integración MCP")
    print("🌿" * 35)

    # Prueba 1: Servidor MCP directo
    await probar_servidor_mcp()

    # Prueba 2: Función herramienta (opcional)
    # await probar_funcion_herramienta()

    print("\n" + "=" * 70)
    print("🎉 Pruebas finalizadas")
    print("=" * 70 + "\n")

    print("💡 Si todas las pruebas pasaron, tu integración MCP está lista!")
    print("   Ahora puedes ejecutar: python sistema_agentes_mejorado.py\n")


if __name__ == "__main__":
    import warnings

    warnings.filterwarnings("ignore", category=ResourceWarning)
    asyncio.run(main())
