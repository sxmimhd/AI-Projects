from pathlib import Path


class Settings:
    """Global project configuration."""

    PROJECT_NAME = "Agentic AI Assistant"

    PROJECT_ROOT = Path(__file__).resolve().parent

    DATA_DIR = PROJECT_ROOT / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    DATASETS_DIR = DATA_DIR / "datasets"

    LOG_DIR = PROJECT_ROOT / "logs"

    MEMORY_DIR = PROJECT_ROOT / "memory"

    OUTPUT_DIR = PROJECT_ROOT / "outputs"
    FIGURES_DIR = OUTPUT_DIR / "figures"
    REPORTS_DIR = OUTPUT_DIR / "reports"
    METRICS_DIR = OUTPUT_DIR / "metrics"
    TOOL_CALLS_DIR = OUTPUT_DIR / "tool_calls"

    MODEL_DIR = PROJECT_ROOT / "models"

    OLLAMA_MODEL = "qwen2.5:7b"

    MAX_ITERATIONS = 5

    TEMPERATURE = 0.2

    RANDOM_STATE = 42


settings = Settings()