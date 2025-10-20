"""
Aplicación Hola Mundo con Reflex y Google ADK + Gemini.
Una app simple que demuestra la integración de Reflex (frontend) con Gemini API.
"""

import os
import reflex as rx
from google.adk import Agent
import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar API de Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None


# Crear un agente ADK simple
hello_agent = Agent(
    name="GeminiAgent",
    description="Agente que usa Gemini para procesar solicitudes",
)


# Función para procesar solicitudes con Gemini
def process_gemini_request(prompt: str) -> str:
    """Procesa la solicitud usando Gemini API."""
    if not model:
        return "⚠️ Error: GEMINI_API_KEY no configurada. Agrega tu API key en el archivo .env"
    
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "No se obtuvo respuesta de Gemini"
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Definir el estado de Reflex
class State(rx.State):
    """Estado de la aplicación Reflex."""

    state_auto_setters: bool = False
    response: str = "Escribe una pregunta y haz clic en el botón"
    loading: bool = False
    user_input: str = ""

    def set_user_input(self, value: str):
        """Setter explícito para user_input."""
        self.user_input = value

    def ask_gemini(self):
        """Event handler que envía la pregunta a Gemini."""
        if not self.user_input.strip():
            self.response = "Por favor, escribe una pregunta"
            return
        
        self.loading = True
        try:
            prompt = self.user_input
            self.response = process_gemini_request(prompt)
        except Exception as e:
            self.response = f"Error: {str(e)}"
        finally:
            self.loading = False


# Definir la UI
def index() -> rx.Component:
    """Página principal con la UI."""
    return rx.vstack(
        rx.heading(
            "Hola Mundo con Gemini",
            size="6",
        ),
        rx.divider(),
        rx.text("Pregúntale cualquier cosa a Gemini"),
        rx.input(
            placeholder="Escribe tu pregunta aquí...",
            value=State.user_input,
            on_change=State.set_user_input,
        ),
        rx.button(
            "Enviar a Gemini",
            on_click=State.ask_gemini,
            is_loading=State.loading,
        ),
        rx.divider(),
        rx.text(
            State.response,
            color="green",
        ),
    )


# Crear la app
app = rx.App()
app.add_page(index, title="Gemini + Reflex")
