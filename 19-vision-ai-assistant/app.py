from rich.console import Console
from rich.panel import Panel

from src.prompting.prompt_builder import PromptBuilder, PromptType

console = Console()

prompt = PromptBuilder.build(
    prompt_type=PromptType.SCENE,
    user_question="What is happening in this image?"
)

console.print(
    Panel(
        prompt,
        title="Generated Prompt",
        border_style="green",
    )
)