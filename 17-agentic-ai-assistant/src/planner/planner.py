from src.tools.registry import ToolRegistry
from src.planner.models import ExecutionPlan

class Planner:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def available_tools(self) -> list[dict]:

        return self.registry.get_tool_descriptions()
    
    def create_plan(self, question: str) -> ExecutionPlan:

        question = question.lower()

        if any(word in question for word in [
            "+", "-", "*", "/", "plus", "minus", "multiply", "divide"
        ]):

            return ExecutionPlan(
                goal="Solve the mathematical calculation.",

                steps=[
                    "Analyze the mathematical request.",
                    "Select the Calculator tool.",
                    "Evaluate the expression.",
                    "Return the calculated result."
                ],

                estimated_tools=[
                    "calculator"
                ]
            )

        return ExecutionPlan(
            goal="Answer the user's request.",

            steps=[
                "Understand the user's request.",
                "Choose the appropriate tool.",
                "Execute the tool.",
                "Return the final answer."
            ],

            estimated_tools=[]
        )