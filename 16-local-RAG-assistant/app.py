from rich.console import Console
from rich.table import Table

from config import settings
from src.dataset.loader import DatasetLoader
from src.dataset.validator import DatasetValidator
from src.utils.helpers import create_directories
from src.utils.logger import Logger


console = Console()
logger = Logger.get_logger()


def display_dataset_info(loader: DatasetLoader) -> None:
    table = Table(title="Dataset Information")

    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    rows, columns = loader.get_shape()

    table.add_row("Rows", f"{rows:,}")
    table.add_row("Columns", f"{columns}")
    table.add_row("Memory Usage", f"{loader.get_memory_usage():.2f} MB")
    table.add_row("Duplicate Rows", str(loader.get_duplicate_count()))

    console.print(table)


def display_validation_report(report: dict) -> None:
    table = Table(title="Validation Report")

    table.add_column("Check", style="cyan")
    table.add_column("Result", style="green")

    table.add_row("Dataset Valid", str(report["valid"]))
    table.add_row("Total Games", f"{report['total_games']:,}")
    table.add_row("Missing Columns", ", ".join(report["missing_columns"]) if report["missing_columns"] else "None")
    table.add_row("Duplicate App IDs", str(report["duplicate_appids"]))
    table.add_row("Missing Titles", str(report["missing_titles"]))
    table.add_row("Missing Descriptions", str(report["missing_descriptions"]))
    table.add_row("Empty Descriptions", str(report["empty_descriptions"]))

    console.print(table)


def main() -> None:
    logger.info(f"Starting {settings.PROJECT_NAME}")

    create_directories()

    loader = DatasetLoader(settings.DATASET_PATH)
    dataframe = loader.load()

    validator = DatasetValidator(dataframe)
    report = validator.validate()

    display_dataset_info(loader)
    display_validation_report(report)

    console.print("\n[bold cyan]Dataset Preview[/bold cyan]\n")
    console.print(loader.preview())

    logger.info("Phase 1 completed successfully.")


if __name__ == "__main__":
    main()