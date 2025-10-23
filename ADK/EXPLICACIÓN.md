# Explicación Pedagógica del Proyecto: Asistente de Expediciones con IA

¡Bienvenido al proyecto de Asistente de Expediciones! Esta guía te llevará paso a paso a través de la arquitectura, los componentes y el funcionamiento de este sistema de inteligencia artificial.

## 1. ¿Qué es este proyecto?

Imagina que estás planeando una expedición a un parque natural. Necesitas saber el clima, calcular el peso de tu equipo y conocer qué animales y plantas podrías encontrar. Este proyecto es un **asistente virtual** que hace todo eso por ti.

Utiliza un equipo de **agentes de IA especializados** (como un meteorólogo, un matemático y un biólogo) que colaboran para darte una respuesta completa. El sistema está construido con el **Agent Development Kit (ADK) de Google** y el modelo de lenguaje **Gemini**.

## 2. La Arquitectura: Un Equipo de Especialistas

El sistema funciona como un equipo de expertos coordinado por un jefe de proyecto.

### El Coordinador (El Jefe de Equipo)

- **Archivo:** `sistema_agentes.py`, `sistema_agentes_con_mcp.py`
- **Función:** Es el cerebro de la operación. Cuando haces una pregunta (ej: "Planeo una expedición a la selva"), el coordinador la analiza y decide qué especialistas necesita. No responde directamente, sino que delega las tareas.

### Los Especialistas (Los Miembros del Equipo)

1.  **Agente Meteorólogo:**
    - **Tarea:** Dar el pronóstico del tiempo.
    - **Herramienta:** Se conecta a la API pública `wttr.in` para obtener datos del clima en tiempo real.
    - **Personalidad:** Habla como un teólogo medieval, ¡dando un toque divertido!

2.  **Agente Matemático:**
    - **Tarea:** Realizar cálculos logísticos.
    - **Herramientas:** Funciones para sumar pesos, calcular distancias, etc.
    - **Personalidad:** Es muy técnico y preciso.

3.  **Agente Biólogo (El más avanzado):**
    - **Tarea:** Informar sobre la biodiversidad.
    - **Herramientas:** Este agente tiene dos formas de obtener datos de la plataforma **iNaturalist**:
        1.  **API REST (Rápida y Simple):** Para consultas sencillas como "¿Qué hay en el Humedal La Conejera?". Utiliza el servidor `api_inaturalist.py`.
        2.  **Servidor MCP (Potente y Avanzado):** Para preguntas complejas como "Busca información sobre el 'Oso de Anteojos' en toda Colombia". Utiliza el `servidor_mcp.py`.

![Arquitectura](https://i.imgur.com/9k8y2yD.png)

### ¿Por qué dos sistemas para el biólogo?

Esta arquitectura dual es una decisión clave:

- La **API REST** es como una llamada telefónica rápida: ideal para una pregunta específica y veloz.
- El **Servidor MCP** (Model Context Protocol) es como enviar un investigador a una biblioteca: tarda un poco más, pero puede realizar búsquedas profundas y complejas.

Esto le da al sistema un balance perfecto entre **velocidad y potencia**.

## 3. Descripción de los Archivos del Proyecto

Aquí tienes un mapa de los archivos más importantes:

- 📜 **`README.md` y otros `.md`:**
  - Tu punto de partida. Contienen la documentación general, diagramas de arquitectura (`ARQUITECTURA de MCP.md`) y guías de uso.

- 🐍 **Scripts Principales (`.py`):**
  - **`sistema_agentes.py`:** La versión original del sistema que orquesta a los agentes y usa la API REST para el biólogo.
  - **`sistema_agentes_con_mcp.py`:** La versión **mejorada** que le da al biólogo acceso al potente servidor MCP.
  - **`agente_biologo_activo.py`:** Un script para "chatear" directamente con el agente biólogo y probar sus capacidades avanzadas.

- 📡 **Servidores:**
  - **`api_inaturalist.py`:** Un pequeño servidor web (hecho con FastAPI) que responde a las consultas simples de biodiversidad. Es una puerta de enlace a iNaturalist.
  - **`servidor_mcp.py`:** El servidor avanzado que expone herramientas complejas (búsqueda de especies, estadísticas, etc.) a través del protocolo MCP.

- 🧪 **Pruebas:**
  - **`test_integracion_mcp.py`:** Un script fundamental para verificar que el servidor MCP funciona correctamente antes de ejecutar todo el sistema.

- ⚙️ **Configuración:**
  - **`requirements.txt`:** La lista de "ingredientes" (librerías de Python) que necesitas instalar.
  - **`.env`:** Un archivo (que debes crear) para guardar tu clave de API de Google de forma segura.

## 4. ¿Cómo Ponerlo en Marcha? (Guía Rápida)

Sigue estos pasos para ver la magia en acción:

1.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configura tu API Key:**
    - Crea un archivo llamado `.env`.
    - Dentro, escribe: `GOOGLE_API_KEY="tu_clave_secreta_de_google"`

3.  **Ejecuta la versión que prefieras:**

    - **Opción A: Sistema Básico (con API REST)**
      1.  En una terminal, inicia el servidor simple: `python api_inaturalist.py`
      2.  En otra terminal, ejecuta el sistema: `python sistema_agentes.py`

    - **Opción B: Sistema Avanzado (con MCP)**
      1.  En una terminal, inicia el servidor avanzado: `python servidor_mcp.py`
      2.  En otra terminal, ejecuta el sistema mejorado: `python sistema_agentes_con_mcp.py`

## 5. Personalización y Futuro

Este proyecto es un punto de partida. Aquí tienes algunas ideas para extenderlo:

- **Añadir un nuevo agente:** ¿Qué tal un "Agente Geólogo" que informe sobre tipos de terreno?
- **Crear nuevas herramientas:** Podrías añadir una herramienta al matemático para calcular raciones de comida.
- **Mejorar las personalidades:** ¡Haz que los agentes sean aún más únicos!

Esperamos que esta explicación te haya sido de gran utilidad para entender a fondo el proyecto. ¡Ahora estás listo para explorar, experimentar y expandir sus capacidades!