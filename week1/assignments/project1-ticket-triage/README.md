# 🎫 AI Support Ticket Triage System

**Week 1 · Project 1** — an AI-powered support-ticket triage system built with plain LLM APIs.

Businesses receive support tickets from email, chat, WhatsApp, forms, and helpdesk tools. Each one must be understood, categorized, prioritized, routed to the right team, summarized, and answered — and some need a human. Manual triage is slow and inconsistent. This project automates it with a **single structured LLM call per ticket**, plus deterministic business rules on top.

---

## ✅ Requirements coverage

| # | Requirement | How it's met |
|---|-------------|--------------|
| 1 | Accept a customer support message | `triage_ticket(message, channel)` (also dataset loop + optional UI) |
| 2 | Classify the ticket **category** | `category` — 7 classes |
| 3 | Detect **priority** level | `priority` — low / medium / high / urgent |
| 4 | Assign the correct **department** | `department` + `enforce_routing()` (intent → team, deterministic) |
| 5 | Generate a short **issue summary** | `issue_summary` |
| 6 | Generate a **customer-facing reply** | `customer_reply` |
| 7 | Decide whether **human escalation** is required | `escalate_to_human` + `apply_safety_net()` |

---

## 📦 Contents

```
project1-ticket-triage/
├── README.md                    ← this file
├── ticket_triage.ipynb          ← main deliverable: the Colab notebook (run top to bottom)
├── triage.py                    ← same logic as a standalone CLI script
├── requirements.txt             ← dependencies
├── dataset/
│   └── support_tickets.csv      ← 16 sample tickets (input dataset)
└── triage_results.csv           ← OUTPUT (created when you run the notebook or script)
```

---

## 🏗️ How it works

```
customer message
       │
       ▼
  ONE structured LLM call
  (OpenAI Responses API .parse + Pydantic schema)   →  guaranteed valid, typed JSON
       │   category, priority, summary, reply, escalate, confidence
       ▼
  enforce_routing()    →  department derived from category (deterministic map)
       │
       ▼
  apply_safety_net()   →  FORCE human escalation when business rules trigger:
       │                    • priority is urgent/high
       │                    • category is complaint
       │                    • confidence < 0.60
       │                    • message mentions refund / legal / GDPR / security / data-loss
       ▼
  triaged ticket  →  results table + human-readable report + triage_results.csv
```

### Structured output schema (`TicketTriageOutput`)
`category` · `priority` · `department` · `issue_summary` · `customer_reply` · `escalate_to_human` · `escalation_reason` · `confidence`

### Categories → Departments (intent-based routing)
| Category | Department |
|---|---|
| billing_and_payments | Billing |
| technical_issue | Technical Support |
| account_access | Account Management |
| product_inquiry | Sales |
| complaint | Customer Success |
| feature_request | Product |
| general_query | General Support |

---

## ▶️ How to run

### Option A — Google Colab (recommended)
1. Upload `ticket_triage.ipynb` to Colab.
2. Add your key(s) in **Colab → Secrets** (🔑 icon): `OPENAI_API_KEY` (required); optionally `GROQ_API_KEY`, `GEMINI_API_KEY`. Enable *Notebook access*.
3. **Runtime → Run all.** The notebook installs deps, triages all 16 tickets, prints a report, and writes `triage_results.csv`.

### Option B — Local CLI
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...

python triage.py                                   # triage the whole dataset -> triage_results.csv
python triage.py "My app crashes every time I upload a file"   # triage one message
```

> The notebook is self-contained: it recreates `support_tickets.csv` from embedded data, so it runs even without the CSV. The CSV is also included so the dataset is a first-class deliverable.

---

## 🔀 Multi-provider support (OpenAI / Groq / Gemini)

All three providers speak the OpenAI wire format, so a **single `openai` SDK** drives everything (fewer dependencies, less to break):

| Provider | Model | How structured output is obtained |
|---|---|---|
| **OpenAI** (default) | `gpt-4.1-mini` | native `responses.parse()` with the Pydantic schema |
| **Groq** | `llama-3.3-70b-versatile` | OpenAI-compatible endpoint, JSON mode + Pydantic validation |
| **Gemini** | `gemini-2.5-flash` | OpenAI-compatible endpoint, JSON mode + Pydantic validation |

Switch by setting `BATCH_PROVIDER` in the notebook (or `PROVIDER=groq python triage.py`). Each provider needs its matching key in Colab Secrets / environment.

---

## 💡 Design decisions

- **One structured call, not many.** Classification, prioritization, routing, summary, reply, and the escalation flag are produced together — cheaper, lower latency, and internally consistent (the reply matches the detected priority).
- **Structured Outputs, not "please return JSON."** The Pydantic schema *guarantees* valid, typed fields, so the pipeline never breaks on a stray sentence or renamed key.
- **`temperature=0`.** Triage is classification — we want consistent, repeatable decisions.
- **A Python safety net over the model.** Consequential routing never relies on the model alone; deterministic rules force human escalation on complaints, urgent/high priority, low confidence, and sensitive (refund/legal/security) keywords.
- **Department derived in Python.** A fixed category → team map can't drift even if the model mislabels the field.

---

## 🚀 Possible extensions
Connect to a real helpdesk via webhook, persist results to a database, add few-shot examples for tricky categories, and build a labeled evaluation set to measure triage accuracy.

---

*Built as the Week 1 capstone applying the OpenAI Responses API + Structured Outputs concepts from the course study guides.*
