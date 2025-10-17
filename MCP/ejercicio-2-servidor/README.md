# Ejercicio 2: Servidor MCP Básico

Este es el **ejercicio MÁS SIMPLE** posible para crear un servidor MCP. Si nunca has trabajado con MCP, ¡este es el lugar perfecto para empezar!

## ¿Qué hace este ejercicio?

Este servidor MCP expone **3 herramientas básicas**:
- 🧮 **`suma(a, b)`** - Suma dos números
- ✖️ **`multiplicacion(a, b)`** - Multiplica dos números  
- 👋 **`saludo(nombre)`** - Devuelve un saludo personalizado

## 🚀 Cómo Ejecutar

### 1. Preparar el entorno

```bash
# Navegar al directorio del ejercicio
cd ejercicio-2-servidor

# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias (solo FastMCP)
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
python servidor_basico.py
```

### 3. Salida esperada

```
🚀 Iniciando servidor MCP básico...
📋 Herramientas disponibles:
   • suma(a, b) - Suma dos números
   • multiplicacion(a, b) - Multiplica dos números
   • saludo(nombre) - Saludo personalizado
🛑 Presiona Ctrl+C para detener
```

## 📖 Explicación del Código

El código es **extremadamente simple**:

### Importación y Creación del Servidor

```python
from fastmcp import FastMCP

mcp = FastMCP(name="My First MCP Server")
```

**Explicación:**
- `FastMCP`: La clase principal para crear servidores MCP
- `name`: Nombre descriptivo del servidor (opcional pero recomendado)

### Definir Herramientas

```python
@mcp.tool
def suma(a: int, b: int) -> int:
    """Devuelve la suma de dos números."""
    return a + b
```

**Explicación:**
- `@mcp.tool`: Decorador que registra la función como herramienta MCP
- `a: int, b: int`: Parámetros con tipos específicos (FastMCP los valida automáticamente)
- `-> int`: Tipo de retorno (opcional pero recomendado)
- Docstring: Se convierte en la descripción de la herramienta

### Ejecutar el Servidor

```python
if __name__ == "__main__":
    mcp.run()
```

**Explicación:**
- `if __name__ == "__main__":` - Solo ejecuta si el archivo se llama directamente
- `mcp.run()` - Inicia el servidor MCP (se ejecuta indefinidamente)

## 🧪 Cómo Probar el Servidor

### Opción 1: Usar el Cliente del Ejercicio 1

1. **Terminal 1** - Ejecutar este servidor básico:
   ```bash
   cd ejercicio-2-servidor
   python servidor_basico.py
   ```

2. **Terminal 2** - Ejecutar el cliente del Ejercicio 1:
   ```bash
   cd ejercicio-1-cliente
   python cliente_mcp.py
   ```

### Opción 2: Testing Manual con Python

```python
# Crear un archivo test_servidor.py
from servidor_basico import suma, multiplicacion, saludo

# Probar las herramientas directamente
print("🧮 Probando suma:", suma(5, 3))           # Resultado: 8
print("✖️ Probando multiplicación:", multiplicacion(4, 7))  # Resultado: 28
print("👋 Probando saludo:", saludo("María"))    # Resultado: ¡Hola María! Bienvenido al servidor MCP.
```

## 🎯 Conceptos Clave Aprendidos

### 1. **Simplicidad de FastMCP**
- Solo necesitas `FastMCP` y el decorador `@mcp.tool`
- No necesitas configurar protocolos, validaciones o manejo de errores
- FastMCP maneja todo automáticamente

### 2. **Decoradores en Python**
- `@mcp.tool` convierte funciones normales en herramientas MCP
- Los decoradores "envuelven" las funciones con funcionalidad adicional

### 3. **Tipado en Python**
- `a: int` especifica que el parámetro debe ser un entero
- FastMCP valida automáticamente los tipos
- Ayuda a detectar errores antes de la ejecución

### 4. **Documentación con Docstrings**
- `"""Devuelve la suma de dos números."""` se convierte en la descripción
- Los clientes MCP pueden ver esta información
- Es una buena práctica de programación

## 🔧 Personalización Fácil

### Agregar Nueva Herramienta

```python
@mcp.tool
def resta(a: int, b: int) -> int:
    """Devuelve la resta de dos números."""
    return a - b
```

### Agregar Herramienta con String

```python
@mcp.tool
def contar_caracteres(texto: str) -> int:
    """Cuenta el número de caracteres en un texto."""
    return len(texto)
```

### Agregar Herramienta Sin Parámetros

```python
@mcp.tool
def hora_actual() -> str:
    """Devuelve la hora actual."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")
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
1. Verifica que el servidor esté corriendo: `python servidor_basico.py`
2. Verifica que no haya errores en la consola del servidor
3. Asegúrate de que el puerto no esté ocupado

### Error: "Tool validation failed"

**Causa:** Los parámetros enviados no coinciden con los tipos esperados.

**Solución:** 
- Para `suma(a: int, b: int)` envía números enteros, no strings
- Para `saludo(nombre: str)` envía texto, no números

## 🎓 Próximos Pasos

Después de dominar este ejercicio básico:

1. **Ejecuta el Ejercicio 1** para aprender a crear un cliente MCP
2. **Ejecuta el Ejercicio 2** para ver un servidor más complejo
3. **Experimenta** agregando tus propias herramientas
4. **Explora** la documentación oficial de FastMCP

## 💡 Consejos

- **Empieza simple**: Agrega una herramienta a la vez
- **Usa tipos**: Especifica tipos para parámetros y retornos
- **Documenta**: Escribe docstrings descriptivos
- **Prueba**: Verifica que cada herramienta funciona correctamente

---

¡Este es el punto de partida perfecto para aprender MCP! 🎉
