from dataclasses import dataclass

@dataclass(slots=True)
class VisionResponse:
    answer: str
    inference_time: float
    model: str