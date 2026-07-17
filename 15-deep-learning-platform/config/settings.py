from pathlib import Path
import torch

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
MODELS_DIR = ROOT_DIR / "models"
OUTPUTS_DIR = ROOT_DIR / "outputs"

FIGURES_DIR = OUTPUTS_DIR / "figures"
METRICS_DIR = OUTPUTS_DIR / "metrics"
PREDICTIONS_DIR = OUTPUTS_DIR / "predictions"
EXPLAINABILITY_DIR = OUTPUTS_DIR / "explainability"
REPORTS_DIR = OUTPUTS_DIR / "reports"
HISTORY_DIR = OUTPUTS_DIR / "history"


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

IMAGE_SIZE = 224

BATCH_SIZE = 32

LEARNING_RATE = 0.001

EPOCHS = 5

PATIENCE = 5

NUM_WORKERS = 2

RANDOM_STATE = 42

MAX_VOCAB_SIZE = 20000

MAX_SEQUENCE_LENGTH = 100

EMBEDDING_DIM = 128

HIDDEN_DIM = 128

DROPOUT = 0.3