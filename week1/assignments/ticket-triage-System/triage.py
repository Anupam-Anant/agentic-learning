"""
AI Support Ticket Triage System — standalone CLI version.

Same logic as ticket_triage.ipynb, runnable from a terminal:

    export OPENAI_API_KEY=sk-...
    python triage.py                      # triage the CSV dataset -> triage_results.csv
    python triage.py "My app keeps crashing on upload"   # triage a single message

Optional: set PROVIDER=openai|groq|gemini  (needs the matching *_API_KEY).
Requires: pip install "openai>=1.50.0" "pydantic>=2.5" pandas
"""

import os
import sys
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field
from openai import OpenAI

# --------------------------------------------------------------------------- config
PROVIDERS = {
    "openai": {"model": "gpt-4.1-mini",            "base_url": None,
               "key": "OPENAI_API_KEY"},
    "groq":   {"model": "llama-3.3-70b-versatile", "base_url": "https://api.groq.com/openai/v1",
               "key": "GROQ_API_KEY"},
    "gemini": {"model": "gemini-2.5-flash",        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
               "key": "GEMINI_API_KEY"},
}
PROVIDER = os.environ.get("PROVIDER", "openai")

CATEGORY_TO_DEPARTMENT = {
    "billing_and_payments": "Billing",
    "technical_issue":      "Technical Support",
    "account_access":       "Account Management",
    "product_inquiry":      "Sales",
    "complaint":            "Customer Success",
    "feature_request":      "Product",
    "general_query":        "General Support",
}
PRIORITY_ICON = {"low": "🟢", "medium": "🟡", "high": "🟠", "urgent": "🔴"}
SENSITIVE_KEYWORDS = [
    "refund", "chargeback", "lawyer", "legal", "gdpr", "sue", "lawsuit",
    "cancel", "terminate", "data loss", "lost all", "breach", "hacked",
    "fraud", "unauthorized", "compensation",
]


# --------------------------------------------------------------------------- schema
class TicketTriageOutput(BaseModel):
    category: Literal[
        "billing_and_payments", "technical_issue", "account_access",
        "product_inquiry", "complaint", "feature_request", "general_query",
    ] = Field(description="Single best category for the ticket.")
    priority: Literal["low", "medium", "high", "urgent"]
    department: Literal[
        "Billing", "Technical Support", "Account Management",
        "Sales", "Customer Success", "Product", "General Support",
    ]
    issue_summary: str = Field(description="One factual sentence describing the core issue.")
    customer_reply: str = Field(description="Short empathetic, professional reply to the customer.")
    escalate_to_human: bool
    escalation_reason: str = Field(description="Reason for escalation, or 'None'.")
    confidence: float = Field(description="Classification confidence 0.0-1.0.")


SYSTEM_PROMPT = """You are an expert customer-support triage assistant for a B2B SaaS company.
You receive ONE customer support message (with the channel it arrived on) and must return a structured triage decision.

Work in this order (intent-based routing): first decide the CATEGORY, then let it drive priority, department, escalation, and the reply.

CATEGORY - choose the single best fit:
- billing_and_payments : charges, invoices, refunds, subscriptions, pricing, plan changes
- technical_issue      : bugs, errors, crashes, outages, performance, API/integration problems
- account_access       : login, passwords, 2FA, locked/suspended accounts, account security
- product_inquiry      : pre-sales or how-to questions about capabilities, plans, upgrades
- complaint            : clear dissatisfaction, escalations, or threats to cancel/churn
- feature_request      : asking for a new feature or enhancement
- general_query        : anything else that does not fit the above

PRIORITY:
- urgent : production outage, security/fraud, data loss, legal/compliance threat, or the customer is completely blocked on a paid service
- high   : a single customer is blocked, an angry customer, a refund/billing dispute, or a repeated unresolved issue
- medium : a partial problem with a workaround, or a non-blocking bug
- low    : general questions, feature requests, minor or cosmetic issues

DEPARTMENT - route to the owning team:
- Billing -> billing_and_payments; Technical Support -> technical_issue; Account Management -> account_access;
  Sales -> product_inquiry; Customer Success -> complaint; Product -> feature_request; General Support -> general_query

ESCALATE_TO_HUMAN = true when ANY hold: priority urgent/high; security/fraud/data-loss/legal (e.g. GDPR);
angry or churn threat; a refund/monetary dispute; needs human judgement or is outside standard policy. Otherwise false.

ISSUE_SUMMARY: one concise factual sentence for an internal agent.
CUSTOMER_REPLY: a short (3-5 sentence) warm, professional reply; acknowledge, give next step, set expectations;
if escalating say a specialist will follow up; never invent facts not in the message.
ESCALATION_REASON: brief reason if escalating, else "None".
CONFIDENCE: float 0.0-1.0.

Base every decision only on the message. If unsure, lower confidence and prefer escalating."""

JSON_INSTRUCTION = """Return ONLY a single JSON object (no markdown, no commentary) with EXACTLY these keys:
"category", "priority", "department", "issue_summary", "customer_reply", "escalate_to_human", "escalation_reason", "confidence".
Use only the allowed values above. "escalate_to_human" must be a boolean and "confidence" a number between 0 and 1."""


# --------------------------------------------------------------------------- clients
_clients = {}
def get_client(provider):
    if provider not in _clients:
        cfg = PROVIDERS[provider]
        key = os.environ.get(cfg["key"])
        if not key:
            raise RuntimeError(f"Missing environment variable {cfg['key']} for provider '{provider}'.")
        _clients[provider] = (OpenAI(api_key=key, base_url=cfg["base_url"])
                              if cfg["base_url"] else OpenAI(api_key=key))
    return _clients[provider]


# --------------------------------------------------------------------------- pipeline
def _user_input(message, channel):
    return f"Channel: {channel}\n\nCustomer support message:\n---\n{message}\n---"

def _call_openai_native(client, model, message, channel):
    resp = client.responses.parse(
        model=model, instructions=SYSTEM_PROMPT, input=_user_input(message, channel),
        text_format=TicketTriageOutput, temperature=0, max_output_tokens=900,
    )
    if getattr(resp, "status", None) == "incomplete":
        raise RuntimeError(f"Incomplete response: {getattr(resp, 'incomplete_details', None)}")
    if resp.output_parsed is None:
        raise RuntimeError("No parsed output (possible refusal).")
    return resp.output_parsed

def _call_json_mode(client, model, message, channel):
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + JSON_INSTRUCTION},
                  {"role": "user", "content": _user_input(message, channel)}],
        response_format={"type": "json_object"}, temperature=0,
    )
    return TicketTriageOutput.model_validate_json(resp.choices[0].message.content)

def enforce_routing(t):
    t.department = CATEGORY_TO_DEPARTMENT.get(t.category, "General Support")
    return t

def apply_safety_net(t, message):
    reasons = []
    if t.escalate_to_human and t.escalation_reason and t.escalation_reason.strip().lower() != "none":
        reasons.append(t.escalation_reason.strip())
    if t.confidence < 0.6:
        reasons.append(f"low model confidence ({t.confidence:.2f})")
    if t.category == "complaint":
        reasons.append("category is complaint")
    if t.priority in ("urgent", "high"):
        reasons.append(f"{t.priority} priority")
    hits = sorted({k for k in SENSITIVE_KEYWORDS if k in message.lower()})
    if hits:
        reasons.append("sensitive keywords: " + ", ".join(hits))
    if reasons:
        t.escalate_to_human = True
        t.escalation_reason = "; ".join(dict.fromkeys(reasons))
    else:
        t.escalate_to_human = False
        t.escalation_reason = "None"
    return t

def triage_ticket(message, channel="email", provider=PROVIDER):
    client = get_client(provider)
    model = PROVIDERS[provider]["model"]
    t = _call_openai_native(client, model, message, channel) if provider == "openai" \
        else _call_json_mode(client, model, message, channel)
    return apply_safety_net(enforce_routing(t), message)

def print_triage(ticket_id, subject, channel, message, t):
    msg = message.strip()
    print("=" * 74)
    print(f"🎫 {ticket_id}  |  channel: {channel}  |  subject: {subject}")
    print("-" * 74)
    print(f"Category  : {t.category}")
    print(f"Priority  : {PRIORITY_ICON.get(t.priority, '')} {t.priority.upper()}")
    print(f"Department: {t.department}")
    print(f"Confidence: {t.confidence:.2f}")
    print(f"Escalate  : {'YES -> ' + t.escalation_reason if t.escalate_to_human else 'No'}")
    print(f"Summary   : {t.issue_summary}")
    print("Reply     :")
    print("   " + t.customer_reply.replace("\n", "\n   "))
    print()


# --------------------------------------------------------------------------- entry
def _find_dataset():
    for path in ("dataset/support_tickets.csv", "support_tickets.csv"):
        if os.path.exists(path):
            return path
    raise FileNotFoundError("support_tickets.csv not found (looked in ./dataset and .).")

def run_single(message):
    t = triage_ticket(message, channel="cli")
    print_triage("CLI-1", "(ad-hoc message)", "cli", message, t)

def run_dataset():
    df = pd.read_csv(_find_dataset())
    print(f"Triaging {len(df)} tickets with provider='{PROVIDER}'...\n")
    rows = []
    for r in df.itertuples(index=False):
        try:
            t = triage_ticket(r.message, r.channel)
            print_triage(r.ticket_id, r.subject, r.channel, r.message, t)
            rows.append({"ticket_id": r.ticket_id, "channel": r.channel, "subject": r.subject,
                         "category": t.category, "priority": t.priority, "department": t.department,
                         "confidence": round(t.confidence, 2), "escalate": t.escalate_to_human,
                         "escalation_reason": t.escalation_reason, "issue_summary": t.issue_summary,
                         "customer_reply": t.customer_reply})
        except Exception as e:
            print(f"✗ {r.ticket_id} FAILED: {e}\n")
            rows.append({"ticket_id": r.ticket_id, "category": "ERROR", "escalation_reason": str(e)})
    out = pd.DataFrame(rows)
    out.to_csv("triage_results.csv", index=False)
    print("Saved -> triage_results.csv")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_single(" ".join(sys.argv[1:]))
    else:
        run_dataset()
