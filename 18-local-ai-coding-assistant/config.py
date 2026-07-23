from pathlib import Path


class Settings:
    # Repository to scan
    REPOSITORY_PATH = Path(".")

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