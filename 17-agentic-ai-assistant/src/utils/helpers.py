from pathlib import Path


def create_directories(paths: list[Path]) -> None:
    """
    Create project directories if they do not exist.
    """

    for path in paths:
        path.mkdir(parents=True, exist_ok=True)