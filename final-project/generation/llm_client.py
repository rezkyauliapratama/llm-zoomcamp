"""LLM client wrapper supporting OpenAI and Ollama backends."""

from typing import List, Dict, Optional


class LLMClient:
    def __init__(self, provider: str = "openai", model: str = "gpt-4o-mini", base_url: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        self._client = self._init_client()

    def _init_client(self):
        from openai import OpenAI
        if self.provider == "ollama":
            return OpenAI(base_url=self.base_url or "http://localhost:11434/v1", api_key="ollama")
        return OpenAI()

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        """Generate a response from the LLM."""
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
