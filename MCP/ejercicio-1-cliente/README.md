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
python cliente_mcp.py
```

### 3. Salida esperada

```
🚀 Probando cliente MCP básico
========================================

📋 Herramientas disponibles en el servidor:
   • suma(a, b) - Suma dos números
   • multiplicacion(a, b) - Multiplica dos números
   • saludo(nombre) - Saludo personalizado

🔧 Probando herramientas:

   1️⃣ Probando suma: 5 + 3
      📊 Resultado: 8

   2️⃣ Probando multiplicación: 4 × 7
      📊 Resultado: 28

   3️⃣ Probando saludo:
      📊 Resultado: ¡Hola Juan! Bienvenido al servidor MCP.

✅ Pruebas completadas exitosamente!

💡 Para probar con un servidor real:
   1. Ejecuta el servidor: cd ejercicio-2-servidor && python servidor_basico.py
   2. En otra terminal, ejecuta este cliente
   3. El cliente se conectará al servidor y podrá usar las herramientas
```

## 📖 Explicación del Código

El código es **extremadamente simple**:

### Importación y Creación del Cliente

```python
from fastmcp import FastMCP

cliente = FastMCP(name="My First MCP Client")
```

**Explicación:**
- `FastMCP`: La clase principal para crear clientes MCP
- `name`: Nombre descriptivo del cliente (opcional pero recomendado)

### Función de Prueba

```python
def probar_herramientas():
    """Prueba las herramientas del servidor MCP de manera simple."""
    
    print("🚀 Probando cliente MCP básico")
    print("=" * 40)
    
    # Simular llamadas a herramientas del servidor
    print("\n   1️⃣ Probando suma: 5 + 3")
    resultado_suma = 5 + 3  # En realidad sería: cliente.call_tool("suma", {"a": 5, "b": 3})
    print(f"      📊 Resultado: {resultado_suma}")
```

**Explicación:**
- Función simple que simula llamadas a herramientas
- Comentarios muestran cómo sería la llamada real
- Salida clara y organizada

### Ejecución Principal

```python
if __name__ == "__main__":
    probar_herramientas()
```

**Explicación:**
- `if __name__ == "__main__":` - Solo ejecuta si el archivo se llama directamente
- `probar_herramientas()` - Ejecuta la función de demostración

## 🧪 Cómo Probar con un Servidor Real

### Opción 1: Usar el Servidor del Ejercicio 2

1. **Terminal 1** - Ejecutar el servidor:
   ```bash
   cd ejercicio-2-servidor
   python servidor_basico.py
   ```

2. **Terminal 2** - Ejecutar este cliente:
   ```bash
   cd ejercicio-1-cliente
   python cliente_mcp.py
   ```

### Opción 2: Modificar el Cliente para Conexión Real

Puedes modificar `cliente_mcp.py` para conectarte a un servidor real:

```python
# Reemplazar las simulaciones con llamadas reales:
resultado_suma = cliente.call_tool("suma", {"a": 5, "b": 3})
resultado_mult = cliente.call_tool("multiplicacion", {"a": 4, "b": 7})
saludo = cliente.call_tool("saludo", {"nombre": "Juan"})
```

## 🎯 Conceptos Clave Aprendidos

### 1. **Simplicidad de FastMCP**
- Solo necesitas `FastMCP` para crear un cliente
- No necesitas configurar protocolos complejos
- FastMCP maneja la comunicación automáticamente

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