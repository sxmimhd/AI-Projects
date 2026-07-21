from collections import deque
from src.memory.event import AgentEvent


class ConversationMemory:

    def __init__(
        self,
        max_messages: int = 10,
        max_events: int = 10,
    ):

        self.history = deque(maxlen=max_messages)

        self.events = deque(maxlen=max_events)

    # Chat Messages

    def add_user_message(self, message: str):

        self.history.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str):

        self.history.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

    def get_history(self):

        return list(self.history)

    # Agent Events

    def add_event(self, event: AgentEvent):

        self.events.append(event)

    def get_events(self):

        return list(self.events)

    def latest_event(self):

        if not self.events:
            return None

        return self.events[-1]

    def clear(self):

        self.history.clear()

        self.events.clear()