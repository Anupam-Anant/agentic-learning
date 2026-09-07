"""
langchain_lcel_demo.py
======================
Runnable version of the Week 3 notebook **Langchain_LCEL.ipynb** (companion to Study
Guide 03 §6). This is the STAR LCEL example: a **fan-out / fan-in** topology.

    question ──┬──▶ [chain 1: model A answers] ──▶ answer1 ──┐
               └──▶ [chain 2: model B answers] ──▶ answer2 ──┴──▶ [chain 3: combine] ──▶ merged answer

Two models answer the SAME question independently (fan-out, in parallel), then a third
chain merges their viewpoints into one coherent answer (fan-in). It shows the pieces that
make LCEL more than straight lines:
  * the pipe `|` to compose Runnables            (SG03 §6)
  * a DICT of Runnables to run branches at once  (fan-out; LangChain runs them in parallel)
  * RunnablePassthrough to forward the original input untouched into a later step
  * RunnablePassthrough.assign(...) to ADD computed keys while keeping existing ones

The notebook's own markdown said it well: "LCEL simplifies syntax and it's easy to use for
simple chains, but it can get confusing once we add complexity." This file is that
complexity, annotated.

SETUP: see langchain_model.py (set COHERE_API_KEY or OPENAI_API_KEY).
    python week3/code/langchain_lcel_demo.py

FAITHFUL CHANGES vs the notebook: dropped Colab `userdata`; provider swappable. The three
Cohere models in the notebook are recreated as three chat models (same config); the
fan-out/fan-in structure is identical.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_model import get_chat_model

# Prompt 1: just pass the user's question straight to the model.
answer_prompt = ChatPromptTemplate.from_template("{question}")

# Prompt 3: given the question + two answers, merge them.
combine_prompt = ChatPromptTemplate.from_template(
    """Given the question: {question} and the below two answers:
Answer 1:
{answer1}

Answer 2:
{answer2}

Combine the viewpoints of two answers and form a coherent combined answer."""
)

# Three chat models (the notebook used three ChatCohere instances). Same model, low temp.
model1 = get_chat_model(temperature=0.2)
model2 = get_chat_model(temperature=0.2)
model3 = get_chat_model(temperature=0.2)

# Three sub-chains. Each is: prompt | model | StrOutputParser()  (a Runnable).
chain1 = answer_prompt | model1 | StrOutputParser()     # produces answer1
chain2 = answer_prompt | model2 | StrOutputParser()     # produces answer2
chain3 = combine_prompt | model3 | StrOutputParser()    # merges into the final answer

QUESTION = (
    "What's the best way to stay up to date with latest Large Language Model news? "
    "Please keep the answer short and concise, limit to 3 bullet points."
)


def manual_version():
    """Invoke each sub-chain by hand — shows the data that flows between stages."""
    print("\n=== (1) Manual: run the 3 sub-chains yourself ===")
    answer1 = chain1.invoke(QUESTION)
    answer2 = chain2.invoke(QUESTION)
    merged = chain3.invoke({"question": QUESTION, "answer1": answer1, "answer2": answer2})
    print("answer1:\n", answer1)
    print("\nanswer2:\n", answer2)
    print("\ncombined:\n", merged)


def composed_version():
    """The whole fan-out/fan-in as ONE composed chain — the LCEL payoff."""
    print("\n=== (2) Composed: one fan-out/fan-in LCEL chain ===")
    # The dict is the FAN-OUT: LangChain runs these three entries and assembles a dict
    # {question, answer1, answer2} — exactly the variables chain3 (combine_prompt) needs.
    #   RunnablePassthrough() forwards the original input (the question) unchanged.
    #   chain1 / chain2 each compute an answer from that same input, IN PARALLEL.
    # Then `| chain3` is the FAN-IN: the assembled dict flows into the combine step.
    combined_chain = {
        "question": RunnablePassthrough(),
        "answer1": chain1,
        "answer2": chain2,
    } | chain3
    print(combined_chain.invoke(QUESTION))


def assign_version():
    """Same result, written with RunnablePassthrough.assign() — the other notebook style."""
    print("\n=== (3) Same chain via RunnablePassthrough.assign() ===")
    # .assign() ADDS a new key to the dict flowing through, keeping what's already there.
    #   start:            {"question": <the question>}
    #   after assign a1:  {"question", "answer1"}
    #   after assign a2:  {"question", "answer1", "answer2"}   -> feeds chain3
    combined_chain = (
        {"question": RunnablePassthrough()}
        | RunnablePassthrough.assign(answer1=chain1)
        | RunnablePassthrough.assign(answer2=chain2)
        | chain3
    )
    print(combined_chain.invoke(QUESTION))


def main():
    manual_version()
    composed_version()
    assign_version()
    print(
        "\nTakeaway: a DICT of Runnables fans out (parallel branches); `| chain3` fans in. "
        "RunnablePassthrough forwards the raw input; .assign() adds keys as data flows. "
        "That's how LCEL expresses non-linear topologies, not just straight lines. (SG03 §6)"
    )


if __name__ == "__main__":
    main()
