"""
MCP Server iNaturalist: Servidor para consultar datos de biodiversidad
"""

from server import mcp


def main():
    """Ejecuta el servidor MCP usando stdio"""
    mcp.run()


if __name__ == "__main__":
    main()
