from pathlib import Path


class Settings:
    # Repository to scan
    REPOSITORY_PATH = Path(".")

    MODELS_DIR = Path("models")

    FAISS_INDEX_PATH = MODELS_DIR / "faiss.index"

    EMBEDDINGS_PATH = MODELS_DIR / "embeddings.npy"

    METADATA_PATH = MODELS_DIR / "metadata.pkl"

    OLLAMA_MODEL = "qwen2.5-coder:7b"

    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
    }

    # Ignore these directories
    IGNORED_DIRECTORIES = {
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "outputs",
        "models",
        "dist",
        "build",
    }


settings = Settings()