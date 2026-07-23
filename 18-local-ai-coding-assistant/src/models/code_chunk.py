from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeChunk:

    chunk_id: str

    chunk_type: str # class | function | method

    name: str

    content: str

    file_path: Path

    start_line: int
    end_line: int

    parent_class: str | None = None