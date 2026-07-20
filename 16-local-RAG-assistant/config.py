from pathlib import Path

class Settings:

    PROJECT_NAME = "Local RAG Knowledge Assistant"
    VERSION = "1.0.0"

    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"

    MODELS_DIR = BASE_DIR / "models"

    OUTPUTS_DIR = BASE_DIR / "outputs"
    REPORTS_DIR = OUTPUTS_DIR / "reports"
    FIGURES_DIR = OUTPUTS_DIR / "figures"
    LOGS_DIR = OUTPUTS_DIR / "logs"
    QUERIES_DIR = OUTPUTS_DIR / "queries"

    DATASET_FILENAME = "steam_games.csv"
    DATASET_PATH = RAW_DATA_DIR / DATASET_FILENAME

    DOCUMENTS_PATH = PROCESSED_DATA_DIR / "documents.pkl"
    CLEAN_DATA_PATH = PROCESSED_DATA_DIR / "clean_dataset.csv"

    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

    EMBEDDING_DIMENSION = 384

    EMBEDDINGS_PATH = MODELS_DIR / "embeddings.npy"

    FAISS_INDEX_PATH = MODELS_DIR / "faiss.index"
    METADATA_PATH = MODELS_DIR / "metadata.pkl"

    TOP_K_RESULTS = 5

    LLM_MODEL = "qwen2.5:7b"

    TEMPERATURE = 0.2

    MAX_TOKENS = 512

    USE_CHUNKING = False

    CHUNK_SIZE = 500

    CHUNK_OVERLAP = 100

    RANDOM_STATE = 42

    EMBEDDING_BATCH_SIZE = 64
    NORMALIZE_EMBEDDINGS = True
    SHOW_PROGRESS_BAR = True

    LOG_FILE = LOGS_DIR / "project.log"
    LOG_LEVEL = "INFO"


settings = Settings()