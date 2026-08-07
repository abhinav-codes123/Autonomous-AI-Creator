"""OpenAI LLM Provider implementation."""

import json
import re
import httpx
from app.core.logging import logger
from app.services.llm.base import LLMGeneratedContent, LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini") -> None:
        self.api_key = api_key
        self.model = model
        self.url = "https://api.openai.com/v1/chat/completions"

    async def generate(self, prompt: str) -> LLMGeneratedContent:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a technical AI expert content generator. Respond strictly with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "response_format": {"type": "json_object"},
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(self.url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    content_str = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content_str)
                    return LLMGeneratedContent(
                        text=parsed.get("text", "").strip(),
                        rationale=parsed.get("rationale", "").strip(),
                        sources=parsed.get("sources", []),
                    )
                else:
                    logger.error(f"OpenAI API error {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"Failed to generate content with OpenAI: {e}")

        # Fallback if OpenAI call fails
        return LLMGeneratedContent(
            text="Analysis failed due to API connection error.",
            rationale="Attempted generation via OpenAI but encountered an unexpected connection error.",
            sources=[],
        )
