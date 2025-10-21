# MCP Server iNaturalist

Servidor MCP para consultar datos de biodiversidad de iNaturalist, **enfocado en el Humedal la Conejera, Bogotá**.

Este servidor proporciona herramientas para acceder a información sobre observaciones, especies, lugares y estadísticas de biodiversidad desde la API pública de iNaturalist usando **coordenadas geográficas** y radio de búsqueda.

## Herramientas Disponibles

El servidor expone las siguientes herramientas MCP:

### 1. `buscar_observaciones`

Busca observaciones en iNaturalist usando coordenadas geográficas.

**Parámetros:**
- `taxon_name` (opcional): Nombre del taxón (especie, género, familia, etc.)
- `lat` (float, default=4.8155): Latitud (Humedal la Conejera por defecto)
- `lng` (float, default=-74.0750): Longitud (Humedal la Conejera por defecto)
- `radius` (float, default=3.0): Radio de búsqueda en km
- `per_page` (int, default=10): Número de resultados (máximo 200)
- `order_by` (str, default="created_at"): Ordenar por 'created_at', 'observed_on', 'species_guess', 'votes'

**Ejemplo:**
```json
{
  "taxon_name": "Quercus",
  "lat": 4.8155,
  "lng": -74.0750,
  "radius": 5.0,
  "per_page": 20
}
```

**Retorna:** Lista de observaciones con ID, especie, nombre científico, fecha, lugar, usuario, URL de foto y URL directa, más las coordenadas usadas en la búsqueda.

---

### 2. `buscar_especies`

Busca información sobre especies y taxones en iNaturalist.

**Parámetros:**
- `nombre` (str, requerido): Nombre común o científico de la especie
- `rank` (opcional): Rango taxonómico (species, genus, family, order, class, phylum, kingdom)
- `is_active` (bool, default=True): Solo taxones activos (no sinónimos)
- `lat` (float, default=4.8155): Latitud (Humedal la Conejera por defecto)
- `lng` (float, default=-74.0750): Longitud (Humedal la Conejera por defecto)
- `radius` (float, default=3.0): Radio de búsqueda en km

**Ejemplo:**
```json
{
  "nombre": "Cuervillo cara pelada",
  "rank": "species",
  "lat": 4.8155,
  "lng": -74.0750,
  "radius": 3.0
}
```

**Retorna:** Lista de especies con ID, nombre científico, nombre común, rango, URL de Wikipedia, total de observaciones, foto y estado de conservación, más las coordenadas usadas en la búsqueda.

---

### 3. `obtener_lugares`

Obtiene información sobre lugares cercanos a las coordenadas especificadas.

**Parámetros:**
- `nombre_lugar` (opcional): Nombre específico del lugar a buscar
- `lat` (float, default=4.8155): Latitud (Humedal la Conejera por defecto)
- `lng` (float, default=-74.0750): Longitud (Humedal la Conejera por defecto)
- `radius` (float, default=5.0): Radio de búsqueda en km

**Ejemplo:**
```json
{
  "nombre_lugar": "Conejera",
  "lat": 4.8155,
  "lng": -74.0750,
  "radius": 5.0
}
```

**Retorna:** Lista de lugares con ID, nombre, tipo, bounding box GeoJSON y número de observaciones, más las coordenadas usadas.

---

### 4. `estadisticas_biodiversidad`

Obtiene estadísticas de biodiversidad en el área especificada.

**Parámetros:**
- `lat` (float, default=4.8155): Latitud (Humedal la Conejera por defecto)
- `lng` (float, default=-74.0750): Longitud (Humedal la Conejera por defecto)
- `radius` (float, default=3.0): Radio de búsqueda en km

**Ejemplo:**
```json
{
  "lat": 4.8155,
  "lng": -74.0750,
  "radius": 3.0
}
```

**Retorna:** Total de observaciones, total de especies, ubicación, y coordenadas con radio usado.

---

### 5. `observaciones_por_usuario`

Busca observaciones de un usuario específico en el área especificada.

**Parámetros:**
- `username` (str, requerido): Nombre de usuario en iNaturalist
- `lat` (float, default=4.8155): Latitud (Humedal la Conejera por defecto)
- `lng` (float, default=-74.0750): Longitud (Humedal la Conejera por defecto)
- `radius` (float, default=3.0): Radio de búsqueda en km
- `per_page` (int, default=10): Número de resultados

**Ejemplo:**
```json
{
  "username": "usuario_colombia",
  "lat": 4.8155,
  "lng": -74.0750,
  "radius": 3.0,
  "per_page": 15
}
```

**Retorna:** Usuario, total de observaciones, lista detallada de observaciones, y coordenadas con radio usado.

---

## Ubicación por Defecto: Humedal la Conejera

**Coordenadas:**
- Latitud: 4.8155° N
- Longitud: -74.0750° W
- Radio predeterminado: 3 km (varía según la función)

El Humedal la Conejera es un área protegida de importancia ecológica ubicada en Bogotá, Colombia. Todas las búsquedas por defecto se centran en esta ubicación.

Para buscar en otras ubicaciones, simplemente proporciona diferentes valores de `lat`, `lng` y `radius`.

---

## Estructura del Proyecto

```
mcp-server-inaturalist/
├── server.py           # Definición del servidor y herramientas MCP
├── main.py             # Punto de entrada del servidor
├── pyproject.toml      # Configuración del proyecto y dependencias
├── README.md           # Este archivo
└── .python-version     # Especificación de versión Python
```

## Notas Importantes

- El servidor usa la API pública de iNaturalist: `https://api.inaturalist.org/v1`
- **Todas las búsquedas usan coordenadas geográficas (lat, lng) con radio en km**
- Por defecto, todas las búsquedas están enfocadas en **Humedal la Conejera, Bogotá**
- Las llamadas a la API tienen un timeout de 30 segundos
- El servidor utiliza asyncio para manejar llamadas HTTP no bloqueantes


