from time import perf_counter

from src.tools.registry import ToolRegistry


class ToolExecutor:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(self, tool_name: str, **kwargs) -> dict:

        tool = self.registry.get(tool_name)

        if tool is None:
            return {
                "success": False,
                "tool": tool_name,
                "result": None,
                "error": f"Tool '{tool_name}' is not registered.",
                "execution_time": 0.0,
            }

        start_time = perf_counter()

        response = tool.execute(**kwargs)

        execution_time = perf_counter() - start_time

        response["tool"] = tool_name
        response["execution_time"] = execution_time

        return response