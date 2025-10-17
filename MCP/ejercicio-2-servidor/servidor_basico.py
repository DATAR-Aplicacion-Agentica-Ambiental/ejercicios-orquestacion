#!/usr/bin/env python3
"""
Servidor MCP Básico - Ejercicio 2
=================================

Este es el ejemplo MÁS SIMPLE posible de un servidor MCP usando FastMCP.
Perfecto para entender los conceptos fundamentales sin complicaciones.

Autor: Ejercicios MCP
Versión: 1.0.0
"""

from fastmcp import FastMCP

# Crear instancia del servidor MCP
mcp = FastMCP(name="My First MCP Server")

@mcp.tool
def suma(a: int, b: int) -> int:
    """Devuelve la suma de dos números."""
    return a + b

@mcp.tool
def multiplicacion(a: int, b: int) -> int:
    """Devuelve la multiplicación de dos números."""
    return a * b

@mcp.tool
def saludo(nombre: str) -> str:
    """Devuelve un saludo personalizado."""
    return f"¡Hola {nombre}! Bienvenido al servidor MCP."

if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP básico...")
    print("📋 Herramientas disponibles:")
    print("   • suma(a, b) - Suma dos números")
    print("   • multiplicacion(a, b) - Multiplica dos números") 
    print("   • saludo(nombre) - Saludo personalizado")
    print("💡 Servidor MCP ejecutándose en modo stdio")
    print("🛑 Presiona Ctrl+C para detener")
    mcp.run()
