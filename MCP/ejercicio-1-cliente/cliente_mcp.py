#!/usr/bin/env python3
"""
Cliente MCP Simple - Ejercicio 1
================================

Este es un ejemplo básico de un cliente MCP que se conecta a un servidor
y realiza peticiones simples. Este código está diseñado para ser educativo
y mostrar los conceptos fundamentales del protocolo MCP.

Autor: Ejercicios MCP
Versión: 1.0.0
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional

# Importamos las clases necesarias de fastmcp
from fastmcp import FastMCP

# Configuramos el logging para ver qué está pasando
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClienteMCPSimple:
    """
    Cliente MCP simple que demuestra cómo conectarse a un servidor
    y realizar operaciones básicas.
    """
    
    def __init__(self, servidor_url: str = "http://localhost:8000"):
        """
        Inicializa el cliente MCP.
        
        Args:
            servidor_url: URL del servidor MCP al que conectarse
        """
        self.servidor_url = servidor_url
        self.cliente = None
        self.conectado = False
        
        logger.info(f"Cliente MCP inicializado para servidor: {servidor_url}")
    
    async def conectar(self) -> bool:
        """
        Establece la conexión con el servidor MCP.
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            logger.info("Iniciando conexión con servidor MCP...")
            
            # Crear instancia del cliente FastMCP
            # FastMCP maneja automáticamente el protocolo MCP
            self.cliente = FastMCP()
            
            # En un caso real, aquí harías la conexión al servidor
            # Para este ejemplo, simularemos una conexión exitosa
            await asyncio.sleep(0.1)  # Simular tiempo de conexión
            
            self.conectado = True
            logger.info("✅ Conexión establecida exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al conectar: {e}")
            self.conectado = False
            return False
    
    async def listar_herramientas(self) -> Optional[Dict[str, Any]]:
        """
        Solicita al servidor la lista de herramientas disponibles.
        
        Returns:
            Dict con las herramientas disponibles o None si hay error
        """
        if not self.conectado:
            logger.error("No hay conexión activa con el servidor")
            return None
        
        try:
            logger.info("📋 Solicitando lista de herramientas...")
            
            # En un caso real, usarías self.cliente.list_tools()
            # Para este ejemplo, simularemos una respuesta
            herramientas_simuladas = {
                "tools": [
                    {
                        "name": "sumar",
                        "description": "Suma dos números enteros",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "number", "description": "Primer número"},
                                "b": {"type": "number", "description": "Segundo número"}
                            },
                            "required": ["a", "b"]
                        }
                    },
                    {
                        "name": "multiplicar",
                        "description": "Multiplica dos números enteros",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "a": {"type": "number", "description": "Primer número"},
                                "b": {"type": "number", "description": "Segundo número"}
                            },
                            "required": ["a", "b"]
                        }
                    }
                ]
            }
            
            logger.info(f"✅ Herramientas disponibles: {len(herramientas_simuladas['tools'])}")
            return herramientas_simuladas
            
        except Exception as e:
            logger.error(f"❌ Error al listar herramientas: {e}")
            return None
    
    async def ejecutar_herramienta(self, nombre: str, parametros: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Ejecuta una herramienta específica con los parámetros dados.
        
        Args:
            nombre: Nombre de la herramienta a ejecutar
            parametros: Parámetros para la herramienta
            
        Returns:
            Resultado de la ejecución o None si hay error
        """
        if not self.conectado:
            logger.error("No hay conexión activa con el servidor")
            return None
        
        try:
            logger.info(f"🔧 Ejecutando herramienta '{nombre}' con parámetros: {parametros}")
            
            # En un caso real, usarías self.cliente.call_tool(nombre, parametros)
            # Para este ejemplo, simularemos la ejecución
            resultado_simulado = None
            
            if nombre == "sumar":
                a = parametros.get("a", 0)
                b = parametros.get("b", 0)
                resultado = a + b
                resultado_simulado = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"El resultado de {a} + {b} = {resultado}"
                        }
                    ]
                }
            elif nombre == "multiplicar":
                a = parametros.get("a", 0)
                b = parametros.get("b", 0)
                resultado = a * b
                resultado_simulado = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"El resultado de {a} × {b} = {resultado}"
                        }
                    ]
                }
            else:
                raise ValueError(f"Herramienta '{nombre}' no encontrada")
            
            logger.info("✅ Herramienta ejecutada exitosamente")
            return resultado_simulado
            
        except Exception as e:
            logger.error(f"❌ Error al ejecutar herramienta: {e}")
            return None
    
    async def desconectar(self):
        """
        Cierra la conexión con el servidor MCP.
        """
        if self.conectado:
            logger.info("🔌 Desconectando del servidor MCP...")
            self.conectado = False
            logger.info("✅ Desconexión completada")


async def demostracion_cliente():
    """
    Función principal que demuestra el uso del cliente MCP.
    Esta función muestra el flujo completo de uso del cliente.
    """
    print("🚀 Iniciando demostración del Cliente MCP Simple")
    print("=" * 50)
    
    # Crear instancia del cliente
    cliente = ClienteMCPSimple()
    
    try:
        # Paso 1: Conectar al servidor
        print("\n1️⃣ Conectando al servidor MCP...")
        conexion_exitosa = await cliente.conectar()
        
        if not conexion_exitosa:
            print("❌ No se pudo conectar al servidor. Saliendo...")
            return
        
        # Paso 2: Listar herramientas disponibles
        print("\n2️⃣ Obteniendo herramientas disponibles...")
        herramientas = await cliente.listar_herramientas()
        
        if herramientas:
            print(f"📋 Herramientas encontradas: {len(herramientas['tools'])}")
            for tool in herramientas['tools']:
                print(f"   • {tool['name']}: {tool['description']}")
        
        # Paso 3: Ejecutar algunas herramientas
        print("\n3️⃣ Ejecutando herramientas...")
        
        # Ejecutar suma
        print("\n   🔧 Ejecutando suma: 15 + 27")
        resultado_suma = await cliente.ejecutar_herramienta("sumar", {"a": 15, "b": 27})
        if resultado_suma:
            print(f"   📊 Resultado: {resultado_suma['content'][0]['text']}")
        
        # Ejecutar multiplicación
        print("\n   🔧 Ejecutando multiplicación: 8 × 7")
        resultado_mult = await cliente.ejecutar_herramienta("multiplicar", {"a": 8, "b": 7})
        if resultado_mult:
            print(f"   📊 Resultado: {resultado_mult['content'][0]['text']}")
        
        # Paso 4: Intentar ejecutar herramienta inexistente
        print("\n   🔧 Intentando ejecutar herramienta inexistente...")
        resultado_error = await cliente.ejecutar_herramienta("dividir", {"a": 10, "b": 2})
        if resultado_error is None:
            print("   ❌ Como era de esperar, la herramienta no existe")
        
        print("\n✅ Demostración completada exitosamente!")
        
    except KeyboardInterrupt:
        print("\n⚠️ Demostración interrumpida por el usuario")
        
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")
        
    finally:
        # Siempre desconectar al final
        await cliente.desconectar()
        print("\n🔌 Cliente desconectado")


def main():
    """
    Función de entrada principal.
    """
    print("Cliente MCP Simple - Ejercicio 1")
    print("Este ejercicio demuestra cómo crear un cliente MCP básico")
    print()
    
    # Ejecutar la demostración
    try:
        asyncio.run(demostracion_cliente())
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")


if __name__ == "__main__":
    main()
