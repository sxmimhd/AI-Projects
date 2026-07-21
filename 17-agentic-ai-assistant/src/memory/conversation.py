from collections import deque


class ConversationMemory:
    """
    Stores the recent conversation between
    the user and the assistant.
    """

    def __init__(self, max_messages: int = 10):

        self.history = deque(maxlen=max_messages)

    def add_user_message(self, message: str) -> None:

        self.history.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:

        self.history.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_history(self) -> list[dict]:

        return list(self.history)

    def clear(self) -> None:

        self.history.clear()