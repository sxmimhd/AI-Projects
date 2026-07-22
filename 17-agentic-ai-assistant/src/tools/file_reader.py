from pathlib import Path


class FileReaderTool:

    name = "file_reader"

    description = (
        "Read text files (.txt, .md, .csv) and return their contents."
    )

    supported_extensions = {
        ".txt",
        ".md",
        ".csv",
    }

    def execute(self, filepath: str):

        try:

            path = Path(filepath)

            if not path.exists():
                raise FileNotFoundError(
                    f"{filepath} does not exist."
                )

            if path.suffix.lower() not in self.supported_extensions:
                raise ValueError(
                    f"Unsupported file type: {path.suffix}"
                )

            text = path.read_text(
                encoding="utf-8"
            )

            return {
                "success": True,
                "result": text,
                "tool": self.name,
                "error": None,
            }

        except Exception as e:

            return {
                "success": False,
                "result": None,
                "tool": self.name,
                "error": str(e),
            }