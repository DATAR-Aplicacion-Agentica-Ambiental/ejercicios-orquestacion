# Servidor MCP de Hola Mundo 🚀

Un servidor **Model Context Protocol (MCP)** básico pero completo que demuestra las funcionalidades principales del protocolo usando **FastMCP**.

## 📋 Características

El servidor incluye tres componentes principales:

### 🛠️ **Herramientas (Tools)**
- `add(a, b)` - Suma dos números enteros

### 📚 **Recursos (Resources)**
- `greeting://{name}` - Proporciona saludos personalizados dinámicos

### 💭 **Prompts**
- `greet_user(name, style)` - Genera prompts de saludo en diferentes estilos:
  - `friendly` - Saludo cálido y amigable
  - `formal` - Saludo profesional y formal
  - `casual` - Saludo relajado e informal

## ⚙️ Instalación

### 1. Navega al directorio del proyecto
```bash
cd mcp-server-demo
```

### 2. El entorno virtual ya está configurado
Las dependencias fueron instaladas automáticamente con `uv`. Si necesitas reinstalar:

```bash
uv sync
```

### 3. Verifica la instalación
```bash
uv run python --version
```

## 🚀 Ejecución

### Opción 1: Ejecutar directamente
```bash
uv run python main.py
```

### Opción 2: Usar el comando MCP CLI
```bash
uv run mcp
```

### Opción 3: Ejecutar como script instalado
```bash
uv run mcp-server-demo
```

## 🧪 Pruebas

### Usar el cliente de prueba de MCP
En otra terminal:

```bash
# Listar herramientas disponibles
uv run mcp list-tools

# Llamar a una herramienta
uv run mcp call add --arguments '{"a": 5, "b": 3}'

# Acceder a un recurso
uv run mcp read greeting://Juan

# Ejecutar un prompt
uv run mcp execute-prompt greet_user --arguments '{"name": "María", "style": "formal"}'
```

## 📁 Estructura del Proyecto

```
mcp-server-demo/
├── main.py              # Punto de entrada del servidor
├── server.py            # Definición del servidor MCP (FastMCP)
├── pyproject.toml       # Configuración del proyecto
├── uv.lock              # Lock file de dependencias
├── README.md            # Este archivo
└── .venv/               # Entorno virtual (no versionado)
```

## 📦 Dependencias

- **mcp[cli]** >= 1.18.0 - Model Context Protocol con herramientas CLI

## 🎯 Ejemplos de Uso

### Ejemplo 1: Sumar números
```bash
uv run mcp call add --arguments '{"a": 10, "b": 25}'
# Resultado: 35
```

### Ejemplo 2: Obtener saludo
```bash
uv run mcp read greeting://Carlos
# Resultado: "Hello, Carlos!"
```

### Ejemplo 3: Generar prompt formal
```bash
uv run mcp execute-prompt greet_user --arguments '{"name": "Ana", "style": "formal"}'
# Resultado: "Please write a formal, professional greeting for someone named Ana."
```

## 🔧 Desarrollo

Para agregar nuevas herramientas, recursos o prompts, edita `server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

@mcp.tool()
def mi_herramienta(parametro: str) -> str:
    """Descripción de la herramienta"""
    return f"Resultado: {parametro}"

@mcp.resource("ruta://{id}")
def mi_recurso(id: str) -> str:
    """Descripción del recurso"""
    return f"Recurso {id}"

@mcp.prompt()
def mi_prompt(input: str) -> str:
    """Descripción del prompt"""
    return f"Prompt para: {input}"
```

## 📚 Recursos

- [Documentación oficial MCP](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [uv - Python Package Manager](https://docs.astral.sh/uv/)

## 📝 Notas

- El servidor usa **stdio** para comunicación (estándar MCP)
- Compatible con cualquier cliente MCP
- Desarrollo rápido gracias a FastMCP

## 🤝 Próximos Pasos

- Agregar más herramientas específicas
- Integrar con APIs externas
- Crear un cliente personalizado
- Añadir persistencia de datos
