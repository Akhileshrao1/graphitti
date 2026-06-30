from langchain_core.prompts import ChatPromptTemplate


# ==========================================================
# ROUTER PROMPT
# ==========================================================

ROUTER_PROMPT = ChatPromptTemplate.from_template(
"""
You are an intelligent query router.

Your task is to choose ONLY ONE retrieval strategy based on the user's intent.

Available strategies:

1. dense
- Semantic questions, general explanations, concept understanding.
Examples: "What is Python?", "Explain decorators."

2. bm25
- Exact keyword search, specific function/API/class names.
Examples: "What is zipimport?", "What is asyncio.run()?"

3. graph
- Relationship-based questions, connections, dependencies, or ownership.
Examples: "Who created Python?", "How is asyncio related to event loop?"

4. hybrid
- Complex technical queries needing both keyword precision and semantic depth.
Examples: "Explain asyncio.run() with an example."

5. chat
- Casual greetings, small talk, introductions, or pleasantries.
- Use this if the user is not asking for specific technical documentation or database facts.
Examples: "hello", "hi", "my name is tharun", "how are you?", "thanks!"

------------------------------------

Return ONLY ONE WORD from the allowed outputs. Do not include punctuation.

Allowed outputs:
dense
bm25
graph
hybrid
chat

Question:
{question}
"""
)


# ==========================================================
# UPDATED ANSWER PROMPT
# ==========================================================





# ==========================================================
# ANSWER PROMPT
# ==========================================================

ANSWER_PROMPT = ChatPromptTemplate.from_template(
"""


You are a helpful and intelligent AI assistant.

CRITICAL INSTRUCTIONS FOR CONTEXT:
1. If the 'Context' section below contains actual retrieved facts or documentation, answer the question accurately using ONLY that context. If the technical answer isn't in that context, reply exactly: "I don't know."
2. If the 'Context' section is empty, "No related information found", or contains general conversational text, it means this is a casual chat or greeting. In this case, IGNORE the "I don't know" rule and respond naturally, politely, and conversationally to the user.

----------------------------
Context:
{context}
----------------------------

Question:
{question}

----------------------------
Answer:

"""
)