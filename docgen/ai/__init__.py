"""
Módulo de Engenharia de IA do DocGen.
Orquestra provedores de LLM (Gemini, OpenAI, Anthropic, Ollama local),
construção de contexto semântico e síntese de arquitetura por agentes de IA.
"""

from docgen.ai.provider import LLMProvider, get_ai_provider
from docgen.ai.architect import AIArchitect

