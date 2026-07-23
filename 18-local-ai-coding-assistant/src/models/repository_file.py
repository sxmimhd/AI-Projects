from dataclasses import dataclass
from pathlib import Path

@dataclass
class RepositoryFile:
    path: Path
    extension: str
    size_bytes: int
    line_count: int

    @property
    def filename(self):
        return self.path.name

    @property
    def relative_path(self):
        return str(self.path)

    @property
    def stem(self):
        return self.path.stem

    @property
    def parent_directory(self):
        return str(self.path.parent)