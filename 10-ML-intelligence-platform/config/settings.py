from pathlib import Path

RANDOM_STATE = 42

# Machine Learning

TEST_SIZE = 0.20
CV_FOLDS = 5

# Output Directories

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = BASE_DIR / "models"

OUTPUT_DIR = BASE_DIR / "outputs"

REPORT_DIR = OUTPUT_DIR / "reports"

CHART_DIR = OUTPUT_DIR / "charts"

PREDICTION_DIR = OUTPUT_DIR / "predictions"

LOG_DIR = OUTPUT_DIR / "logs"