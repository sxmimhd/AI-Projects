from pathlib import Path

from PIL import Image

from config import (
    MAX_IMAGE_SIZE_MB,
    MIN_HEIGHT,
    MIN_WIDTH,
    SUPPORTED_FORMATS,
)
from src.utils.types import ImagePath


class ImageValidator:

    @staticmethod
    def validate(image_path: ImagePath) -> bool:
        image_path = Path(image_path)

        ImageValidator._validate_exists(image_path)
        ImageValidator._validate_extension(image_path)
        ImageValidator._validate_size(image_path)
        ImageValidator._validate_integrity(image_path)
        ImageValidator._validate_dimensions(image_path)

        return True

    @staticmethod
    def _validate_exists(image_path: Path) -> None:
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

    @staticmethod
    def _validate_extension(image_path: Path) -> None:
        if image_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {image_path.suffix}"
            )

    @staticmethod
    def _validate_size(image_path: Path) -> None:
        size_mb = image_path.stat().st_size / (1024 * 1024)

        if size_mb > MAX_IMAGE_SIZE_MB:
            raise ValueError(
                f"Image exceeds maximum size ({MAX_IMAGE_SIZE_MB} MB)."
            )

    @staticmethod
    def _validate_integrity(image_path: Path) -> None:
        try:
            with Image.open(image_path) as image:
                image.verify()

        except Exception as e:
            raise ValueError(
                f"Corrupted or unreadable image: {image_path.name}"
            ) from e

    @staticmethod
    def _validate_dimensions(image_path: Path) -> None:
        with Image.open(image_path) as image:
            width, height = image.size

        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise ValueError(
                f"Image dimensions too small ({width}x{height}). "
                f"Minimum is {MIN_WIDTH}x{MIN_HEIGHT}."
            )