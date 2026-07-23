from math import gcd
from pathlib import Path

from PIL import Image
from src.preprocessing.image_metadata import ImageMetadata

class ImageLoader:

    @staticmethod
    def load_image(image_path: str | Path) -> Image.Image:
        return Image.open(image_path)

    @staticmethod
    def get_metadata(image_path: str | Path) -> ImageMetadata:

        image_path = Path(image_path)

        with Image.open(image_path) as image:

            width, height = image.size

            divisor = gcd(width, height)

            aspect_ratio = f"{width // divisor}:{height // divisor}"

            file_size_mb = image_path.stat().st_size / (1024 * 1024)

            return ImageMetadata(
                filename=image_path.name,
                extension=image_path.suffix.lower(),
                width=width,
                height=height,
                mode=image.mode,
                image_format=image.format,
                file_size_mb=round(file_size_mb, 2),
                aspect_ratio=aspect_ratio,
            )

    @staticmethod
    def close_image(image: Image.Image) -> None:
        image.close()