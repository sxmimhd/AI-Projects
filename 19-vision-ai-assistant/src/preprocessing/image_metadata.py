from dataclasses import dataclass

@dataclass(slots=True)
class ImageMetadata:
    filename: str
    extension: str
    width: int
    height: int
    mode: str
    image_format: str
    file_size_mb: float
    aspect_ratio: str