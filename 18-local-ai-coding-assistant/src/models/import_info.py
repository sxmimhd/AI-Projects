from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImportInfo:
    
    module: str
    name: str | None

    alias: str | None

    file_path: Path