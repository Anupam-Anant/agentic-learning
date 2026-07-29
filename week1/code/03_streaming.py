"""
Streaming — receive the reply incrementally (like SSE / a reactive stream)
instead of waiting for the whole thing. Great for live chat UIs.
Run:  python 03_streaming.py
"""

from openai_client import client, OPENAI_MODEL


def stream_response():
    stream = client.responses.create(
        model=OPENAI_MODEL,
        input="Explain vector databases in simple language.",
        stream=True,                     # flip to event-stream mode
    )

    for event in stream:
        if event.type == "response.output_text.delta":
            # a new chunk arrived: print it immediately, no newline, flush the buffer
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
            print("\n--- completed ---")
        elif event.type == "error":
            print("\nStreaming error:", event)


if __name__ == "__main__":
    stream_response()
