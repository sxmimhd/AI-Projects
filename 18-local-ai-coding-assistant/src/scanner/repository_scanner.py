from pathlib import Path

from config import settings
from src.models.repository_file import RepositoryFile
from collections import Counter

class RepositoryScanner:

    def __init__(self):
        self.files = []

    def scan(self):

        self.files.clear()

        for file_path in settings.REPOSITORY_PATH.rglob("*"):

            # Ignore directories
            if file_path.is_dir():
                continue

            # Ignore unwanted folders
            if any(
                ignored in file_path.parts
                for ignored in settings.IGNORED_DIRECTORIES
            ):
                continue

            # Supported extension?
            if file_path.suffix not in settings.SUPPORTED_EXTENSIONS:
                continue

            repository_file = RepositoryFile(
                path=file_path.relative_to(settings.REPOSITORY_PATH),
                extension=file_path.suffix,
                size_bytes=file_path.stat().st_size,
                line_count=self._count_lines(file_path),
            )

            self.files.append(repository_file)

        return self.files

    @staticmethod
    def _count_lines(path: Path) -> int:

        try:
            with open(path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def get_statistics(self):

        extension_counter = Counter(file.extension for file in self.files)

        total_files = len(self.files)
        total_lines = sum(file.line_count for file in self.files)
        total_size = sum(file.size_bytes for file in self.files)

        return {
            "total_files": total_files,
            "extensions": extension_counter,
            "total_lines": total_lines,
            "average_lines": total_lines / total_files if total_files else 0,
            "average_size": total_size / total_files if total_files else 0,
        }