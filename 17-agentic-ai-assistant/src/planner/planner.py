from src.tools.registry import ToolRegistry
from src.planner.models import ExecutionPlan


class Planner:

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def available_tools(self) -> list[dict]:
        return self.registry.get_tool_descriptions()

    def create_plan(self, question: str) -> ExecutionPlan:

        question = question.lower()

        # Mathematical requests
        if any(word in question for word in [
            "+", "-", "*", "/", "%",
            "plus", "minus",
            "multiply", "divide",
            "calculate", "compute"
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

        # Directories requests
        if any(word in question for word in [
            "list",
            "folder",
            "directory",
            "files",
            "contents"
        ]):

            return ExecutionPlan(
                goal="Inspect a directory.",

                steps=[
                    "Determine the requested directory.",
                    "Select the Directory tool.",
                    "List the directory contents.",
                    "Return the results."
                ],

                estimated_tools=[
                    "directory"
                ]
            )

        # File reading requests
        if any(word in question for word in [
            "read",
            "open",
            "load",
            "file",
            ".txt",
            ".md",
            ".csv"
        ]):

            return ExecutionPlan(
                goal="Read the requested file.",
                steps=[
                    "Locate the requested file.",
                    "Select the File Reader tool.",
                    "Read the file contents.",
                    "Return the extracted text."
                ],
                estimated_tools=[
                    "file_reader"
                ]
            )

        #system info
        if any(word in question for word in [
            "system",
            "computer",
            "cpu",
            "ram",
            "memory",
            "python",
            "operating system",
            "os",
            "directory"
        ]):

            return ExecutionPlan(
                goal="Retrieve system information.",

                steps=[
                    "Understand the requested system information.",
                    "Select the System tool.",
                    "Retrieve system details.",
                    "Return the information."
                ],

                estimated_tools=[
                    "system"
                ]
            )

        

        return ExecutionPlan(
            goal="Answer the user's request.",
            steps=[
                "Understand the user's request.",
                "Select the most appropriate tool.",
                "Execute the tool if needed.",
                "Generate the final response."
            ],
            estimated_tools=[]
        )