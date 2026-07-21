class PromptBuilder:

    @staticmethod
    def build_tool_selection_prompt(
        question: str,
        tools: list[dict],
        history: list[dict],
    ) -> str:

        tool_descriptions = "\n".join(
            f"- {tool['name']}: {tool['description']}"
            for tool in tools
        )
        
        conversation = "\n".join(
            f"{item['role']}: {item['content']}"
            for item in history
        )

        return f"""
        You are an AI planning agent.

        Conversation History

        {conversation}

        Available Tools

        {tool_descriptions}

        Current User Question

        {question}

        Return ONLY valid JSON.
        """