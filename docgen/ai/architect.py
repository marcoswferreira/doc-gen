"""
Orquestrador de IA do DocGen (AI Architect Engine).
Executa as cadeias de raciocínio arquitetural com o LLM sobre o contexto do repositório.
"""

import re
from typing import Optional, Dict
from docgen.models import ProjectData
from docgen.ai.provider import LLMProvider
from docgen.ai.context_builder import CodebaseContextBuilder
from docgen.ai.prompts import (
    SYSTEM_ARCHITECT_PROMPT,
    C4_PROMPT,
    HLD_PROMPT,
    DAS_PROMPT,
    UBIQUITOUS_LANGUAGE_PROMPT,
)
from docgen.ui import Colors, print_step, print_info, print_warning


def _clean_llm_markdown(text: str) -> str:
    """Remove blocos de markdown envolventes desnecessários retornados por LLMs."""
    text = text.strip()
    if text.startswith("```markdown") and text.endswith("```"):
        text = text[11:-3].strip()
    elif text.startswith("```md") and text.endswith("```"):
        text = text[5:-3].strip()
    return text


class AIArchitect:
    """Agente de arquitetura de software alimentado por IA Generativa."""

    def __init__(self, project_data: ProjectData, provider: LLMProvider, lang: str = "pt"):
        self.project = project_data
        self.provider = provider
        self.lang = "Português do Brasil (pt-BR)" if lang == "pt" else "English (en-US)"
        self.context_builder = CodebaseContextBuilder(project_data)
        self._cached_context: Optional[str] = None

    def get_context(self) -> str:
        """Gera ou recupera o contexto técnico do repositório."""
        if self._cached_context is None:
            self._cached_context = self.context_builder.build_context()
        return self._cached_context

    def _call_llm(self, prompt_template: str, task_name: str) -> str:
        """Executa a chamada para o provedor de IA com contexto preenchido."""
        print_step(f"Sintetizando com IA ({self.provider.name} - {self.provider.model_name}): {task_name}...")
        context = self.get_context()
        prompt = prompt_template.format(
            project_name=self.project.project_name,
            lang=self.lang,
            context=context,
        )
        system_prompt = SYSTEM_ARCHITECT_PROMPT.format(lang=self.lang)
        raw_response = self.provider.generate(prompt=prompt, system_prompt=system_prompt)
        return _clean_llm_markdown(raw_response)

    def synthesize_c4(self) -> str:
        """Gera o documento C4_MODEL.md via raciocínio de IA."""
        return self._call_llm(C4_PROMPT, "Modelo C4 (Contexto, Containers, Componentes e Código)")

    def synthesize_hld(self) -> str:
        """Gera o documento HLD.md via raciocínio de IA."""
        return self._call_llm(HLD_PROMPT, "High-Level Design (HLD)")

    def synthesize_das(self) -> str:
        """Gera o documento DAS.md via raciocínio de IA."""
        return self._call_llm(DAS_PROMPT, "Documento de Arquitetura de Software (DAS / Arc42)")

    def synthesize_ubiquitous_language(self) -> str:
        """Gera a Linguagem Ubíqua e Bounded Contexts via raciocínio de IA."""
        return self._call_llm(UBIQUITOUS_LANGUAGE_PROMPT, "Linguagem Ubíqua (DDD)")

