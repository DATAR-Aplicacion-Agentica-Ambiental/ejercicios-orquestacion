#!/usr/bin/env python3
"""
Servidor MCP básico de "Hola mundo"
Demuestra las funcionalidades básicas de un servidor MCP.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Crear instancia del servidor
server = Server("hola-mundo-server")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """Lista las herramientas disponibles del servidor."""
    return [
        Tool(
            name="saludar",
            description="Saluda al usuario con un mensaje personalizado",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {
                        "type": "string",
                        "description": "Nombre de la persona a saludar"
                    },
                    "idioma": {
                        "type": "string",
                        "description": "Idioma del saludo (es, en, fr)",
                        "default": "es"
                    }
                },
                "required": ["nombre"]
            }
        ),
        Tool(
            name="obtener_info",
            description="Obtiene información básica del servidor",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="calcular",
            description="Realiza operaciones matemáticas básicas",
            inputSchema={
                "type": "object",
                "properties": {
                    "operacion": {
                        "type": "string",
                        "description": "Tipo de operación (suma, resta, multiplicacion, division)"
                    },
                    "a": {
                        "type": "number",
                        "description": "Primer número"
                    },
                    "b": {
                        "type": "number",
                        "description": "Segundo número"
                    }
                },
                "required": ["operacion", "a", "b"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Ejecuta las herramientas del servidor."""
    
    if name == "saludar":
        nombre = arguments.get("nombre", "Usuario")
        idioma = arguments.get("idioma", "es")
        
        saludos = {
            "es": f"¡Hola {nombre}! 👋 Bienvenido al servidor MCP de Hola Mundo.",
            "en": f"Hello {nombre}! 👋 Welcome to the MCP Hello World server.",
            "fr": f"Bonjour {nombre}! 👋 Bienvenue sur le serveur MCP Hello World."
        }
        
        mensaje = saludos.get(idioma, saludos["es"])
        return [TextContent(type="text", text=mensaje)]
    
    elif name == "obtener_info":
        info = {
            "servidor": "Hola Mundo MCP Server",
            "version": "1.0.0",
            "descripcion": "Servidor MCP básico para demostrar funcionalidades",
            "herramientas_disponibles": ["saludar", "obtener_info", "calcular"],
            "estado": "activo"
        }
        
        return [TextContent(
            type="text", 
            text=f"📊 **Información del Servidor**\n\n" +
                 f"**Nombre:** {info['servidor']}\n" +
                 f"**Versión:** {info['version']}\n" +
                 f"**Descripción:** {info['descripcion']}\n" +
                 f"**Estado:** {info['estado']}\n" +
                 f"**Herramientas:** {', '.join(info['herramientas_disponibles'])}"
        )]
    
    elif name == "calcular":
        operacion = arguments.get("operacion")
        a = arguments.get("a", 0)
        b = arguments.get("b", 0)
        
        try:
            if operacion == "suma":
                resultado = a + b
                simbolo = "+"
            elif operacion == "resta":
                resultado = a - b
                simbolo = "-"
            elif operacion == "multiplicacion":
                resultado = a * b
                simbolo = "×"
            elif operacion == "division":
                if b == 0:
                    return [TextContent(type="text", text="❌ Error: No se puede dividir por cero")]
                resultado = a / b
                simbolo = "÷"
            else:
                return [TextContent(type="text", text="❌ Error: Operación no válida")]
            
            return [TextContent(
                type="text", 
                text=f"🧮 **Resultado:** {a} {simbolo} {b} = {resultado}"
            )]
            
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error en el cálculo: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"❌ Herramienta '{name}' no encontrada")]

async def main():
    """Función principal que inicia el servidor."""
    print("🚀 Iniciando servidor MCP de Hola Mundo...", file=sys.stderr)
    
    # Configurar el servidor
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="hola-mundo-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    import sys
    asyncio.run(main())
