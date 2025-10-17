#!/usr/bin/env python3
"""
Cliente MCP Básico - Ejercicio 1
=================================

Este es el ejemplo MÁS SIMPLE posible de un cliente MCP usando FastMCP.
Perfecto para entender cómo consumir servicios MCP sin complicaciones.

Autor: Ejercicios MCP
Versión: 1.0.0
"""

from fastmcp import FastMCP

# Crear instancia del cliente MCP
cliente = FastMCP(name="My First MCP Client")

def probar_herramientas():
    """Prueba las herramientas del servidor MCP de manera simple."""
    
    print("🚀 Probando cliente MCP básico")
    print("=" * 40)
    
    # En un caso real, aquí te conectarías al servidor
    # Para este ejemplo, simularemos las herramientas directamente
    
    print("\n📋 Herramientas disponibles en el servidor:")
    print("   • suma(a, b) - Suma dos números")
    print("   • multiplicacion(a, b) - Multiplica dos números")
    print("   • saludo(nombre) - Saludo personalizado")
    
    print("\n🔧 Probando herramientas:")
    
    # Simular llamadas a herramientas del servidor
    print("\n   1️⃣ Probando suma: 5 + 3")
    resultado_suma = 5 + 3  # En realidad sería: cliente.call_tool("suma", {"a": 5, "b": 3})
    print(f"      📊 Resultado: {resultado_suma}")
    
    print("\n   2️⃣ Probando multiplicación: 4 × 7")
    resultado_mult = 4 * 7  # En realidad sería: cliente.call_tool("multiplicacion", {"a": 4, "b": 7})
    print(f"      📊 Resultado: {resultado_mult}")
    
    print("\n   3️⃣ Probando saludo:")
    saludo = "¡Hola Juan! Bienvenido al servidor MCP."  # En realidad sería: cliente.call_tool("saludo", {"nombre": "Juan"})
    print(f"      📊 Resultado: {saludo}")
    
    print("\n✅ Pruebas completadas exitosamente!")
    print("\n💡 Para probar con un servidor real:")
    print("   1. Ejecuta el servidor: cd ejercicio-2-servidor && python servidor_basico.py")
    print("   2. En otra terminal, ejecuta este cliente")
    print("   3. El cliente se conectará al servidor y podrá usar las herramientas")

if __name__ == "__main__":
    probar_herramientas()
