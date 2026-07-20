from pathlib import Path
import json
import pickle
import numpy as np

from config import settings

def create_directories() -> None:
    directories = [
        settings.DATA_DIR,
        settings.RAW_DATA_DIR,
        settings.PROCESSED_DATA_DIR,
        settings.MODELS_DIR,
        settings.OUTPUTS_DIR,
        settings.REPORTS_DIR,
        settings.FIGURES_DIR,
        settings.LOGS_DIR,
        settings.QUERIES_DIR,
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def save_pickle(obj, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as file:
        pickle.dump(obj, file)


def load_pickle(filepath: Path):
    with open(filepath, "rb") as file:
        return pickle.load(file)


def save_json(data: dict, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_json(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


def save_numpy(array: np.ndarray, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)

    np.save(filepath, array)


def load_numpy(filepath: Path) -> np.ndarray:
    return np.load(filepath)


def file_exists(filepath: Path) -> bool:
    return Path(filepath).exists()