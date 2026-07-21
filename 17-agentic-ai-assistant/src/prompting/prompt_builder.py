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
        You are an intelligent AI Agent.

        Your task is to choose the SINGLE best tool for solving the user's request.

        Rules:

        1. Read the ENTIRE conversation history.
        2. The user may refer to previous answers using words like:
        - it
        - that
        - previous result
        - previous answer
        - plus
        - minus
        - multiply it
        - divide it

        3. Resolve those references using the conversation history.

        4. If the user asks for a mathematical calculation,
        always generate a complete mathematical expression.

        5. Never ask questions.

        6. Return ONLY valid JSON.

        Conversation History

        {conversation}

        Available Tools

        {tool_descriptions}

        Current User Question

        {question}
        """