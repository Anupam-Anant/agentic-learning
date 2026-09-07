"""
langchain_model.py  — shared chat-model factory for the Week 3 LangChain demos.

This is a SHARED MODULE, not an entry point (same role as week1/code/openai_client.py):
the three langchain_*_demo.py scripts import get_chat_model() from here so provider
config lives in ONE place. Think a singleton "which LLM?" bean.

PROVIDER-SWAPPABLE (matches the repo's ethos):
  * If COHERE_API_KEY is set  -> ChatCohere  (faithful to the course notebooks)
  * elif OPENAI_API_KEY is set -> ChatOpenAI  (the key you already have from Week 1)
  * else -> a clear error telling you what to set.

Setup:
  pip install langchain langchain-core langchain-classic
  # plus ONE provider:
  pip install langchain-cohere   &&  export COHERE_API_KEY=...   # free tier at cohere.com
  # or
  pip install langchain-openai   &&  export OPENAI_API_KEY=...

Why LangChain hides the provider: this whole file is the "JCA/JDBC" seam from SG03 §2②
— the demos never name a vendor; they just ask for "a chat model" and pipe it into a chain.
"""

import os


def get_chat_model(temperature: float = 0.2):
    """Return a LangChain chat model, picking the provider from environment variables.

    temperature: 0 = deterministic/repeatable, higher = more varied wording.
    """
    if os.getenv("COHERE_API_KEY"):
        # ChatCohere reads COHERE_API_KEY from the environment automatically.
        from langchain_cohere import ChatCohere

        return ChatCohere(model="command-a-03-2025", temperature=temperature)

    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)

    raise RuntimeError(
        "No LLM provider configured. Set COHERE_API_KEY (free at cohere.com) "
        "or OPENAI_API_KEY, and pip install the matching langchain-<provider> package."
    )
