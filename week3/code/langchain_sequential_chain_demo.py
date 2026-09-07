"""
langchain_sequential_chain_demo.py
==================================
Runnable version of the Week 3 notebook **Langchain_Chains.ipynb** (companion to
Study Guide 03 §5-§7). The notebook is titled "Sequential Chain" and is about running a
chain over a scientific-process topic ("Photosynthesis").

⚠️ TWO FAITHFUL NOTES about the original notebook (important — read these):
  1) MODEL BACKEND: the notebook ran a LOCAL open-source model — `mistralai/Mistral-7B-v0.1`
     loaded in **4-bit quantization** (bitsandbytes `load_in_4bit`, `nf4`) via
     `HuggingFacePipeline`. That path needs an **NVIDIA CUDA GPU** and won't run on a Mac
     — so here we use the same swappable chat model as the other demos (Cohere/OpenAI).
     LangChain wrapping a *local* HF model is a real capability (that's the whole point of
     `HuggingFacePipeline`); we just can't exercise it without a GPU. See the chat notes.
  2) IT WASN'T ACTUALLY SEQUENTIAL: despite the "Sequential Chain" heading, the notebook's
     code was a SINGLE `LLMChain` (one prompt -> one call). Its output also showed the base
     Mistral model stuck in a **repetition loop** ("...convert light energy into chemical
     energy." over and over) — a classic sign of a BASE (not instruction-tuned) model at low
     temperature. (Teaching note in chat.)

So this file delivers what the title PROMISED: a TRUE multi-step **sequential chain**, where
step 1's output feeds step 2. This is "prompt chaining" from W2·SG02, now as real code.

    topic ──▶ [chain 1: write a 3-point outline] ──▶ outline ──▶ [chain 2: expand outline] ──▶ explanation

SETUP: see langchain_model.py (set COHERE_API_KEY or OPENAI_API_KEY).
    python week3/code/langchain_sequential_chain_demo.py
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_model import get_chat_model

model = get_chat_model(temperature=0.3)  # low-ish: we want focused, on-topic output

# STEP 1 prompt: topic -> a short outline.
outline_prompt = ChatPromptTemplate.from_template(
    "You are a science teacher. Give a 3-bullet outline of the key ideas of: {topic}. "
    "Bullets only, no intro."
)

# STEP 2 prompt: consume STEP 1's outline -> a short explanation built from it.
expand_prompt = ChatPromptTemplate.from_template(
    "Using ONLY this outline:\n{outline}\n\n"
    "Write a clear ~120-word explanation of the topic for a beginner."
)

# Two sub-chains, each: prompt | model | (plain string out).
outline_chain = outline_prompt | model | StrOutputParser()
expand_chain = expand_prompt | model | StrOutputParser()

# THE SEQUENTIAL WIRING (LCEL). The middle step is the key idea:
#   { "outline": outline_chain }  runs step 1 and puts its text under the key `outline`,
#   which is exactly the {outline} variable expand_prompt needs. So step 1's OUTPUT
#   becomes step 2's INPUT — that is what makes the chain *sequential*. (SG03 §7②)
sequential_chain = {"outline": outline_chain} | expand_chain


def main():
    topic = "Photosynthesis"   # same topic as the notebook

    print(f"=== TRUE sequential chain on: {topic} ===")

    # Peek at step 1 alone so you can SEE the intermediate result feeding step 2.
    outline = outline_chain.invoke({"topic": topic})
    print("\n[step 1] outline:\n", outline)

    # Now the full two-step chain end to end.
    explanation = sequential_chain.invoke({"topic": topic})
    print("\n[step 1 -> step 2] explanation:\n", explanation)

    print(
        "\nNote how step 2's text is BUILT FROM step 1's outline — that hand-off is the "
        "whole point of a sequential chain (prompt chaining, W2·SG02, as code)."
    )


if __name__ == "__main__":
    main()
