import json

import ollama

from config import settings
from src.LLM.models import ToolDecision


class LLMClient:

    def __init__(self):
        self.model = settings.OLLAMA_MODEL

    def generate(self, prompt: str) -> ToolDecision:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                format=ToolDecision.model_json_schema(),
            )

            content = response["message"]["content"]

            data = json.loads(content)

            return ToolDecision(**data)

        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")