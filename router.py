from llm import llm
from prompts import ROUTER_PROMPT


router_chain = ROUTER_PROMPT | llm


def route_question(question: str) -> str:
    """
    Routes the user's question to the most suitable retrieval strategy.

    Returns one of:
        dense
        bm25
        graph
        hybrid
    """

    response = router_chain.invoke(
        {
            "question": question
        }
    )

    strategy = response.content.strip().lower()

    valid = {
        "dense",
        "bm25",
        "graph",
        "hybrid"
    }

    if strategy not in valid:
        strategy = "dense"

    return strategy