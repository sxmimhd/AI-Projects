from dataclasses import dataclass

@dataclass
class AgentEvent:

    question: str

    thought: str

    tool: str

    arguments: dict

    observation: str

    answer: str