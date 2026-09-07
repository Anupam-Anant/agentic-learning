"""
langchain_simple_chain_demo.py
==============================
Runnable version of the Week 3 notebook **Langchain_Setup_and_Simple_Chain.ipynb**
(companion to Study Guide 03 §5-§6). It builds the simplest useful chain:
    prompt template  ->  model  ->  text out
using the notebook's "Tell me a {adjective} joke" example.

TEACHING GOAL — see the OLD way and the NEW way side by side:
  * The notebook uses `LLMChain(llm=..., prompt=...)` from `langchain_classic`, which
    is DEPRECATED — running it prints:
        "LangChainDeprecationWarning: The class `LLMChain` was deprecated ...
         Use `RunnableSequence, e.g., `prompt | llm`` instead."
    That warning IS the lesson: LangChain moved to LCEL. (SG03 §6)
  * So this file shows BOTH: (A) the deprecated LLMChain, and (B) the modern LCEL
    equivalent `prompt | model | StrOutputParser()`. Same result, better syntax.

SETUP: see langchain_model.py (set COHERE_API_KEY or OPENAI_API_KEY).
    python week3/code/langchain_simple_chain_demo.py

FAITHFUL CHANGES vs the notebook: dropped the Colab `userdata.get('COHERE_KEY')` secret
lookup (use an env var via langchain_model.py); provider is swappable, not hard-coded to
Cohere. The prompt and flow are otherwise identical.
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_model import get_chat_model

# A PromptTemplate = a reusable prompt with typed {variables} filled at runtime.
# 💻 Like a PreparedStatement / MessageFormat — bind-parameters, not string concat. (SG03 §5)
prompt = PromptTemplate(input_variables=["adjective"], template="Tell me a {adjective} joke")

model = get_chat_model(temperature=0.7)  # a bit of randomness so the joke varies


def way_a_deprecated_llmchain():
    """The notebook's original approach — DEPRECATED, kept to show what changed."""
    print("\n=== (A) Deprecated LLMChain (the notebook's way) ===")
    # This import + call is exactly what triggers the LangChainDeprecationWarning.
    from langchain_classic.chains import LLMChain

    chain = LLMChain(llm=model, prompt=prompt, verbose=True)  # verbose prints the filled prompt
    response = chain.invoke("funny")   # LLMChain returns a DICT
    # Note the awkward part: you must dig the text out of response['text'].
    print("response['text']:\n", response["text"])


def way_b_modern_lcel():
    """The modern, recommended approach — LCEL with the pipe operator. (SG03 §6)"""
    print("\n=== (B) Modern LCEL: prompt | model | StrOutputParser() ===")
    # Read `|` like a Unix pipe / Java Function.andThen(): the input flows left->right.
    #   dict {adjective} -> [prompt fills template] -> [model answers] -> [parser -> str]
    chain = prompt | model | StrOutputParser()
    # StrOutputParser pulls the plain string OUT of the model's message object, so we
    # don't have to index response['text'] like the deprecated version did.
    text = chain.invoke({"adjective": "funny"})   # LCEL returns the parsed value directly
    print(text)

    # Bonus: because every stage is a Runnable, .batch() and .stream() work for free.
    print("\n--- .batch() over several adjectives (free, no code change) ---")
    for out in chain.batch([{"adjective": "corny"}, {"adjective": "nerdy"}]):
        print("•", out.splitlines()[0] if out else out)


def main():
    way_a_deprecated_llmchain()
    way_b_modern_lcel()
    print(
        "\nTakeaway: same prompt->model->text flow, but LCEL (B) is cleaner, returns the "
        "value directly, and gives you batch/stream/async for free. Prefer it. (SG03 §6)"
    )


if __name__ == "__main__":
    main()
