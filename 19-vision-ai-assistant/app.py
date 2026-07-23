from rich.console import Console
from rich.panel import Panel

from src.prompting.prompt_builder import PromptType
from src.vision.vision_assistant import VisionAssistant

console = Console()

assistant = VisionAssistant()

response = assistant.analyze(
    image_path="images/natural/beach.jpg",
    prompt_type=PromptType.SCENE,
    question="Describe this image in detail.",
)

console.print(
    Panel(
        response.answer,
        title=f"{response.model} ({response.inference_time}s)",
        border_style="green",
    )
)