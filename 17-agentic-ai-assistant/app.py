from rich.console import Console
from rich.panel import Panel

from config  import settings
from src.agent.agent import Agent
from src.utils.helpers import create_directories


console = Console()


def initialize_project() -> None:

    create_directories(
        [
            settings.DATA_DIR,
            settings.DOCUMENTS_DIR,
            settings.DATASETS_DIR,
            settings.LOG_DIR,
            settings.MEMORY_DIR,
            settings.OUTPUT_DIR,
            settings.FIGURES_DIR,
            settings.REPORTS_DIR,
            settings.METRICS_DIR,
            settings.TOOL_CALLS_DIR,
            settings.MODEL_DIR,
        ]
    )


def main():

    console.print(
        Panel.fit(
            "[bold cyan]Agentic AI Assistant[/bold cyan]",
            subtitle="Project Initialization",
        )
    )

    initialize_project()

    console.print("[green]✓ Project initialized successfully.[/green]")

    agent = Agent()

    agent.display_tools()

    while True:

        question = console.input(
            "\n[bold yellow]Ask the Agent[/bold yellow] > "
        )

        if question.lower() in {"exit", "quit"}:
            console.print("\n[bold red]Goodbye![/bold red]")
            break

        agent.run(question)


if __name__ == "__main__":
    main()