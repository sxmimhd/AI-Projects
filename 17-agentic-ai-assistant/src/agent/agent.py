from rich.console import Console
from rich.table import Table

from src.executor.executor import ToolExecutor
from src.LLM.client import LLMClient
from src.planner.planner import Planner
from src.prompting.prompt_builder import PromptBuilder
from src.tools.calculator import CalculatorTool
from src.tools.registry import ToolRegistry
from src.memory.conversation import ConversationMemory

class Agent:

    def __init__(self):
        self.console = Console()

        # Tool Registry
        self.registry = ToolRegistry()
        self.registry.register(CalculatorTool())

        # Core Components
        self.executor = ToolExecutor(self.registry)
        self.planner = Planner(self.registry)
        self.llm = LLMClient()

        self.memory = ConversationMemory()

    def display_tools(self) -> None:

        self.console.print("\n[bold magenta]Available Tools[/bold magenta]\n")

        for tool in self.planner.available_tools():
            self.console.print(f"[cyan]{tool['name']}[/cyan]")
            self.console.print(tool["description"])
            self.console.print()

    def run(self, question: str) -> None:
        self.memory.add_user_message(question)

        prompt = PromptBuilder.build_tool_selection_prompt(
            question=question,
            tools=self.planner.available_tools(),
            history=self.memory.get_history(),
        )

        decision = self.llm.generate(prompt)

        result = self.executor.execute(
            tool_name=decision.tool,
            **decision.arguments,
        )

        self.memory.add_assistant_message(
            str(result["result"])
        )

        self.console.rule("[bold blue]Agent Reasoning[/bold blue]")

        self.console.print(f"[cyan]Question[/cyan] : {question}")
        self.console.print(f"[cyan]Selected Tool[/cyan] : {decision.tool}")
        self.console.print(f"[cyan]Reason[/cyan] : {decision.reason}")
        self.console.print(f"[cyan]Arguments[/cyan] : {decision.arguments}")

        self.console.print()

        table = Table(title="Execution Result")

        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        for key, value in result.items():
            table.add_row(str(key), str(value))

        self.console.print(table)