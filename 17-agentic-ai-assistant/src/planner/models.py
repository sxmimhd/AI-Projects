from pydantic import BaseModel

class ExecutionPlan(BaseModel):
    goal: str
    steps: list[str]
    estimated_tools: list[str]