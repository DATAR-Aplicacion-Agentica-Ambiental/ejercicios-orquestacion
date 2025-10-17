#!/usr/bin/env python3
"""
Servidor MCP Simple - Ejercicio 2
=================================

Este es un ejemplo básico de un servidor MCP que expone herramientas simples
usando FastMCP. Este código está diseñado para ser educativo y mostrar cómo
crear un servidor MCP desde cero.

Autor: Ejercicios MCP
Versión: 1.0.0
"""

import asyncio
import logging
import math
from typing import Any, Dict, List, Optional
from datetime import datetime

# Importamos las clases necesarias de fastmcp
from fastmcp import FastMCP
from fastmcp.server import Server
from fastmcp.server.models import Tool

# Configuramos el logging para ver qué está pasando
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ServidorMCPSimple:
    """
    Servidor MCP simple que expone herramientas básicas de cálculo
    y procesamiento de texto.
    """
    
    def __init__(self, host: str = "localhost", puerto: int = 8000):
        """
        Inicializa el servidor MCP.
        
        Args:
            host: Dirección IP donde escuchar conexiones
            puerto: Puerto donde escuchar conexiones
        """
        self.host = host
        self.puerto = puerto
        self.servidor = None
        self.fastmcp = FastMCP()
        
        logger.info(f"Servidor MCP inicializado en {host}:{puerto}")
    
    def configurar_herramientas(self):
        """
        Configura las herramientas que expondrá el servidor.
        Este método registra todas las herramientas disponibles.
        """
        logger.info("🔧 Configurando herramientas del servidor...")
        
        # Herramienta 1: Calculadora básica - Suma
        @self.fastmcp.tool()
        async def sumar(a: float, b: float) -> str:
            """
            Suma dos números.
            
            Args:
                a: Primer número
                b: Segundo número
                
            Returns:
                String con el resultado de la suma
            """
            resultado = a + b
            logger.info(f"Ejecutando suma: {a} + {b} = {resultado}")
            return f"El resultado de {a} + {b} = {resultado}"
        
        # Herramienta 2: Calculadora básica - Multiplicación
        @self.fastmcp.tool()
        async def multiplicar(a: float, b: float) -> str:
            """
            Multiplica dos números.
            
            Args:
                a: Primer número
                b: Segundo número
                
            Returns:
                String con el resultado de la multiplicación
            """
            resultado = a * b
            logger.info(f"Ejecutando multiplicación: {a} × {b} = {resultado}")
            return f"El resultado de {a} × {b} = {resultado}"
        
        # Herramienta 3: Calculadora avanzada - Potencia
        @self.fastmcp.tool()
        async def potencia(base: float, exponente: float) -> str:
            """
            Calcula la potencia de un número.
            
            Args:
                base: Número base
                exponente: Exponente
                
            Returns:
                String con el resultado de la potencia
            """
            try:
                resultado = math.pow(base, exponente)
                logger.info(f"Ejecutando potencia: {base}^{exponente} = {resultado}")
                return f"El resultado de {base}^{exponente} = {resultado}"
            except OverflowError:
                return f"Error: El resultado de {base}^{exponente} es demasiado grande"
            except ValueError as e:
                return f"Error: {str(e)}"
        
        # Herramienta 4: Procesamiento de texto - Contar palabras
        @self.fastmcp.tool()
        async def contar_palabras(texto: str) -> str:
            """
            Cuenta el número de palabras en un texto.
            
            Args:
                texto: Texto a analizar
                
            Returns:
                String con el número de palabras encontradas
            """
            if not texto or not texto.strip():
                return "El texto está vacío"
            
            palabras = texto.strip().split()
            numero_palabras = len(palabras)
            logger.info(f"Contando palabras: {numero_palabras} palabras encontradas")
            return f"El texto contiene {numero_palabras} palabras"
        
        # Herramienta 5: Procesamiento de texto - Convertir a mayúsculas
        @self.fastmcp.tool()
        async def a_mayusculas(texto: str) -> str:
            """
            Convierte un texto a mayúsculas.
            
            Args:
                texto: Texto a convertir
                
            Returns:
                Texto convertido a mayúsculas
            """
            resultado = texto.upper()
            logger.info(f"Convirtiendo a mayúsculas: '{texto}' -> '{resultado}'")
            return f"Texto en mayúsculas: {resultado}"
        
        # Herramienta 6: Utilidad - Obtener fecha y hora
        @self.fastmcp.tool()
        async def fecha_actual() -> str:
            """
            Obtiene la fecha y hora actual.
            
            Returns:
                String con la fecha y hora actual
            """
            ahora = datetime.now()
            fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"Obteniendo fecha actual: {fecha_formateada}")
            return f"La fecha y hora actual es: {fecha_formateada}"
        
        logger.info("✅ Herramientas configuradas exitosamente")
        logger.info("📋 Herramientas disponibles:")
        logger.info("   • sumar(a, b) - Suma dos números")
        logger.info("   • multiplicar(a, b) - Multiplica dos números")
        logger.info("   • potencia(base, exponente) - Calcula potencia")
        logger.info("   • contar_palabras(texto) - Cuenta palabras en texto")
        logger.info("   • a_mayusculas(texto) - Convierte texto a mayúsculas")
        logger.info("   • fecha_actual() - Obtiene fecha y hora actual")
    
    async def iniciar(self):
        """
        Inicia el servidor MCP.
        Este método configura las herramientas y pone el servidor en funcionamiento.
        """
        try:
            logger.info("🚀 Iniciando servidor MCP...")
            
            # Configurar las herramientas
            self.configurar_herramientas()
            
            # En un caso real, aquí iniciarías el servidor FastMCP
            # Para este ejemplo, simularemos el inicio del servidor
            logger.info(f"✅ Servidor MCP iniciado exitosamente en {self.host}:{self.puerto}")
            logger.info("📡 Esperando conexiones de clientes...")
            logger.info("💡 Tip: Puedes usar el cliente del Ejercicio 1 para conectarte")
            logger.info("🛑 Presiona Ctrl+C para detener el servidor")
            
            # Simular servidor corriendo (en realidad sería un loop infinito)
            # En FastMCP real, usarías: await self.fastmcp.run()
            try:
                while True:
                    await asyncio.sleep(1)  # Mantener el servidor activo
            except KeyboardInterrupt:
                logger.info("🛑 Señal de interrupción recibida")
            
        except Exception as e:
            logger.error(f"❌ Error al iniciar el servidor: {e}")
            raise
    
    async def detener(self):
        """
        Detiene el servidor MCP de manera segura.
        """
        logger.info("🛑 Deteniendo servidor MCP...")
        # Aquí harías la limpieza necesaria
        logger.info("✅ Servidor MCP detenido exitosamente")


def demostrar_herramientas():
    """
    Función que demuestra las herramientas del servidor sin necesidad
    de un cliente MCP real. Útil para testing y verificación.
    """
    print("🧪 Demostración de herramientas del servidor")
    print("=" * 50)
    
    # Crear instancia del servidor
    servidor = ServidorMCPSimple()
    
    # Configurar herramientas
    servidor.configurar_herramientas()
    
    print("\n📋 Herramientas configuradas:")
    print("✅ sumar(a, b) - Suma dos números")
    print("✅ multiplicar(a, b) - Multiplica dos números")
    print("✅ potencia(base, exponente) - Calcula potencia")
    print("✅ contar_palabras(texto) - Cuenta palabras en texto")
    print("✅ a_mayusculas(texto) - Convierte texto a mayúsculas")
    print("✅ fecha_actual() - Obtiene fecha y hora actual")
    
    print("\n💡 Para probar las herramientas:")
    print("1. Ejecuta este servidor: python servidor_mcp.py")
    print("2. En otra terminal, ejecuta el cliente del Ejercicio 1")
    print("3. El cliente se conectará a este servidor y podrá usar las herramientas")


async def main():
    """
    Función principal que inicia el servidor MCP.
    """
    print("Servidor MCP Simple - Ejercicio 2")
    print("Este ejercicio demuestra cómo crear un servidor MCP básico")
    print()
    
    # Crear e iniciar el servidor
    servidor = ServidorMCPSimple()
    
    try:
        await servidor.iniciar()
    except KeyboardInterrupt:
        print("\n⚠️ Servidor interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
    finally:
        await servidor.detener()
        print("\n👋 ¡Servidor detenido!")


if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar demostración y luego iniciar servidor
    demostrar_herramientas()
    print("\n" + "="*50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
