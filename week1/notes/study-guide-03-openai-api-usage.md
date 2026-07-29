# 📘 Week 1 · Study Guide 03 — OpenAI API Usage Guide (Responses API, Structured Outputs, Streaming)

> **Self-contained document.** Contains the **complete original PDF content** *plus* first-principles explanations and **line-by-line code walkthroughs**. You do **not** need to open the PDF.
>
> **How to read:** 📄 **`FROM THE PDF`** = original text/code · 🧠 **`EXPLAINED`** = plain-English teaching · 🔑 **bold jargon** defined on first use. Written for a **Java/backend engineer** — so I lean on REST/DTO/SSE analogies throughout.
>
> ⚠️ **Note on the code:** the source PDF's code was OCR-scrambled (e.g. `OpenAlO`, `input=l`, `OPENAI_AP|_KEY`, `end="'*`). Every code block below is the **corrected, runnable version**. Clean copies also live in `week1/code/`.
>
> 🧭 **Where this fits:** Reading 02 listed *5 ways to access a model* — this reading is **method #1 (Pre-trained models via API)** in practice. It's the "how do I actually call an LLM from code" reading, and the code companion to Week 1's Playground theme.

---

## 📑 Table of Contents

1. [What this guide is & the recommended pattern](#page-1-2--overview--recommended-usage-pattern)
2. [Getting an API key + Colab setup (securely)](#page-2--getting-an-openai-api-key--colab-setup)
3. [Quick setup & the reusable client](#page-2-3--quick-setup--reusable-client)
4. [The Responses API — parameters & examples](#page-3-5--the-responses-api)
5. [Structured Outputs — schema-safe JSON](#page-5-8--structured-outputs)
6. [Streaming responses](#page-8--streaming-responses)
7. [Common mistakes](#page-9--common-mistakes)
8. [References](#references)
9. [➕ Appendix — Responses API vs Chat Completions API](#-appendix--responses-api-vs-chat-completions-api)
10. [🗂️ Jargon Dictionary](#-jargon-dictionary)
10. [📊 Comparison tables](#-comparison-tables)
11. [🧵 Connected mental model](#-connected-mental-model)
12. [⚡ 60-second recap](#-60-second-recap)

---

## Page 1–2 — Overview & Recommended Usage Pattern

> 📄 **FROM THE PDF**
> **OpenAI API Usage Guide.** This document gives developers a practical starting point for using OpenAI's **Responses API**, producing **schema-safe structured outputs**, and **streaming** results to applications.
>
> **Recommended usage pattern:** Use the **Responses API** as the default interface for new text, JSON, image-input, tool-calling, and multi-turn response workflows. Use **Structured Outputs** when your app needs predictable JSON. Use **streaming** when you want lower perceived latency or live UI updates.

### 🧠 EXPLAINED

This whole reading is about **three tools**, and the recommendation tells you *when* to reach for each:

| Tool | What it does | Reach for it when… |
|---|---|---|
| 🔑 **Responses API** | The main way to send a prompt and get a model reply from code. | Almost always — it's the default door in. |
| 🔑 **Structured Outputs** | Forces the reply to match a **JSON schema you define**. | Your code needs *predictable fields* to act on (save to DB, call another API, render UI). |
| 🔑 **Streaming** | Sends the reply **piece by piece** as it's generated. | You want the UI to feel fast (text appears live, like ChatGPT typing). |

- 🔑 **API (Application Programming Interface):** *(recap from Reading 02)* a network endpoint your code calls. You send a request (your prompt + settings), you get a JSON response (the model's output). As a backend dev, this is just a **REST client call to a remote service** — the service happens to be a giant LLM.

- 🔑 **Responses API:** OpenAI's current *primary* interface for talking to their models. It's a single endpoint — `POST /v1/responses` — that handles text in/out, image inputs, JSON outputs, built-in tools, function calling, multi-turn conversation state, and streaming. Think of it as **one unified endpoint** that replaced older, more fragmented ones.

- 🔑 **Perceived latency:** how *slow it feels* to a user, which is different from total time. Streaming doesn't make the model finish faster, but showing the first words immediately makes it *feel* far faster. (Same trick as rendering a page skeleton before data loads.)

> 💻 **Backend framing:** you already know "call a REST API, get JSON back." This reading adds three LLM-specific wrinkles: (1) the request body has *prompt-shaped* fields, (2) you can *guarantee the response shape* with a schema, and (3) you can *stream* the body like Server-Sent Events.

---

## Page 2 — Getting an OpenAI API Key + Colab Setup

> 📄 **FROM THE PDF**
> Before using the notebook, you'll need an OpenAI API key.
> - Go to the OpenAI Platform: https://platform.openai.com/
> - Sign in (or create an account).
> - Navigate to **API Keys** → click **Create new secret key**.
> - Give the key a name (optional) and create it.
> - **Copy the API key immediately and store it securely. You won't be able to view it again** after closing the dialog.
> - (If required) Add a payment method and ensure your account has sufficient API credits.
>
> To use the notebook, add your OpenAI API key to **Google Colab secrets**:
> - Open the notebook in Google Colab.
> - In the left sidebar, click the **Secrets** (key) icon.
> - Click **+ Add new secret**.
> - Set the **Name** to `OPENAI_API_KEY` and paste your key into the **Value** field.
> - Enable **Notebook access** (toggle on).
> - Run the notebook — it will read the key automatically from Colab Secrets.

### 🧠 EXPLAINED

- 🔑 **API key:** a **secret credential** (a long string starting `sk-…`) that authenticates your requests and ties usage to *your* billing account. It's exactly like a **password / bearer token** for the API.

- 🔑 **Google Colab:** a free, browser-based **Jupyter notebook** environment from Google that runs Python in the cloud (no local install). It's where this course's example code runs. (A 🔑 **notebook** = a document mixing runnable code cells + text; great for learning/experimenting.)

- 🔑 **Colab Secrets:** Colab's built-in secret store. You save the key there **once**, and code reads it via `userdata.get("OPENAI_API_KEY")` — so the key **never appears in your code**.

> 🔐 **Security — take this seriously (backend instincts apply):**
> - **Never hardcode** the key in source, and **never commit it to git**. A leaked `sk-…` key = someone spending *your* money.
> - Treat it like a DB password: keep it in a **secret manager / environment variable** (Colab Secrets here; `.env`, Vault, or cloud secrets in real apps).
> - If it ever leaks, **revoke and rotate** it immediately from the OpenAI dashboard.
> - 🔑 **API credits / billing:** OpenAI charges **per token** (input + output). No credits → calls fail. Set usage limits so a runaway loop can't drain your balance.

---

## Page 2–3 — Quick Setup & Reusable Client

> 📄 **FROM THE PDF** — *1. Quick setup*
> Install the OpenAI Python SDK and supporting packages: `pip install openai`

```bash
pip install openai
```

### 🧠 EXPLAINED
- 🔑 **SDK (Software Development Kit):** a library that wraps the raw HTTP API in clean, native function calls, so you write `client.responses.create(...)` instead of hand-building HTTP requests. The `openai` Python package is OpenAI's official SDK. *(Like using a generated client / `RestTemplate` wrapper instead of hand-rolling HTTP in Java.)*
- 🔑 **`pip`:** Python's package installer (the `npm`/`Maven` of Python).

---

> 📄 **FROM THE PDF** — *Create a reusable client module* (OCR-corrected):

```python
# openai_client.py
import os
from openai import OpenAI
from google.colab import userdata

OPENAI_MODEL = "gpt-4.1-mini"
os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")

client = OpenAI()
# client = OpenAI(api_key=userdata.get("OPENAI_API_KEY"))  # this also works
```

### 🧠 EXPLAINED — line by line

| Line | What it does | Why it's written this way |
|---|---|---|
| `import os` | Access environment variables. | The SDK looks for the key in an env var by default. |
| `from openai import OpenAI` | Import the SDK's main client class. | `OpenAI` is your entry point to every API call. |
| `from google.colab import userdata` | Import Colab's secret reader. | Lets you fetch the key without hardcoding it. |
| `OPENAI_MODEL = "gpt-4.1-mini"` | Define the model ID **once**, in a constant. | 🌟 **Best practice**: centralize model choice so you can swap models in *one* place (the PDF's "common mistakes" warns against hardcoding a model everywhere). |
| `os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")` | Read the key from Colab Secrets and put it in the env var the SDK expects. | Keeps the secret out of code. |
| `client = OpenAI()` | Create the client. With no args, it **auto-reads `OPENAI_API_KEY`** from the environment. | This shared `client` object is reused for every request. |

> 💻 **Backend analogy:** this file is your **configured singleton client** — like a `@Bean` `WebClient`/`RestClient` wired up once with base URL + auth, then injected everywhere. `OPENAI_MODEL` is your externalized config constant.

- 🔑 **`gpt-4.1-mini`:** a specific model ID. "mini" = a **smaller, cheaper, faster** model (recall Reading 02's *cost/latency/accuracy trade-off*). Fine for learning and many production tasks; swap to a bigger model only where you need more capability.

---

## Page 3–5 — The Responses API

> 📄 **FROM THE PDF**
> The Responses API is OpenAI's primary interface for generating model responses. It supports text and image inputs, text and JSON outputs, built-in tools, function calling, conversation state, and streaming. The endpoint is `POST /v1/responses`.

### The core parameters (the request "body")

> 📄 **FROM THE PDF** (parameter tables, pages 3–4):

| Parameter | Meaning (PDF) | 🧠 Backend translation |
|---|---|---|
| 🔑 `model` | The model ID used for the request. Set once; override only when needed. | Which brain to use. Externalize it (our `OPENAI_MODEL`). |
| 🔑 `instructions` | System/developer-level behavior instruction. Use for role, tone, rules, output quality, safety. | The **system prompt** — global config for *how* the model should behave. Like app-level config/policy. |
| 🔑 `input` | User message, or a list of role-based messages. The actual task/context/files/images. | The **request payload** — the actual thing you're asking. |
| 🔑 `max_output_tokens` | Upper bound on generated output tokens. Controls cost and prevents runaway responses. | A **hard cap / circuit breaker** on response size → caps cost & latency. |
| 🔑 `previous_response_id` | Reference to a previous response, for follow-up turns without resending prior context. | A **server-side session pointer** — "continue *that* conversation." |
| 🔑 `text.format` | Controls plain text, JSON mode, or JSON-schema output. | Declares the **response content-type / shape** (see Structured Outputs). |
| 🔑 `stream` | Returns server-sent events incrementally. Use for live UI, long responses, chat, progress. | Turn on **SSE-style streaming**. |
| 🔑 `store` | Whether the response is stored for later retrieval. Set per data-retention/product needs. | Server-side persistence toggle (needed for `previous_response_id` chaining). |

> **The two most important to grasp first:** `instructions` vs `input`.
> - `instructions` = **the system prompt** = *who the model is and the rules it follows* ("You are a concise technical assistant"). Set by *you, the developer*.
> - `input` = **the user prompt** = *the actual request* ("Explain RAG in three bullets").
> Keeping these separate is a core prompt-engineering habit: **stable behavior in `instructions`, changing task in `input`.**

- 🔑 **Token** *(recap):* the chunk of text models read/write (~¾ of a word). You're billed per token and every model has a max **context window** in tokens. `max_output_tokens` caps only the *output* side.

---

### Example 1 — Basic response

> 📄 **FROM THE PDF** (corrected):

```python
response = client.responses.create(
    model=OPENAI_MODEL,
    instructions="You are a concise technical assistant.",
    input="Explain RAG in three bullet points for developers.",
    max_output_tokens=300,
)
print(response.output_text)
```

### 🧠 EXPLAINED
- `client.responses.create(...)` — the one call that sends your request to `POST /v1/responses`. It's **synchronous**: it blocks until the full reply is back (contrast with `stream=True` later).
- `instructions=` sets the system behavior; `input=` is the task; `max_output_tokens=300` caps the reply.
- 🔑 `response.output_text` — a **convenience accessor** that pulls the plain text out of the (richer) response object. The full `response` also carries metadata: `id`, `status`, token usage, etc. `output_text` is just the "give me the words" shortcut.

---

### Example 2 — Multi-message input (roles)

> 📄 **FROM THE PDF** (corrected):

```python
response = client.responses.create(
    model=OPENAI_MODEL,
    input=[
        {"role": "system", "content": "You explain GenAI concepts in simple language."},
        {"role": "user",   "content": "What is the difference between RAG and fine-tuning?"},
    ],
)
print(response.output_text)
```

### 🧠 EXPLAINED
Instead of a plain string, `input` can be a **list of messages**, each with a 🔑 **role**:

| Role | Meaning | Analogy |
|---|---|---|
| 🔑 `system` | Sets behavior/rules (same idea as `instructions`). | App config / policy |
| 🔑 `user` | What the human is asking. | The incoming request |
| 🔑 `assistant` | A *previous model reply* (used to give conversation history). | Prior response in the thread |

This role-based format is how you hand the model **context and conversation history** in one shot. (Note: you can express the system role either via the top-level `instructions=` param *or* as a `system` message in the list — both work.)

---

### Example 3 — Follow-up conversation (`previous_response_id`)

> 📄 **FROM THE PDF** (corrected):

```python
first = client.responses.create(
    model=OPENAI_MODEL,
    input="Create a short product description for an AI load testing tool.",
)

second = client.responses.create(
    model=OPENAI_MODEL,
    previous_response_id=first.id,          # ← links to the first turn
    input="Now rewrite it for QA engineers.",
)
print(second.output_text)
```

### 🧠 EXPLAINED — this is a big convenience
Normally, to continue a conversation you'd have to **resend the entire history** every turn (every prior user+assistant message). That's verbose and costs tokens.

`previous_response_id=first.id` tells OpenAI: *"continue from that stored response"* — the server already remembers the prior turn, so your second call only sends the **new** instruction ("Now rewrite it for QA engineers"). The model still "knows" what *it* is.

> 💻 **Backend analogy:** it's the difference between a **stateless** API (client resends full state every call) and a **stateful session** (server holds the state, client sends a **session id**). `previous_response_id` = that session pointer.
> ⚠️ **Requires `store=True`** (the default) — the server must have *stored* the first response for you to reference it.

---

## Page 5–8 — Structured Outputs

> 📄 **FROM THE PDF**
> Structured Outputs force the model response to match a schema. This is better than asking the model to "return JSON" because your application can **validate** the returned fields before saving them, calling downstream APIs, or rendering a UI. Use Structured Output when your application needs the model response in a **fixed JSON format**, not just normal text. OpenAI Structured Outputs ensure that the model response follows a **JSON Schema** you define, so **required keys are not missed** and **enum values do not randomly change**.

### 🧠 EXPLAINED — why this matters more than it looks

An LLM's natural output is *free-form text*. But your code needs **structure** — specific fields, specific types — to do anything with it programmatically. If you just *ask* "please return JSON," the model **usually** complies but **sometimes** adds a stray sentence, renames a field, or invents an enum value → your parser crashes in production.

**Structured Outputs remove the gamble:** you declare a **schema**, and OpenAI *guarantees* the reply conforms to it.

- 🔑 **JSON Schema:** a formal, machine-readable description of what a JSON object must look like — which fields exist, their types, which are required, and allowed values. *(Like an OpenAPI/DTO contract, or Java Bean Validation, but for the model's output.)*
- 🔑 **Enum:** a fixed set of allowed values (e.g., urgency ∈ {low, medium, high}). Structured Outputs guarantee the model can't return anything outside that set.

> 💻 **The killer analogy for you:** Structured Outputs = **the model returns a validated DTO/POJO instead of a String you have to parse and pray over.** It's Jackson deserialization *with the guarantee that deserialization can't fail on shape*.

### The three approaches (page 5 table)

> 📄 **FROM THE PDF**:

| Approach | Guarantee | Best use case |
|---|---|---|
| 🔑 **Plain JSON prompt** ("return JSON") | ❌ No hard guarantee. | Prototyping only. |
| 🔑 **JSON mode** | ⚠️ Valid JSON, but **not** strict field adherence. | Legacy/simple JSON responses. |
| 🔑 **Structured Outputs** | ✅ Valid JSON that **follows your declared schema**. | Production: extraction, classifiers, routing, reports, UI data. |

**Read the middle row carefully:** "JSON mode" guarantees the output *parses* as JSON, but **not** that it has *your fields*. Structured Outputs guarantees *both*. For anything production, use Structured Outputs.

---

### Structured Output via Pydantic (the easy, recommended way)

> 📄 **FROM THE PDF** (corrected):

```python
from typing import Literal
from pydantic import BaseModel, Field
from openai_client import client, OPENAI_MODEL

class SupportTicket(BaseModel):
    intent: Literal["billing", "technical", "sales", "other"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(description="One sentence summary of the issue")
    suggested_action: str

response = client.responses.parse(
    model=OPENAI_MODEL,
    input=[
        {"role": "system", "content": "Classify the customer support ticket."},
        {"role": "user",   "content": "I was charged twice for my subscription."},
    ],
    text_format=SupportTicket,          # ← the schema the reply must match
)

ticket: SupportTicket = response.output_parsed   # ← a real, typed object
print(ticket.intent)            # -> "billing"
print(ticket.urgency)           # -> "high" (model's judgment, but guaranteed in-set)
print(ticket.suggested_action)
```

### 🧠 EXPLAINED — line by line

- 🔑 **Pydantic:** the standard Python library for defining **data models with types and validation**. A `BaseModel` subclass is basically a **typed schema class**. → **This is your Java `record` / POJO + Bean Validation.** Pydantic auto-generates the JSON Schema from the class, so you never hand-write schema.
- `class SupportTicket(BaseModel):` — declares the exact shape you want back.
  - `intent: Literal[...]` — 🔑 `Literal` restricts the value to that **exact set** (an enum). The model *must* pick one of `billing/technical/sales/other`.
  - `urgency: Literal[...]` — same, for low/medium/high.
  - `summary: str = Field(description="...")` — a free-text field. 🔑 `Field(description=...)` gives the model a **hint about what to put there** — the description is passed into the schema and genuinely improves output quality. *(Like a Javadoc the model actually reads.)*
  - `suggested_action: str` — another free-text field.
- 🔑 `client.responses.parse(...)` — a **helper method** (note: `.parse`, not `.create`). It (1) converts your Pydantic model into a JSON Schema, (2) tells the model to conform, and (3) **parses the reply back into an instance of your class**.
- `text_format=SupportTicket` — hand it the schema class.
- 🔑 `response.output_parsed` — the **already-deserialized, typed object**. No `json.loads`, no manual validation. `ticket.intent` is type-safe and guaranteed to be one of your literals.

> **Why this is the pattern to remember:** you defined a contract (`SupportTicket`), and the model was *forced* to fill it. This is how you build reliable classifiers, extractors, and routers — the model becomes a **structured function** you can trust in a pipeline.

---

### Structured Output via manual JSON Schema

> 📄 **FROM THE PDF** — the PDF truncated this example mid-code. Below is the **correct, complete equivalent** using a hand-written JSON Schema (use this when you're *not* in Python/Pydantic, or need full control over the schema):

```python
import json
from openai_client import client, OPENAI_MODEL

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
            "strict": True,                       # enforce the schema exactly
            "schema": {
                "type": "object",
                "properties": {
                    "company":  {"type": "string"},
                    "budget":   {"type": "string"},
                    "timeline": {"type": "string"},
                },
                "required": ["company", "budget", "timeline"],
                "additionalProperties": False,     # no surprise extra keys
            },
        }
    },
)

data = json.loads(response.output_text)
print(data["company"], data["budget"], data["timeline"])
```

### 🧠 EXPLAINED
Same guarantee as Pydantic, but you write the JSON Schema **by hand**. Two keywords the PDF's best-practices call out:

- 🔑 `"required": [...]` — lists fields that **must** be present. Set these **explicitly** so downstream code never hits a missing key.
- 🔑 `"additionalProperties": false` — forbids **any keys you didn't declare**, so the model can't sneak in surprise fields.
- `"strict": True` — turns on the hard schema-enforcement mode.

> **Pydantic vs manual schema:** Pydantic is cleaner and less error-prone in Python (use it by default). Hand-written JSON Schema is the portable, language-agnostic form — useful in other languages or when generating schemas dynamically.

### Best practices (page 8)

> 📄 **FROM THE PDF**
> - Set **required** fields explicitly so downstream code is predictable.
> - Use `additionalProperties: false` to avoid unexpected keys.
> - **Handle refusals, incomplete responses, and validation errors before saving data.**

### 🧠 EXPLAINED — the third bullet is the one people forget
Even with a schema, three things can go wrong — check them **before** trusting the data:
- 🔑 **Refusal:** the model declines (e.g., the request violates safety policy). Your parser will choke if you assume success. Check for a refusal field/status.
- 🔑 **Incomplete response:** the reply got **truncated** (often because it hit `max_output_tokens`) → you may get *half* a JSON object. Check `response.status` and `incomplete_details`.
- **Validation errors:** wrap parsing in error handling so a bad edge case logs cleanly instead of crashing your pipeline.

> 💻 **Backend takeaway:** treat the model like any **untrusted upstream service** — validate status, handle the sad paths (refusal/truncation), *then* persist. Never save unvalidated model output straight to your DB.

---

## Page 8 — Streaming Responses

> 📄 **FROM THE PDF**
> Streaming sends the model response **incrementally** instead of waiting for the full response.

### Event types

> 📄 **FROM THE PDF**:

| Event type | Meaning | Typical handling |
|---|---|---|
| 🔑 `response.created` | The response has started. | Initialize UI state. |
| 🔑 `response.output_text.delta` | A new text token/chunk is available. | Append to the chat bubble / stream to client. |
| 🔑 `response.completed` | The response finished successfully. | Mark final answer complete, save result. |
| 🔑 `error` | A streaming error occurred. | Show fallback message, log details. |

### 🧠 EXPLAINED
When `stream=True`, the call **doesn't return one big object** — it returns an **iterable stream of events** you loop over as they arrive.

- 🔑 **Delta:** a small **incremental chunk** of the output (a token or few). "Delta" = "the new bit since last time." You concatenate deltas to build the full text as it streams in.
- 🔑 **Server-Sent Events (SSE):** the underlying web mechanism — a one-way stream where the server pushes events to the client over a single HTTP connection.

> 💻 **Backend analogy:** this is exactly **SSE / chunked transfer / a reactive `Flux<String>`**. Instead of `String result = call()` (wait for everything), you subscribe to a stream and handle chunks as they land. The `event.type` switch is your typical event-dispatch loop.

### Streaming example

> 📄 **FROM THE PDF** (corrected — the OCR mangled the quotes/escapes):

```python
stream = client.responses.create(
    model=OPENAI_MODEL,
    input="Explain vector databases in simple language.",
    stream=True,                      # ← turn on streaming
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)   # append chunk, no newline
    elif event.type == "response.completed":
        print("\n--- completed ---")
    elif event.type == "error":
        print("\nStreaming error:", event)
```

### 🧠 EXPLAINED — line by line
- `stream=True` — flips the call from "return the whole thing" to "yield events."
- `for event in stream:` — iterate over events as they arrive in real time.
- `if event.type == "response.output_text.delta":` — a new chunk arrived…
  - `print(event.delta, end="", flush=True)` — print the chunk with **no trailing newline** (`end=""`) and 🔑 `flush=True` to force it to the screen **immediately** (don't buffer) — that's what makes text appear live, ChatGPT-style.
- `elif event.type == "response.completed":` — stream finished cleanly → print a marker (in a real app: finalize + save).
- `elif event.type == "error":` — handle failures mid-stream gracefully.

> **Trade-off to remember:** streaming improves *perceived* latency and UX, but adds handling complexity (you assemble the text yourself, and must handle mid-stream errors). Use it for user-facing chat/long outputs; skip it for quick backend calls where you just need the final object.

---

## Page 9 — Common Mistakes

> 📄 **FROM THE PDF** (cleaned):

| Mistake | Why it hurts | Fix |
|---|---|---|
| Only prompting **"return JSON"** | Model may add extra text or wrong fields. | Use **Structured Outputs** with a schema. |
| **No `max_output_tokens`** | Long outputs raise cost & latency. | Set a reasonable cap per use case. |
| **Ignoring incomplete status** | Truncated/partial JSON enters your system. | Check `response.status` and `incomplete_details`. |
| **Not handling refusals** | Your parser fails when a refusal is returned. | Detect refusal/content edge cases before parsing. |
| **Rendering only after completion** | Chat UI feels slow for long responses. | Stream `output_text.delta` events. |
| **Hardcoding one model everywhere** | Can't tune quality/latency/cost per task. | Use **environment-based model selection**. |

### 🧠 EXPLAINED — the pattern behind all six
Five of these are the same lesson in different clothes: **treat the model as an unreliable external dependency and engineer around it.**
- *Guarantee the shape* (schema, not "please return JSON").
- *Bound the blast radius* (cap tokens).
- *Handle the sad paths* (truncation, refusals).
- *Optimize the UX* (stream).
- *Keep config flexible* (don't hardcode the model — exactly why we put `OPENAI_MODEL` in one constant).

This checklist *is* the difference between a demo and a production integration.

---

## References

> 📄 **FROM THE PDF**
> 1. OpenAI API Reference — Responses: https://platform.openai.com/docs/api-reference/responses
> 2. OpenAI API Guide — Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
> 3. OpenAI API Guide — Streaming Responses: https://developers.openai.com/api/docs/guides/streaming-responses

---

## ➕ Appendix — Responses API vs Chat Completions API

> *Not in the PDF — added to answer a common question: OpenAI has **two** text-generation APIs. This reading (and the course) uses the **Responses API**, but you'll constantly see the older **Chat Completions API** in tutorials and other providers' SDKs, so know the difference.*

### ⚡ Short answer
- **Chat Completions API** (`/v1/chat/completions`) — the **original, stateless, industry-standard** interface (since 2023). *You* manage everything: conversation history, tool-execution loops.
- **Responses API** (`/v1/responses`) — the **newer (2025), OpenAI-recommended** interface. A **superset** that adds **optional server-side state** and **built-in hosted tools**, built for **agentic** workflows.

Both call the *same* underlying models. The difference is the **interface** — how much the API does *for* you.

### 🕰️ Why there are two
OpenAI historically had **Chat Completions** (simple request/response) *and* the **Assistants API** (stateful, with tools/threads). The **Responses API** merged the best of both into one interface, now positioned as the **default for new projects**. Chat Completions isn't going away — it's the *de-facto cross-industry standard* (other providers mimic its shape) — but Responses is where OpenAI is investing.

### 📊 Head-to-head

| Dimension | **Chat Completions** | **Responses** |
|---|---|---|
| **Endpoint** | `POST /v1/chat/completions` | `POST /v1/responses` |
| **SDK call** | `client.chat.completions.create(...)` | `client.responses.create(...)` |
| **State** | ❌ **Stateless** — resend full history every turn | ✅ **Optional server-side state** via `previous_response_id` + `store=True` |
| **System prompt** | A `system` message inside `messages[]` | Dedicated `instructions` param (or a system message) |
| **Input field** | `messages=[{role, content}, …]` (always a list) | `input=` (a string **or** a message list) |
| **Get the text** | `response.choices[0].message.content` | `response.output_text` |
| **Tools** | **Function calling only** — *you* execute the function & feed the result back | **Built-in hosted tools** (web search, file search, code interpreter, computer use) run server-side, **plus** your own functions |
| **Streaming** | Raw token deltas (`choices[0].delta.content`) | **Semantic typed events** (`response.output_text.delta`, `response.completed`, …) |
| **Best for** | Existing code, cross-provider portability, simple one-shot calls | New OpenAI projects, agents, multi-turn, hosted tools |
| **Status** | Mature, ubiquitous, fully supported | OpenAI's **recommended default** going forward |

### 👀 The difference in code

**Same simple task, both APIs:**

```python
# Chat Completions — system prompt lives in the messages list
resp = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "You are a concise technical assistant."},
        {"role": "user",   "content": "Explain RAG in three bullet points."},
    ],
)
print(resp.choices[0].message.content)     # <- Chat Completions accessor

# Responses — system prompt is its own param; simpler text accessor
resp = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are a concise technical assistant.",
    input="Explain RAG in three bullet points.",
)
print(resp.output_text)                    # <- Responses accessor
```

**Where they really diverge — a follow-up turn:**

```python
# Chat Completions: YOU keep the history and resend ALL of it every time
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "Write a product description for a load-testing tool."},
]
first = client.chat.completions.create(model="gpt-4.1-mini", messages=messages)
messages.append(first.choices[0].message)                                          # append model reply
messages.append({"role": "user", "content": "Now rewrite it for QA engineers."})   # append new turn
second = client.chat.completions.create(model="gpt-4.1-mini", messages=messages)   # resend EVERYTHING

# Responses: the server remembers; you just point at the previous response
first  = client.responses.create(model="gpt-4.1-mini",
             input="Write a product description for a load-testing tool.")
second = client.responses.create(model="gpt-4.1-mini",
             previous_response_id=first.id,                       # <- server holds the state
             input="Now rewrite it for QA engineers.")
```

> 💻 **Backend intuition:** Chat Completions is a **pure stateless REST endpoint** — the client owns all state and replays it every call. Responses adds an optional **stateful session** — the server holds the thread and you pass a **session pointer** (`previous_response_id`). That's the single biggest conceptual difference.

### 🧠 The 3 differences that actually matter
1. **State** — Responses can offload conversation memory to the server; Chat Completions never does (you resend the whole history, which also costs more input tokens on long chats).
2. **Tools** — Responses has **hosted tools** OpenAI runs for you (web search, file search, code interpreter, computer use). Chat Completions only has **function calling**, where *you* execute functions and loop results back. This is why Responses is the "agentic" API.
3. **Streaming shape** — Responses emits **structured, typed events** (easy to `switch` on); Chat Completions gives raw content deltas you assemble yourself.

### ✅ Which to use
| If… | Use |
|---|---|
| Starting a **new** OpenAI project | **Responses** (OpenAI's recommendation — what this course uses) |
| You want **built-in tools / agents / server-side memory** | **Responses** |
| You need **cross-provider portability**, or have existing code / libs on the standard | **Chat Completions** |
| Quick one-shot completion, shape already known | Either |

> **For this course:** stick with **Responses**. Just recognize the "Chat Completions shape" (`messages[]` → `choices[0].message.content`), because most tutorials and other providers' APIs still speak it.

---

## 🗂️ Jargon Dictionary

| Term | Definition | Why it matters |
|---|---|---|
| **API key** | Secret credential (`sk-…`) authenticating your requests to your billing account. | Guard it like a password. |
| **Assistant (role)** | A message representing a previous model reply, used to supply history. | Multi-turn context. |
| **Chat Completions API** | OpenAI's original stateless interface (`/v1/chat/completions`); you manage history & tool loops. | Industry-standard; the alternative to Responses. |
| **Function calling** | Model requests a function; *you* execute it and return the result. | Chat Completions' tool mechanism (client-run). |
| **Hosted tools** | Tools OpenAI runs server-side (web search, file search, code interpreter, computer use). | Responses-only; enables agents. |
| **Colab / notebook** | Google's cloud Python notebook environment where the course code runs. | Where you'll run examples. |
| **Colab Secrets** | Colab's secret store; code reads keys via `userdata.get(...)`. | Keeps your key out of code. |
| **Delta** | An incremental chunk of streamed output (a token or few). | You concatenate deltas to build the text. |
| **Enum / `Literal`** | A fixed set of allowed values. | Structured Outputs guarantee values stay in-set. |
| **Incomplete response** | A truncated reply (often hit `max_output_tokens`). | Check `status`/`incomplete_details` before use. |
| **`input`** | The user message(s)/task sent to the model. | The request payload. |
| **`instructions`** | System-level behavior rules (the system prompt). | Defines the model's role/rules. |
| **JSON mode** | Guarantees valid JSON, but *not* your specific fields. | Weaker than Structured Outputs. |
| **JSON Schema** | Formal description of required fields/types/values. | The contract Structured Outputs enforce. |
| **`max_output_tokens`** | Cap on output length. | Controls cost & latency; prevents runaways. |
| **`output_parsed`** | The reply already deserialized into your typed object. | No manual JSON parsing. |
| **`output_text`** | Convenience accessor for the plain-text reply. | Quick "give me the words." |
| **`previous_response_id`** | Server-side pointer to continue a prior response. | Multi-turn without resending history. |
| **Pydantic / `BaseModel`** | Python typed-data-model + validation library. | Your DTO/POJO for defining schemas. |
| **Perceived latency** | How slow it *feels* to the user. | Streaming improves it. |
| **Refusal** | The model declines a request (e.g., safety). | Detect before parsing, or code breaks. |
| **Responses API** | OpenAI's primary endpoint (`POST /v1/responses`). | The default way to call the model. |
| **Role (system/user/assistant)** | Labels on messages defining who said what. | Structures context & history. |
| **SDK** | Library wrapping the raw HTTP API in native calls. | `openai` package; write code, not HTTP. |
| **Streaming / SSE** | Sending the reply incrementally as events. | Live UI, lower perceived latency. |
| **`store`** | Whether the response is persisted server-side. | Needed for `previous_response_id`. |
| **Structured Outputs** | Guarantees the reply matches your JSON Schema. | Production-grade JSON from the model. |
| **`text.format`** | Selects plain text / JSON mode / JSON schema. | Declares the output shape. |
| **Token** | ~¾-word text unit; billing & context unit. | `max_output_tokens` caps the output side. |

---

## 📊 Comparison Tables

### `.create()` vs `.parse()`
| | `client.responses.create(...)` | `client.responses.parse(...)` |
|---|---|---|
| Returns | Raw response (text/JSON as text) | Response with `.output_parsed` typed object |
| Schema | Optional (`text.format`) | Driven by a Pydantic model (`text_format=`) |
| Use when | Plain text, streaming, manual schema | You want a validated typed object back |

### Sync vs Streaming
| | Default (sync) | `stream=True` |
|---|---|---|
| Returns | One complete object | An iterable of events |
| Perceived speed | Slower (wait for all) | Fast (words appear live) |
| Complexity | Simple | You assemble text + handle events/errors |
| Best for | Backend calls, structured data | Chat UIs, long outputs |

---

## 🧵 Connected Mental Model

```
        OpenAI SDK  →  client = OpenAI()   (configured once, key from Secrets)
                                │
                    client.responses.create / .parse
                                │
     ┌──────────────┬───────────┼───────────────┬──────────────┐
   model        instructions   input        max_output_tokens  stream / store
  (which brain) (system prompt)(the task)    (cost guardrail)  (live? persisted?)
                                │
        ┌───────────────────────┼───────────────────────┐
   PLAIN TEXT             STRUCTURED OUTPUT            STREAMING
   response.output_text   schema-guaranteed JSON       events: created →
                          (Pydantic .parse →           output_text.delta* →
                           .output_parsed)             completed / error
                                │
                 multi-turn via previous_response_id (server holds state)
```

**Ties back to earlier readings:** Reading 02 said "access models via **API**" — this is that API, concretely. The `instructions`/`input` split is the *system vs user prompt* idea you'll also use in Playgrounds. Structured Outputs is the reliability layer that makes LLMs usable as real *functions* in a backend — the foundation for the **agents/tool-use** you'll build later.

---

## ⚡ 60-Second Recap

- **Responses API** = OpenAI's main endpoint (`POST /v1/responses`); call it via `client.responses.create(...)`.
- **Key params:** `model` (which model), `instructions` (system prompt), `input` (the task), `max_output_tokens` (cost cap), `previous_response_id` (multi-turn), `stream`, `store`.
- **Secrets:** store the `sk-…` key in **Colab Secrets / env var** — never in code or git.
- **Structured Outputs** > "please return JSON": define a **Pydantic model** (or JSON Schema) → `client.responses.parse(text_format=...)` → get a **validated typed object** (`.output_parsed`). Use `required` + `additionalProperties:false`.
- **Streaming** (`stream=True`): loop over events (`response.output_text.delta` for chunks) for live, fast-feeling UIs.
- **Always** handle **refusals**, **incomplete/truncated** responses, and **validation errors** before saving.
- **Don't hardcode** the model — centralize it (`OPENAI_MODEL`) to tune cost/latency/quality.
- **Mental model:** treat the LLM like an *untrusted external service* — cap it, guarantee its shape, handle its sad paths.

---

*This is your complete Week 1 Reading 03. Runnable code: `week1/code/`. Next: the Playground hands-on, or your Week 1 assignment when it's introduced.*
