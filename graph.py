from typing import TypedDict

from langgraph.graph import StateGraph, END

from router import route_question
from answer_generator import generate_answer

from search_dense import DenseRetriever
from check_bm25 import BM25Retriever
from search_graph import GraphRetriever

# ==========================================================
# Create ONE retriever object
# ==========================================================
dense = DenseRetriever()

bm25 = BM25Retriever()

graph_retriever = GraphRetriever()


# ==========================================================
# Graph State
# ==========================================================

class GraphState(TypedDict):
    question: str
    strategy: str
    context: str
    answer: str


# ==========================================================
# Router Node
# ==========================================================

def router_node(state: GraphState):

    strategy = route_question(state["question"])

    state["strategy"] = strategy

    return state


# ==========================================================
# Retrieval Node
# ==========================================================

def retrieval_node(state: GraphState):

    question = state["question"]
    strategy = state["strategy"]

    if strategy == "dense":

        results = dense.dense_search(question)

    elif strategy == "bm25":

        results = bm25.bm25_search(question)

    elif strategy == "graph":

        results = graph_retriever.graph_search(question)

    elif strategy == "hybrid":

        dense_results = dense.dense_search(question)

        bm25_results = bm25.bm25_search(question)

        results = dense_results + bm25_results

    else:

        raise ValueError(
            f"Unknown retrieval strategy : {strategy}"
        )

    # Convert list -> string for LLM
    context = "\n\n".join(

    item["text"]

    for item in results
   )

    state["context"] = context

    return state


# ==========================================================
# Answer Generator Node
# ==========================================================

def answer_node(state: GraphState):

    answer = generate_answer(
        state["question"],
        state["context"]
    )

    state["answer"] = answer

    return state


# ==========================================================
# Build LangGraph
# ==========================================================

builder = StateGraph(GraphState)

builder.add_node("router", router_node)

builder.add_node("retriever", retrieval_node)

builder.add_node("answer", answer_node)

builder.set_entry_point("router")

builder.add_edge("router", "retriever")

builder.add_edge("retriever", "answer")

builder.add_edge("answer", END)

graph = builder.compile()