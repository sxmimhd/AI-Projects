from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics.pairwise import cosine_similarity
from config import settings
from src.utils.logger import Logger


class EmbeddingVisualizer:

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe.copy()

        self.logger = Logger.get_logger()

        self.output_dir = (
            Path(settings.OUTPUTS_DIR)
            / "figures"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_figure(
        self,
        filename: str
    ) -> None:

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()

        self.logger.info(
            f"Saved figure: {filename}"
        )

    def dataset_statistics(self) -> None:

        genres = (
            self.dataframe["genres"]
            .dropna()
            .str.findall(r"'([^']+)'")
            .explode()
        )

        counts = (
            genres
            .value_counts()
            .head(15)
        )

        plt.figure(figsize=(12, 7))

        counts.sort_values().plot.barh()

        plt.title("Top Game Genres")
        plt.xlabel("Games")
        plt.ylabel("Genre")

        self.save_figure(
            "01_dataset_statistics.png"
        )

    def document_length_distribution(self, documents) -> None:

        lengths = [
            len(document.document.split())
            for document in documents
        ]

        plt.figure(figsize=(10, 6))

        plt.hist(
            lengths,
            bins=40
        )

        plt.title("Knowledge Document Length Distribution")
        plt.xlabel("Words")
        plt.ylabel("Documents")

        self.save_figure(
            "02_document_length_distribution.png"
        )

    def embedding_norm_distribution(
        self,
        embeddings
    ) -> None:

        norms = np.linalg.norm(
            embeddings,
            axis=1
        )

        plt.figure(figsize=(10,6))

        plt.hist(
            norms,
            bins=40
        )

        plt.title("Embedding Vector Norm Distribution")
        plt.xlabel("Vector Norm")
        plt.ylabel("Count")

        self.save_figure(
            "03_embedding_norm_distribution.png"
        )

    def pca_projection(
        self,
        embeddings
    ) -> None:

        sample = embeddings[:5000]

        pca = PCA(
            n_components=2,
            random_state=42
        )

        reduced = pca.fit_transform(sample)

        plt.figure(figsize=(9,9))

        plt.scatter(
            reduced[:,0],
            reduced[:,1],
            s=5,
            alpha=0.5
        )

        plt.title("Embedding Space (PCA)")

        self.save_figure(
            "04_pca_projection.png"
        )
        
    def tsne_projection(
        self,
        embeddings
    ) -> None:

        sample = embeddings[:2000]

        tsne = TSNE(
            n_components=2,
            random_state=42,
            perplexity=30
        )

        reduced = tsne.fit_transform(sample)

        plt.figure(figsize=(9,9))

        plt.scatter(
            reduced[:,0],
            reduced[:,1],
            s=8,
            alpha=0.6
        )

        plt.title("Embedding Space (t-SNE)")

        self.save_figure(
            "05_tsne_projection.png"
        )

    def search_results(
    self,
        results
    ) -> None:

        names = [
            result["document"].title
            for result in results
        ]

        scores = [
            result["score"]
            for result in results
        ]

        plt.figure(figsize=(10,5))

        plt.barh(
            names[::-1],
            scores[::-1]
        )

        plt.xlabel("Cosine Similarity")

        plt.title("Top Retrieved Games")

        self.save_figure(
            "06_search_results.png"
        )

    def similarity_heatmap(
        self,
        embeddings
    ) -> None:

        sample = embeddings[:20]

        similarity = cosine_similarity(sample)

        plt.figure(figsize=(8,7))

        plt.imshow(similarity)

        plt.colorbar()

        plt.title("Embedding Similarity Heatmap")

        self.save_figure(
            "07_similarity_heatmap.png"
        )

    def explained_variance(
        self,
        embeddings
    ) -> None:

        pca = PCA(
            n_components=20
        )

        pca.fit(
            embeddings[:5000]
        )

        plt.figure(figsize=(10,5))

        plt.plot(
            pca.explained_variance_ratio_,
            marker="o"
        )

        plt.title("PCA Explained Variance")

        plt.xlabel("Principal Component")

        plt.ylabel("Variance Ratio")

        self.save_figure(
            "08_explained_variance.png"
        )

    def genre_distribution(self) -> None:

        genres = (
            self.dataframe["genres"]
            .dropna()
            .str.findall(r"'([^']+)'")
            .explode()
        )

        counts = genres.value_counts().head(10)

        plt.figure(figsize=(10,6))

        plt.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%"
        )

        plt.title("Top Genres")

        self.save_figure(
            "09_genre_distribution.png"
        )