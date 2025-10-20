# MCP Server iNaturalist

Servidor MCP para consultar datos de biodiversidad de iNaturalist, enfocado en Colombia.

Este servidor proporciona herramientas para acceder a información sobre observaciones, especies, lugares y estadísticas de biodiversidad desde la API pública de iNaturalist.

## Requisitos

- Python 3.13 o superior
- `uv` (gestor de paquetes y ambientes virtuales)

## Instalación

### 1. Clonar o preparar el proyecto

```bash
cd /Users/manglerojo/Desarollo/DATAR/ejercicios-orquestacion/MCP/mcp-server-inaturalist
```

### 2. Instalar dependencias con `uv`

```bash
# Instalar las dependencias del proyecto
uv sync
```

Esto creará un entorno virtual e instalará:
- `mcp[cli]>=1.18.0` - Framework MCP para crear servidores
- `httpx>=0.25.0` - Cliente HTTP asíncrono para consultas a la API

### 3. Ejecutar el servidor

```bash
# Opción 1: Ejecutar directamente con Python
uv run python -m main

# Opción 2: Usar el script de consola
uv run mcp-server-inaturalist

# Opción 3: Dentro del entorno virtual
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python -m main
```

## Herramientas Disponibles

El servidor expone las siguientes herramientas MCP:

### 1. `buscar_observaciones`

Busca observaciones en iNaturalist en Colombia.

**Parámetros:**
- `taxon_name` (opcional): Nombre del taxón (especie, género, familia, etc.)
- `place_id` (int, default=7562): ID del lugar (7562 es Colombia)
- `per_page` (int, default=10): Número de resultados (máximo 200)
- `order_by` (str, default="created_at"): Ordenar por 'created_at', 'observed_on', 'species_guess', 'votes'

**Ejemplo:**
```json
{
  "taxon_name": "Quercus",
  "place_id": 7562,
  "per_page": 20
}
```

**Retorna:** Lista de observaciones con ID, especie, nombre científico, fecha, lugar, usuario, URL de foto y URL directa.

---

### 2. `buscar_especies`

Busca información sobre especies y taxones en iNaturalist.

**Parámetros:**
- `nombre` (str, requerido): Nombre común o científico de la especie
- `rank` (opcional): Rango taxonómico (species, genus, family, order, class, phylum, kingdom)
- `is_active` (bool, default=True): Solo taxones activos (no sinónimos)

**Ejemplo:**
```json
{
  "nombre": "Jaguar",
  "rank": "species"
}
```

**Retorna:** Lista de especies con ID, nombre científico, nombre común, rango, URL de Wikipedia, total de observaciones, foto y estado de conservación.

---

### 3. `obtener_lugares_colombia`

Obtiene información sobre lugares y departamentos en Colombia.

**Parámetros:**
- `nombre_lugar` (opcional): Nombre del departamento o lugar a buscar

**Ejemplo:**
```json
{
  "nombre_lugar": "Cundinamarca"
}
```

**Retorna:** Lista de lugares con ID, nombre, tipo, bounding box GeoJSON y número de observaciones.

---

### 4. `estadisticas_biodiversidad_colombia`

Obtiene estadísticas generales de biodiversidad en Colombia.

**Parámetros:** Ninguno

**Ejemplo:**
```json
{}
```

**Retorna:** Total de observaciones, total de especies y país.

---

### 5. `observaciones_por_usuario`

Busca observaciones de un usuario específico en Colombia.

**Parámetros:**
- `username` (str, requerido): Nombre de usuario en iNaturalist
- `place_id` (int, default=7562): ID del lugar (7562 es Colombia)
- `per_page` (int, default=10): Número de resultados

**Ejemplo:**
```json
{
  "username": "usuario_colombia",
  "per_page": 15
}
```

**Retorna:** Usuario, total de observaciones y lista detallada de observaciones.

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
- Por defecto, todas las búsquedas están enfocadas en Colombia (place_id = 7562)
- Las llamadas a la API tienen un timeout de 30 segundos
- El servidor utiliza asyncio para manejar llamadas HTTP no bloqueantes

## Troubleshooting

### Error: "No module named 'mcp'"
Asegúrate de ejecutar dentro del entorno virtual de `uv`:
```bash
uv sync
uv run python -m main
```

### Error de timeout
Si obtienes errores de timeout, aumenta el timeout en las llamadas HTTP. Esto puede deberse a la velocidad de la conexión o a problemas en el servidor de iNaturalist.

### No se encuentran resultados
Verifica que:
- El nombre del taxón o usuario sea correcto
- La place_id sea válida (7562 para Colombia)
- La API de iNaturalist esté disponible

## Referencias

- [API iNaturalist](https://api.inaturalist.org/v1/)
- [MCP Documentation](https://modelcontextprotocol.io/)
