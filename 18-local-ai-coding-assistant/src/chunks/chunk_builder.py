from pathlib import Path

from src.models.class_info import ClassInfo
from src.models.code_chunk import CodeChunk
from src.models.function_info import FunctionInfo


class ChunkBuilder:
    """
    Builds semantic chunks from parsed code.
    """

    def build_chunks(
        self,
        file_path: Path,
        functions: list[FunctionInfo],
        classes: list[ClassInfo],
    ) -> list[CodeChunk]:

        with open(file_path, "r", encoding="utf-8") as file:
            source = file.readlines()

        chunks = []

        # -----------------------------------
        # Standalone Functions
        # -----------------------------------

        for function in functions:

            code = "".join(
                source[
                    function.start_line - 1:
                    function.end_line
                ]
            )

            chunks.append(
                CodeChunk(
                    chunk_id=f"function::{function.name}",
                    chunk_type="function",
                    name=function.name,
                    content=code,
                    file_path=file_path,
                    start_line=function.start_line,
                    end_line=function.end_line,
                )
            )

        # -----------------------------------
        # Classes
        # -----------------------------------

        for cls in classes:

            class_code = "".join(
                source[
                    cls.start_line - 1:
                    cls.end_line
                ]
            )

            # Class chunk

            chunks.append(
                CodeChunk(
                    chunk_id=f"class::{cls.name}",
                    chunk_type="class",
                    name=cls.name,
                    content=class_code,
                    file_path=file_path,
                    start_line=cls.start_line,
                    end_line=cls.end_line,
                )
            )

            # -----------------------------------
            # Method chunks
            # -----------------------------------

            for method in cls.methods:

                method_code = "".join(
                    source[
                        method.start_line - 1:
                        method.end_line
                    ]
                )

                chunks.append(
                    CodeChunk(
                        chunk_id=f"method::{cls.name}.{method.name}",
                        chunk_type="method",
                        name=method.name,
                        parent_class=cls.name,
                        content=method_code,
                        file_path=file_path,
                        start_line=method.start_line,
                        end_line=method.end_line,
                    )
                )

        return chunks