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

    def to_embedding_text(self) -> str:

        text = [
            f"Type: {self.chunk_type}",
            f"Name: {self.name}",
        ]

        if self.parent_class:
            text.append(f"Class: {self.parent_class}")

        text.append(f"File: {self.file_path}")

        text.append("")
        text.append("Code:")
        text.append(self.content)

        return "\n".join(text)