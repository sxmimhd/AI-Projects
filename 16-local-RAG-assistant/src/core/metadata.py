from dataclasses import dataclass, field


@dataclass(slots=True)
class Metadata:
    game_id: int
    title: str
    metadata: dict = field(default_factory=dict)