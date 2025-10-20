#!/usr/bin/env python3
"""
Cliente de prueba para el servidor MCP de Hola Mundo
Demuestra cómo interactuar con el servidor MCP.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any

class MCPCliente:
    """Cliente simple para probar el servidor MCP."""
    
    def __init__(self):
        self.proceso = None
    
    async def conectar(self):
        """Conecta al servidor MCP."""
        try:
            # Iniciar el servidor como subproceso
            self.proceso = await asyncio.create_subprocess_exec(
                sys.executable, "servidor_hola_mundo.py",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            print("✅ Conectado al servidor MCP")
            return True
        except Exception as e:
            print(f"❌ Error al conectar: {e}")
            return False
    
    async def enviar_mensaje(self, mensaje: Dict[str, Any]) -> Dict[str, Any]:
        """Envía un mensaje al servidor y recibe la respuesta."""
        if not self.proceso:
            return {"error": "No conectado al servidor"}
        
        try:
            # Enviar mensaje
            mensaje_json = json.dumps(mensaje) + "\n"
            self.proceso.stdin.write(mensaje_json.encode())
            await self.proceso.stdin.drain()
            
            # Leer respuesta
            respuesta_linea = await self.proceso.stdout.readline()
            if respuesta_linea:
                return json.loads(respuesta_linea.decode().strip())
            else:
                return {"error": "No se recibió respuesta"}
                
        except Exception as e:
            return {"error": f"Error en comunicación: {e}"}
    
    async def listar_herramientas(self):
        """Lista las herramientas disponibles."""
        print("\n🔧 Listando herramientas disponibles...")
        mensaje = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        respuesta = await self.enviar_mensaje(mensaje)
        if "result" in respuesta:
            herramientas = respuesta["result"].get("tools", [])
            print(f"📋 Encontradas {len(herramientas)} herramientas:")
            for herramienta in herramientas:
                print(f"  • {herramienta['name']}: {herramienta['description']}")
        else:
            print(f"❌ Error: {respuesta}")
    
    async def usar_herramienta(self, nombre: str, argumentos: Dict[str, Any]):
        """Usa una herramienta específica."""
        print(f"\n🛠️ Usando herramienta '{nombre}' con argumentos: {argumentos}")
        
        mensaje = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": nombre,
                "arguments": argumentos
            }
        }
        
        respuesta = await self.enviar_mensaje(mensaje)
        if "result" in respuesta:
            contenido = respuesta["result"].get("content", [])
            for item in contenido:
                if item.get("type") == "text":
                    print(f"📝 Resultado: {item['text']}")
        else:
            print(f"❌ Error: {respuesta}")
    
    async def cerrar(self):
        """Cierra la conexión."""
        if self.proceso:
            self.proceso.terminate()
            await self.proceso.wait()
            print("🔌 Conexión cerrada")

async def demo_completo():
    """Demostración completa del cliente MCP."""
    print("🚀 Iniciando demostración del cliente MCP...")
    
    cliente = MCPCliente()
    
    # Conectar
    if not await cliente.conectar():
        return
    
    try:
        # Listar herramientas
        await cliente.listar_herramientas()
        
        # Probar herramienta de saludo
        await cliente.usar_herramienta("saludar", {
            "nombre": "Juan",
            "idioma": "es"
        })
        
        # Probar herramienta de información
        await cliente.usar_herramienta("obtener_info", {})
        
        # Probar herramienta de cálculo
        await cliente.usar_herramienta("calcular", {
            "operacion": "suma",
            "a": 15,
            "b": 25
        })
        
        await cliente.usar_herramienta("calcular", {
            "operacion": "multiplicacion",
            "a": 7,
            "b": 8
        })
        
    finally:
        await cliente.cerrar()

if __name__ == "__main__":
    print("🎯 Cliente de prueba para servidor MCP de Hola Mundo")
    print("=" * 50)
    asyncio.run(demo_completo())
