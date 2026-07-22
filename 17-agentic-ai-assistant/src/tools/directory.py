from pathlib import Path

from src.tools.base_tool import BaseTool


class DirectoryTool(BaseTool):

    @property
    def name(self):
        return "directory"

    @property
    def description(self):
        return "List files and folders inside a directory."

    @property
    def parameters(self):
        return {
            "path": "Directory path."
        }

    def execute(self, path: str = "."):

        try:
            directory = Path(path)

            if not directory.exists():
                return {
                    "success": False,
                    "result": None,
                    "tool": self.name,
                    "error": "Directory not found."
                }

            items = []

            for item in directory.iterdir():

                items.append({
                    "name": item.name,
                    "type": "folder" if item.is_dir() else "file"
                })

            return {
                "success": True,
                "result": items,
                "tool": self.name,
                "error": None
            }

        except Exception as e:

            return {
                "success": False,
                "result": None,
                "tool": self.name,
                "error": str(e)
            }