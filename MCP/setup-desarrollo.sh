#!/bin/bash
# setup-desarrollo.sh
# Script para configurar el entorno de desarrollo MCP

echo "🚀 Configurando entorno de desarrollo para ejercicios MCP"
echo "========================================================="

# Verificar que Python esté instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual principal
echo ""
echo "📦 Creando entorno virtual principal..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Entorno virtual creado en ./venv"
else
    echo "ℹ️  Entorno virtual ya existe"
fi

# Activar entorno virtual
echo ""
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo ""
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias generales
echo ""
echo "📚 Instalando dependencias generales..."
pip install fastmcp

# Configurar entorno para ejercicio 1 (Cliente)
echo ""
echo "🔧 Configurando ejercicio 1 (Cliente)..."
cd ejercicio-1-cliente
pip install -r requirements.txt
cd ..

# Configurar entorno para ejercicio 2 (Servidor)
echo ""
echo "🔧 Configurando ejercicio 2 (Servidor)..."
cd ejercicio-2-servidor
pip install -r requirements.txt
cd ..

echo ""
echo "🎉 ¡Configuración completada exitosamente!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Para activar el entorno: source venv/bin/activate"
echo "2. Ejecutar ejercicio 1: cd ejercicio-1-cliente && python cliente_mcp.py"
echo "3. Ejecutar ejercicio 2: cd ejercicio-2-servidor && python servidor_mcp.py"
echo ""
echo "💡 Tip: Siempre activa el entorno virtual antes de trabajar"
echo "   source venv/bin/activate"
