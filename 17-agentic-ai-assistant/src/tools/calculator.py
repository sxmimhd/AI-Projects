from src.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):

    name = "calculator"

    description = (
        "Evaluate mathematical expressions "
        "using +, -, *, /, %, ** and parentheses."
    )

    def execute(self, expression: str) -> dict:

        try:
            result = eval(
                expression,
                {"__builtins__": {}},
                {},
            )

            return {
                "success": True,
                "result": result,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "result": None,
                "error": str(e),
            }