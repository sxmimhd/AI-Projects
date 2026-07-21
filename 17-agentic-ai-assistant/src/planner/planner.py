from src.tools.registry import ToolRegistry


class Planner:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def available_tools(self) -> list[dict]:

        return self.registry.get_tool_descriptions()