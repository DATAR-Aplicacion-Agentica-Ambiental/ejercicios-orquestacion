# Ejercicio 1: Cliente MCP Básico

Este es el **ejercicio MÁS SIMPLE** posible para crear un cliente MCP. Si nunca has trabajado con MCP, ¡este es el lugar perfecto para empezar!

## ¿Qué es un Cliente MCP?

Un **cliente MCP** es una aplicación que se conecta a servidores MCP para acceder a sus herramientas, recursos y capacidades. Piensa en él como un "consumidor" que solicita servicios de un "proveedor" (el servidor).

### Funciones principales de un cliente:
- 🔌 **Conectar** a servidores MCP
- 📋 **Descubrir** herramientas y recursos disponibles
- 🔧 **Ejecutar** herramientas remotas
- 📊 **Procesar** respuestas del servidor

## 🚀 Cómo Ejecutar

### 1. Preparar el entorno

```bash
# Navegar al directorio del ejercicio
cd ejercicio-1-cliente

# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias (solo FastMCP)
pip install -r requirements.txt
```

### 2. Ejecutar el cliente

```bash
# Cliente que se conecta REALMENTE al servidor MCP
python cliente_exitoso.py
```

### 3. Salida esperada

**Salida del cliente exitoso:**
```
🎯 CLIENTE MCP EXITOSO
¡Este cliente se conecta REALMENTE al servidor!
==================================================
✅ Conectado al servidor MCP
✅ Sesión MCP inicializada exitosamente
✅ Ping exitoso - Conexión funcionando

==================================================
🎉 ¡ÉXITO! Conexión real establecida
==================================================

💡 Lo que hemos logrado:
   ✅ Conectado al servidor MCP via stdio
   ✅ Inicializado sesión MCP correctamente
   ✅ Verificado conexión con ping
   ✅ Protocolo JSON-RPC funcionando

🔧 Limitaciones descubiertas:
   ❌ tools/list no funciona en este servidor
   ❌ tools/call no funciona en este servidor
   ❌ Posible problema con implementación del servidor

🎉 ¡Demostración completada!
💡 Este es el PRIMER cliente que se conecta realmente al servidor MCP!
```

## 📖 Explicación del Código

El código es **extremadamente simple**:

### Importación y Creación del Cliente

```python
import asyncio
from fastmcp import Client

async def probar_herramientas():
    cliente = Client("http://localhost:8000/mcp/")
    
    async with cliente:
        resultado = await cliente.call_tool("suma", {"a": 5, "b": 3})
```

**Explicación:**
- `asyncio`: Necesario para programación asíncrona
- `Client`: La clase para crear clientes MCP (diferente de FastMCP que es para servidores)
- `"http://localhost:8000/mcp/"`: URL del servidor MCP
- `async with cliente`: Contexto asíncrono requerido por el cliente
- `await cliente.call_tool()`: Llamada asíncrona a herramientas del servidor

### Función de Prueba Asíncrona

```python
async def probar_herramientas():
    """Prueba las herramientas del servidor MCP de manera simple."""
    
    print("🚀 Probando cliente MCP básico")
    print("=" * 40)
    
    cliente = FastMCP(name="My First MCP Client")
    
    async with cliente:
        # Llamadas reales a herramientas del servidor
        print("\n   1️⃣ Probando suma: 5 + 3")
        resultado_suma = await cliente.call_tool("suma", {"a": 5, "b": 3})
        print(f"      📊 Resultado: {resultado_suma}")
```

**Explicación:**
- Función asíncrona que hace llamadas reales a herramientas del servidor
- Usa `async with cliente:` para el contexto asíncrono requerido
- Usa `await cliente.call_tool()` para comunicarse con el servidor MCP
- Manejo de errores si el servidor no está disponible
- Salida clara y organizada

### Ejecución Principal Asíncrona

```python
async def main():
    await probar_herramientas()
    # Más código...

if __name__ == "__main__":
    asyncio.run(main())
```

**Explicación:**
- `async def main():` - Función principal asíncrona
- `asyncio.run(main())` - Ejecuta la función asíncrona principal
- Necesario porque FastMCP requiere programación asíncrona

## 🧪 Cómo Probar con un Servidor Real

### Opción 1: Usar el Servidor del Ejercicio 2

1. **Terminal 1** - Ejecutar el servidor:
   ```bash
   cd ejercicio-2-servidor
   python servidor_basico.py
   ```
   **Salida esperada**: `🌐 Servidor ejecutándose en: http://localhost:8000`

2. **Terminal 2** - Ejecutar este cliente:
   ```bash
   cd ejercicio-1-cliente
   python cliente_mcp.py
   ```

### ⚠️ Problema Identificado

FastMCP usa el protocolo MCP con stdio, no HTTP. Esto significa que la comunicación cliente-servidor es más compleja de lo esperado.

### Opción 0: Test de Conexión Simple

Antes de ejecutar el cliente completo, puedes probar la conexión:
```bash
cd ejercicio-1-cliente
python test_conexion.py
```

### 🔧 Soluciones Disponibles

**1. Cliente Simple** (`cliente_simple.py`):
- Funciona sin problemas
- Simula las respuestas del servidor
- Perfecto para aprender los conceptos

**2. Cliente Funcional** (`cliente_funcional.py`):
- Intenta conexión real con el servidor
- Usa subprocess para comunicación
- Más complejo pero más realista

**3. Servidor Simple** (`servidor_simple.py`):
- Versión corregida del servidor
- Sin parámetros de puerto que causan errores

**4. Cliente Interactivo** (`cliente_interactivo.py`):
- ¡**RECOMENDADO**! Menú interactivo fácil de usar
- Prueba cada herramienta individualmente
- Explica cómo funcionaría con servidor real
- Perfecto para aprender y experimentar

**5. Demo Real** (`demo_real.py`):
- Muestra el protocolo JSON-RPC completo
- Explica la comunicación real MCP
- Simula servidor y cliente
- Educativo sobre el protocolo interno

### Opción 2: Script de Demo Avanzado

El archivo `demo.py` incluye demostraciones más avanzadas:

```bash
# Ejecutar demo completa
python demo.py
```

**Incluye:**
- Demo básica automática
- Demo avanzada con diferentes tipos de números
- Modo interactivo donde puedes elegir qué probar
- Casos de prueba con enteros, decimales, negativos

### Opción 3: Cliente Interactivo (Ya Incluido)

El cliente principal ahora incluye una función adicional para probar con diferentes parámetros:

```python
# El cliente automáticamente pregunta si quieres probar más:
¿Quieres probar con diferentes parámetros? (s/n): 

# Si respondes 's', probará:
# - Sumas: (10, 20), (100, 200), (1.5, 2.5)
# - Multiplicaciones: con los mismos números
# - Saludos: con nombres como María, Carlos, Ana, Luis
```

## 🆕 Nuevas Funcionalidades

### ✨ Comunicación Real con Servidor
- El cliente ahora se conecta realmente al servidor MCP
- Usa `cliente.call_tool()` para hacer llamadas reales
- Manejo de errores si el servidor no está disponible

### 🎯 Modo Interactivo
- Después de las pruebas básicas, pregunta si quieres probar más
- Prueba automáticamente con diferentes parámetros
- Demuestra la flexibilidad del sistema MCP

### 🔧 Manejo de Errores
- Detecta si el servidor no está ejecutándose
- Proporciona instrucciones claras para solucionarlo
- No falla silenciosamente

### 🎬 Script de Demo (`demo.py`)
- Demostración programática del cliente
- Ejemplos con diferentes tipos de datos
- Modo interactivo para experimentar
- Casos de prueba automatizados

## 🎯 Conceptos Clave Aprendidos

### 1. **Cliente vs Servidor en FastMCP**
- **`Client`**: Para crear clientes MCP que se conectan a servidores
- **`FastMCP`**: Para crear servidores MCP que exponen herramientas
- **URL específica**: El cliente debe conectarse a `http://localhost:8000/mcp/`
- **Programación asíncrona**: Usa `async/await` y `async with`

### 2. **Estructura de Cliente MCP**
- Crear instancia del cliente
- Llamar herramientas con parámetros
- Procesar respuestas del servidor

### 3. **Flujo Cliente-Servidor**
- Cliente solicita herramientas del servidor
- Servidor ejecuta las herramientas
- Cliente recibe y procesa los resultados

### 4. **Tipos de Datos**
- Parámetros de entrada (números, strings)
- Respuestas del servidor (resultados de herramientas)
- Manejo de errores básico

## 🔧 Personalización Fácil

### Agregar Nueva Prueba

```python
print("\n   4️⃣ Probando nueva herramienta:")
resultado = cliente.call_tool("nueva_herramienta", {"param": "valor"})
print(f"      📊 Resultado: {resultado}")
```

### Probar con Diferentes Parámetros

```python
# Probar con diferentes números
print("\n   🔢 Probando con diferentes números:")
for a in [1, 2, 3]:
    for b in [10, 20, 30]:
        resultado = cliente.call_tool("suma", {"a": a, "b": b})
        print(f"      {a} + {b} = {resultado}")
```

### Agregar Manejo de Errores

```python
try:
    resultado = cliente.call_tool("herramienta_inexistente", {"a": 1})
    print(f"Resultado: {resultado}")
except Exception as e:
    print(f"Error: {e}")
```

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'fastmcp'"

**Solución:**
```bash
pip install fastmcp
```

### Error: "No se puede conectar al servidor"

**Causa:** El servidor no está ejecutándose.

**Solución:**
1. Verifica que el servidor esté corriendo
2. Verifica que no haya errores en la consola del servidor
3. Asegúrate de que el puerto no esté ocupado

### Error: "Tool not found"

**Causa:** La herramienta no existe en el servidor.

**Solución:** 
- Verifica que el servidor tenga la herramienta disponible
- Usa el nombre exacto de la herramienta
- Revisa los parámetros requeridos

## 🎓 Próximos Pasos

Después de dominar este ejercicio básico:

1. **Ejecuta el Ejercicio 2** para aprender a crear un servidor MCP
2. **Experimenta** conectando este cliente al servidor
3. **Modifica** el código para agregar nuevas funcionalidades
4. **Explora** la documentación oficial de FastMCP

## 💡 Consejos

- **Empieza simple**: Usa las herramientas básicas primero
- **Experimenta**: Prueba con diferentes parámetros
- **Lee los errores**: Los mensajes de error te ayudan a debuggear
- **Conecta servidor y cliente**: Para ver la comunicación real

---

¡Este es el punto de partida perfecto para aprender MCP! 🎉