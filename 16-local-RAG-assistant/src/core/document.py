from dataclasses import dataclass, field


@dataclass(slots=True)
class Document:
    game_id: int
    title: str
    document: str
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "game_id": self.game_id,
            "title": self.title,
            "document": self.document,
            "metadata": self.metadata,
        }