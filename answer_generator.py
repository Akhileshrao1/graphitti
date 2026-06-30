from prompts import ANSWER_PROMPT
from llm import llm


chain = ANSWER_PROMPT | llm


def generate_answer(question: str, context: str) -> str:
    """
    Generates the final answer from the retrieved context.
    """

    response = chain.invoke(
        {
            "question": question,
            "context": context
        }
    )

    return response.content