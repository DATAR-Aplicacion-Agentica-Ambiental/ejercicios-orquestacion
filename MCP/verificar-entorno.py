#!/usr/bin/env python3
"""
Script para verificar que los entornos virtuales tienen las dependencias correctas
"""

import sys
import subprocess

def verificar_fastmcp():
    """Verifica que FastMCP esté instalado y muestre la versión."""
    try:
        import fastmcp
        print(f"✅ FastMCP instalado: {fastmcp.__version__}")
        
        # Verificar si tiene Client
        try:
            from fastmcp import Client
            print("✅ Clase 'Client' disponible")
        except ImportError:
            print("❌ Clase 'Client' NO disponible")
            
        # Verificar si tiene FastMCP
        try:
            from fastmcp import FastMCP
            print("✅ Clase 'FastMCP' disponible")
        except ImportError:
            print("❌ Clase 'FastMCP' NO disponible")
            
    except ImportError:
        print("❌ FastMCP NO instalado")
        print("💡 Instala con: pip install fastmcp")

def verificar_python():
    """Verifica la versión de Python."""
    print(f"🐍 Python: {sys.version}")

def verificar_dependencias():
    """Verifica otras dependencias importantes."""
    try:
        import asyncio
        print("✅ asyncio disponible")
    except ImportError:
        print("❌ asyncio NO disponible")

def main():
    print("🔍 Verificando entorno MCP")
    print("=" * 40)
    
    verificar_python()
    print()
    verificar_fastmcp()
    print()
    verificar_dependencias()
    
    print("\n" + "=" * 40)
    print("💡 Si hay errores, ejecuta:")
    print("   pip install --upgrade fastmcp")

if __name__ == "__main__":
    main()
