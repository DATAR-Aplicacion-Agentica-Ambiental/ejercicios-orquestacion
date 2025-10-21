import os # Required for path operations
from dotenv import load_dotenv # Required for loading environment variables
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Eres un asistente naturalista.',
    instruction='Responde las preguntas del usuario con la mayor precisión posible.',
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params = StdioServerParameters(
                    command='/Users/manglerojo/.local/bin/uv',
                    args=[
                        "run",
                        "--directory",
                        "/path/to/your/folder/ejercicios-orquestacion/MCP/mcp-server-inaturalist",
                        "python",
                        "-m",
                        "main"
                    ],
                ),
            ),
        )
    ],
)
