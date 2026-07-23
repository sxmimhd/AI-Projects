from enum import Enum


class PromptType(Enum):
    SCENE = "scene"
    OCR = "ocr"
    CHART = "chart"
    UI = "ui"
    DOCUMENT = "document"
    CODE = "code"
    GAME = "game"
    DIAGRAM = "diagram"
    GENERAL = "general"


class PromptBuilder:

    SYSTEM_PROMPT = (
        "You are an expert AI Vision Assistant. "
        "Carefully analyze the provided image and answer accurately. "
        "Do not invent details that are not visible. "
        "If something is uncertain, clearly state that."
    )

    PROMPTS = {
        PromptType.SCENE: (
            "Describe this image in detail.\n"
            "Mention the environment, objects, people, actions, "
            "lighting, colors, and anything noteworthy."
        ),
        PromptType.OCR: (
            "Extract every visible text from the image.\n"
            "Preserve formatting whenever possible."
        ),
        PromptType.CHART: (
            "Analyze this chart.\n"
            "Explain trends, patterns, anomalies, and summarize the data."
        ),
        PromptType.UI: (
            "Explain this user interface.\n"
            "Describe the layout, components, and their purpose."
        ),
        PromptType.DOCUMENT: (
            "Summarize this document.\n"
            "Extract the important information and key points."
        ),
        PromptType.CODE: (
            "Analyze this code screenshot.\n"
            "Explain what the code does, identify possible issues, "
            "and suggest improvements."
        ),
        PromptType.GAME: (
            "Identify the game if possible.\n"
            "Describe the gameplay, environment, HUD, and genre."
        ),
        PromptType.DIAGRAM: (
            "Explain this diagram.\n"
            "Describe the relationships and summarize its meaning."
        ),
        PromptType.GENERAL: (
            "Analyze the image carefully and answer the user's question."
        ),
    }

    @classmethod
    def build(
        cls,
        prompt_type: PromptType = PromptType.GENERAL,
        user_question: str | None = None,
    ) -> str:

        prompt = cls.PROMPTS[prompt_type]

        if user_question:
            prompt += f"\n\nUser Question:\n{user_question}"

        return (
            f"{cls.SYSTEM_PROMPT}\n\n"
            f"{prompt}"
        )