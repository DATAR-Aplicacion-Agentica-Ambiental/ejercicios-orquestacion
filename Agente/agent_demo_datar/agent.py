from google.adk.agents.llm_agent import Agent

def obtener_lugares() -> dict:
    """Obtiene una lista de tres lugares ambientales disponibles"""
    lugares = [
        {
            "id": 1,
            "nombre": "Humedal La Conejera",
            "tipo": "Humedal",
            "descripcion": "Área protegida de importancia ecológica"
        },
        {
            "id": 2,
            "nombre": "Cerro La Conejera",
            "tipo": "Cerro",
            "descripcion": "Formación geológica con vegetación nativa"
        },
        {
            "id": 3,
            "nombre": "Quebrada La Salitrosa",
            "tipo": "Quebrada",
            "descripcion": "Recurso hídrico con ecosistema acuático"
        }
    ]
    return {
        "total": len(lugares),
        "lugares": lugares
    }


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Eres un asistente naturalista.',
    instruction='Responde las preguntas del usuario con la mayor precisión posible.',
    tools=[obtener_lugares]
)
