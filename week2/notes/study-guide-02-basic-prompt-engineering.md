# Study Guide 02·02 — Basic Prompt Engineering Techniques

> **Source:** Week 2 reading PDF #2 — *"Basic Prompt Engineering Techniques"* (TMLC).
> **Where it fits in the course:** W2·SG01 asked *which* model to build on (open vs closed). This reading is the very next layer: once you have a model, **how do you talk to it so it does what you want?** Prompt engineering is the day-one skill of every GenAI engineer — it sits under RAG, agents, and everything else. You already did it implicitly in the Week 1 ticket-triage assignment; here it's made explicit with four named techniques + runnable code.
>
> **How to read this file:** It is **self-contained** — you never need the original PDF. Each section has two blocks:
> - 📄 **`FROM THE PDF`** — the original text, cleaned up (the PDF pasted with all spaces stripped, a repeating `TMLC` watermark, and page breaks; wording is preserved, including its jokey tone).
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies and the "why."
>
> **Three faithfulness notes** (per our repo rule to flag any repair):
> 1. The PDF's code omitted the OpenAI **client setup** (`from openai import OpenAI` / `client = OpenAI()`). It's added in the runnable file so the code actually runs.
> 2. The PDF labels technique #2 **"One Shot Prompting"**, but its function is `few_shot_prompt` and it passes **three** examples — so it is really **few-shot**. Flagged inline.
> 3. The PDF uses the older **Chat Completions API**, *not* the Responses API from Week 1. Both are shown and compared in [§7](#7-bridge--chat-completions-vs-the-week-1-responses-api).
>
> **Runnable code:** `week2/code/prompt_engineering_demo.py` (+ `week2/code/README.md`).

---

## 📑 Table of Contents

1. [What is prompt engineering?](#1-what-is-prompt-engineering)
2. [Technique 1 — Zero-shot prompting](#2-technique-1--zero-shot-prompting)
3. [Technique 2 — Few-shot prompting](#3-technique-2--few-shot-prompting)
4. [Technique 3 — Prompt chaining](#4-technique-3--prompt-chaining)
5. [Technique 4 — Chain-of-Thought (CoT) reasoning](#5-technique-4--chain-of-thought-cot-reasoning)
6. [The Python demo — prerequisites & code, line by line](#6-the-python-demo--prerequisites--code-line-by-line)
7. [Bridge — Chat Completions vs the Week 1 Responses API](#7-bridge--chat-completions-vs-the-week-1-responses-api)
8. [The one insight that ties it together](#8-the-one-insight-that-ties-it-together)
9. [When to use which technique (decision table)](#9-when-to-use-which-technique-decision-table)
10. [Deep dives beyond the PDF](#10-deep-dives-beyond-the-pdf)
11. [🧵 Connected mental model](#11--connected-mental-model)
12. [⚡ 60-second recap](#12--60-second-recap)
13. [🗂️ Jargon Dictionary](#13--jargon-dictionary)
14. [🧠 Knowledge check](#14--knowledge-check)

---

## 1. What is prompt engineering?

### 📄 FROM THE PDF
> Prompt engineering is like learning the secret handshake to get the best out of large language models like OpenAI's GPT series. It's the art of sweet-talking an AI into giving you exactly what you want — without it going on a philosophical rant about the meaning of life. Let's dive into this mystical art with some fun techniques and a Python demo to make you feel like an AI whisperer.
>
> **What is Prompt Engineering?**
> Imagine you're at a restaurant, and the waiter is a super-intelligent AI. If you just say, *"Food, please,"* you're probably going to end up with a surprise dish. Prompt engineering is like crafting a detailed order: *"I'd like a Ghee Podi Idli, please."* With great prompts come great results (and fewer surprises).

### 🧠 EXPLAINED
**Prompt engineering** is the practice of **crafting the input text you send an LLM so it reliably produces the output you want.** No model retraining, no code deep in the network — just *what you say and how you say it.*

> **`Prompt`** = the text you send the model (in Week 1's terms, the `input` plus the `instructions`). **`Prompt engineering`** = deliberately designing that text.

💻 **Java analogies (pick whichever clicks):**
- It's like **writing a precise method contract / Javadoc**: a vague spec ("process the data") gets you a vague implementation; a precise one ("return a sorted, de-duplicated `List<String>`, throw on null") gets you exactly what you meant.
- Even closer: it's like **SQL query tuning**. Same database engine, but the *shape* of your query changes the result and the cost enormously. The LLM is the engine; the prompt is your query.
- The restaurant analogy is exactly right: the model is a capable but literal waiter. `"Food, please"` = an underspecified request → you get *a* valid answer, just maybe not *your* answer. `"Ghee Podi Idli, please"` = a specified request → predictable result.

**Why this matters so much:** an LLM is **non-deterministic** and will *always* return *something*. The failure mode isn't a crash or a `null` — it's a confident, plausible, *wrong-for-you* answer. Prompt engineering is how you shrink that gap between "a valid response" and "the response you needed." It is the cheapest, fastest lever you have (no GPUs, no fine-tuning, no redeploy).

The reading gives four core techniques, in rough order of sophistication: **zero-shot → few-shot → prompt chaining → chain-of-thought.**

---

## 2. Technique 1 — Zero-shot prompting

### 📄 FROM THE PDF
> **1. Zero-shot Prompting**
> This technique is the YOLO (You Only Live Once) of AI interactions: no examples, just vibes. You simply ask a question and hope the AI gets it right. Perfect for when you're feeling lucky.

### 🧠 EXPLAINED
**Zero-shot prompting** = you give the model **only an instruction, with zero examples**, and rely on the general knowledge it already learned during pretraining (W1·N01). You met this term in Week 1 — here it's technique #1.

- **Prompt:** `"Explain the concept of quantum computing in simple terms."`
- **You provide:** the task, nothing else.
- **The model relies on:** everything it absorbed in pretraining.

💻 **Java analogy:** calling a well-named library method with just its arguments and trusting the sensible defaults — `Collections.sort(list)` with no comparator. Often it's exactly right; sometimes the defaults aren't what you wanted.

**When it shines:** common, well-understood tasks (summarize, explain, translate, classify sentiment) where the model has seen millions of examples in training. It's the **cheapest** (fewest tokens) and **simplest** technique — always try it *first*.

**Where it breaks:** tasks needing a **specific output format**, a niche convention, or your house style. With no example to anchor on, the model guesses the format — and its guess may not match what your downstream code expects. That's the problem few-shot solves.

---

## 3. Technique 2 — Few-shot prompting

### 📄 FROM THE PDF
> **2. Few-shot Prompting**
> Few-shot prompting is like showing the AI a couple of magic tricks and then asking it to perform the next one. By providing a few examples, you're saying, *"Here's how it's done — now your turn."*

> ⚠️ **Heading note:** in the code, the PDF titles this section **"One Shot Prompting"**, but the function is `few_shot_prompt` and the demo provides **three** worked examples. Three examples = **few-shot**, not one-shot. (One-shot = exactly one example.) Treat the technique as few-shot; the "One Shot" heading is a PDF slip.

### 🧠 EXPLAINED
**Few-shot prompting** = you put **a few worked examples (input → output pairs) right inside the prompt**, then give the real input and let the model continue the pattern. You met the term in Week 1; here's the mechanism in action.

The demo's prompt:
```
Translate the following English phrases to French:
English: Hello, how are you?
French: Bonjour, comment ça va?
English: What is your name?
French: Comment vous appelez-vous?
English: Where is the library?
French:                          ← left hanging on purpose
```
The prompt *stops* right after `French:`. The model, having seen the pattern three times, completes the fourth by imitation:
```
French: Où est la bibliothèque ?
```

**Why it works — `in-context learning`.** The model isn't retrained; it **infers the pattern from the examples in the context window** and applies it *at inference time*. This is a superpower of LLMs called **in-context learning (ICL)**.

> **`In-context learning (ICL)`** = the model learning a task purely from instructions/examples placed in the prompt, **without any change to its weights.**

🔑 **Critical distinction — few-shot vs fine-tuning** (a classic interview trap):

| | Few-shot (in-context learning) | Fine-tuning (W1·N01) |
|---|---|---|
| What changes | Nothing — just the prompt | The model's **weights** |
| When | Every call, at inference time | Once, ahead of time (a training job) |
| Cost | A few extra tokens per call | GPU training run + hosting the tuned model |
| Persistence | Gone the moment the prompt ends | Baked into the model permanently |
| 💻 Java analogy | Passing **config/args at runtime** | **Recompiling & redeploying** the app |

> 🕐 **Callout — "training time" vs "inference time" (the split behind everything above)**
> A model lives in **two separate time periods**, and nearly every GenAI concept belongs to one of them:
>
> | Phase | What happens | When | Cost | 💻 Java analogy |
> |---|---|---|---|---|
> | **Training time** | The model's **weights** are built/adjusted from massive data | Once, offline, ahead of time | Enormous (GPUs for days) | `javac` / `mvn package` — build the JAR once |
> | **Inference time** | The finished, frozen model is **run to answer one input** | Every single API call | Tiny per call | A request hitting the running service |
>
> **`Inference time`** = the moment you call the model and it generates a response to your prompt. **Zero-shot, few-shot, prompt chaining, and CoT all happen at inference time** — they shape *one request* and vanish when it ends; the weights never change. **Fine-tuning** happens at *training time* and permanently rewrites the weights. That single distinction is the whole reason **few-shot ≠ fine-tuning** — it's **passing runtime args (inference)** vs **rebuilding the JAR (training)**.

**When to use few-shot:** when you need a **specific format or style**, the task is unusual, or zero-shot gave inconsistent structure. The examples pin down the format far better than any description. **Cost:** every example is tokens you pay for on *every* call — so use the *fewest* examples that lock the behavior.

---

## 4. Technique 3 — Prompt chaining

### 📄 FROM THE PDF
> **3. Prompt Chaining**
> Prompt chaining is the AI equivalent of a treasure hunt. You give it one clue (prompt), then use its answer to move to the next clue. It's a step-by-step process, and by the end, you've struck informational gold.

### 🧠 EXPLAINED
**Prompt chaining** = break a complex job into a **sequence of separate LLM calls**, where **the output of one call becomes (part of) the input to the next.**

The demo does it in two links:
1. **Step 1** — `"Provide a list of three popular programming languages."` → model returns `Python, JavaScript, Java`.
2. **Step 2** — takes that list and asks `"Explain the primary use case for each of these programming languages: <step-1 output>"` → model explains each (and, fittingly for you, describes **Java** as the enterprise/JVM/Spring/Hibernate language).

The key line is where the first answer is spliced into the second prompt:
```python
follow_up_prompt = f"Explain the primary use case for each of these programming languages:\n{response_part1}"
```

💻 **Java analogies:**
- **Function composition** — `explain(list())`: the result of one call feeds the next.
- The **Chain of Responsibility / pipeline pattern** — each stage does one job and hands off.
- A **multi-stage ETL pipeline** — extract, then transform, then load, each a discrete step.

**Why chain instead of one big prompt?**
- **Reliability** — one focused task per call beats one giant "do everything" prompt (which tends to drop requirements). Same reason you decompose a 200-line method into small ones.
- **Debuggability** — you can inspect the intermediate result (`response_part1`) and see *exactly* which step went wrong. A monolithic prompt is a black box.
- **Control / branching** — your Python code sits *between* the calls, so you can validate, filter, loop, or route based on the intermediate output.

**Cost/latency trade-off:** N steps = N API round-trips = more tokens and more latency than a single call. You're trading speed/cost for reliability and control. (This decomposition idea is the seed of **agents**, coming later — an agent is essentially a dynamic, self-directed prompt chain.)

---

## 5. Technique 4 — Chain-of-Thought (CoT) reasoning

### 📄 FROM THE PDF
> **4. Chain-of-Thought (CoT) Reasoning**
> CoT reasoning is like asking the AI to show its work, math-class style. Instead of jumping to conclusions, it walks you through the logic step by step. This technique can make even the trickiest problems feel like a stroll in the park.

### 🧠 EXPLAINED
**Chain-of-Thought (CoT)** = prompt the model to **spell out its reasoning step by step *before* giving the final answer** — usually by adding a phrase like **"Explain your reasoning step by step"** or the famous **"Let's think step by step."**

The demo's problem: *A train leaves at 60 mph. A second leaves the same station one hour later at 80 mph. How long until the second catches the first? Explain your reasoning step by step.*

The model works it out (cleaned up from the PDF's output):
```
Let t = hours the FIRST train has traveled when caught.
  First train distance   = 60 · t
  Second train travels (t − 1) hours → distance = 80 · (t − 1)
Set them equal (same point):   60t = 80(t − 1)
  60t = 80t − 80  →  20t = 80  →  t = 4
First train traveled 4 h; the second started 1 h later,
so the SECOND train travels 4 − 1 = 3 hours.
Answer: 3 hours.
```

**Why does "show your work" actually make it more accurate?** This is the deep part:

An LLM is **autoregressive** (W1·N01) — it generates one token at a time and **cannot go back and edit**. If you demand the final number immediately, all the "computation" has to happen in a single forward pass — it's forced to *blurt* an answer. By letting it **write the intermediate steps first**, each step it writes becomes **context for the next step**, effectively giving the model *more compute and a scratchpad* to reach the right answer. It's the difference between doing long division in your head vs. on paper.

💻 **Java analogy:** forcing a method to **log its intermediate state** (or **rubber-duck debugging** out loud) instead of returning a single opaque value. The act of narrating the steps catches errors that a straight-to-answer path would make.

🧵 **Connection to Week 1 — reasoning models (W1·SG02).** Remember "reasoning models spend extra compute at answer-time to think longer"? CoT is the *prompting trick* that manually induces that behavior on an ordinary model. Modern **reasoning models** (o-series, etc.) do CoT *internally by default*, so you often don't need to ask. But for standard chat models, CoT is your go-to for math, logic, and multi-step problems.

**Trade-off:** CoT produces lots of extra tokens (all that reasoning) → **more cost and higher latency**, and the reasoning bloats the answer. Use it when correctness on a hard, multi-step problem matters more than brevity/speed. For simple lookups, it's overkill.

---

## 6. The Python demo — prerequisites & code, line by line

### 📄 FROM THE PDF
> **Python Demo: Implementing Prompt Engineering Techniques**
> Here's a Python script that showcases these techniques using OpenAI's API (you can use **Cohere** or any other open-source model from Hugging Face as well).
>
> **Prerequisites**
> - Install the OpenAI Python library: `pip install openai`
> - Obtain an OpenAI API key from OpenAI's platform.

*(Note the callback to W2·SG01: "you can use Cohere or any open-source model from Hugging Face" — the technique is provider-agnostic. **`Cohere`** is another closed-source LLM provider, like OpenAI/Anthropic.)*

### 🧠 EXPLAINED — the code

**Setup (added — the PDF omitted it):**
```python
from openai import OpenAI
client = OpenAI()          # reads OPENAI_API_KEY from the environment
MODEL = "gpt-4o-mini"      # a small, cheap, fast chat model — fine for demos
```
- `client = OpenAI()` builds the SDK client (W1·SG03). With no argument, it reads your key from the `OPENAI_API_KEY` env var — the same pattern as `week1/code/openai_client.py`.

**Technique 1 — Zero-shot:**
```python
def zero_shot_prompt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    print("Zero-shot Prompting:\n", response.choices[0].message.content)

zero_shot_prompt("Explain the concept of quantum computing in simple terms.")
```
- `client.chat.completions.create(...)` — the **Chat Completions** API call (see [§7](#7-bridge--chat-completions-vs-the-week-1-responses-api) for how this differs from Week 1).
- `messages=[{"role": "user", "content": prompt}]` — a list of role-tagged messages (W1·SG03: `system`/`user`/`assistant`). Here, one `user` message, no examples → **zero-shot**.
- `response.choices[0].message.content` — Chat Completions returns a list of `choices`; `[0]` is the first (usually only) completion, and `.message.content` is its text. *(Contrast Week 1's Responses API, which gives you the tidy `response.output_text`.)*

**Sample response (abridged):**
> Quantum computing … uses the principles of quantum mechanics … **1. Bits vs. Qubits** (superposition — 0 and 1 at once) … **2. Entanglement** … **3. Parallelism** … **4. Quantum Gates** … potentially leading to breakthroughs in cryptography, chemistry, and optimization.

**Technique 2 — Few-shot:** the function body is **identical** to `zero_shot_prompt` — only the prompt differs (see [§8](#8-the-one-insight-that-ties-it-together)). The prompt supplies three `English:/French:` pairs then a dangling `French:`, and the model completes: `Où est la bibliothèque ?`

**Technique 3 — Prompt chaining:**
```python
def chain_part1(initial_prompt):
    response1 = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": initial_prompt}])
    return response1.choices[0].message.content         # step-1 output

def chain_part2(follow_up_prompt):
    response2 = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": follow_up_prompt}])
    return response2.choices[0].message.content

response_part1 = chain_part1("Provide a list of three popular programming languages.")
follow_up_prompt = f"Explain the primary use case for each of these programming languages:\n{response_part1}"
response_part2 = chain_part2(follow_up_prompt)
```
- Two separate calls. The magic is the **f-string** splicing `response_part1` into the second prompt — that's the "chain." Note each call is **independent/stateless**: `chain_part2` knows about step 1 *only* because you literally pasted its text into the new prompt. (Week 1's `previous_response_id` is the *server-side* alternative to this manual threading.)

**Technique 4 — Chain-of-Thought:** again the same call shape; the technique is entirely in the prompt ending with `"Explain your reasoning step by step."`, which triggers the step-by-step derivation shown in [§5](#5-technique-4--chain-of-thought-cot-reasoning).

### 📄 FROM THE PDF — Conclusion
> Prompt engineering isn't just a technical skill — it's a superpower. Whether you're coaxing an AI to solve complex problems or just getting it to say something funny, crafting the right prompt is key. Now, go forth and experiment!

---

## 7. Bridge — Chat Completions vs the Week 1 Responses API

This PDF uses **Chat Completions**; Week 1 used the **Responses API**. Same model, same techniques — different endpoint shape. Know both, because you'll see both in the wild.

| | **Chat Completions** (this PDF) | **Responses API** (Week 1) |
|---|---|---|
| Call | `client.chat.completions.create(...)` | `client.responses.create(...)` |
| Input arg | `messages=[{role, content}, …]` | `input=...` (+ `instructions=`) |
| Get the text | `resp.choices[0].message.content` | `resp.output_text` |
| Multi-turn | You resend the whole `messages` history, **or** chain manually | Server-side via `previous_response_id` |
| Status | Original, stateless, universally supported | OpenAI's newer, recommended API |

**The same zero-shot call in Responses-API style (Week 1 idiom):**
```python
resp = client.responses.create(
    model="gpt-4.1-mini",
    input="Explain the concept of quantum computing in simple terms.",
)
print(resp.output_text)
```
> **Takeaway:** the four techniques (zero-shot, few-shot, chaining, CoT) are **API-agnostic and even provider-agnostic** — they're about *what text you send*, not *which endpoint*. The PDF itself says so ("you can use Cohere or any open-source model"). This is the same swappability you saw in the ticket-triage assignment.

---

## 8. The one insight that ties it together

Look at the demo's `zero_shot_prompt` and `few_shot_prompt` — they are the **exact same function**:
```python
def zero_shot_prompt(prompt):
    response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}])
    print(..., response.choices[0].message.content)

def few_shot_prompt(prompt):        # ← identical body!
    response = client.chat.completions.create(model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}])
    print(..., response.choices[0].message.content)
```

**The technique is not in the code — it's in the prompt string you pass.** Zero-shot vs few-shot vs CoT differ only by *what text* goes into `content`. Prompt chaining is the one that adds *code* structure (multiple calls + splicing).

💻 This is the mental unlock for a backend engineer: you're used to behavior living in **code**. In GenAI, an enormous amount of behavior lives in **data** (the prompt). "Programming" the model often means **editing a string**, not editing logic. That's why prompt engineering is a first-class skill, not an afterthought.

---

## 9. When to use which technique (decision table)

| Technique | Use when… | Cost (tokens/latency) | 💻 Backend analogy |
|---|---|---|---|
| **Zero-shot** | Common task, format not critical; always your first try | 💲 lowest | Method call with defaults |
| **Few-shot** | You need a specific format/style, or zero-shot is inconsistent | 💲💲 (examples add tokens every call) | Pass config/examples at runtime |
| **Prompt chaining** | Complex multi-part task; you want to inspect/validate intermediate steps | 💲💲💲 (N calls) | Pipeline / function composition |
| **Chain-of-Thought** | Math, logic, multi-step reasoning where correctness > brevity | 💲💲💲 (lots of reasoning tokens) | Log intermediate state / rubber-duck |

**Rules of thumb:**
- **Escalate, don't jump.** Try zero-shot → if the *format* is off, add few-shot examples → if the *reasoning* is off, add CoT → if the *task* is too big for one call, chain it. Each step up costs more tokens; don't pay for what you don't need.
- These **compose**: a single step in a prompt chain can itself be few-shot *and* use CoT.

---

## 10. Deep dives beyond the PDF

- **Prompt engineering vs fine-tuning vs RAG (the "how do I make it better?" ladder).** Prompt engineering (free, instant, this reading) → RAG (feed it your data, coming later) → fine-tuning (change the weights, W1). Always exhaust the cheap lever (prompting) before the expensive one (fine-tuning).
- **Determinism.** This demo omits `temperature`, so outputs vary run-to-run. The Week 1 ticket-triage assignment used `temperature=0` precisely because *classification/routing* must be repeatable. Prompt technique and sampling settings are two different knobs — pair them deliberately.
- **Format-locking with Structured Outputs.** Few-shot nudges format; **Structured Outputs** (W1·SG03, Pydantic schema) *guarantees* it. For production JSON, prefer Structured Outputs over hoping few-shot examples hold.
- **CoT and reasoning models.** If you're on a dedicated reasoning model, explicit "think step by step" is often redundant (it reasons internally) and can even hurt — read the model's own guidance. On plain chat models, CoT is still gold.
- **Prompt injection (a security seed).** Because behavior lives in the prompt, *untrusted text inside the prompt* can hijack it ("ignore previous instructions…"). Keep this in the back of your mind for when we build agents and RAG.

---

## 11. 🧵 Connected mental model

```
  W2·SG01: pick a model (open ⇄ closed)
                 │
                 ▼
  W2·SG02: TALK to the model  ── prompt engineering ──┐
                 │                                      │  behavior lives in the
     ┌───────────┼───────────────┬──────────────┐      │  PROMPT (data), not code
     ▼           ▼               ▼              ▼      │
  zero-shot   few-shot        chaining        CoT      │
  (no ex.)  (examples=ICL)  (multi-call)  (show work)  │
     └───────────┴───────────────┴──────────────┘      │
                 │                                      │
                 ▼                                      ▼
   escalate as needed ─────────────▶ later: RAG · Agents (chaining++) · Fine-tuning
```

**One-line thread:** `choose a model (SG01) → engineer the prompt to steer it (SG02) → zero-shot → few-shot (in-context learning) → chaining → CoT → these grow into RAG & agents.`

Ties back to Week 1: **few-shot ≠ fine-tuning** (prompt vs weights), **CoT ≈ manual reasoning-model behavior**, and **chaining + `previous_response_id`** are two ways to carry state across calls.

---

## 12. ⚡ 60-second recap

- **Prompt engineering** = crafting the input text so the model reliably gives *your* desired output. Cheapest, fastest lever — no retraining. (Restaurant: "Food please" vs "Ghee Podi Idli please.")
- **Zero-shot** — just ask, no examples. Cheapest; try first. Weak on specific formats.
- **Few-shot** — put a few input→output examples in the prompt; the model copies the pattern via **in-context learning** (no weight change → *not* fine-tuning). Best for locking format/style.
- **Prompt chaining** — split a big task into multiple calls, feeding each output into the next. More reliable, debuggable, controllable; costs more calls. Seed of agents.
- **Chain-of-Thought** — ask it to reason "step by step." Works because writing intermediate tokens gives an autoregressive model a scratchpad. Great for math/logic; costs tokens. Reasoning models do it internally.
- **The unlock:** zero-shot/few-shot/CoT differ only by the *prompt string*, not the code — behavior lives in **data**.
- The techniques are **API- and provider-agnostic** (Chat Completions or Responses; OpenAI or Cohere/Hugging Face).

---

## 13. 🗂️ Jargon Dictionary

*(New this reading. Zero-shot & few-shot were defined in Week 1 — reused here.)*

| Term | Definition |
|---|---|
| **Prompt engineering** | Deliberately crafting the input text sent to an LLM so it reliably produces the desired output — "programming in natural language." |
| **Prompt** | The text you send the model (the `input` + any `instructions`). |
| **In-context learning (ICL)** | The model learning a task from examples/instructions in the prompt *at inference time*, with **no change to its weights** — the mechanism behind few-shot. |
| **Training time vs inference time** | Training time = when a model's weights are built (once, offline, expensive; ≈ compile/build). Inference time = when the finished model is run to answer an input (per call, cheap; ≈ runtime request). All prompt techniques act at inference time. |
| **One-shot prompting** | Prompting with **exactly one** worked example (between zero-shot and few-shot). *(The PDF's "One Shot" heading actually shows few-shot.)* |
| **Prompt chaining** | Breaking a complex task into a sequence of LLM calls where each output feeds the next call's input. |
| **Chain-of-Thought (CoT) reasoning** | Prompting the model to spell out its reasoning step by step before answering, improving accuracy on multi-step problems. |
| **"Let's think step by step"** | The canonical trigger phrase that elicits CoT reasoning from a standard chat model. |
| **Chat Completions API** | OpenAI's original endpoint (`client.chat.completions.create`, `messages=[…]`, read `choices[0].message.content`); the style used in this PDF. *(Also W1·SG03.)* |
| **`gpt-4o-mini`** | A small, fast, low-cost OpenAI chat model used in the demo. |
| **Cohere** | Another closed-source LLM provider (API), given as a drop-in alternative to OpenAI. |

---

## 14. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining any mistakes rather than just giving answers.

**Conceptual**
1. Define prompt engineering in one sentence, and explain why it's often preferable to fine-tuning as a *first* attempt at improving output.
2. Few-shot prompting and fine-tuning both "teach" the model. What is the fundamental difference, and which one changes the model's weights?
3. Why does Chain-of-Thought make an LLM *more accurate* on a math problem? Tie your answer to the word "autoregressive."

**Applied**
4. In the demo, `zero_shot_prompt` and `few_shot_prompt` have identical bodies. What, then, actually makes one "zero-shot" and the other "few-shot"? What does this tell you about where LLM behavior lives?
5. You must extract `{name, email, order_id}` as strict JSON from messy customer emails, and downstream code parses it. Which technique(s) would you reach for, and would you *also* use anything from Week 1 to be safe?
6. Rewrite the two-step language demo as a **three-link** chain that ends by producing a one-line "hello world" snippet in the *first* language returned. Describe each link's prompt.

**Interview-style**
7. A teammate says "few-shot prompting fine-tunes the model on the examples." Correct them precisely.
8. When would you deliberately *avoid* Chain-of-Thought, and when would explicit CoT be redundant?

---

*End of Study Guide 02·02. Next Week 2 reading → paste it and I'll build Study Guide 02·03, extending the glossary and the mental model.*
