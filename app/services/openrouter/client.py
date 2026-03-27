import httpx
import os
from app.utils.errors import AIServiceError


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("APP_URL", "http://localhost:5173"),
        }

    def chat(
        self, messages: list, model: str = "anthropic/claude-3.5-sonnet", **kwargs
    ):
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.BASE_URL}/chat/completions",
                    headers=self.headers,
                    json={"model": model, "messages": messages, **kwargs},
                    timeout=30,
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise AIServiceError(f"OpenRouter error: {e.response.status_code}")

    def stream(self, messages: list, model: str = "anthropic/claude-3.5-sonnet"):
        """Returns a generator for SSE streaming."""
        with httpx.Client() as client:
            with client.stream(
                "POST",
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json={"model": model, "messages": messages, "stream": True},
                timeout=60,
            ) as response:
                for line in response.iter_lines():
                    if line.startswith("data: "):
                        yield line[6:]  # Strip "data: " prefix
