from src.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:

        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> BaseTool | None:

        return self._tools.get(tool_name)

    def list_tools(self) -> list[str]:

        return list(self._tools.keys())
    
    def get_tool_descriptions(self) -> list[dict]:

        return [
            {
                "name": tool.name,
                "description": tool.description,
            }
            for tool in self._tools.values()
        ]