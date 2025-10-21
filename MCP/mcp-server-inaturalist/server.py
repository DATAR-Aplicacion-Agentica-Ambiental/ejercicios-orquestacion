from mcp.server.fastmcp import FastMCP
import httpx
from typing import Optional, List, Dict

mcp = FastMCP("iNaturalist")

BASE_URL = "https://api.inaturalist.org/v1"

@mcp.tool()
async def buscar_observaciones(
    taxon_name: Optional[str] = None,
    lat: float = 4.8155,  # Humedal la Conejera - Bogotá
    lng: float = -74.0750,
    radius: float = 3.0,  # Radio en km
    per_page: int = 10,
    order_by: str = "created_at"
) -> dict:
    """
    Busca observaciones en iNaturalist usando coordenadas geográficas.
    Por defecto busca en Humedal la Conejera, Bogotá.
    
    Args:
        taxon_name: Nombre del taxón (especie, género, familia, etc.)
        lat: Latitud (default: 4.8155 - Humedal la Conejera)
        lng: Longitud (default: -74.0750 - Humedal la Conejera)
        radius: Radio de búsqueda en km (default: 3)
        per_page: Número de resultados (máx 200)
        order_by: Ordenar por 'created_at', 'observed_on', 'species_guess', 'votes'
    """
    try:
        params = {
            "lat": lat,
            "lng": lng,
            "radius": radius,
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
                "coordenadas": {"lat": lat, "lng": lng, "radius_km": radius},
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
async def obtener_lugares(
    nombre_lugar: Optional[str] = None,
    lat: float = 4.8155,  # Humedal la Conejera - Bogotá
    lng: float = -74.0750,
    radius: float = 5.0
) -> dict:
    """
    Obtiene información sobre lugares cercanos a las coordenadas especificadas.
    Por defecto busca alrededor de Humedal la Conejera.
    
    Args:
        nombre_lugar: Nombre del departamento o lugar a buscar
        lat: Latitud (default: 4.8155 - Humedal la Conejera)
        lng: Longitud (default: -74.0750 - Humedal la Conejera)
        radius: Radio de búsqueda en km (default: 5)
    """
    try:
        params = {
            "lat": lat,
            "lng": lng,
            "radius": radius
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
                "coordenadas": {"lat": lat, "lng": lng, "radius_km": radius},
                "lugares": lugares
            }
            
    except Exception as e:
        return {"error": f"Error al obtener lugares: {str(e)}"}


@mcp.tool()
async def estadisticas_biodiversidad(
    lat: float = 4.8155,  # Humedal la Conejera - Bogotá
    lng: float = -74.0750,
    radius: float = 3.0
) -> dict:
    """
    Obtiene estadísticas de biodiversidad en el área especificada.
    Por defecto usa Humedal la Conejera.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Obtener observaciones en el área
            response = await client.get(
                f"{BASE_URL}/observations",
                params={"lat": lat, "lng": lng, "radius": radius, "per_page": 0}
            )
            response.raise_for_status()
            data = response.json()
            
            # Obtener especies en el área
            response_especies = await client.get(
                f"{BASE_URL}/taxa",
                params={"lat": lat, "lng": lng, "radius": radius, "per_page": 0}
            )
            response_especies.raise_for_status()
            data_especies = response_especies.json()
            
            return {
                "total_observaciones": data.get("total_results"),
                "total_especies": data_especies.get("total_results"),
                "ubicacion": "Humedal la Conejera, Bogotá",
                "coordenadas": {"lat": lat, "lng": lng, "radius_km": radius}
            }
            
    except Exception as e:
        return {"error": f"Error al obtener estadísticas: {str(e)}"}


@mcp.tool()
async def observaciones_por_usuario(
    username: str,
    lat: float = 4.8155,  # Humedal la Conejera - Bogotá
    lng: float = -74.0750,
    radius: float = 3.0,
    per_page: int = 10
) -> dict:
    """
    Busca observaciones de un usuario específico en el área especificada.
    Por defecto busca en Humedal la Conejera.
    
    Args:
        username: Nombre de usuario en iNaturalist
        lat: Latitud (default: 4.8155 - Humedal la Conejera)
        lng: Longitud (default: -74.0750 - Humedal la Conejera)
        radius: Radio de búsqueda en km (default: 3)
        per_page: Número de resultados
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{BASE_URL}/observations",
                params={
                    "user_login": username,
                    "lat": lat,
                    "lng": lng,
                    "radius": radius,
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
                "coordenadas": {"lat": lat, "lng": lng, "radius_km": radius},
                "total_observaciones": data.get("total_results"),
                "observaciones": observaciones
            }
            
    except Exception as e:
        return {"error": f"Error al obtener observaciones del usuario: {str(e)}"}


if __name__ == "__main__":
    mcp.run()