# 📘 Week 1 · Study Guide 04 — How to Choose a GenAI Model (Types, Criteria & Benchmarks)

> **Self-contained document.** Contains the **complete original PDF content** *plus* first-principles explanations of every concept and piece of jargon. You do **not** need to open the PDF.
>
> **How to read:** 📄 **`FROM THE PDF`** = original text · 🧠 **`EXPLAINED`** = plain-English teaching · 🔑 **bold jargon** defined on first use and again in the **Jargon Dictionary**. Written for a **Java/backend engineer**.
>
> 🧭 **Where this fits:** Reading 02 introduced the *cost/latency/accuracy trade-off*; Reading 03 showed you *how* to call a model. This reading answers **"which model do I even pick?"** — it's an **architecture-decision guide**. Treat it like choosing a database or a message broker: there's no "best," only "best *for this use case + these constraints*."

---

## 📑 Table of Contents

1. [Why choosing is hard](#page-1-3--why-choosing-is-hard)
2. [The 5 types of GenAI models](#page-3--types-of-generative-ai-models)
3. [The 9 criteria for choosing](#page-3-4--criteria-for-choosing-a-model)
4. [Benchmarks & key metrics](#page-5--benchmarks--key-metrics)
5. [The 5-step decision framework](#page-5--decision-making-framework)
6. [Closing: not every problem needs GenAI](#page-6--closing)
7. [🗂️ Jargon Dictionary](#-jargon-dictionary)
8. [📊 Comparison tables](#-comparison-tables)
9. [🧵 Connected mental model](#-connected-mental-model)
10. [⚡ 60-second recap](#-60-second-recap)

---

## Page 1–3 — Why Choosing Is Hard

> 📄 **FROM THE PDF**
> *"Choosing a GenAI model is easy" — said no one ever.*
> Most people met the term "GenAI" via **ChatGPT**. But choosing the right model can feel overwhelming given the diversity of options and rapid advancements. Most of you would check **cost, inference time, and ease of use** — but remember: *"One does not simply choose the cheapest vendor every time."*
>
> **"Choosing the right model involves balancing various factors like governance, use case, performance, data, and resources."**

### 🧠 EXPLAINED

The whole reading hangs on that one bolded sentence. The naïve instinct is to optimize a single axis (usually **cheapest** or **most powerful**). The reading's thesis: model selection is a **multi-factor balancing act**, not a single-number decision.

The five balancing factors named upfront:

| Factor | Question it asks | 💻 Backend parallel |
|---|---|---|
| 🔑 **Governance** | Are we allowed to use it? (privacy, legal, data-handling policy) | Compliance/security review before adopting a vendor |
| **Use case** | What exactly are we solving? | Functional requirements |
| **Performance** | Is it accurate/fast enough? | SLAs, latency budgets |
| **Data** | What data can/must we feed it? Where does it go? | Data residency, PII handling |
| **Resources** | Budget, hardware, team skills? | Infra & staffing constraints |

- 🔑 **Governance:** the rules, policies, and controls around *how* AI is used — who's accountable, what data is allowed, what's auditable. In an enterprise this is often the *first* gate, before technical fit. (Easy for engineers to overlook; it's frequently the deciding factor.)

- 🔑 **Inference time** *(recap):* how long the model takes to produce a response (Reading 03's **latency**). Critical for anything user-facing.

> 💻 **Reframe for you:** this is an **Architecture Decision Record (ADR)**. You wouldn't pick a datastore purely on "cheapest" — you'd weigh consistency, latency, ops burden, team familiarity, compliance. Same discipline here.

---

## Page 3 — Types of Generative AI Models

> 📄 **FROM THE PDF** — models categorized by **output type**:
>
> **1. Text Generation** — GPT (OpenAI), Gemini (Google), LLaMA (Meta), Claude (Anthropic). *Use cases:* chatbots, content creation, summarization, code generation.
> **2. Image Generation/Segmentation** — DALL·E, MidJourney, Stable Diffusion, Segment Anything Model. *Use cases:* art, design, product visualization, inpainting.
> **3. Speech & Audio Generation** — WaveNet, VALL-E, Tacotron. *Use cases:* voice assistants, dubbing, music generation.
> **4. Code Generation** — GitHub Copilot (powered by GPT), OpenAI Codex. *Use cases:* writing code, debugging, automation.
> **5. Multimodal** — Gemini (DeepMind), GPT-4 with vision, Grounding DINO. *Use cases:* cross-domain tasks like captioning images or combining text + image.

### 🧠 EXPLAINED

The organizing principle: **categorize by what the model outputs.** Match the output type to your goal first — that instantly narrows the field.

| Type | Outputs | Notable models | 🔑 Term to know |
|---|---|---|---|
| **Text** | Words/tokens | GPT, Gemini, LLaMA, Claude | These are the **LLMs** from earlier readings (Transformer decoders). |
| **Image** | Pixels | DALL·E, MidJourney, Stable Diffusion, SAM | Mostly **diffusion models** (Reading 02). |
| **Speech/Audio** | Sound waves | WaveNet, VALL-E, Tacotron | 🔑 **TTS (text-to-speech)** & voice cloning. |
| **Code** | Source code | Copilot, Codex | Text models specialized on code. |
| **Multimodal** | Mixed | Gemini, GPT-4V, Grounding DINO | Reading 02's **multimodal** models. |

**Quick definitions of the less-obvious names:**
- 🔑 **Inpainting:** filling in or editing *part* of an image (e.g., remove an object and regenerate the background). A common image-gen use case.
- 🔑 **Segmentation / Segment Anything Model (SAM):** identifying and outlining *objects* in an image pixel-by-pixel (which pixels are "the cat"). Meta's SAM is the famous one. Note this is *analysis*, bundled here with image models.
- 🔑 **WaveNet / VALL-E / Tacotron:** speech-synthesis models (turn text → natural-sounding speech; VALL-E can clone a voice from seconds of audio).
- 🔑 **Codex / Copilot:** code-generation models; **GitHub Copilot** is the IDE assistant, historically powered by OpenAI **Codex** (a GPT specialized on code).
- 🔑 **Grounding DINO:** a multimodal model that finds objects in an image *from a text description* ("point to the red mug") — bridges text + vision.

> **Practical takeaway:** Step 1 of choosing is trivial once framed right — **what output do I need?** Text summary → text model. Product mockups → image model. Voiceover → audio model. Only *within* a category do the hard trade-offs begin.

---

## Page 3–4 — Criteria for Choosing a Model

> 📄 **FROM THE PDF** (9 criteria):

Here are the nine factors, each explained with what to actually *do*:

### 1. Use Case Requirements
> Define the specific problem (text summarization vs. code generation). Consider **domain-specific models** (e.g., **BioGPT** for biomedical text).

🧠 Start from the problem, not the model. A 🔑 **domain-specific model** is pre-trained/tuned on a narrow field (medicine, law, finance) — it can beat a bigger general model *on that domain* while being smaller/cheaper. (BioGPT = biomedical; there are legal/finance equivalents.)

### 2. Model Size and Performance
> Smaller models (e.g., **DistilGPT**) are faster and cost-efficient but may lack depth. Larger models (GPT-4, Claude) give higher accuracy but are computationally expensive.

🧠 The core trade-off again. 🔑 **DistilGPT** is a *distilled* model — see 🔑 **distillation**: training a small "student" model to mimic a big "teacher," keeping most of the quality at a fraction of the size/cost. Bigger ≠ always better (recall the **Chinchilla** lesson + the cost/latency/accuracy triangle).

### 3. Inference Cost
> Cloud-hosted APIs (OpenAI, Hugging Face) **vs.** deploying open-source models (LLaMA, Falcon) locally. Evaluate hardware requirements for self-hosted models.

🧠 The classic **buy vs. build / SaaS vs. self-host** decision:
- **API (managed):** pay per token, zero infra, instant scale — but ongoing per-call cost and data leaves your walls.
- **Self-hosted open model:** you run it on your **GPUs** — more control & privacy, but you own the hardware, ops, and scaling. (🔑 **Falcon** = a well-known open LLM, like LLaMA.)

### 4. Training Data
> Check if the model is pre-trained on diverse large-scale data or domain-specific data. Consider **fine-tuning** for niche needs.

🧠 What a model "knows" comes from its training data. If your domain is niche, either pick a domain model or plan to **fine-tune** (Reading 01/02 term: cheaply specialize a pretrained model on your own data).

### 5. Customizability
> Ability to **fine-tune** using techniques like **LoRA** or **QLoRA** for personalized tasks.

🧠 Two important efficiency techniques:
- 🔑 **LoRA (Low-Rank Adaptation):** fine-tune by training a *tiny set of extra weights* instead of the whole giant model — dramatically cheaper/faster, and you keep the base model frozen. This is 🔑 **PEFT (Parameter-Efficient Fine-Tuning)**.
- 🔑 **QLoRA:** LoRA on top of a **quantized** (compressed) model, so you can fine-tune huge models on modest hardware (even a single GPU). 🔑 **Quantization** = storing weights at lower precision (e.g., 4-bit) to shrink memory with minimal quality loss.

### 6. Data Security 🔐
> **Open-source (self-hosted):** complete data control & privacy, but needs technical setup/maintenance. **Closed-source (API):** convenient & scalable but may expose sensitive data — always review the provider's data-handling policies.

🧠 **The privacy fork.** If you handle sensitive data (health, finance, PII), *where the data goes* can override everything else. Self-hosting keeps data in-house; APIs send it to a third party (read their retention/training policies carefully). This ties directly back to **governance** (factor #1 of the intro).

### 7. Latency and Scalability
> Does it meet real-time response needs? Can it handle growing users / large-scale deployment?

🧠 Pure engineering concerns you already know: 🔑 **latency** (per-request speed) and 🔑 **scalability** (handle load). A brilliant-but-slow model fails a real-time chat SLA.

### 8. Ethical and Legal Compliance
> Does it align with privacy laws (e.g., **GDPR**) and ethical AI? Check for built-in safeguards against harmful/biased content.

🧠 🔑 **GDPR** = the EU's strict data-protection law (heavy fines for mishandling personal data). Also check the model's **guardrails** (safety filters). Connects to Reading 02's ethics section (bias, misinformation).

### 9. Integration and Ecosystem
> Ease of integration with existing workflows, frameworks (**TensorFlow, PyTorch**), or **APIs**.

🧠 A model that plugs into your stack (good SDK, framework support, tooling) beats a marginally-better one that fights your architecture. Developer experience and ecosystem maturity are real selection factors.

> **The pattern across all 9:** they cluster into **(A) Fit** (use case, training data, size), **(B) Cost/Ops** (inference cost, latency, scalability, integration), and **(C) Trust** (data security, compliance, customizability for control). A good choice satisfies all three, not just one.

---

## Page 5 — Benchmarks & Key Metrics

> 📄 **FROM THE PDF** — *Specialized Benchmarks:*
> - **MMLU (Massive Multitask Language Understanding):** academic/professional tasks.
> - **HellaSwag** and **WinoGrande:** reasoning and commonsense understanding.
> - **OpenLLM Leaderboard:** compare open-source LLMs like Mistral, Falcon, LLaMA.
>
> *Key Metrics to Evaluate:*
> - **Accuracy / Factual Correctness:** factually correct and coherent?
> - **Creativity:** can it generate novel, useful outputs?
> - **Bias and Safety:** fair, unbiased, safe?
> - **Inference Time:** speed of response (crucial for real-time).

### 🧠 EXPLAINED

- 🔑 **Benchmark** *(recap):* a standardized test that scores a model so you can compare models on the same yardstick.

| Benchmark | Tests | In plain terms |
|---|---|---|
| 🔑 **MMLU** | 57 subjects (law, medicine, math, history…) | "Broad exam knowledge" — the general-smarts score. |
| 🔑 **HellaSwag** | Commonsense sentence completion | "Does it pick the obviously-sensible next event?" |
| 🔑 **WinoGrande** | Pronoun/ambiguity resolution | "Does it understand what 'it'/'they' refers to?" (commonsense reasoning) |
| 🔑 **OpenLLM Leaderboard** | Aggregated scores for **open** models | A public ranking to compare Mistral/Falcon/LLaMA etc. (🔑 **Mistral** = another strong open model family.) |

**The four key metrics** map to real product concerns:

| Metric | Why it matters | Watch out for |
|---|---|---|
| **Accuracy / factual correctness** | Wrong answers erode trust | 🔑 **Hallucination** — confidently stated falsehoods |
| **Creativity** | Needed for content/ideation | Hard to measure objectively |
| **Bias & safety** | Fairness, legal, reputational | Test with adversarial/edge inputs |
| **Inference time** | Real-time UX | Trades off against model size |

> ⚠️ **Critical caveat the PDF doesn't stress (interview gold):** **benchmarks are a starting filter, not the verdict.** Three reasons:
> 1. 🔑 **Benchmark contamination** — test questions may have leaked into training data, inflating scores.
> 2. **Benchmarks ≠ your task** — a top MMLU score says nothing about *your* specific customer-support classification.
> 3. That's exactly why the framework below ends with **Prototype** — *your own eval on your own data* is the real test.

---

## Page 5 — Decision-Making Framework

> 📄 **FROM THE PDF** (5 steps):
> 1. **Define Objectives** — clearly outline what you aim to achieve.
> 2. **Shortlist Models** — based on type and use case.
> 3. **Evaluate Benchmarks** — compare shortlisted models against industry benchmarks.
> 4. **Prototype** — test on a small dataset or subset of tasks.
> 5. **Deploy and Monitor** — continuous monitoring for performance and user feedback.

### 🧠 EXPLAINED — this is your repeatable playbook

```
1. DEFINE ────► 2. SHORTLIST ────► 3. BENCHMARK ────► 4. PROTOTYPE ────► 5. DEPLOY + MONITOR
   objectives      by type +          filter with        test on YOUR       ship, watch,
   & constraints   use case           public scores      data (the real     iterate on
                   (narrows fast)     (rough cut)         test)              feedback
```

- **1. Define** — nail objectives *and* constraints (budget, latency, privacy) up front. Vague goals → wrong model.
- **2. Shortlist** — output type + use case slashes the list to a handful (Step 1 of choosing was easy, remember).
- **3. Benchmark** — use public scores as a *rough filter*, not gospel (see caveat above).
- **4. Prototype** — 🌟 **the most important step.** Test the finalists on *your* data/tasks. This is where the "best on paper" model often loses to a cheaper one that's plenty good for *your* job.
- **5. Deploy & Monitor** — models drift, usage changes, edge cases appear. 🔑 **Monitoring** (logging quality, latency, cost, user feedback) is ongoing, not one-time.

> 💻 **You already do this.** It's the same loop as choosing any tech: define requirements → shortlist candidates → check reputation/benchmarks → **spike/POC** → adopt with observability. The GenAI twist is that **Prototype uses your real prompts/data**, because benchmark scores generalize poorly to specific tasks.

---

## Page 6 — Closing

> 📄 **FROM THE PDF**
> But remember: **Not every problem needs GenAI.** But when it does, choosing the right model can make the difference between *"Wow, this is amazing!"* and *"Why is this even a thing?"*

### 🧠 EXPLAINED
The maturity takeaway. GenAI is a powerful, *expensive, non-deterministic* tool — not a hammer for every nail. If a problem is solved better by a **regex, a SQL query, a rules engine, or a small classic ML model**, use that. Reach for GenAI when the task genuinely needs *language understanding, generation, or reasoning over unstructured input*. Choosing well (both *whether* and *which*) is what separates an impressive product from an over-engineered gimmick.

---

## 🗂️ Jargon Dictionary

| Term | Definition | Why it matters |
|---|---|---|
| **Benchmark** | Standardized test scoring/comparing models. | Rough filter when shortlisting. |
| **Benchmark contamination** | Test data leaked into training, inflating scores. | Why benchmarks aren't the final word. |
| **BioGPT** | A biomedical domain-specific text model. | Example of domain specialization. |
| **Closed-source model** | Accessed via API; provider hosts it. | Convenient/scalable; data leaves your walls. |
| **Codex / Copilot** | Code-generation model / IDE assistant. | Code-gen category. |
| **Creativity (metric)** | Ability to produce novel, useful output. | Key eval metric; hard to quantify. |
| **Distillation / DistilGPT** | Training a small "student" to mimic a big "teacher." | Smaller, faster, cheaper models. |
| **Domain-specific model** | Pre-trained/tuned on one field (med/law/finance). | Can beat bigger general models on that domain. |
| **Falcon** | A well-known open LLM. | Self-hosting option. |
| **GDPR** | EU data-protection law. | Compliance gate for handling personal data. |
| **Governance** | Rules/policies/accountability for AI use. | Often the first (overlooked) selection gate. |
| **Grounding DINO** | Finds objects in an image from a text prompt. | Multimodal example. |
| **Guardrails** | Built-in safety filters against harmful output. | Part of safety evaluation. |
| **Hallucination** | Confidently stated falsehoods. | The main accuracy risk. |
| **HellaSwag** | Commonsense completion benchmark. | Tests everyday reasoning. |
| **Inference cost / time** | Price / latency per response. | Core cost & UX factors. |
| **Inpainting** | Editing/filling part of an image. | Image-gen use case. |
| **LoRA** | Fine-tune tiny extra weights, base frozen. | Cheap, fast customization (PEFT). |
| **MMLU** | 57-subject knowledge exam benchmark. | "General smarts" score. |
| **Mistral** | Strong open LLM family. | Open-model option. |
| **Monitoring** | Ongoing tracking of quality/latency/cost/feedback. | Step 5 of the framework. |
| **Multimodal** | Handles mixed input/output types. | Cross-domain tasks. |
| **OpenLLM Leaderboard** | Public ranking of open LLMs. | Compare Mistral/Falcon/LLaMA. |
| **Open-source model** | Downloadable, self-hostable. | Data control & privacy; you run the infra. |
| **PEFT** | Parameter-Efficient Fine-Tuning (LoRA/QLoRA family). | Customize huge models cheaply. |
| **Quantization** | Store weights at lower precision (e.g., 4-bit). | Shrinks models; enables QLoRA. |
| **QLoRA** | LoRA on a quantized model. | Fine-tune big models on small hardware. |
| **SAM (Segment Anything)** | Meta's image segmentation model. | Outlines objects pixel-by-pixel. |
| **Scalability** | Handle growing load/users. | Production readiness. |
| **TTS** | Text-to-speech synthesis. | Speech/audio category. |
| **WaveNet / VALL-E / Tacotron** | Speech-synthesis models. | Audio generation examples. |
| **WinoGrande** | Pronoun/ambiguity reasoning benchmark. | Commonsense reasoning. |

---

## 📊 Comparison Tables

### Open-source (self-hosted) vs Closed-source (API)
| | Open-source (self-host) | Closed-source (API) |
|---|---|---|
| **Data privacy** | ✅ Stays in-house | ⚠️ Sent to provider |
| **Setup/ops burden** | ❌ You run GPUs, scaling, updates | ✅ None — just call the API |
| **Cost model** | Upfront hardware + ops | Pay per token |
| **Customization** | ✅ Full (weights, fine-tune, LoRA) | Limited (prompting, some fine-tune) |
| **Scaling** | You engineer it | ✅ Provider handles it |
| **Best when** | Privacy-critical, high volume, control | Fast start, low volume, small team |

### Smaller vs Larger models
| | Smaller (e.g. DistilGPT) | Larger (e.g. GPT-4, Claude) |
|---|---|---|
| **Speed / latency** | ✅ Fast | ❌ Slower |
| **Cost** | ✅ Cheap | ❌ Expensive |
| **Accuracy / depth** | ⚠️ Lower | ✅ Higher |
| **Best when** | High volume, simple tasks, real-time | Hard reasoning, quality-critical |

---

## 🧵 Connected Mental Model

```
                    "Which GenAI model?"  (an ARCHITECTURE DECISION)
                                 │
                 ┌───────────────┴────────────────┐
        1) What OUTPUT?                    2) Under what CONSTRAINTS?
        (narrows type fast)                (the real balancing act)
   text│image│audio│code│multimodal        governance · use case ·
                 │                          performance · data · resources
                 ▼                                    │
            SHORTLIST  ──►  BENCHMARK (rough filter)  ──►  PROTOTYPE on YOUR data
                 │              MMLU/HellaSwag/                    │  ← the real test
                 │              WinoGrande/leaderboards            │
                 └──────────────────────────────────────────► DEPLOY + MONITOR
                                                                  (quality/cost/feedback)

   Trade-off axes running underneath everything:
     cost  ⇄  latency  ⇄  accuracy      |      privacy/control (self-host) ⇄ convenience (API)
```

**Ties to earlier readings:** the *cost/latency/accuracy* triangle (Reading 02) is the spine here. The *5 model families* (Reading 02) map onto the *5 output types*. *Fine-tuning* (Readings 01–02) reappears as LoRA/QLoRA under "Customizability." And you'd *implement* the chosen model via the *API* skills from Reading 03.

---

## ⚡ 60-Second Recap

- **No "best" model — only best-for-your-use-case + constraints.** Balance **governance, use case, performance, data, resources.**
- **Choose by output type first:** text · image · audio · code · multimodal — this instantly shortlists.
- **9 criteria:** use case · size/perf · inference cost · training data · customizability (**LoRA/QLoRA**) · **data security** · latency/scalability · **ethical/legal (GDPR)** · integration.
- **Open (self-host)** = privacy + control, you run the infra. **Closed (API)** = convenient + scalable, data leaves your walls.
- **Benchmarks (MMLU, HellaSwag, WinoGrande, OpenLLM Leaderboard)** = *rough filter only* — beware contamination and "benchmark ≠ your task."
- **Metrics:** accuracy/factual · creativity · bias/safety · inference time.
- **Framework:** Define → Shortlist → Benchmark → **Prototype on YOUR data (the real test)** → Deploy & Monitor.
- **And:** not every problem needs GenAI — use the simplest tool that works.

---

*This is your complete Week 1 Reading 04. Next: Playground hands-on, more readings, or your Week 1 assignment.*
