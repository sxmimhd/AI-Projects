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

        Rules

        1. Read the conversation history before answering.

        2. Use the conversation history ONLY if the current message refers to previous context (for example: it, that, previous result, previous answer).

        3. If the current question is complete by itself, ignore previous conversation.

        4. Choose the SINGLE most appropriate tool.

        5. Provide all required arguments for that tool.

        6. Return valid JSON only.

        7. Do not include markdown or code fences.


        Available Tools

        {tool_descriptions}

        
        Conversation History
        
            {conversation}

        Current User Question

        {question}

        Return a JSON object with this structure:

        Return ONLY one JSON object.

        Example for Calculator:

        {{
            "tool": "calculator",
            "arguments": {{
                "expression": "5 + 7"
            }},
            "reason": "The user requested a mathematical calculation."
        }}

        Example for File Reader:

        {{
            "tool": "file_reader",
            "arguments": {{
                "filepath": "README.md"
            }},
            "reason": "The user requested to read a file."
        }}

        Example for System Tool:

        {{
            "tool": "system",
            "arguments": {{}},
            "reason": "The user requested information about the current computer."
        }}

        If the user wants to inspect folders or list files,
        use the directory tool.
        {{
            "tool": "directory",
            "arguments": {{
                "path": "."
            }},
            "reason": "..."
        }}

        Do not use markdown.
        Do not wrap the JSON in ```json.
        Return JSON only.

        The arguments object must contain all parameters required by the selected tool.

        Do not write explanations.

        """