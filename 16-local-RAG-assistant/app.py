from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import settings
from src.dataset.loader import DatasetLoader
from src.dataset.validator import DatasetValidator
from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.document_builder import DocumentBuilder
from src.utils.helpers import create_directories
from src.utils.logger import Logger
from src.retrieval.retriever import Retriever
from src.LLM.rag_pipeline import RAGPipeline
from src.visualization.visualizer import EmbeddingVisualizer

console = Console()
logger = Logger.get_logger()


def display_dataset_info(loader: DatasetLoader) -> None:
    table = Table(title="Dataset Information")

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    rows, columns = loader.get_shape()

    table.add_row("Rows", f"{rows:,}")
    table.add_row("Columns", str(columns))
    table.add_row("Memory Usage", f"{loader.get_memory_usage():.2f} MB")
    table.add_row("Duplicate Rows", str(loader.get_duplicate_count()))

    console.print(table)


def display_validation_report(report: dict) -> None:
    table = Table(title="Validation Report")

    table.add_column("Check", style="cyan")
    table.add_column("Result", style="green")

    table.add_row("Dataset Valid", str(report["valid"]))
    table.add_row("Total Games", f"{report['total_games']:,}")
    table.add_row(
        "Missing Columns",
        ", ".join(report["missing_columns"]) if report["missing_columns"] else "None"
    )
    table.add_row("Duplicate App IDs", str(report["duplicate_appids"]))
    table.add_row("Missing Titles", str(report["missing_titles"]))
    table.add_row("Missing Descriptions", str(report["missing_descriptions"]))
    table.add_row("Empty Descriptions", str(report["empty_descriptions"]))

    console.print(table)


def display_document(document) -> None:
    metadata = document.metadata

    console.print(
        Panel.fit(
            f"[bold cyan]Game ID:[/bold cyan] {document.game_id}\n"
            f"[bold cyan]Title:[/bold cyan] {document.title}\n\n"
            f"[bold cyan]Genres:[/bold cyan] {', '.join(metadata['genres'])}\n"
            f"[bold cyan]Developers:[/bold cyan] {', '.join(metadata['developers'])}\n"
            f"[bold cyan]Publishers:[/bold cyan] {', '.join(metadata['publishers'])}\n"
            f"[bold cyan]Price:[/bold cyan] ${metadata['price']}\n"
            f"[bold cyan]Release Date:[/bold cyan] {metadata['release_date']}\n\n"
            f"[bold cyan]Top Tags:[/bold cyan] "
            f"{', '.join(metadata['tags'][:10])}\n\n"
            f"[bold cyan]Document:[/bold cyan]\n\n"
            f"{document.document[:1000]}...",
            title="Sample Knowledge Document",
            border_style="green",
        )
    )


def main() -> None:
    logger.info(f"Starting {settings.PROJECT_NAME}")

    create_directories()

    loader = DatasetLoader(settings.DATASET_PATH)
    dataframe = loader.load()

    validator = DatasetValidator(dataframe)
    report = validator.validate()

    display_dataset_info(loader)
    display_validation_report(report)

    cleaner = TextCleaner(dataframe)
    cleaned_dataframe = cleaner.clean()

    console.print(
        f"\n[bold green]Cleaned Dataset:[/bold green] {len(cleaned_dataframe):,} games"
    )

    builder = DocumentBuilder(cleaned_dataframe)
    documents = builder.build()

    console.print(
        f"[bold green]Knowledge Documents:[/bold green] {len(documents):,}"
    )

    console.print()
    display_document(documents[0])


    retriever = Retriever(documents)

    pipeline = RAGPipeline(retriever)

    question = "Recommend me best survival crafting open world games."

    answer, results = pipeline.ask(question)

    console.print("\n[bold cyan]Retrieved Documents[/bold cyan]\n")

    for rank, result in enumerate(results, start=1):

        console.print(
            f"{rank}. "
            f"{result['document'].title} "
            f"([green]{result['score']:.4f}[/green])"
        )

    console.print("\n[bold green]LLM Answer[/bold green]\n")

    console.print(answer)

    visualizer = EmbeddingVisualizer(cleaned_dataframe)
    visualizer.dataset_statistics()
    visualizer.document_length_distribution(documents)
    visualizer.pca_projection(retriever.embeddings)
    visualizer.tsne_projection(retriever.embeddings)
    visualizer.search_results(results)
    visualizer.similarity_heatmap(retriever.embeddings)
    visualizer.explained_variance(retriever.embeddings)
    visualizer.genre_distribution()

    logger.info("All visualizations generated successfully")

if __name__ == "__main__":
    main()