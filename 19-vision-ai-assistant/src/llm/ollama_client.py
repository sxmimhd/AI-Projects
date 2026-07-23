import time
from pathlib import Path

import ollama

from config import MODEL_NAME
from src.utils.types import ImagePath
from src.llm.vision_response import VisionResponse


class OllamaClient:

    def __init__(self, model: str = MODEL_NAME):
        self.model = model

    def generate(
        self,
        image_path: ImagePath,
        prompt: str,
    ) -> tuple[str, float]:

        image_path = Path(image_path)

        start = time.perf_counter()

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [str(image_path)],
                }
            ],
        )

        elapsed = time.perf_counter() - start

        answer = response["message"]["content"]

        return VisionResponse(
            answer=answer,
            inference_time=round(elapsed, 2),
            model=self.model,
        )