from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.prompting.prompt_builder import PromptType
from src.vision.vision_assistant import VisionAssistant

console = Console()

assistant = VisionAssistant()


PROMPT_TYPES = {
    "1": ("Natural Scene", PromptType.SCENE, "natural"),
    "2": ("OCR / Document", PromptType.OCR, "documents"),
    "3": ("Chart Analysis", PromptType.CHART, "charts"),
    "4": ("UI Analysis", PromptType.UI, "ui"),
    "5": ("Code Analysis", PromptType.CODE, "code"),
    "6": ("Gaming", PromptType.GAME, "games"),
    "7": ("Diagram", PromptType.DIAGRAM, "diagrams"),
    "8": ("Custom Question", PromptType.GENERAL, None),
}


def choose_image(folder: str) -> str:

    image_dir = Path("images") / folder

    images = sorted(
        [
            file
            for file in image_dir.iterdir()
            if file.is_file()
        ]
    )

    table = Table(title=f"{folder.title()} Images")

    table.add_column("#", style="cyan")
    table.add_column("Image", style="green")

    for index, image in enumerate(images, start=1):
        table.add_row(str(index), image.name)

    console.print(table)

    choice = Prompt.ask(
        "Choose image",
        choices=[str(i) for i in range(1, len(images) + 1)],
    )

    return str(images[int(choice) - 1])


while True:

    console.clear()

    console.print(
        Panel.fit(
            "[bold cyan]Vision AI Assistant[/bold cyan]",
            border_style="blue",
        )
    )

    table = Table(show_header=False)

    table.add_row("1", "Describe Natural Scene")
    table.add_row("2", "OCR / Document")
    table.add_row("3", "Analyze Chart")
    table.add_row("4", "Explain UI")
    table.add_row("5", "Analyze Code")
    table.add_row("6", "Gaming Screenshot")
    table.add_row("7", "Diagram")
    table.add_row("8", "Custom Question")
    table.add_row("0", "Exit")

    console.print(table)

    choice = Prompt.ask(
        "Choice",
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"],
    )

    if choice == "0":
        break

    title, prompt_type, folder = PROMPT_TYPES[choice]

    if folder is None:

        folder = Prompt.ask(
            "Folder inside images"
        )

    image_path = choose_image(folder)

    question = Prompt.ask(
        "Question",
        default="Analyze this image."
    )

    console.print("\n[bold yellow]Running Vision Model...[/bold yellow]\n")

    response = assistant.analyze(
        image_path=image_path,
        prompt_type=prompt_type,
        question=question,
    )

    console.print(
        Panel(
            response.answer,
            title=f"{response.model} ({response.inference_time}s)",
            border_style="green",
        )
    )

    input("\nPress ENTER to continue...")