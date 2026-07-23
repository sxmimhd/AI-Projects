import ast
from pathlib import Path

from src.models.class_info import ClassInfo
from src.models.function_info import FunctionInfo
from src.models.import_info import ImportInfo

class ASTParser:

    def parse(self, file_path: Path):

        with open(file_path, "r", encoding="utf-8") as file:
            source_code = file.read()

        tree = ast.parse(source_code)

        functions: list[FunctionInfo] = []
        classes: list[ClassInfo] = []
        imports = []

        # Only inspect the module's direct children
        for node in tree.body:

            if isinstance(node, ast.FunctionDef):

                functions.append(
                    self._parse_function(
                        node=node,
                        file_path=file_path
                    )
                )

            elif isinstance(node, ast.ClassDef):

                classes.append(
                    self._parse_class(
                        node=node,
                        file_path=file_path
                    )
                )

        return functions, classes, imports

    def _parse_function(
        self,
        node: ast.FunctionDef,
        file_path: Path,
        parent_class: str | None = None,
    ) -> FunctionInfo:

        return FunctionInfo(
            name=node.name,

            file_path=file_path,

            start_line=node.lineno,
            end_line=node.end_lineno,

            arguments=[
                arg.arg
                for arg in node.args.args
            ],

            docstring=ast.get_docstring(node),

            parent_class=parent_class,
        )

    def _parse_class(
        self,
        node: ast.ClassDef,
        file_path: Path,
    ) -> ClassInfo:

        methods = []

        for child in node.body:

            if isinstance(child, ast.FunctionDef):

                methods.append(
                    self._parse_function(
                        node=child,
                        file_path=file_path,
                        parent_class=node.name,
                    )
                )

        return ClassInfo(
            name=node.name,

            file_path=file_path,

            start_line=node.lineno,
            end_line=node.end_lineno,

            docstring=ast.get_docstring(node),

            methods=methods,
        )

    def _parse_import(
        self,
        node,
        file_path: Path,
    ):

        imports = []

        # import numpy as np
        if isinstance(node, ast.Import):

            for alias in node.names:

                imports.append(
                    ImportInfo(
                        module=alias.name,
                        name=None,
                        alias=alias.asname,
                        file_path=file_path,
                    )
                )

        # from pathlib import Path
        elif isinstance(node, ast.ImportFrom):

            for alias in node.names:

                imports.append(
                    ImportInfo(
                        module=node.module,
                        name=alias.name,
                        alias=alias.asname,
                        file_path=file_path,
                    )
                )

        return imports