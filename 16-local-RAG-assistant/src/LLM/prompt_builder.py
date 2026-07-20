from src.core.document import Document


class PromptBuilder:

    @staticmethod
    def build(
        question: str,
        documents: list[Document]
    ) -> str:

        context = []

        for index, document in enumerate(documents, start=1):

            context.append(
                f"""
Document {index}

Title:
{document.title}

Content:
{document.document}
"""
            )

        context = "\n" + ("\n" + "-" * 80 + "\n").join(context)

        prompt = f"""
You are an AI assistant specialized in Steam games.

Answer the user's question using ONLY the information contained in the provided documents.

If the answer cannot be found in the documents, clearly say that you do not have enough information.

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt.strip()