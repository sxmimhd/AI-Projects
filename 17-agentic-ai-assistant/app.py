from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from config import settings
from src.utils.helpers import create_directories
from src.tools.calculator import CalculatorTool
from src.tools.registry import ToolRegistry
from src.executor.executor import ToolExecutor
from src.planner.planner import Planner

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

    registry = ToolRegistry()

    registry.register(CalculatorTool())

    console.print()

    console.print("[bold yellow]Registered Tools[/bold yellow]")

    for tool in registry.list_tools():
        console.print(f" • {tool}")

    executor = ToolExecutor(registry)
    result = executor.execute(
        tool_name="calculator",
        expression="(150*12)-40",
    )

    console.print()

    table = Table(title="Tool Execution")

    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")

    for key, value in result.items():
        table.add_row(str(key), str(value))

    console.print(table)


    planner = Planner(registry)

    console.print()

    console.print("[bold magenta]Available Tools[/bold magenta]")

    for tool in planner.available_tools():

        console.print(f"[cyan]{tool['name']}[/cyan]")

        console.print(tool["description"])

        console.print()


if __name__ == "__main__":
    main()