from pathlib import Path

BASE_DIR = Path(__file__).parent

IMAGE_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "outputs"

MODEL_NAME = "qwen2.5vl:7b"

MAX_IMAGE_SIZE = 15 * 1024 * 1024  # 15 MB
MAX_IMAGE_SIZE_MB = 15
SUPPORTED_FORMATS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".webp"
}

MIN_WIDTH = 64
MIN_HEIGHT = 64
