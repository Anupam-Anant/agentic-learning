"""
Structured Outputs — force the reply to match a schema you define.
Two ways: (A) Pydantic model (recommended in Python), (B) manual JSON Schema.
Run:  python 02_structured_output.py
"""

import json
from typing import Literal
from pydantic import BaseModel, Field

from openai_client import client, OPENAI_MODEL


# ---------- (A) Pydantic model = your typed contract ----------
class SupportTicket(BaseModel):
    intent: Literal["billing", "technical", "sales", "other"]   # enum: value MUST be in-set
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(description="One sentence summary of the issue")  # hint improves quality
    suggested_action: str


def classify_with_pydantic():
    response = client.responses.parse(          # note: .parse, not .create
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Classify the customer support ticket."},
            {"role": "user",   "content": "I was charged twice for my subscription."},
        ],
        text_format=SupportTicket,              # the schema the reply must match
    )

    # Defensive checks BEFORE trusting the data (refusal / truncation):
    if getattr(response, "status", None) == "incomplete":
        print("Incomplete:", getattr(response, "incomplete_details", None))
        return

    ticket: SupportTicket = response.output_parsed   # already deserialized + validated
    print("intent:          ", ticket.intent)
    print("urgency:         ", ticket.urgency)
    print("summary:         ", ticket.summary)
    print("suggested_action:", ticket.suggested_action)


# ---------- (B) Manual JSON Schema (portable / non-Pydantic) ----------
def extract_with_manual_schema():
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Extract lead qualification data."},
            {"role": "user",   "content": "Acme Corp wants a demo next week; budget around $50k."},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "lead_data",
                "strict": True,                      # enforce the schema exactly
                "schema": {
                    "type": "object",
                    "properties": {
                        "company":  {"type": "string"},
                        "budget":   {"type": "string"},
                        "timeline": {"type": "string"},
                    },
                    "required": ["company", "budget", "timeline"],  # set required explicitly
                    "additionalProperties": False,                  # no surprise keys
                },
            }
        },
    )
    data = json.loads(response.output_text)
    print(data["company"], "|", data["budget"], "|", data["timeline"])


if __name__ == "__main__":
    print("=== Pydantic structured output ==="); classify_with_pydantic()
    print("\n=== Manual JSON Schema ===");        extract_with_manual_schema()
