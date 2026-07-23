from src.models.code_chunk import CodeChunk


class PromptBuilder:

    def build(
        self,
        question: str,
        chunks: list[CodeChunk],
    ) -> str:

        context = []

        for chunk in chunks:

            title = chunk.name

            if chunk.parent_class:

                title = f"{chunk.parent_class}.{chunk.name}"

            context.append(
                f"""
                === {chunk.chunk_type.upper()} ===
                Name: {title}
                File: {chunk.file_path}

                {chunk.content}
                """
                            )

        prompt = f"""
            You are an expert Python software engineer.

            Answer the user's question ONLY using the repository context below.

            If the answer cannot be determined from the context, clearly say so.

            Repository Context:

            {"".join(context)}

            User Question:

            {question}

            Answer:
            """

        return prompt