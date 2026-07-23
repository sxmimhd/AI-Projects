from dataclasses import dataclass, field
from pathlib import Path

from src.models.function_info import FunctionInfo


@dataclass
class ClassInfo:

    name: str

    file_path: Path

    start_line: int
    end_line: int

    docstring: str | None

    methods: list[FunctionInfo] = field(default_factory=list)