# Servidor MCP de Hola Mundo

Un servidor MCP (Model Context Protocol) básico que demuestra las funcionalidades fundamentales del protocolo.

## 🚀 Características

- **3 herramientas disponibles:**
  - `saludar`: Saluda al usuario en diferentes idiomas
  - `obtener_info`: Obtiene información del servidor
  - `calcular`: Realiza operaciones matemáticas básicas

- **Protocolo MCP estándar**
- **Interfaz JSON-RPC**
- **Cliente de prueba incluido**

## 📋 Instalación y Uso

### 1. Crear entorno virtual
```bash
cd MCP
python -m venv venv
```

### 2. Activar entorno virtual
```bash
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor
```bash
python servidor_hola_mundo.py
```

### 5. Probar con el cliente
En otra terminal:
```bash
python cliente_prueba.py
```

## 🛠️ Herramientas Disponibles

### 1. Saludar
```json
{
  "name": "saludar",
  "arguments": {
    "nombre": "Juan",
    "idioma": "es"  // opcional: es, en, fr
  }
}
```

### 2. Obtener Información
```json
{
  "name": "obtener_info",
  "arguments": {}
}
```

### 3. Calcular
```json
{
  "name": "calcular",
  "arguments": {
    "operacion": "suma",  // suma, resta, multiplicacion, division
    "a": 10,
    "b": 5
  }
}
```

## 🔧 Estructura del Proyecto

```
MCP/
├── servidor_hola_mundo.py    # Servidor MCP principal
├── cliente_prueba.py         # Cliente de prueba
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

## 📝 Ejemplo de Uso

El cliente de prueba ejecuta automáticamente:

1. **Lista las herramientas** disponibles
2. **Saluda** al usuario en español
3. **Obtiene información** del servidor
4. **Realiza cálculos** matemáticos

## 🎯 Próximos Pasos

- Agregar más herramientas
- Implementar persistencia de datos
- Crear interfaz web
- Integrar con otros servicios

## 📚 Recursos

- [Documentación MCP](https://modelcontextprotocol.io/)
- [Protocolo JSON-RPC](https://www.jsonrpc.org/)
