from pydantic import BaseModel, Field


class ToolDecision(BaseModel):

    tool: str = Field(
        description="Name of the selected tool."
    )

    arguments: dict = Field(
        default_factory=dict,
        description="Arguments passed to the tool."
    )

    reason: str = Field(
        description="Reason for choosing the tool."
    )