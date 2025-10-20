"""
FastMCP DATAR: Prueba de MCP
"""

from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("DATAR: Prueba de MCP")

@mcp.tool()
def obtener_lugares() -> dict:
    """Obtiene una lista de tres lugares ambientales disponibles"""
    lugares = [
        {
            "id": 1,
            "nombre": "Humedal La Conejera",
            "tipo": "Humedal",
            "descripcion": "Área protegida de importancia ecológica"
        },
        {
            "id": 2,
            "nombre": "Cerro La Conejera",
            "tipo": "Cerro",
            "descripcion": "Formación geológica con vegetación nativa"
        },
        {
            "id": 3,
            "nombre": "Quebrada La Salitrosa",
            "tipo": "Quebrada",
            "descripcion": "Recurso hídrico con ecosistema acuático"
        }
    ]
    return {
        "total": len(lugares),
        "lugares": lugares
    }