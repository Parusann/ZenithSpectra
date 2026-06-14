from abc import ABC, abstractmethod

from app.config import settings


class LLMProvider(ABC):
    """Provider-agnostic LLM interface. Swap providers via LLM_PROVIDER env var."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass


class OllamaProvider(LLMProvider):
    def __init__(self):
        import httpx
        self.client = httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=300.0)
        self.model = settings.llm_model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.post("/api/chat", json={
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        })
        response.raise_for_status()
        return response.json()["message"]["content"]


class GroqProvider(LLMProvider):
    def __init__(self):
        import httpx
        self.client = httpx.AsyncClient(
            base_url="https://api.groq.com/openai/v1",
            headers={"Authorization": f"Bearer {settings.groq_api_key}"},
            timeout=60.0,
        )
        self.model = settings.llm_model

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = await self.client.post("/chat/completions", json={
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        })
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider == "groq":
        return GroqProvider()
    return OllamaProvider()
