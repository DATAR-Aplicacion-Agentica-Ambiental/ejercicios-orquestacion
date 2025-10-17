# Ejercicio 1: Cliente MCP Simple

Este ejercicio te enseña cómo crear un **cliente MCP básico** que se conecta a un servidor y realiza peticiones simples. Es el punto de partida perfecto para entender cómo funciona el protocolo MCP desde la perspectiva del consumidor.

## ¿Qué es un Cliente MCP?

Un **cliente MCP** es una aplicación que se conecta a servidores MCP para acceder a sus herramientas, recursos y capacidades. Piensa en él como un "consumidor" que solicita servicios de un "proveedor" (el servidor).

### Funciones principales de un cliente:
- 🔌 **Conectar** a servidores MCP
- 📋 **Descubrir** herramientas y recursos disponibles
- 🔧 **Ejecutar** herramientas remotas
- 📊 **Procesar** respuestas del servidor
- ❌ **Manejar** errores de comunicación

## Estructura del Código

El archivo `cliente_mcp.py` contiene una clase `ClienteMCPSimple` que demuestra todos estos conceptos:

```python
class ClienteMCPSimple:
    def __init__(self, servidor_url)      # Inicialización
    async def conectar(self)              # Establecer conexión
    async def listar_herramientas(self)   # Descubrir herramientas
    async def ejecutar_herramienta(self)  # Ejecutar herramientas
    async def desconectar(self)           # Cerrar conexión
```

## Cómo Ejecutar el Ejercicio

### 1. Preparar el entorno

```bash
# Asegúrate de estar en el directorio del ejercicio
cd ejercicio-1-cliente

# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar el cliente

```bash
python cliente_mcp.py
```

### 3. Salida esperada

```
🚀 Iniciando demostración del Cliente MCP Simple
==================================================

1️⃣ Conectando al servidor MCP...
✅ Conexión establecida exitosamente

2️⃣ Obteniendo herramientas disponibles...
📋 Herramientas encontradas: 2
   • sumar: Suma dos números enteros
   • multiplicar: Multiplica dos números enteros

3️⃣ Ejecutando herramientas...

   🔧 Ejecutando suma: 15 + 27
   📊 Resultado: El resultado de 15 + 27 = 42

   🔧 Ejecutando multiplicación: 8 × 7
   📊 Resultado: El resultado de 8 × 7 = 56

   🔧 Intentando ejecutar herramienta inexistente...
   ❌ Como era de esperar, la herramienta no existe

✅ Demostración completada exitosamente!

🔌 Cliente desconectado
```

## Explicación Línea por Línea

### Importaciones y Configuración

```python
import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastmcp import FastMCP
```

- `asyncio`: Para programación asíncrona (operaciones no bloqueantes)
- `json`: Para manejar datos en formato JSON (estándar MCP)
- `logging`: Para registrar información durante la ejecución
- `typing`: Para especificar tipos de datos (mejores prácticas)
- `fastmcp`: Framework que simplifica el trabajo con MCP

### Clase ClienteMCPSimple

```python
def __init__(self, servidor_url: str = "http://localhost:8000"):
    self.servidor_url = servidor_url
    self.cliente = None
    self.conectado = False
```

**Línea por línea:**
- `servidor_url`: URL del servidor MCP (por defecto localhost:8000)
- `self.cliente`: Instancia de FastMCP (se inicializa en `conectar()`)
- `self.conectado`: Bandera para saber si hay conexión activa

### Método de Conexión

```python
async def conectar(self) -> bool:
    try:
        self.cliente = FastMCP()
        await asyncio.sleep(0.1)  # Simular tiempo de conexión
        self.conectado = True
        return True
    except Exception as e:
        logger.error(f"❌ Error al conectar: {e}")
        return False
```

**Explicación:**
- `async`: Indica que es una función asíncrona (no bloquea)
- `FastMCP()`: Crea la instancia del cliente MCP
- `await asyncio.sleep(0.1)`: Simula tiempo de conexión (en realidad, aquí harías la conexión real)
- `self.conectado = True`: Marca la conexión como exitosa

### Listar Herramientas

```python
async def listar_herramientas(self) -> Optional[Dict[str, Any]]:
    if not self.conectado:
        logger.error("No hay conexión activa con el servidor")
        return None
    
    # Simular respuesta del servidor
    herramientas_simuladas = {
        "tools": [
            {
                "name": "sumar",
                "description": "Suma dos números enteros",
                "inputSchema": {...}
            }
        ]
    }
    return herramientas_simuladas
```

**Conceptos importantes:**
- Verificación de conexión antes de hacer peticiones
- Estructura de respuesta estándar MCP
- `inputSchema`: Define qué parámetros necesita la herramienta

### Ejecutar Herramienta

```python
async def ejecutar_herramienta(self, nombre: str, parametros: Dict[str, Any]):
    if nombre == "sumar":
        a = parametros.get("a", 0)
        b = parametros.get("b", 0)
        resultado = a + b
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"El resultado de {a} + {b} = {resultado}"
                }
            ]
        }
```

**Explicación:**
- `parametros.get("a", 0)`: Obtiene el parámetro "a" o usa 0 como defecto
- Estructura de respuesta estándar con `content` y `type: "text"`
- Manejo de diferentes tipos de herramientas

## Conceptos Clave Aprendidos

### 1. **Programación Asíncrona**
- `async/await`: Permite operaciones no bloqueantes
- Importante para aplicaciones que hacen múltiples peticiones

### 2. **Protocolo MCP**
- Estructura estándar de mensajes JSON
- Manejo de herramientas, recursos y prompts
- Validación de parámetros

### 3. **Manejo de Errores**
- Verificación de conexión antes de operaciones
- Try/catch para manejar excepciones
- Logging para debugging

### 4. **Arquitectura Cliente-Servidor**
- Separación clara de responsabilidades
- Cliente consume, servidor proporciona
- Comunicación a través de protocolo estándar

## Troubleshooting Común

### Error: "ModuleNotFoundError: No module named 'fastmcp'"

**Solución:**
```bash
pip install fastmcp
# o
pip install -r requirements.txt
```

### Error: "No hay conexión activa con el servidor"

**Causa:** El método `conectar()` no se ejecutó correctamente.

**Solución:** Verifica que el servidor esté ejecutándose y la URL sea correcta.

### Error: "Herramienta 'X' no encontrada"

**Causa:** Intentaste ejecutar una herramienta que no existe en el servidor.

**Solución:** Usa `listar_herramientas()` para ver qué herramientas están disponibles.

## Próximos Pasos

Ahora que entiendes cómo funciona un cliente MCP:

1. **Ejecuta el Ejercicio 2** para aprender a crear un servidor MCP
2. **Experimenta** modificando los parámetros de las herramientas
3. **Intenta** conectarte a un servidor MCP real
4. **Explora** la documentación oficial de FastMCP

## Referencias

- [Documentación FastMCP](https://github.com/jlowin/fastmcp)
- [Protocolo MCP](https://modelcontextprotocol.io/)
- [Python Asyncio](https://docs.python.org/3/library/asyncio.html)

---

¡Felicitaciones! Has completado el Ejercicio 1. 🎉
