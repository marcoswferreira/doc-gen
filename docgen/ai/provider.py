"""
Provedores de LLM para o DocGen.
Suporta Google Gemini, OpenAI, Anthropic Claude e Ollama local,
utilizando exclusivamente a biblioteca padrão (urllib) para zero dependências externas.
"""

import os
import json
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMProvider(ABC):
    """Interface abstrata para provedores de inteligência artificial generativa."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Gera resposta a partir de um prompt e instrução de sistema."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome do provedor."""
        pass

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Nome do modelo utilizado."""
        pass


class GeminiProvider(LLMProvider):
    """Integração com Google Gemini API via REST nativo."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = model
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não foi encontrada nas variáveis de ambiente.")

    @property
    def name(self) -> str:
        return "Google Gemini"

    @property
    def model_name(self) -> str:
        return self.model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        contents = []
        if system_prompt:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction:\n{system_prompt}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will act strictly according to these instructions."}]})

        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 8192,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")
                return ""
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Erro na API do Gemini ({e.code}): {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Falha de conexão com Gemini: {e}")


class OpenAIProvider(LLMProvider):
    """Integração com OpenAI (GPT-4o, GPT-4o-mini) via REST nativo."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY não foi encontrada nas variáveis de ambiente.")

    @property
    def name(self) -> str:
        return "OpenAI"

    @property
    def model_name(self) -> str:
        return self.model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = "https://api.openai.com/v1/chat/completions"
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                choices = result.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                return ""
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Erro na API da OpenAI ({e.code}): {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Falha de conexão com OpenAI: {e}")


class AnthropicProvider(LLMProvider):
    """Integração com Anthropic Claude via REST nativo."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.model = model
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY não foi encontrada nas variáveis de ambiente.")

    @property
    def name(self) -> str:
        return "Anthropic Claude"

    @property
    def model_name(self) -> str:
        return self.model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = "https://api.anthropic.com/v1/messages"
        payload: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": 8192,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            payload["system"] = system_prompt

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                content_blocks = result.get("content", [])
                if content_blocks:
                    return content_blocks[0].get("text", "")
                return ""
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Erro na API da Anthropic ({e.code}): {err_msg}")
        except Exception as e:
            raise RuntimeError(f"Falha de conexão com Anthropic: {e}")


class OllamaProvider(LLMProvider):
    """Integração com LLM local via Ollama (DeepSeek-R1, Llama 3, Qwen, etc.)."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "deepseek-r1"):
        self.base_url = (base_url or "http://localhost:11434").rstrip("/")
        self.model = model

    @property
    def name(self) -> str:
        return "Ollama (Local LLM)"

    @property
    def model_name(self) -> str:
        return self.model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
            }
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "")
        except urllib.error.URLError:
            raise RuntimeError(f"Ollama não está respondendo em {self.base_url}. Certifique-se de executar 'ollama serve'.")
        except Exception as e:
            raise RuntimeError(f"Erro no Ollama: {e}")


class MockProvider(LLMProvider):
    """Provedor mock utilizado para testes unitários ou modo determinístico."""

    def __init__(self, model: str = "mock-architect"):
        self._model = model

    @property
    def name(self) -> str:
        return "Mock AI Provider"

    @property
    def model_name(self) -> str:
        return self._model

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        return "Conteúdo gerado via Mock AI Provider."


def get_ai_provider(
    provider_name: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    ollama_url: Optional[str] = None,
) -> Optional[LLMProvider]:
    """
    Fábrica inteligente de provedores de IA.
    Detecta automaticamente com base em flags e variáveis de ambiente:
    1. Flag explícita --provider
    2. GEMINI_API_KEY -> Gemini
    3. OPENAI_API_KEY -> OpenAI
    4. ANTHROPIC_API_KEY -> Anthropic
    5. Ollama local (se especificado ou rodando)
    """
    p_name = (provider_name or "").lower().strip()

    # 1. Provedor explícito solicitado
    if p_name == "gemini":
        return GeminiProvider(api_key=api_key, model=model or "gemini-2.5-flash")
    elif p_name in ("openai", "gpt"):
        return OpenAIProvider(api_key=api_key, model=model or "gpt-4o-mini")
    elif p_name in ("anthropic", "claude"):
        return AnthropicProvider(api_key=api_key, model=model or "claude-3-5-sonnet-20241022")
    elif p_name == "ollama":
        return OllamaProvider(base_url=ollama_url or "http://localhost:11434", model=model or "deepseek-r1")
    elif p_name == "mock":
        return MockProvider(model=model or "mock-model")

    # 2. Detecção automática por variáveis de ambiente
    if api_key:
        # Se uma chave foi passada via CLI sem especificar provedor, assume Gemini por padrão
        return GeminiProvider(api_key=api_key, model=model or "gemini-2.5-flash")

    if os.environ.get("GEMINI_API_KEY"):
        return GeminiProvider(model=model or "gemini-2.5-flash")

    if os.environ.get("OPENAI_API_KEY"):
        return OpenAIProvider(model=model or "gpt-4o-mini")

    if os.environ.get("ANTHROPIC_API_KEY"):
        return AnthropicProvider(model=model or "claude-3-5-sonnet-20241022")

    # 3. Testa se o Ollama local está ativo
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=1) as response:
            if response.status == 200:
                return OllamaProvider(model=model or "deepseek-r1")
    except Exception:
        pass

    return None

