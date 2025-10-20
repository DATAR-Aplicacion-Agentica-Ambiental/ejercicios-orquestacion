# MCP

## Instalación

### Agregar MCP al proyecto de python

```bash
cd MCP
```

Se recomienda usar [uv](https://docs.astral.sh/uv/) para manejar el proyecto de python.

   ```bash
   uv init mcp-server-demo
   cd mcp-server-demo
   ```

   Luego agrega las dependencias:

   ```bash
   uv add "mcp[cli]"
   ```

Si se utiliza pip:

```bash
pip install "mcp[cli]"
```

### Ejecuta las herramientas de desarrollo de MCP

```bash
uv run python main.py
```

Se puede instalar este servidor en  [Claude Desktop](https://claude.ai/download) apara interactuar:

```bash
uv run mcp install server.py
```

También se puede correr el MCP Inspector:

```bash
uv run mcp dev server.py
