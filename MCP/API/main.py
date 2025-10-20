"""
API REST para consultar observaciones de iNaturalist Colombia
Consulta observaciones aleatorias del Humedal La Conejera en tiempo real
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
import random
from typing import Optional

# Crear aplicación FastAPI
app = FastAPI(
    title="iNaturalist API",
    description="API REST para consultar observaciones de iNaturalist Colombia",
    version="1.0.0"
)

# Modelos de respuesta
class Observacion(BaseModel):
    """Modelo de una observación"""
    exitoso: bool
    lugar: str
    ciudad: str
    especie: str
    nombre_comun: str
    fecha_observacion: str
    usuario: str

class Error(BaseModel):
    """Modelo de error"""
    exitoso: bool
    error: str


@app.get("/", tags=["Info"])
async def root():
    """Endpoint raíz que retorna información de la API"""
    return {
        "nombre": "iNaturalist API",
        "version": "1.0.0",
        "descripcion": "API REST para consultar observaciones de iNaturalist Colombia",
        "endpoints": {
            "info": "/",
            "observaciones_aleatorias": "/observaciones/aleatoria",
            "documentacion": "/docs"
        }
    }


@app.get("/observaciones/aleatoria", response_model=Observacion, tags=["Observaciones"])
async def obtener_observacion_aleatoria(
    lugar: str = Query("Humedal La Conejera", description="Lugar a consultar"),
    ciudad: str = Query("Bogotá", description="Ciudad")
):
    """
    Obtiene una observación aleatoria de iNaturalist para un lugar específico
    
    - **lugar**: Nombre del lugar (default: Humedal La Conejera)
    - **ciudad**: Nombre de la ciudad (default: Bogotá)
    
    Retorna una observación aleatoria del lugar especificado
    """
    try:
        # Coordenadas del Humedal La Conejera en Bogotá
        coordenadas = {
            "Humedal La Conejera": {"lat": 4.7519, "lon": -74.0841, "radio": 1000}
        }
        
        if lugar not in coordenadas:
            raise HTTPException(
                status_code=400,
                detail=f"Lugar '{lugar}' no configurado. Lugares disponibles: {list(coordenadas.keys())}"
            )
        
        coords = coordenadas[lugar]
        
        # Construir URL y parámetros para la API de iNaturalist
        url = "https://api.inaturalist.org/v1/observations"
        params = {
            "lat": coords["lat"],
            "lng": coords["lon"],
            "radius": coords["radio"],
            "quality_grade": "research",
            "per_page": 20,
            "order_by": "created_at",
            "order": "desc"
        }
        
        # Hacer consulta a la API
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        datos = response.json()
        observaciones = datos.get("results", [])
        
        if not observaciones:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron observaciones en {lugar}"
            )
        
        # Seleccionar una observación al azar
        observacion_aleatoria = random.choice(observaciones)
        
        # Extraer información de forma segura
        especie = observacion_aleatoria.get("taxon", {})
        especie_nombre = especie.get("name") if especie else None
        especie_nombre = especie_nombre if especie_nombre else "Desconocida"
        
        nombre_comun = especie.get("preferred_common_name") if especie else None
        nombre_comun = nombre_comun if nombre_comun else "N/A"
        
        fecha = observacion_aleatoria.get("observed_on")
        fecha = fecha if fecha else "Desconocida"
        
        usuario_obj = observacion_aleatoria.get("user")
        usuario_nombre = usuario_obj.get("name") if usuario_obj and isinstance(usuario_obj, dict) else None
        usuario_nombre = usuario_nombre if usuario_nombre else "Anónimo"
        
        return Observacion(
            exitoso=True,
            lugar=lugar,
            ciudad=ciudad,
            especie=especie_nombre,
            nombre_comun=nombre_comun,
            fecha_observacion=fecha,
            usuario=usuario_nombre
        )
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Tiempo de espera agotado al consultar iNaturalist"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Error de conexión al consultar iNaturalist"
        )
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error al consultar iNaturalist: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@app.get("/health", tags=["Info"])
async def health_check():
    """Verificar que el servidor está funcionando"""
    return {"status": "OK", "servicio": "iNaturalist API"}
