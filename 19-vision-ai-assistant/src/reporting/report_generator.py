import json
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR
from src.llm.vision_response import VisionResponse
from src.preprocessing.image_loader import ImageLoader
from src.prompting.prompt_builder import PromptType
from src.utils.types import ImagePath


class ReportGenerator:

    def __init__(self) -> None:
        self.loader = ImageLoader()

        self.responses_dir = OUTPUT_DIR / "responses"
        self.reports_dir = OUTPUT_DIR / "reports"

        self.responses_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save(
        self,
        image_path: ImagePath,
        prompt_type: PromptType,
        question: str,
        response: VisionResponse,
    ) -> None:

        metadata = self.loader.get_metadata(image_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        text_path = self.responses_dir / f"{timestamp}.txt"
        report_path = self.reports_dir / f"{timestamp}.json"

        text_path.write_text(
            response.answer,
            encoding="utf-8",
        )

        report = {
            "timestamp": timestamp,
            "image": metadata.filename,
            "format": metadata.image_format,
            "resolution": f"{metadata.width}x{metadata.height}",
            "prompt_type": prompt_type.value,
            "question": question,
            "model": response.model,
            "inference_time": response.inference_time,
            "response": response.answer,
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)