# Ejercicio 2: Servidor MCP Simple

Este ejercicio te enseña cómo crear un **servidor MCP básico** que expone herramientas simples usando FastMCP. Es el complemento perfecto al Ejercicio 1 y te muestra cómo funciona el protocolo MCP desde la perspectiva del proveedor.

## ¿Qué es un Servidor MCP?

Un **servidor MCP** es una aplicación que expone herramientas, recursos y capacidades a través del protocolo MCP. Piensa en él como un "proveedor" que ofrece servicios a "consumidores" (clientes MCP).

### Funciones principales de un servidor:
- 🔧 **Exponer** herramientas (funciones que pueden ejecutarse)
- 📊 **Procesar** solicitudes de clientes
- ✅ **Validar** parámetros de entrada
- 📤 **Devolver** resultados a los clientes
- 🛡️ **Manejar** errores y excepciones

## Herramientas Disponibles

Este servidor expone las siguientes herramientas:

### 🧮 Calculadora Básica
- **`sumar(a, b)`** - Suma dos números
- **`multiplicar(a, b)`** - Multiplica dos números
- **`potencia(base, exponente)`** - Calcula la potencia de un número

### 📝 Procesamiento de Texto
- **`contar_palabras(texto)`** - Cuenta el número de palabras en un texto
- **`a_mayusculas(texto)`** - Convierte texto a mayúsculas

### 🕒 Utilidades
- **`fecha_actual()`** - Obtiene la fecha y hora actual

## Cómo Ejecutar el Ejercicio

### 1. Preparar el entorno

```bash
# Asegúrate de estar en el directorio del ejercicio
cd ejercicio-2-servidor

# Crear entorno virtual (si no existe)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
python servidor_mcp.py
```

### 3. Salida esperada

```
Servidor MCP Simple - Ejercicio 2
Este ejercicio demuestra cómo crear un servidor MCP básico

🧪 Demostración de herramientas del servidor
==================================================

🔧 Configurando herramientas del servidor...
✅ Herramientas configuradas exitosamente
📋 Herramientas disponibles:
   • sumar(a, b) - Suma dos números
   • multiplicar(a, b) - Multiplica dos números
   • potencia(base, exponente) - Calcula potencia
   • contar_palabras(texto) - Cuenta palabras en texto
   • a_mayusculas(texto) - Convierte texto a mayúsculas
   • fecha_actual() - Obtiene fecha y hora actual

📋 Herramientas configuradas:
✅ sumar(a, b) - Suma dos números
✅ multiplicar(a, b) - Multiplica dos números
✅ potencia(base, exponente) - Calcula potencia
✅ contar_palabras(texto) - Cuenta palabras en texto
✅ a_mayusculas(texto) - Convierte texto a mayúsculas
✅ fecha_actual() - Obtiene fecha y hora actual

💡 Para probar las herramientas:
1. Ejecuta este servidor: python servidor_mcp.py
2. En otra terminal, ejecuta el cliente del Ejercicio 1
3. El cliente se conectará a este servidor y podrá usar las herramientas

==================================================

🚀 Iniciando servidor MCP...
✅ Servidor MCP iniciado exitosamente en localhost:8000
📡 Esperando conexiones de clientes...
💡 Tip: Puedes usar el cliente del Ejercicio 1 para conectarte
🛑 Presiona Ctrl+C para detener el servidor
```

## Explicación del Código

### Estructura Principal

```python
class ServidorMCPSimple:
    def __init__(self, host, puerto)        # Inicialización
    def configurar_herramientas(self)       # Registrar herramientas
    async def iniciar(self)                 # Iniciar servidor
    async def detener(self)                 # Detener servidor
```

### Decorador @fastmcp.tool()

La clave para crear herramientas MCP está en el decorador `@self.fastmcp.tool()`:

```python
@self.fastmcp.tool()
async def sumar(a: float, b: float) -> str:
    """
    Suma dos números.
    
    Args:
        a: Primer número
        b: Segundo número
        
    Returns:
        String con el resultado de la suma
    """
    resultado = a + b
    return f"El resultado de {a} + {b} = {resultado}"
```

**Explicación:**
- `@self.fastmcp.tool()`: Registra la función como una herramienta MCP
- `async def`: Hace la función asíncrona (recomendado para MCP)
- Tipos de parámetros: `float`, `str`, etc. (FastMCP los valida automáticamente)
- Docstring: Se convierte en la descripción de la herramienta

### Herramienta con Manejo de Errores

```python
@self.fastmcp.tool()
async def potencia(base: float, exponente: float) -> str:
    try:
        resultado = math.pow(base, exponente)
        return f"El resultado de {base}^{exponente} = {resultado}"
    except OverflowError:
        return f"Error: El resultado de {base}^{exponente} es demasiado grande"
    except ValueError as e:
        return f"Error: {str(e)}"
```

**Conceptos importantes:**
- Manejo de excepciones específicas (`OverflowError`, `ValueError`)
- Mensajes de error informativos para el cliente
- Logging para debugging del servidor

### Herramienta Sin Parámetros

```python
@self.fastmcp.tool()
async def fecha_actual() -> str:
    """
    Obtiene la fecha y hora actual.
    
    Returns:
        String con la fecha y hora actual
    """
    ahora = datetime.now()
    fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
    return f"La fecha y hora actual es: {fecha_formateada}"
```

**Notas:**
- Las herramientas pueden no tener parámetros
- Siempre deben devolver algo (string, dict, etc.)
- La documentación es importante para que los clientes sepan qué hace

## Cómo Probar el Servidor

### Método 1: Usar el Cliente del Ejercicio 1

1. **Terminal 1** - Ejecutar el servidor:
   ```bash
   cd ejercicio-2-servidor
   python servidor_mcp.py
   ```

2. **Terminal 2** - Ejecutar el cliente:
   ```bash
   cd ejercicio-1-cliente
   python cliente_mcp.py
   ```

### Método 2: Testing Manual

Puedes modificar el archivo `cliente_mcp.py` para probar herramientas específicas:

```python
# En el método demostracion_cliente(), agregar:
resultado_potencia = await cliente.ejecutar_herramienta("potencia", {"base": 2, "exponente": 3})
if resultado_potencia:
    print(f"   📊 Potencia: {resultado_potencia['content'][0]['text']}")

resultado_palabras = await cliente.ejecutar_herramienta("contar_palabras", {"texto": "Hola mundo MCP"})
if resultado_palabras:
    print(f"   📊 Palabras: {resultado_palabras['content'][0]['text']}")
```

## Conceptos Clave Aprendidos

### 1. **Decoradores en FastMCP**
- `@self.fastmcp.tool()`: Convierte funciones en herramientas MCP
- Validación automática de tipos de parámetros
- Documentación automática a partir de docstrings

### 2. **Validación de Parámetros**
- FastMCP valida automáticamente los tipos
- Manejo de errores de validación
- Parámetros opcionales y requeridos

### 3. **Arquitectura de Servidor**
- Separación entre configuración y ejecución
- Manejo asíncrono de múltiples clientes
- Logging para monitoreo y debugging

### 4. **Tipos de Herramientas**
- Herramientas de cálculo (matemáticas)
- Herramientas de procesamiento (texto)
- Herramientas de utilidad (sistema)

## Extensión del Servidor

### Agregar Nueva Herramienta

```python
@self.fastmcp.tool()
async def dividir(a: float, b: float) -> str:
    """
    Divide dos números.
    
    Args:
        a: Dividendo
        b: Divisor
        
    Returns:
        String con el resultado de la división
    """
    if b == 0:
        return "Error: No se puede dividir por cero"
    
    resultado = a / b
    return f"El resultado de {a} ÷ {b} = {resultado}"
```

### Agregar Validación Personalizada

```python
@self.fastmcp.tool()
async def raiz_cuadrada(numero: float) -> str:
    """
    Calcula la raíz cuadrada de un número.
    
    Args:
        numero: Número para calcular raíz cuadrada
        
    Returns:
        String con el resultado
    """
    if numero < 0:
        return "Error: No se puede calcular la raíz cuadrada de un número negativo"
    
    resultado = math.sqrt(numero)
    return f"La raíz cuadrada de {numero} = {resultado}"
```

## Troubleshooting Común

### Error: "ModuleNotFoundError: No module named 'fastmcp'"

**Solución:**
```bash
pip install fastmcp
# o
pip install -r requirements.txt
```

### Error: "Address already in use"

**Causa:** El puerto 8000 ya está siendo usado por otra aplicación.

**Solución:**
```python
# Cambiar el puerto en el código
servidor = ServidorMCPSimple(puerto=8001)
```

### Error: "Tool validation failed"

**Causa:** Los parámetros enviados no coinciden con los tipos esperados.

**Solución:** Verifica que el cliente envíe los tipos correctos (float, str, etc.).

## Próximos Pasos

Ahora que entiendes cómo funciona un servidor MCP:

1. **Combina** el cliente y servidor para crear un sistema completo
2. **Experimenta** agregando nuevas herramientas
3. **Explora** recursos MCP (no solo herramientas)
4. **Implementa** herramientas que se conecten a APIs externas

## Referencias

- [Documentación FastMCP](https://github.com/jlowin/fastmcp)
- [Protocolo MCP](https://modelcontextprotocol.io/)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)

---

¡Felicitaciones! Has completado el Ejercicio 2. 🎉
