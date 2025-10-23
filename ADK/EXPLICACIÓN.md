# Explicación del Contenido de la Carpeta

Esta carpeta contiene un sistema de agentes multi-especializados para la planificación de expediciones. El sistema utiliza el Agent Development Kit (ADK) de Google y el modelo Gemini para coordinar a varios agentes especializados que proporcionan información sobre el clima, la logística y la biodiversidad.

## Componentes Principales

A continuación se describen los archivos más importantes de la carpeta:

*   **`sistema_agentes.py`**: Este es el script principal que define y orquesta a los agentes. Crea un agente coordinador que delega las tareas a tres agentes especializados:
    *   **Meteorólogo:** Proporciona información meteorológica utilizando la API de `wttr.in`.
    *   **Matemático:** Realiza cálculos logísticos, como el peso total del equipaje.
    *   **Biólogo:** Ofrece datos sobre la biodiversidad del lugar de la expedición, utilizando una API local de iNaturalist.

*   **`api_inaturalist.py`**: Es una API REST construida con FastAPI que sirve como intermediario para obtener datos de iNaturalist. Actualmente, está configurada para obtener observaciones del Humedal La Conejera en Bogotá.

*   **`servidor_mcp.py`**: Este script implementa un servidor de Model Context Protocol (MCP) que permite realizar consultas más avanzadas a la API de iNaturalist. Esto incluye la búsqueda de especies, la obtención de estadísticas y el filtrado de observaciones.

*   **`sistema_agentes_con_mcp.py`**: Una versión mejorada del sistema de agentes que integra el cliente MCP para comunicarse con `servidor_mcp.py` y realizar consultas de biodiversidad más complejas.

*   **`test_integracion_mcp.py`**: Un script de pruebas para verificar la correcta integración y funcionamiento del servidor MCP.

*   **`requirements.txt`**: Este archivo lista todas las dependencias de Python necesarias para ejecutar el proyecto.

*   **Archivos de Documentación (`.md`)**:
    *   **`README.md`**: Proporciona una introducción general al proyecto, sus características y cómo utilizarlo.
    *   **`ARQUITECTURA de MCP.md`**: Ofrece una descripción detallada de la arquitectura del sistema, con diagramas de flujo y explicaciones sobre las decisiones de diseño.
    *   **`README de la implementación MCP.md`**: Se centra en la integración de MCP, explicando sus ventajas y cómo utilizar las nuevas funcionalidades.

## Arquitectura

El sistema sigue un patrón de coordinador, donde un agente principal recibe las consultas del usuario y las descompone en tareas más pequeñas que son asignadas a los agentes especializados.

Para la consulta de datos de biodiversidad, se utilizan dos enfoques:

1.  **API REST (`api_inaturalist.py`)**: Para consultas rápidas y sencillas sobre un lugar específico.
2.  **Servidor MCP (`servidor_mcp.py`)**: Para consultas más complejas y avanzadas que requieren una mayor flexibilidad y capacidad de búsqueda.

Esta arquitectura dual permite un equilibrio entre la velocidad y la potencia de las consultas.

## Uso

Para ejecutar el sistema, sigue estos pasos:

1.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar la API Key de Google:**
    Crea un archivo `.env` en la raíz del proyecto y añade tu clave de API de Google:
    ```
    GOOGLE_API_KEY="tu_api_key_aqui"
    ```

3.  **Iniciar los servidores:**
    *   Para la funcionalidad básica, inicia la API de iNaturalist:
        ```bash
        python api_inaturalist.py
        ```
    *   Para la funcionalidad avanzada con MCP, inicia el servidor MCP:
        ```bash
        python servidor_mcp.py
        ```

4.  **Ejecutar el sistema de agentes:**
    *   Para la versión básica:
        ```bash
        python sistema_agentes.py
        ```
    *   Para la versión con MCP:
        ```bash
        python sistema_agentes_con_mcp.py
        ```

## Personalización

El sistema está diseñado para ser extensible. Puedes añadir nuevos agentes, herramientas o funcionalidades modificando los scripts principales. La documentación en los archivos `.md` proporciona una guía detallada sobre cómo realizar estas personalizaciones.
