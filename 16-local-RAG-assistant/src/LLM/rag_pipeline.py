from src.LLM.ollama_client import OllamaClient
from src.LLM.prompt_builder import PromptBuilder
from src.retrieval.retriever import Retriever


class RAGPipeline:

    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = OllamaClient()

    def ask(
        self,
        question: str
    ) -> tuple[str, list[dict]]:

        results = self.retriever.retrieve(question)

        documents = [
            result["document"]
            for result in results
        ]

        prompt = self.prompt_builder.build(
            question,
            documents
        )

        answer = self.llm.generate(prompt)

        return answer, results