from abc import ABC, abstractmethod
from functools import lru_cache

from app.config import settings


class LLMProvider(ABC):
    """Provider-agnostic LLM interface."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        ...

    async def aclose(self) -> None:
        """Release any underlying network resources."""
        return None


class OllamaProvider(LLMProvider):
    def __init__(self):
        import httpx
        self.client = httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=300.0)
        self.model = settings.llm_model

    async def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }
        if json_mode:
            # Constrain Ollama to emit a valid JSON object (avoids fenced/prose output).
            payload["format"] = "json"

        response = await self.client.post("/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and data.get("error"):
            raise RuntimeError(f"Ollama error: {data['error']}")
        try:
            return data["message"]["content"]
        except (KeyError, TypeError) as exc:
            raise RuntimeError(f"Unexpected Ollama response shape: {str(data)[:200]}") from exc

    async def aclose(self) -> None:
        await self.client.aclose()


@lru_cache(maxsize=1)
def get_llm_provider() -> LLMProvider:
    """Return a process-wide LLM provider (single pooled httpx client)."""
    return OllamaProvider()
