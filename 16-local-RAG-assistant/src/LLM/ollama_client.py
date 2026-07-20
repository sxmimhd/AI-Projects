from ollama import Client

from config import settings
from src.utils.logger import Logger


class OllamaClient:

    def __init__(self):
        self.logger = Logger.get_logger()

        self.client = Client(
            host=settings.OLLAMA_HOST
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        self.logger.info(
            f"Generating response using {settings.OLLAMA_MODEL}..."
        )

        response = self.client.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]