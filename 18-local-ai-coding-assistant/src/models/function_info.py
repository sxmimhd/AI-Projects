from dataclasses import dataclass
from pathlib import Path

@dataclass
class FunctionInfo:

    name: str

    file_path: Path

    start_line: int

    end_line: int

    arguments: list[str]

    docstring: str | None

    parent_class: str | None = None