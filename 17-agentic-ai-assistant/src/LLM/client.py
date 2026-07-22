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
                #format=ToolDecision.model_json_schema(),
            )

            content = response["message"]["content"].strip()

            # Remove markdown code fences if the model added them
            if content.startswith("```"):
                lines = content.splitlines()

                # Remove first line (``` or ```json)
                lines = lines[1:]

                # Remove last line if it's ```
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]

                content = "\n".join(lines)


            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                print(content)
                raise

            return ToolDecision(**data)

        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")
        
    def generate_text(self, prompt: str) -> str:

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]