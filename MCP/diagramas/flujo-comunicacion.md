# Flujo de Comunicación Cliente-Servidor MCP

## Diagrama de Flujo Detallado

```mermaid
flowchart TD
    A[Inicio Cliente] --> B[Crear Conexión MCP]
    B --> C[Handshake Inicial]
    C --> D{¿Conexión Exitosa?}
    
    D -->|No| E[Error de Conexión]
    D -->|Sí| F[Cliente Listo]
    
    F --> G[Seleccionar Operación]
    G --> H{Tipo de Operación}
    
    H -->|Herramientas| I[Listar Herramientas]
    H -->|Recursos| J[Listar Recursos]
    H -->|Prompts| K[Listar Prompts]
    H -->|Ejecutar| L[Invocar Herramienta]
    
    I --> M[Enviar Solicitud]
    J --> M
    K --> M
    L --> N[Enviar Parámetros]
    
    M --> O[Servidor Procesa]
    N --> O
    
    O --> P{Tipo de Respuesta}
    P -->|Éxito| Q[Procesar Resultado]
    P -->|Error| R[Manejar Error]
    
    Q --> S[Mostrar Resultado]
    R --> T[Mostrar Error]
    
    S --> U{¿Continuar?}
    T --> U
    U -->|Sí| G
    U -->|No| V[Cerrar Conexión]
    
    V --> W[Fin]
    E --> W
    
    style A fill:#e8f5e8
    style W fill:#ffe8e8
    style E fill:#ffcccc
    style Q fill:#e8f8e8
    style R fill:#ffe8e8
```

## Secuencia de Mensajes Detallada

```mermaid
sequenceDiagram
    participant C as Cliente
    participant T as Transport
    participant S as Servidor
    participant H as Herramienta
    
    Note over C,H: Fase 1: Establecimiento de Conexión
    C->>T: 1. Crear conexión TCP/WebSocket
    T->>S: 2. Conectar a servidor MCP
    S->>T: 3. Aceptar conexión
    T->>C: 4. Conexión establecida
    
    Note over C,H: Fase 2: Handshake MCP
    C->>S: 5. {"jsonrpc": "2.0", "method": "initialize", "params": {...}}
    S->>C: 6. {"jsonrpc": "2.0", "result": {"capabilities": {...}}}
    C->>S: 7. {"jsonrpc": "2.0", "method": "initialized"}
    
    Note over C,H: Fase 3: Descubrimiento de Capacidades
    C->>S: 8. {"jsonrpc": "2.0", "method": "tools/list"}
    S->>C: 9. {"jsonrpc": "2.0", "result": {"tools": [...]}}
    
    C->>S: 10. {"jsonrpc": "2.0", "method": "resources/list"}
    S->>C: 11. {"jsonrpc": "2.0", "result": {"resources": [...]}}
    
    Note over C,H: Fase 4: Ejecución de Herramienta
    C->>S: 12. {"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "sumar", "arguments": {"a": 5, "b": 3}}}
    S->>H: 13. Ejecutar herramienta "sumar"
    H->>S: 14. Resultado: 8
    S->>C: 15. {"jsonrpc": "2.0", "result": {"content": [{"type": "text", "text": "8"}]}}
    
    Note over C,H: Fase 5: Cierre de Conexión
    C->>S: 16. {"jsonrpc": "2.0", "method": "shutdown"}
    S->>C: 17. {"jsonrpc": "2.0", "result": null}
    C->>T: 18. Cerrar conexión
```

## Tipos de Mensajes JSON-RPC

### 1. Mensajes de Inicialización

**Cliente → Servidor (initialize)**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "mi-cliente-mcp",
      "version": "1.0.0"
    }
  }
}
```

**Servidor → Cliente (response)**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {
        "listChanged": true
      }
    },
    "serverInfo": {
      "name": "mi-servidor-mcp",
      "version": "1.0.0"
    }
  }
}
```

### 2. Mensajes de Herramientas

**Listar herramientas**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

**Respuesta de herramientas**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "sumar",
        "description": "Suma dos números",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
          },
          "required": ["a", "b"]
        }
      }
    ]
  }
}
```

**Invocar herramienta**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "sumar",
    "arguments": {
      "a": 5,
      "b": 3
    }
  }
}
```

**Respuesta de herramienta**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "8"
      }
    ]
  }
}
```

## Estados del Cliente

```mermaid
stateDiagram-v2
    [*] --> Desconectado
    Desconectado --> Conectando : Crear conexión
    Conectando --> Conectado : Conexión exitosa
    Conectando --> Desconectado : Error de conexión
    Conectado --> Inicializando : Enviar initialize
    Inicializando --> Listo : Recibir capabilities
    Inicializando --> Error : Error de inicialización
    Listo --> Ejecutando : Invocar herramienta
    Ejecutando --> Listo : Recibir resultado
    Ejecutando --> Error : Error de ejecución
    Listo --> Desconectado : Cerrar conexión
    Error --> Desconectado : Limpiar recursos
```

## Manejo de Errores

### Tipos de Errores Comunes

1. **Error de Conexión**
   - Servidor no disponible
   - Puerto incorrecto
   - Firewall bloqueando

2. **Error de Protocolo**
   - Versión incompatible
   - Formato JSON inválido
   - Método no soportado

3. **Error de Herramienta**
   - Herramienta no encontrada
   - Parámetros inválidos
   - Error de ejecución

4. **Error de Recurso**
   - Recurso no disponible
   - Permisos insuficientes
   - Archivo no encontrado

### Flujo de Manejo de Errores

```mermaid
flowchart TD
    A[Error Detectado] --> B{Tipo de Error}
    B -->|Conexión| C[Reintentar conexión]
    B -->|Protocolo| D[Validar formato]
    B -->|Herramienta| E[Verificar parámetros]
    B -->|Recurso| F[Verificar permisos]
    
    C --> G{¿Reintento exitoso?}
    D --> H[Enviar error al usuario]
    E --> H
    F --> H
    
    G -->|Sí| I[Continuar operación]
    G -->|No| J[Abortar operación]
    
    I --> K[Continuar flujo normal]
    J --> L[Notificar error final]
    H --> M[Mostrar mensaje de error]
    
    style A fill:#ffebee
    style L fill:#ffcdd2
    style M fill:#ffcdd2
```

## Mejores Prácticas

### Para el Cliente
- Implementar timeout en las conexiones
- Validar respuestas antes de procesarlas
- Manejar reconexión automática
- Logging detallado para debugging

### Para el Servidor
- Validar todos los parámetros de entrada
- Implementar rate limiting
- Proporcionar mensajes de error descriptivos
- Mantener logs de auditoría

### Para la Comunicación
- Usar compresión para mensajes grandes
- Implementar heartbeat para mantener conexión
- Manejar desconexiones inesperadas
- Serialización eficiente de datos
