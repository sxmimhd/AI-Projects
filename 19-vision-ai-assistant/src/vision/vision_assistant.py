from PIL import Image

from src.llm.ollama_client import OllamaClient
from src.llm.vision_response import VisionResponse
from src.preprocessing.image_loader import ImageLoader
from src.preprocessing.image_preprocessor import ImagePreprocessor
from src.prompting.prompt_builder import PromptBuilder, PromptType
from src.utils.types import ImagePath
from src.validation.image_validator import ImageValidator
from src.reporting.report_generator import ReportGenerator

class VisionAssistant:

    def __init__(self) -> None:
        self.loader = ImageLoader()
        self.validator = ImageValidator()
        self.preprocessor = ImagePreprocessor()
        self.prompt_builder = PromptBuilder()
        self.client = OllamaClient()
        self.report_generator = ReportGenerator()

    def analyze(
        self,
        image_path: ImagePath,
        prompt_type: PromptType = PromptType.GENERAL,
        question: str | None = None,
        resize: bool = False,
        max_size: tuple[int, int] = (1024, 1024),
    ) -> VisionResponse:

        # Validate image
        self.validator.validate(image_path)

        # Load image
        image = self.loader.load_image(image_path)

        processed_image = None
        temp_image = None

        try:
            # Preprocess image
            processed_image = self.preprocessor.preprocess(
                image=image,
                convert_rgb=True,
                resize=resize,
                max_size=max_size,
            )

            # Save processed image temporarily
            temp_image = self.preprocessor.create_temp_image(processed_image)

            # Build prompt
            prompt = self.prompt_builder.build(
                prompt_type=prompt_type,
                user_question=question,
            )

            # Run inference
            response = self.client.generate(
                image_path=temp_image,
                prompt=prompt,
            )

            # reports
            self.report_generator.save(
                image_path=image_path,
                prompt_type=prompt_type,
                question=question or "",
                response=response,
            )

            return response

        finally:
            image.close()

            if processed_image is not None:
                processed_image.close()

            if temp_image is not None:
                temp_image.unlink(missing_ok=True)