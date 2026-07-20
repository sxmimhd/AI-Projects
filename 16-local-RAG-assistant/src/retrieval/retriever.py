from pathlib import Path

from config import settings
from src.core.document import Document
from src.embeddings.sentence_transformer import SentenceTransformerEmbedder
from src.utils.logger import Logger
from src.vectorstore.faiss_store import FAISSVectorStore


class Retriever:

    def __init__(self, documents: list[Document]):
        self.logger = Logger.get_logger()

        self.documents = documents

        self.embedder = SentenceTransformerEmbedder()
        self.embedder.load_model()

        self.vector_store = FAISSVectorStore()

        self.embeddings = None

        self.initialize()

    def initialize(self) -> None:

        if Path(settings.EMBEDDINGS_PATH).exists():

            self.logger.info("Loading existing embeddings...")

            self.embeddings = self.embedder.load_embeddings()

            self.embedder.attach_embeddings(
                self.documents,
                self.embeddings
            )

        else:

            self.logger.info("Generating embeddings...")

            self.embeddings = self.embedder.generate_embeddings(
                self.documents
            )

            self.embedder.attach_embeddings(
                self.documents,
                self.embeddings
            )

            self.embedder.save_embeddings(
                self.embeddings
            )

            self.embedder.save_metadata(
                self.documents
            )

        if self.vector_store.exists():

            self.logger.info("Loading existing FAISS index...")

            self.vector_store.load()

        else:

            self.logger.info("Building FAISS index...")

            self.vector_store.create(
                self.embeddings
            )

            self.vector_store.save()

    def retrieve(
        self,
        query: str,
        top_k: int = settings.TOP_K_RESULTS
    ):

        query_embedding = self.embedder.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=settings.NORMALIZE_EMBEDDINGS
        )

        scores, indices = self.vector_store.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            results.append(
                {
                    "document": self.documents[index],
                    "score": float(score)
                }
            )

        return results