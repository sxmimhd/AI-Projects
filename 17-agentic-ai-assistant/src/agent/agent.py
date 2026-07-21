from rich.console import Console
from rich.table import Table

from src.executor.executor import ToolExecutor
from src.LLM.client import LLMClient
from src.planner.planner import Planner
from src.prompting.prompt_builder import PromptBuilder
from src.tools.calculator import CalculatorTool
from src.tools.registry import ToolRegistry
from src.memory.conversation import ConversationMemory
from src.agent.state import AgentState
from src.memory.event import AgentEvent

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

        # Create the execution state
        state = AgentState(question=question)

        # Save the user's message
        self.memory.add_user_message(state.question)

        # Build the prompt
        prompt = PromptBuilder.build_tool_selection_prompt(
            question=state.question,
            tools=self.planner.available_tools(),
            history=self.memory.get_history(),
        )

        # Ask the LLM to decide what to do
        decision = self.llm.generate(prompt)

        # Update the state with the LLM decision
        state.current_thought = decision.reason
        state.selected_tool = decision.tool
        state.tool_arguments = decision.arguments
        self.console.print("\n[bold yellow]Raw LLM Decision[/bold yellow]")
        self.console.print(decision)

        # Execute the selected tool
        result = self.executor.execute(
            tool_name=state.selected_tool,
            **state.tool_arguments,
        )

        # Update the state with the observation
        state.observation = str(result["result"])
        state.tool_calls.append(result)
        state.iterations += 1

        # Save assistant response into memory
        self.memory.add_assistant_message(state.observation)

        event = AgentEvent(
            question=state.question,
            thought=state.current_thought,
            tool=state.selected_tool,
            arguments=state.tool_arguments,
            observation=state.observation,
            answer=state.observation,
        )
        self.memory.add_event(event)

        # Display reasoning

        self.console.rule("[bold blue]Agent Reasoning[/bold blue]")

        self.console.print(f"[cyan]Question[/cyan]      : {state.question}")
        self.console.print(f"[cyan]Thought[/cyan]      : {state.current_thought}")
        self.console.print(f"[cyan]Selected Tool[/cyan] : {state.selected_tool}")
        self.console.print(f"[cyan]Arguments[/cyan]     : {state.tool_arguments}")
        self.console.print(f"[cyan]Observation[/cyan]   : {state.observation}")
        self.console.print(f"[cyan]Iterations[/cyan]    : {state.iterations}")

        # Execution table

        table = Table(title="Execution Result")

        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        for key, value in result.items():
            table.add_row(str(key), str(value))

        self.console.print()
        self.console.print(table)


        latest = self.memory.latest_event()

        self.console.print()

        self.console.rule("[bold green]Latest Agent Event[/bold green]")

        self.console.print(f"[cyan]Question[/cyan]    : {latest.question}")
        self.console.print(f"[cyan]Thought[/cyan]    : {latest.thought}")
        self.console.print(f"[cyan]Tool[/cyan]        : {latest.tool}")
        self.console.print(f"[cyan]Arguments[/cyan]   : {latest.arguments}")
        self.console.print(f"[cyan]Observation[/cyan] : {latest.observation}")
        self.console.print(f"[cyan]Answer[/cyan]      : {latest.answer}")