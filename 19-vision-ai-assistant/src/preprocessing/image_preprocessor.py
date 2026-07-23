from pathlib import Path

from PIL import Image
from src.utils.types import ImagePath

class ImagePreprocessor:

    @staticmethod
    def convert_to_rgb(image: Image.Image) -> Image.Image:
        if image.mode != "RGB":
            return image.convert("RGB")

        return image.copy()

    @staticmethod
    def resize(
        image: Image.Image,
        max_size: tuple[int, int] = (1024, 1024),
    ) -> Image.Image:
        resized = image.copy()
        resized.thumbnail(max_size)

        return resized

    @staticmethod
    def create_thumbnail(
        image: Image.Image,
        size: tuple[int, int] = (256, 256),
    ) -> Image.Image:
        thumbnail = image.copy()
        thumbnail.thumbnail(size)

        return thumbnail

    @staticmethod
    def save_image(
        image: Image.Image,
        output_path: ImagePath,
    ) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        image.save(output_path)

    @staticmethod
    def preprocess(
        image: Image.Image,
        convert_rgb: bool = True,
        resize: bool = False,
        max_size: tuple[int, int] = (1024, 1024),
    ) -> Image.Image:

        processed = image.copy()

        if convert_rgb:
            processed = ImagePreprocessor.convert_to_rgb(processed)

        if resize:
            processed = ImagePreprocessor.resize(
                processed,
                max_size=max_size,
            )

        return processed