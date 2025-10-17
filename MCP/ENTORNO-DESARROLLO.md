# 🛠️ Guía de Entorno de Desarrollo MCP

Esta guía te ayudará a configurar y mantener un entorno de desarrollo profesional para trabajar con los ejercicios MCP.

## 🚀 Configuración Inicial

### Opción 1: Configuración Automática (Recomendada)

```bash
# Ejecutar script de configuración
./setup-desarrollo.sh
```

Este script automáticamente:
- ✅ Verifica que Python 3.8+ esté instalado
- 📦 Crea entorno virtual en `./venv`
- 🔧 Instala todas las dependencias necesarias
- 📚 Configura ambos ejercicios

### Opción 2: Configuración Manual

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate     # Windows

# 3. Actualizar pip
pip install --upgrade pip

# 4. Instalar dependencias principales
pip install fastmcp pydantic uvicorn aiohttp

# 5. Instalar dependencias de desarrollo
pip install pytest black flake8 mypy

# 6. Instalar dependencias de cada ejercicio
cd ejercicio-1-cliente && pip install -r requirements.txt && cd ..
cd ejercicio-2-servidor && pip install -r requirements.txt && cd ..
```

## 📦 Gestión de Dependencias

### Estructura de Dependencias

```
📦 Dependencias del Proyecto
├── 🎯 Producción
│   ├── fastmcp>=0.1.0          # Framework MCP principal
│   ├── pydantic>=2.0.0         # Validación de datos
│   ├── uvicorn>=0.24.0         # Servidor ASGI
│   └── aiohttp>=3.8.0          # Cliente HTTP asíncrono
├── 🧪 Desarrollo
│   ├── pytest>=7.0.0           # Testing
│   ├── black>=23.11.0          # Formateo de código
│   ├── flake8>=6.1.0           # Linting
│   └── mypy>=1.7.1             # Verificación de tipos
└── 📚 Documentación
    ├── sphinx>=5.0.0           # Generación de docs
    └── sphinx-rtd-theme>=1.2.0 # Tema de documentación
```

### Comandos de Gestión

```bash
# Ver dependencias instaladas
pip list

# Ver dependencias de un ejercicio específico
pip list | grep fastmcp

# Actualizar todas las dependencias
pip install --upgrade -r ejercicio-1-cliente/requirements.txt
pip install --upgrade -r ejercicio-2-servidor/requirements.txt

# Crear requirements.txt actualizado
pip freeze > requirements-actual.txt
```

## 🔧 Herramientas de Desarrollo

### Formateo de Código

```bash
# Formatear código con Black
black ejercicio-1-cliente/
black ejercicio-2-servidor/

# Verificar formato sin modificar
black --check ejercicio-1-cliente/
```

### Análisis de Código

```bash
# Verificar estilo con Flake8
flake8 ejercicio-1-cliente/
flake8 ejercicio-2-servidor/

# Verificar tipos con MyPy
mypy ejercicio-1-cliente/cliente_mcp.py
mypy ejercicio-2-servidor/servidor_mcp.py
```

### Testing

```bash
# Ejecutar tests (cuando los implementes)
pytest tests/

# Ejecutar tests con cobertura
pytest --cov=ejercicio_1_cliente tests/
```

## 🌍 Gestión de Entornos Virtuales

### Activación/Desactivación

```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que está activo (debería mostrar la ruta del venv)
which python

# Desactivar entorno virtual
deactivate
```

### Comandos Útiles

```bash
# Ver ubicación del entorno virtual
echo $VIRTUAL_ENV

# Ver versión de Python del entorno
python --version

# Ver paquetes instalados en el entorno
pip list

# Crear requirements.txt del entorno actual
pip freeze > requirements-actual.txt
```

## 🐛 Debugging y Troubleshooting

### Problemas Comunes

#### Error: "command not found: python3"
```bash
# Verificar instalación de Python
which python3
python3 --version

# Si no está instalado, instalar con Homebrew (macOS)
brew install python3

# O descargar desde python.org
```

#### Error: "No module named 'fastmcp'"
```bash
# Verificar que el entorno virtual esté activo
echo $VIRTUAL_ENV

# Si no está activo, activarlo
source venv/bin/activate

# Reinstalar fastmcp
pip install fastmcp
```

#### Error: "Permission denied: ./setup-desarrollo.sh"
```bash
# Dar permisos de ejecución
chmod +x setup-desarrollo.sh

# Ejecutar el script
./setup-desarrollo.sh
```

### Logs y Debugging

```bash
# Ejecutar con logs detallados
python -v ejercicio-1-cliente/cliente_mcp.py

# Ver logs del servidor
python ejercicio-2-servidor/servidor_mcp.py 2>&1 | tee server.log

# Verificar conectividad
python -c "
import asyncio
import aiohttp
async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000') as response:
            print(f'Status: {response.status}')
asyncio.run(test())
"
```

## 🔄 Flujo de Trabajo Diario

### Al comenzar a trabajar

```bash
# 1. Navegar al directorio del proyecto
cd /ruta/a/ejercicios-orquestacion/MCP

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Verificar que todo funciona
python -c "import fastmcp; print('✅ FastMCP listo')"

# 4. Ejecutar tests rápidos (si existen)
pytest tests/ -v
```

### Durante el desarrollo

```bash
# Formatear código antes de commit
black ejercicio-1-cliente/ ejercicio-2-servidor/

# Verificar estilo
flake8 ejercicio-1-cliente/ ejercicio-2-servidor/

# Probar cambios
python ejercicio-1-cliente/cliente_mcp.py
```

### Al finalizar el trabajo

```bash
# Desactivar entorno virtual
deactivate

# Hacer commit de cambios
git add .
git commit -m "feat: agregar nueva funcionalidad MCP"
```

## 📊 Monitoreo y Performance

### Verificar Estado del Entorno

```bash
# Script de verificación completa
cat > verificar-entorno.sh << 'EOF'
#!/bin/bash
echo "🔍 Verificando entorno de desarrollo MCP..."
echo "============================================"

# Verificar Python
echo "Python: $(python --version)"
echo "Ubicación: $(which python)"

# Verificar entorno virtual
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Entorno virtual activo: $VIRTUAL_ENV"
else
    echo "❌ Entorno virtual no activo"
fi

# Verificar dependencias principales
echo ""
echo "📦 Dependencias principales:"
python -c "import fastmcp; print('✅ FastMCP:', fastmcp.__version__)" 2>/dev/null || echo "❌ FastMCP no instalado"
python -c "import pydantic; print('✅ Pydantic:', pydantic.VERSION)" 2>/dev/null || echo "❌ Pydantic no instalado"
python -c "import uvicorn; print('✅ Uvicorn:', uvicorn.__version__)" 2>/dev/null || echo "❌ Uvicorn no instalado"

# Verificar ejercicios
echo ""
echo "🎯 Estado de ejercicios:"
[ -f "ejercicio-1-cliente/cliente_mcp.py" ] && echo "✅ Ejercicio 1 (Cliente): Listo" || echo "❌ Ejercicio 1 (Cliente): Faltante"
[ -f "ejercicio-2-servidor/servidor_mcp.py" ] && echo "✅ Ejercicio 2 (Servidor): Listo" || echo "❌ Ejercicio 2 (Servidor): Faltante"

echo ""
echo "🎉 Verificación completada!"
EOF

chmod +x verificar-entorno.sh
./verificar-entorno.sh
```

## 🚀 Optimizaciones

### Configuración de VS Code

Crear `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

### Configuración de PyCharm

1. **File → Settings → Project → Python Interpreter**
2. **Add Interpreter → Existing Environment**
3. **Seleccionar**: `./venv/bin/python`
4. **Apply**

### Configuración de Jupyter

```bash
# Instalar kernel de Jupyter para el entorno virtual
pip install ipykernel
python -m ipykernel install --user --name=mcp-ejercicios --display-name="MCP Ejercicios"
```

## 📚 Recursos Adicionales

- [Documentación oficial de Python venv](https://docs.python.org/3/library/venv.html)
- [Guía de pip](https://pip.pypa.io/en/stable/user_guide/)
- [Black - Formateador de código](https://black.readthedocs.io/)
- [Flake8 - Linter](https://flake8.pycqa.org/)
- [MyPy - Verificador de tipos](https://mypy.readthedocs.io/)

---

¡Con esta configuración tendrás un entorno de desarrollo profesional para trabajar con MCP! 🎉
