"""
Responses API — basic call, multi-message input, and multi-turn follow-up.
Run:  python 01_basic_and_multiturn.py
"""

from openai_client import client, OPENAI_MODEL


def basic_response():
    """Single prompt in, plain text out."""
    response = client.responses.create(
        model=OPENAI_MODEL,
        instructions="You are a concise technical assistant.",  # system prompt: behavior/rules
        input="Explain RAG in three bullet points for developers.",  # the actual task
        max_output_tokens=300,  # cost/latency guardrail
    )
    print(response.output_text)


def multi_message_input():
    """Pass a list of role-based messages instead of a single string."""
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "You explain GenAI concepts in simple language."},
            {"role": "user",   "content": "What is the difference between RAG and fine-tuning?"},
        ],
    )
    print(response.output_text)


def follow_up_conversation():
    """Continue a conversation WITHOUT resending prior context (server holds state)."""
    first = client.responses.create(
        model=OPENAI_MODEL,
        input="Create a short product description for an AI load testing tool.",
    )

    second = client.responses.create(
        model=OPENAI_MODEL,
        previous_response_id=first.id,       # link to the first turn (requires store=True, the default)
        input="Now rewrite it for QA engineers.",
    )
    print(second.output_text)


if __name__ == "__main__":
    print("=== basic ===");            basic_response()
    print("\n=== multi-message ===");  multi_message_input()
    print("\n=== follow-up ===");      follow_up_conversation()
