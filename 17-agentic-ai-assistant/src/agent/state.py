from dataclasses import dataclass, field

@dataclass
class AgentState:

    question: str

    current_thought: str = ""

    selected_tool: str = ""

    tool_arguments: dict = field(default_factory=dict)

    observation: str = ""

    final_answer: str = ""

    iterations: int = 0

    tool_calls: list = field(default_factory=list)

    plan: list[str] = field(default_factory=list)

    current_step: int = 0
    
    finished: bool = False