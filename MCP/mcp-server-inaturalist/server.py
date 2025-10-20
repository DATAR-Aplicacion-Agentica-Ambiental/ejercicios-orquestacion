from mcp.server.fastmcp import FastMCP
import httpx
from typing import Optional, List, Dict

mcp = FastMCP("iNaturalist Colombia")

BASE_URL = "https://api.inaturalist.org/v1"

@mcp.tool()
async def buscar_observaciones(
    taxon_name: Optional[str] = None,
    place_id: int = 7562,  # Colombia por defecto
    per_page: int = 10,
    order_by: str = "created_at"
) -> dict:
    """
    Busca observaciones en iNaturalist Colombia.
    
    Args:
        taxon_name: Nombre del taxón (especie, género, familia, etc.)
        place_id: ID del lugar (7562 es Colombia)
        per_page: Número de resultados (máx 200)
        order_by: Ordenar por 'created_at', 'observed_on', 'species_guess', 'votes'
    """
    try:
        params = {
            "place_id": place_id,
            "per_page": min(per_page, 200),
            "order_by": order_by
        }
        
        if taxon_name:
            params["taxon_name"] = taxon_name
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/observations",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            observaciones = []
            for obs in data.get("results", []):
                observaciones.append({
                    "id": obs.get("id"),
                    "especie": obs.get("species_guess", "No identificado"),
                    "nombre_cientifico": obs.get("taxon", {}).get("name"),
                    "fecha_observacion": obs.get("observed_on_string"),
                    "lugar": obs.get("place_guess"),
                    "usuario": obs.get("user", {}).get("login"),
                    "foto_url": obs.get("photos", [{}])[0].get("url") if obs.get("photos") else None,
                    "url": f"https://www.inaturalist.org/observations/{obs.get('id')}"
                })
            
            return {
                "total": data.get("total_results"),
                "observaciones": observaciones
            }
            
    except httpx.TimeoutException:
        return {"error": "Tiempo de espera agotado al consultar iNaturalist"}
    except httpx.HTTPStatusError as e:
        return {"error": f"Error HTTP {e.response.status_code}: {e.response.text}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}


@mcp.tool()
async def buscar_especies(
    nombre: str,
    rank: Optional[str] = None,
    is_active: bool = True
) -> dict:
    """
    Busca información sobre especies/taxones.
    
    Args:
        nombre: Nombre común o científico de la especie
        rank: Rango taxonómico (species, genus, family, order, class, phylum, kingdom)
        is_active: Solo taxones activos (no sinónimos)
    """
    try:
        params = {
            "q": nombre,
            "is_active": is_active,
            "locale": "es"
        }
        
        if rank:
            params["rank"] = rank
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/taxa",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            especies = []
            for taxon in data.get("results", []):
                especies.append({
                    "id": taxon.get("id"),
                    "nombre_cientifico": taxon.get("name"),
                    "nombre_comun": taxon.get("preferred_common_name"),
                    "rango": taxon.get("rank"),
                    "wikipedia_url": taxon.get("wikipedia_url"),
                    "observaciones_totales": taxon.get("observations_count"),
                    "foto_url": taxon.get("default_photo", {}).get("medium_url"),
                    "estado_conservacion": taxon.get("conservation_status", {}).get("status")
                })
            
            return {
                "total": data.get("total_results"),
                "especies": especies
            }
            
    except Exception as e:
        return {"error": f"Error al buscar especies: {str(e)}"}


@mcp.tool()
async def obtener_lugares_colombia(
    nombre_lugar: Optional[str] = None
) -> dict:
    """
    Obtiene información sobre lugares/departamentos en Colombia.
    
    Args:
        nombre_lugar: Nombre del departamento o lugar a buscar
    """
    try:
        # Buscar dentro de Colombia (place_id = 7562)
        params = {
            "place_id": 7562
        }
        
        if nombre_lugar:
            params["q"] = nombre_lugar
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/places",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            lugares = []
            for place in data.get("results", []):
                lugares.append({
                    "id": place.get("id"),
                    "nombre": place.get("display_name"),
                    "tipo": place.get("place_type_name"),
                    "bbox": place.get("bounding_box_geojson"),
                    "observaciones": place.get("observations_count")
                })
            
            return {
                "total": data.get("total_results"),
                "lugares": lugares
            }
            
    except Exception as e:
        return {"error": f"Error al obtener lugares: {str(e)}"}


@mcp.tool()
async def estadisticas_biodiversidad_colombia() -> dict:
    """
    Obtiene estadísticas generales de biodiversidad en Colombia.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Obtener observaciones en Colombia
            response = await client.get(
                f"{BASE_URL}/observations",
                params={"place_id": 7562, "per_page": 0}
            )
            response.raise_for_status()
            data = response.json()
            
            # Obtener especies en Colombia
            response_especies = await client.get(
                f"{BASE_URL}/taxa",
                params={"place_id": 7562, "per_page": 0}
            )
            response_especies.raise_for_status()
            data_especies = response_especies.json()
            
            return {
                "total_observaciones": data.get("total_results"),
                "total_especies": data_especies.get("total_results"),
                "pais": "Colombia"
            }
            
    except Exception as e:
        return {"error": f"Error al obtener estadísticas: {str(e)}"}


@mcp.tool()
async def observaciones_por_usuario(
    username: str,
    place_id: int = 7562,
    per_page: int = 10
) -> dict:
    """
    Busca observaciones de un usuario específico en Colombia.
    
    Args:
        username: Nombre de usuario en iNaturalist
        place_id: ID del lugar (7562 es Colombia)
        per_page: Número de resultados
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/observations",
                params={
                    "user_login": username,
                    "place_id": place_id,
                    "per_page": per_page
                }
            )
            response.raise_for_status()
            data = response.json()
            
            observaciones = []
            for obs in data.get("results", []):
                observaciones.append({
                    "id": obs.get("id"),
                    "especie": obs.get("species_guess"),
                    "fecha": obs.get("observed_on_string"),
                    "lugar": obs.get("place_guess"),
                    "url": f"https://www.inaturalist.org/observations/{obs.get('id')}"
                })
            
            return {
                "usuario": username,
                "total_observaciones": data.get("total_results"),
                "observaciones": observaciones
            }
            
    except Exception as e:
        return {"error": f"Error al obtener observaciones del usuario: {str(e)}"}


if __name__ == "__main__":
    mcp.run()