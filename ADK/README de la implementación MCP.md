# 🌿 Sistema de Agentes Multi-Especializados con MCP

Sistema inteligente para planificación de expediciones usando Google ADK (Agent Development Kit) y Model Context Protocol (MCP) para consultas avanzadas de biodiversidad colombiana.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4.svg)](https://ai.google.dev/adk)
[![MCP](https://img.shields.io/badge/MCP-1.1.2-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 ¿Qué hace este sistema?

Un asistente inteligente que coordina múltiples agentes especializados para ayudarte a planificar expediciones, combinando:

- 🌤️ **Información meteorológica** en tiempo real
- 🔢 **Cálculos logísticos** precisos
- 🦜 **Datos de biodiversidad** de iNaturalist Colombia

### ⭐ Novedad: Integración MCP

Ahora con capacidades avanzadas de búsqueda de biodiversidad:
- 📊 Estadísticas de toda Colombia
- 🔍 Búsqueda de especies específicas
- 🔎 Observaciones filtradas
- 👤 Historial de observadores

---

## 🚀 Inicio rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar API Key

Crea un archivo `.env`:

```bash
GOOGLE_API_KEY=tu_clave_aqui
```

> 💡 Obtén tu API key en: https://makersuite.google.com/app/apikey

### 3. Ejecutar servidor MCP (Terminal 1)

```bash
python servidor_mcp.py
```

### 4. Ejecutar sistema de agentes (Terminal 2)

```bash
python sistema_agentes_mejorado.py
```

---

## 📚 Documentación

| Documento | Descripción | Tiempo |
|-----------|-------------|--------|
| 📗 [INICIO_RAPIDO.md](INICIO_RAPIDO.md) | Guía de configuración | 5 min |
| 📋 [RESUMEN.md](RESUMEN.md) | Resumen de la integración | 5 min |
| 📘 [INTEGRACION_MCP.md](INTEGRACION_MCP.md) | Documentación completa | 15 min |
| 🏛️ [ARQUITECTURA.md](ARQUITECTURA.md) | Diseño técnico | 20 min |
| 📚 [INDICE.md](INDICE.md) | Índice navegable | - |

**👉 ¿Primera vez?** Empieza con [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

---

## 🎭 Los agentes

### 🎯 Coordinador
Analiza tu pregunta y delega a los agentes especializados.

### 🌤️ Meteorólogo
Consulta el clima actual. *Habla como un teólogo medieval.*

### 🔢 Matemático
Realiza cálculos logísticos precisos. *Muy técnico y puntual.*

### 🦜 Biólogo (⭐ Mejorado)
Consulta biodiversidad local y nacional. *Apasionado y educativo.*

**Nuevas capacidades:**
- Observaciones aleatorias de lugares (API REST - rápido)
- Búsquedas avanzadas de especies (MCP - potente)
- Estadísticas nacionales
- Consultas por usuario

---

## 💡 Ejemplos de uso

### Consulta simple

```python
"¿Qué especies hay en el Humedal La Conejera?"
```

**Respuesta:**
```
Observación en Humedal La Conejera, Bogotá:
Especie: Fulica americana (Focha Americana)
Fecha: 2025-01-15
Observador: naturalista123
```

### Consulta avanzada (MCP)

```python
"Dame información detallada sobre el Colibrí"
```

**Respuesta:**
```
🔍 Búsqueda de 'Colibrí':

1. Trochilidae
   Nombre común: Colibrí
   Rango: family
   Observaciones: 89,456

2. Colibri coruscans
   Nombre común: Colibrí Chillón
   Rango: species
   Observaciones: 12,345
```

### Coordinación completa

```python
"Quiero hacer una expedición al Humedal La Conejera.
 Necesito clima, peso total de 15+20+10+5 kg, y biodiversidad"
```

**El coordinador consulta a:**
- ✅ Meteorólogo → Clima actual
- ✅ Matemático → Peso total: 50 kg
- ✅ Biólogo → Especies observadas

---

## 🏗️ Arquitectura

```
Usuario → Coordinador → [Meteorólogo, Matemático, Biólogo]
                                               │
                        ┌──────────────────────┴─────────────┐
                        │                                    │
                        ▼                                    ▼
                   API REST                           Servidor MCP
                   (rápida)                           (avanzado)
                        │                                    │
                        └──────────────┬─────────────────────┘
                                       │
                                       ▼
                              iNaturalist API
```

**[Ver arquitectura completa →](ARQUITECTURA.md)**

---

## 📊 Comparación de herramientas

| Característica | API REST | Servidor MCP |
|----------------|----------|--------------|
| **Velocidad** | Rápida (~200ms) | Moderada (~3s) |
| **Alcance** | 1 lugar específico | Toda Colombia |
| **Resultados** | 1 observación | Múltiples resultados |
| **Ideal para** | Exploración rápida | Investigación detallada |
| **Información** | Observación aleatoria | Búsqueda filtrada |

---

## 🧪 Pruebas

Verifica que todo funcione:

```bash
python test_integracion_mcp.py
```

Ejecuta 4 pruebas de integración:
- ✅ Estadísticas de Colombia
- ✅ Búsqueda de especies
- ✅ Observaciones por especie
- ✅ Lugares de Colombia

---

## 📁 Estructura del proyecto

```
.
├── 🐍 Python
│   ├── sistema_agentes_mejorado.py  ⭐ Sistema con MCP
│   ├── servidor_mcp.py              Servidor MCP
│   ├── api_inaturalist.py           API REST
│   └── test_integracion_mcp.py      Tests
│
├── ⚙️ Configuración
│   ├── .env.example                 Plantilla configuración
│   ├── requirements.txt             Dependencias
│   └── .gitignore                   Git ignore
│
└── 📚 Documentación
    ├── README.md                    Este archivo
    ├── INICIO_RAPIDO.md             Guía de inicio
    ├── RESUMEN.md                   Resumen ejecutivo
    ├── INTEGRACION_MCP.md           Documentación completa
    ├── ARQUITECTURA.md              Diseño técnico
    └── INDICE.md                    Índice navegable
```

---

## 🛠️ Tecnologías

- **[Google ADK](https://ai.google.dev/adk)** - Agent Development Kit
- **[Gemini 2.0 Flash](https://ai.google.dev/)** - Modelo de IA de Google
- **[FastMCP](https://github.com/jlowin/fastmcp)** - Framework para servidores MCP
- **[FastAPI](https://fastapi.tiangolo.com/)** - API REST moderna
- **[iNaturalist](https://www.inaturalist.org/)** - Base de datos de biodiversidad

---

## 🎓 Aprende más

### Conceptos clave

**¿Qué es un Agente?**
Un sistema de IA que puede usar herramientas para completar tareas de forma autónoma.

**¿Qué es MCP?**
Model Context Protocol - Un estándar para conectar modelos de IA con fuentes de datos y herramientas.

**¿Por qué múltiples agentes?**
Especialización: cada agente domina su área, el coordinador los orquesta.

### Recursos externos

- 📖 [Documentación de Google ADK](https://ai.google.dev/adk)
- 📖 [Especificación MCP](https://modelcontextprotocol.io/)
- 📖 [API de iNaturalist](https://api.inaturalist.org/v1/docs/)

---

## 🔧 Personalización

### Cambiar personalidad de un agente

```python
agente_biologo = Agent(
    name="biologo",
    instruction="Tu nueva personalidad aquí...",
    tools=[consultar_biodiversidad, consultar_biodiversidad_avanzada]
)
```

### Agregar nueva herramienta

```python
def mi_herramienta(parametro: str) -> str:
    """Descripción de la herramienta"""
    # Tu lógica aquí
    return "resultado"

# Agregar al agente
agente_biologo = Agent(
    tools=[..., mi_herramienta]
)
```

**[Ver guía completa de extensión →](ARQUITECTURA.md#extensibilidad)**

---

## 🐛 Solución de problemas

### Error: "GOOGLE_API_KEY no encontrada"

**Solución:** Crea el archivo `.env` con tu API key.

```bash
echo "GOOGLE_API_KEY=tu_clave_aqui" > .env
```

### Error: "No se pudo conectar al servidor MCP"

**Solución:** Asegúrate de que `servidor_mcp.py` esté corriendo.

```bash
# Terminal 1
python servidor_mcp.py
```

### Las consultas MCP son lentas

**Normal:** Las consultas MCP tardan 2-4 segundos. Es el costo de iniciar un nuevo proceso.

**[Ver más soluciones →](INTEGRACION_MCP.md#resolucion-de-problemas)**

---

## 📈 Roadmap

### Versión 1.0 (Actual)
- ✅ Integración MCP completa
- ✅ Agente biólogo mejorado
- ✅ Documentación exhaustiva
- ✅ Tests de integración

### Versión 1.1 (Futuro)
- 🔄 Cache de consultas MCP
- 🎨 Dashboard web
- 📊 Visualización de datos
- 🌍 Soporte para más países

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas!

1. Lee [ARQUITECTURA.md](ARQUITECTURA.md) para entender el diseño
2. Mantén la simplicidad del proyecto
3. Documenta tus cambios
4. Prueba tu código

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **iNaturalist** - Por su increíble API de biodiversidad
- **Google** - Por el Agent Development Kit
- **FastMCP** - Por simplificar la implementación de MCP
- **Comunidad open source** - Por todas las herramientas utilizadas

---

## 📞 Contacto y soporte

- 📖 **Documentación:** Lee los archivos .md en este repositorio
- 🐛 **Issues:** Reporta bugs con información detallada
- 💡 **Ideas:** Comparte tus sugerencias de mejora

---

## ⭐ Características destacadas

- ✅ **Integración MCP:** Consultas avanzadas de biodiversidad
- ✅ **Multi-agente:** 4 agentes especializados trabajando juntos
- ✅ **Tiempo real:** Datos actualizados de clima y biodiversidad
- ✅ **Personalizable:** Fácil de extender y modificar
- ✅ **Bien documentado:** 5 archivos de documentación
- ✅ **Código limpio:** Simple y mantenible
- ✅ **Tests incluidos:** Verifica que todo funcione

---

## 🌟 ¿Por qué este proyecto?

Este sistema demuestra cómo:
- 🎯 Coordinar múltiples agentes especializados
- 🔌 Integrar MCP para capacidades avanzadas
- 🏗️ Diseñar una arquitectura modular y extensible
- 📚 Documentar un proyecto técnico exhaustivamente
- ⚡ Balancear simplicidad y funcionalidad

---

<div align="center">

**🌿 ¡Explora la biodiversidad colombiana con IA! 🇨🇴**

[Documentación](INDICE.md) • [Inicio Rápido](INICIO_RAPIDO.md) • [Arquitectura](ARQUITECTURA.md)

---

*Hecho con ❤️ para la comunidad de conservación y tecnología*

</div>
