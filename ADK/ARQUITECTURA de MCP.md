# 🏛️ ARQUITECTURA DEL SISTEMA

## Vista general

```
┌────────────────────────────────────────────────────────────────────┐
│                         USUARIO                                    │
│                  (Hace preguntas sobre expediciones)               │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│                    AGENTE COORDINADOR                              │
│                    (Gemini 2.0 Flash)                              │
│                                                                    │
│  Analiza la pregunta y decide qué agentes necesita:                │
│  ¿Clima? → Meteorólogo                                             │
│  ¿Cálculos? → Matemático                                           │
│  ¿Biodiversidad? → Biólogo                                         │
└─────────┬──────────────────────┬──────────────────────┬────────────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│   METEORÓLOGO    │  │   MATEMÁTICO     │  │   BIÓLOGO ⭐         │
│   (Gemini 2.0)   │  │   (Gemini 2.0)   │  │   (Gemini 2.0)       │
├──────────────────┤  ├──────────────────┤  ├──────────────────────┤
│                  │  │                  │  │                      │
│ Herramientas:    │  │ Herramientas:    │  │ Herramientas:        │
│ • consultar_     │  │ • calcular_peso_ │  │ • consultar_         │
│   clima          │  │   total          │  │   biodiversidad      │
│                  │  │ • calcular_      │  │                      │
│                  │  │   distancia      │  │ • consultar_         │
│                  │  │ • raiz_cuadrada  │  │   biodiversidad_     │
│                  │  │                  │  │   avanzada (NUEVA)   │
└────────┬─────────┘  └──────────────────┘  └──────────┬───────────┘
         │                                             │
         ▼                                             │
┌──────────────────┐                                   │
│   wttr.in API    │                                   │
│   (Clima)        │                                   │
└──────────────────┘                                   │
                                                       │
        ┌──────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│              DECISIÓN DE HERRAMIENTA                        │
│                                                             │
│  ¿Consulta simple de un lugar específico?                   │
│         │                       │                           │
│        SÍ                      NO                           │
│         │                       │                           │
│         ▼                       ▼                           │
│  ┌──────────────┐      ┌──────────────────────────┐         │
│  │  API REST    │      │  SERVIDOR MCP            │         │
│  │  (FastAPI)   │      │  (FastMCP + Cliente)     │         │
│  └──────────────┘      └──────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌──────────────────┐         ┌──────────────────────────────┐
│  api_inaturalist │         │     servidor_mcp.py          │
│  .py             │         │                              │
│                  │         │  ┌────────────────────────┐  │
│  Endpoints:      │         │  │ Herramientas MCP:      │  │
│  • /             │         │  │                        │  │
│  • /observaciones│         │  │ • estadisticas_        │  │
│    /aleatoria    │         │  │   biodiversidad        │  │
│  • /health       │         │  │                        │  │
│                  │         │  │ • buscar_especies      │  │
│                  │         │  │                        │  │
│                  │         │  │ • buscar_              │  │
│                  │         │  │   observaciones        │  │
│                  │         │  │                        │  │
│                  │         │  │ • obtener_lugares      │  │
│                  │         │  │                        │  │
│                  │         │  │ • observaciones_por_   │  │
│                  │         │  │   usuario              │  │
│                  │         │  └────────────────────────┘  │
└────────┬─────────┘         └──────────────┬───────────────┘
         │                                  │
         │                                  │
         └──────────┬───────────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │  iNaturalist API     │
         │  (api.inaturalist    │
         │   .org/v1)           │
         │                      │
         │  Base de datos de    │
         │  observaciones de    │
         │  biodiversidad       │
         │  mundial             │
         └──────────────────────┘
```

---

## Flujo de datos detallado

### 1. Consulta simple (API REST)

```
Usuario: "¿Qué especies hay en el Humedal La Conejera?"
   │
   ▼
Coordinador: "Es una pregunta de biodiversidad"
   │
   ▼
Biólogo: "Es un lugar específico, usaré API REST"
   │
   ▼
consultar_biodiversidad("Humedal La Conejera", "Bogotá")
   │
   ▼
GET http://localhost:8000/observaciones/aleatoria
   │
   ▼
api_inaturalist.py consulta iNaturalist API
   │
   ▼
GET https://api.inaturalist.org/v1/observations
   │
   ▼
Respuesta: {especie, nombre_comun, fecha, usuario}
   │
   ▼
Biólogo formatea respuesta
   │
   ▼
Usuario recibe: "Observación en Humedal La Conejera..."
```

**Tiempo total: ~200-500ms**

---

### 2. Consulta avanzada (Servidor MCP)

```
Usuario: "Dame información detallada sobre el Colibrí"
   │
   ▼
Coordinador: "Es una pregunta de biodiversidad"
   │
   ▼
Biólogo: "Necesito búsqueda avanzada, usaré MCP"
   │
   ▼
consultar_biodiversidad_avanzada("buscar_especie", "Colibrí")
   │
   ▼
1. Iniciar StdioServerParameters
   │
   ▼
2. Crear ClientSession con servidor_mcp.py
   │
   ▼
3. session.initialize()
   │
   ▼
4. session.call_tool("buscar_especies", {"nombre": "Colibrí"})
   │
   ▼
servidor_mcp.py ejecuta buscar_especies()
   │
   ▼
GET https://api.inaturalist.org/v1/taxa?q=Colibrí
   │
   ▼
Respuesta: [{id, nombre_cientifico, nombre_comun, rango, ...}, ...]
   │
   ▼
servidor_mcp.py formatea datos
   │
   ▼
Cliente MCP recibe JSON
   │
   ▼
_consultar_mcp_async procesa y formatea
   │
   ▼
Biólogo recibe texto formateado
   │
   ▼
Usuario recibe: "🔍 Búsqueda de 'Colibrí':\n1. Trochilidae..."
```

**Tiempo total: ~2-4 segundos**

---

### 3. Coordinación completa

```
Usuario: "Expedición a Humedal La Conejera:
         clima + peso (15,20,10,5 kg) + biodiversidad"
   │
   ▼
Coordinador analiza: "Necesito 3 agentes"
   │
   ├──────────────────┬───────────────────┐
   ▼                  ▼                   ▼
Meteorólogo       Matemático          Biólogo
   │                  │                   │
   ▼                  ▼                   ▼
consultar_clima   calcular_peso_     consultar_
("Bogotá")        total(15,20,       biodiversidad(
                  10,5)               "Humedal...")
   │                  │                   │
   ▼                  ▼                   ▼
wttr.in API       Cálculo local       API REST
   │                  │                   │
   └──────────────────┴───────────────────┘
                      │
                      ▼
           Coordinador integra resultados
                      │
                      ▼
           Usuario recibe recomendación completa
```

---

## Componentes del sistema

### 🎯 Agentes (Google ADK)

| Agente | Modelo | Personalidad | Herramientas |
|--------|--------|--------------|--------------|
| **Coordinador** | Gemini 2.0 Flash | Organizado, decisivo | Ninguna (coordina) |
| **Meteorólogo** | Gemini 2.0 Flash | Medieval, teológico | consultar_clima |
| **Matemático** | Gemini 2.0 Flash | Técnico, preciso | cálculos varios |
| **Biólogo** | Gemini 2.0 Flash | Apasionado, educativo | biodiversidad + MCP |

### 🔧 Herramientas

| Herramienta | Tipo | Velocidad | Alcance |
|-------------|------|-----------|---------|
| `consultar_clima` | HTTP | Rápida | Ciudad específica |
| `calcular_*` | Local | Instantánea | N/A |
| `consultar_biodiversidad` | HTTP/REST | Rápida | 1 lugar |
| `consultar_biodiversidad_avanzada` | MCP | Moderada | Colombia |

### 📡 Servidores

| Servidor | Puerto | Protocolo | Función |
|----------|--------|-----------|---------|
| **api_inaturalist.py** | 8000 | HTTP/REST | Obs. aleatorias |
| **servidor_mcp.py** | stdio | MCP | Búsquedas avanzadas |

---

## Comunicación entre componentes

### Google ADK ↔ Herramientas

```python
# ADK llama herramientas automáticamente
runner.run_async(
    user_id="...",
    session_id="...",
    new_message=Content(...)
)

# ADK detecta que necesita llamar una herramienta
↓
# ADK ejecuta la función Python
result = consultar_biodiversidad_avanzada(...)

# ADK integra el resultado en el contexto del agente
↓
# Agente usa el resultado para responder
```

### Cliente MCP ↔ Servidor MCP

```python
# 1. Iniciar servidor como subproceso
server_params = StdioServerParameters(
    command="python",
    args=["servidor_mcp.py"]
)

# 2. Crear cliente stdio
async with stdio_client(server_params) as (read, write):

    # 3. Crear sesión
    async with ClientSession(read, write) as session:

        # 4. Inicializar
        await session.initialize()

        # 5. Llamar herramienta
        result = await session.call_tool(
            "buscar_especies",
            arguments={"nombre": "Colibrí"}
        )

        # 6. Procesar resultado
        data = json.loads(result.content[0].text)
```

---

## Ciclo de vida de una consulta

```
┌─────────────────────────────────────────────────────────┐
│ 1. INICIALIZACIÓN                                       │
│    • Cargar .env                                        │
│    • Configurar API key de Google                       │
│    • Crear sesiones de agentes                          │
│    • Crear runners                                      │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 2. RECEPCIÓN DE CONSULTA                                │
│    • Usuario hace pregunta                              │
│    • Crear Content con la pregunta                      │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 3. ANÁLISIS POR COORDINADOR                             │
│    • Identificar tipo de información necesaria          │
│    • Decidir qué agentes involucrar                     │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 4. DELEGACIÓN A SUBAGENTES                              │
│    • Enviar subtareas a cada agente                     │
│    • Cada agente ejecuta sus herramientas               │
│    • Recolectar respuestas                              │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 5. EJECUCIÓN DE HERRAMIENTAS                            │
│    A. Si es API REST:                                   │
│       • HTTP GET a localhost:8000                       │
│       • Respuesta inmediata                             │
│    B. Si es MCP:                                        │
│       • Iniciar servidor MCP                            │
│       • Crear sesión                                    │
│       • Llamar herramienta                              │
│       • Procesar respuesta JSON                         │
│       • Cerrar sesión                                   │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 6. INTEGRACIÓN DE RESULTADOS                            │
│    • Coordinador recibe todas las respuestas            │
│    • Analiza y sintetiza información                    │
│    • Crea recomendación final                           │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│ 7. RESPUESTA AL USUARIO                                 │
│    • Formatear respuesta                                │
│    • Enviar al usuario                                  │
└─────────────────────────────────────────────────────────┘
```

---

## Decisiones arquitectónicas

### ¿Por qué dos sistemas (API REST + MCP)?

| Aspecto | API REST | MCP |
|---------|----------|-----|
| **Propósito** | Observaciones rápidas | Búsquedas complejas |
| **Velocidad** | Rápida (200ms) | Moderada (3s) |
| **Complejidad** | Simple | Avanzada |
| **Alcance** | 1 lugar | Toda Colombia |
| **Cuando usar** | Exploración | Investigación |

### ¿Por qué Stdio en lugar de HTTP para MCP?

✅ **Ventajas:**
- Más simple de implementar
- No requiere gestión de puertos
- Estándar en MCP
- Aislamiento de procesos

❌ **Desventajas:**
- Más lento (inicio de proceso)
- No se puede cachear fácilmente

**Decisión:** Elegimos simplicidad sobre velocidad.

---

## Extensibilidad

### Agregar nuevas herramientas al biólogo

```python
def mi_nueva_herramienta(parametro: str) -> str:
    """Mi descripción"""
    # Tu lógica aquí
    return "resultado"

agente_biologo = Agent(
    name="biologo",
    tools=[
        consultar_biodiversidad,
        consultar_biodiversidad_avanzada,
        mi_nueva_herramienta  # ← Agregar aquí
    ]
)
```

### Agregar nuevas consultas MCP

```python
# En _consultar_mcp_async:
elif tipo_consulta == "mi_nueva_consulta":
    result = await session.call_tool(
        "mi_herramienta_mcp",
        arguments={"param": valor}
    )
    # Procesar...
```

### Agregar nuevo agente

```python
agente_nuevo = Agent(
    name="mi_agente",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[mi_herramienta]
)

runner_nuevo = Runner(
    agent=agente_nuevo,
    app_name=APP_NAME,
    session_service=session_service
)
```

---

## Patrones de diseño utilizados

### 1. **Patrón Coordinador**
- Agente principal delega tareas
- Subagentes especializados

### 2. **Patrón Wrapper**
- `consultar_biodiversidad_avanzada` encapsula MCP
- Oculta complejidad al agente

### 3. **Patrón Cliente-Servidor**
- API REST: cliente HTTP
- MCP: cliente stdio

### 4. **Patrón Herramienta**
- Funciones simples que el agente puede llamar
- Decorador @mcp.tool() en servidor

---

## Seguridad y buenas prácticas

### ✅ Implementado

- API key en .env (no hardcodeado)
- Manejo de errores en todas las herramientas
- Timeouts en requests HTTP
- Validación de parámetros
- Logging apropiado

### 🔒 Recomendaciones adicionales

- Limitar rate de consultas a APIs
- Validar entrada de usuario
- Sanitizar respuestas de APIs
- Implementar cache para consultas frecuentes

---

**Esta arquitectura balancea simplicidad, funcionalidad y extensibilidad** 🎯
