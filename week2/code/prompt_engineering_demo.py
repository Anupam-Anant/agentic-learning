"""
Week 2 · Study Guide 02 companion — Basic Prompt Engineering Techniques
=======================================================================
Runnable version of the four techniques demonstrated in the Week 2 PDF #2:
  1. Zero-shot prompting
  2. Few-shot prompting   (the PDF heading mislabels this "One Shot Prompting")
  3. Prompt chaining
  4. Chain-of-Thought (CoT) reasoning

Faithful to the PDF, this uses the OpenAI *Chat Completions* API
(client.chat.completions.create, model="gpt-4o-mini") — NOT the Responses API
used elsewhere in this course (week1/code). The prompt-engineering TECHNIQUES
are identical either way; see the study guide for the Responses-API version.

NOTE: the PDF omitted the client setup (the `from openai import OpenAI` /
`client = OpenAI()` lines); they are added here so the script actually runs.
Everything else matches the PDF's code.

Notice that zero_shot_prompt() and few_shot_prompt() are the SAME function —
the technique lives entirely in the PROMPT you pass, not in the code.

Run:
    pip install openai
    export OPENAI_API_KEY=sk-...
    python prompt_engineering_demo.py
"""

from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment (added — the PDF omitted this)
MODEL = "gpt-4o-mini"


# ── 1. Zero-shot prompting ──────────────────────────────────────────────────
def zero_shot_prompt(prompt):
    """Demonstrate zero-shot prompting: just ask, no examples."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    print("Zero-shot Prompting:\n", response.choices[0].message.content)


# ── 2. Few-shot prompting (PDF heading says "One Shot"; it is few-shot) ──────
def few_shot_prompt(prompt):
    """Demonstrate few-shot prompting: show examples, then let it complete."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    print("Few-shot Prompting:\n", response.choices[0].message.content)


# ── 3. Prompt chaining ──────────────────────────────────────────────────────
def chain_part1(initial_prompt):
    """Step 1 of the chain: generate an intermediate result."""
    response1 = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": initial_prompt}],
    )
    languages = response1.choices[0].message.content
    return languages


def chain_part2(follow_up_prompt):
    """Step 2 of the chain: consume step 1's output as input."""
    response2 = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": follow_up_prompt}],
    )
    return response2.choices[0].message.content


# ── 4. Chain-of-Thought reasoning ───────────────────────────────────────────
def chain_of_thought(prompt):
    """Demonstrate chain-of-thought: ask the model to reason step by step."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    print("Chain of Thought:\n", response.choices[0].message.content)


if __name__ == "__main__":
    # 1. Zero-shot — just ask, hope the model gets it.
    zero_shot_prompt("Explain the concept of quantum computing in simple terms.")

    # 2. Few-shot — show the English->French pattern, then leave it hanging so
    #    the model completes the last line by imitation.
    prompt = (
        "Translate the following English phrases to French:\n"
        "English: Hello, how are you?\n"
        "French: Bonjour, comment ça va?\n"
        "English: What is your name?\n"
        "French: Comment vous appelez-vous?\n"
        "English: Where is the library?\n"
        "French:"
    )
    few_shot_prompt(prompt)

    # 3. Prompt chaining — step 1's answer becomes part of step 2's prompt.
    initial_prompt = "Provide a list of three popular programming languages."
    response_part1 = chain_part1(initial_prompt)
    follow_up_prompt = (
        "Explain the primary use case for each of these programming "
        f"languages:\n{response_part1}"
    )
    response_part2 = chain_part2(follow_up_prompt)
    print("Part 1:\n", response_part1, "\n")
    print("-" * 150, "\n")
    print("Part 2:\n", response_part2)

    # 4. Chain-of-Thought — the phrase "step by step" triggers explicit reasoning.
    prompt = (
        "A train leaves the station at 60 miles per hour. Another train leaves the "
        "same station one hour later at 80 miles per hour. How long will it take for "
        "the second train to catch the first train? Explain your reasoning step by step."
    )
    chain_of_thought(prompt)
