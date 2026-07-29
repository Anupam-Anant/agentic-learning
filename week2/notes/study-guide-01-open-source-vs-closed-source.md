# Study Guide 02·01 — Open-Source vs. Closed-Source Models in Generative AI

> **Source:** Week 2 reading PDF #1 — *"Open-Source vs. Closed-Source Models in Generative AI: What You Need to Know"* (TMLC).
> **Where it fits in the course:** Week 1 taught you *what* an LLM is and *how* to call one (OpenAI Responses API). Week 2 opens with the **first big architectural decision** every GenAI engineer makes: **which kind of model do I build on — one I download and run myself (open-source), or one I rent over an API (closed-source)?** Everything later in the course (RAG, agents, fine-tuning, deployment) sits on top of this choice.
>
> **How to read this file:** It is **self-contained** — you never need the original PDF. Each section has two blocks:
> - 📄 **`FROM THE PDF`** — the original text, cleaned up (the PDF was pasted with all spaces stripped and a repeating `TMLC` watermark + page numbers `01`–`05`; those were removed, wording preserved).
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies, why it matters, and what the PDF leaves out.
>
> New terms are **bolded and defined on first use**, then collected in the 🗂️ Jargon Dictionary at the end.

---

## 📑 Table of Contents

1. [Overview — why this decision matters](#1-overview--why-this-decision-matters)
2. [What are open-source and closed-source models?](#2-what-are-open-source-and-closed-source-models)
3. [Key difference #1 — Transparency & Customization](#3-key-difference-1--transparency--customization)
4. [Key difference #2 — Performance & Accessibility](#4-key-difference-2--performance--accessibility)
5. [Key difference #3 — Cost](#5-key-difference-3--cost)
6. [Key difference #4 — Community & Support](#6-key-difference-4--community--support)
7. [Pros and cons (comparison table)](#7-pros-and-cons-comparison-table)
8. [Which should you choose?](#8-which-should-you-choose)
9. [Use cases](#9-use-cases)
10. [Getting started with open-source models](#10-getting-started-with-open-source-models)
11. [Conclusion](#11-conclusion)
12. [⚠️ Important nuance the PDF skips: "open-weight" ≠ "open-source"](#12--important-nuance-the-pdf-skips-open-weight--open-source)
13. [🧵 Connected mental model](#13--connected-mental-model)
14. [⚡ 60-second recap](#14--60-second-recap)
15. [🗂️ Jargon Dictionary](#15--jargon-dictionary)
16. [🧠 Knowledge check](#16--knowledge-check)

---

## 1. Overview — why this decision matters

### 📄 FROM THE PDF
> Generative AI (GenAI) has transformed fields from creative writing to code generation, but choosing the right tools often boils down to one crucial decision: **open-source or closed-source models?** Whether you're just starting out or exploring advanced applications, understanding this distinction can shape your approach to AI development and deployment.

### 🧠 EXPLAINED
Before you write a single line of GenAI code, you make a fork-in-the-road decision that colors *everything* after it: cost, privacy, speed, how much you can customize, and even which libraries you'll use.

- **Open-source model** — the model's **weights** (the trained numbers that *are* the model) are published, so you can **download it and run it on your own hardware**.
- **Closed-source model** — the weights stay locked on the vendor's servers; you **rent access over an API** and never see the weights.

💻 **Java analogy:** it's the classic **"self-host an open-source library (Postgres on your own box) vs. call a managed SaaS API (a paid cloud database)"** decision.
- Self-hosting Postgres = full control, you patch/scale/secure it, no per-query bill, but *you* own the ops burden.
- Managed SaaS = it just works, someone else runs it, but you pay per use and can't touch the internals.

That exact trade-off — **control vs. convenience** — is the spine of this entire reading. Keep it in your head; every "key difference" below is just this trade-off viewed from a different angle.

> **`Model weights`** = the millions/billions of floating-point numbers learned during training. Shipping the weights = shipping the model. This is why "open-source" in GenAI almost always means "**open-weight**" — you get the *numbers*, and possibly the code, so you can run it yourself.

---

## 2. What are open-source and closed-source models?

### 📄 FROM THE PDF
> **🛠 What Are Open-Source and Closed-Source Models?**
>
> - **Open-Source Models:** These are freely accessible, allowing anyone to view, modify, and distribute the underlying code. Notable examples include **Mistral**, **LLaMA**, and **Stable Diffusion**.
> - **Closed-Source Models:** These are proprietary, meaning the code is not publicly available. They are typically offered through **APIs** or platforms, like **GPT-4** from OpenAI or **Claude** by Anthropic.

### 🧠 EXPLAINED
Two opposite distribution models:

| | Open-source | Closed-source |
|---|---|---|
| **You receive** | The weights (and often code) — you can download them | Only an API endpoint to call |
| **Where it runs** | **Your** hardware (laptop, server, cloud VM you rent) | The **vendor's** servers |
| **Can you inspect it?** | Yes — view/modify/redistribute | No — it's a **black box** |
| **Examples in the PDF** | Mistral, LLaMA, Stable Diffusion | GPT-4 (OpenAI), Claude (Anthropic) |

Meet the example models (all recur throughout the course):

- **LLaMA** — Meta's family of open-weight LLMs; the single most influential open model line, the base for thousands of fine-tunes.
- **Mistral** — a French lab shipping small, fast, genuinely-open LLMs (Apache-2.0 licensed) that punch above their size.
- **Stable Diffusion** — the landmark open **image-generation** model (a **diffusion model** — generates images by iteratively removing noise; you met this term in W1·SG02). Proof that "open-source" isn't just about text.
- **GPT-4** — OpenAI's frontier model, API-only.
- **Claude** — Anthropic's model family, API-only. *(You're literally talking to a Claude model right now.)*

> **`Proprietary`** = owned and controlled by a company; internals kept secret. Closed-source models are proprietary.
> **`Black box`** = a system you can use but can't see inside. 💻 Java analogy: calling a **closed-source vendor JAR with no source attached** — you know the method signature, not the implementation.

⚠️ **Watch the word "code."** The PDF says open-source means the *code* is available. In practice, what matters most and what actually ships is the **weights**. The training *code* and especially the **training data** are frequently **not** released even for "open" models. More on this in [§12](#12--important-nuance-the-pdf-skips-open-weight--open-source).

---

## 3. Key difference #1 — Transparency & Customization

### 📄 FROM THE PDF
> **1. Transparency and Customization**
> - **Open-Source:** Complete access to the model's code allows for deep customization and optimization. Researchers and developers can tweak the architecture or train it on **domain-specific data**.
> - **Closed-Source:** You get a polished, tested product but with limited control. Customization is usually limited to **parameter adjustments** or **prompt engineering**.

### 🧠 EXPLAINED
This is about **how far you can bend the model to your needs.**

**Open-source → you can change the model itself.** Because you hold the weights, you can:
- **Fine-tune** it (W1·N01) on your own **domain-specific data** — e.g. train LLaMA on 10 years of your company's legal contracts so it speaks "legalese."
- Modify the **architecture** (W1·SG02 — the structural design: layers and how they connect).
- Apply compression tricks you learned in W1·SG04 — **quantization** (store weights at lower precision to shrink it), **LoRA/QLoRA** (fine-tune tiny add-on weights while the base stays frozen).

**Closed-source → you can only change how you *ask*.** You don't hold the weights, so your levers are:
- **Prompt engineering** (W1·SG03) — carefully wording the `instructions`/`input`.
- **Parameter adjustments** — the request-time dials the API exposes.

> **`Parameter adjustments`** here means **inference parameters** (request-time settings like `temperature`, `top_p`, `max_output_tokens`) — *not* the model's internal weights. ⚠️ Don't confuse with **parameter** = a learned weight (W1·N01). Same word, two meanings:
> - *Training-time* parameters = the model's weights (open-source lets you retrain these).
> - *Inference-time* parameters = knobs on each API call (both open and closed expose these).
>
> 💻 **Java analogy:** open-source is having the **full source of a library** — you can fork it and rewrite a method. Closed-source is a library where you can only pass **constructor arguments and config flags**; the compiled logic is sealed. Note that many closed vendors *do* now offer **hosted fine-tuning** (you upload data, they tune a private copy server-side) — so "closed = zero customization" is a simplification; it's "customization on the vendor's leash."

---

## 4. Key difference #2 — Performance & Accessibility

### 📄 FROM THE PDF
> **2. Performance and Accessibility**
> - **Open-Source:** Performance varies widely. While top-tier models rival closed-source ones, others may need **fine-tuning** or additional resources.
> - **Closed-Source:** These models often lead in performance and user-friendliness due to significant resources invested in their development and maintenance.

### 🧠 EXPLAINED
**Open-source is a huge spectrum.** "Open-source model" ranges from a tiny 1-billion-parameter model that runs on your laptop but is only okay, up to giant models that rival the best closed ones — *if* you can supply the hardware to run them and possibly fine-tune them. **You** are responsible for making it perform: choosing the right size, tuning it, and paying for the **GPUs** (W1·SG02) it runs on.

**Closed-source usually leads on raw capability and polish** because the vendor pours enormous money into training the **frontier model** (W1·SG04 — the largest, most capable, most expensive cutting-edge models) and into the surrounding product: reliable uptime, clean SDKs, safety **guardrails** (W1·SG04), and documentation. You get that for free (well — for the subscription fee) with zero ops work.

The gap has narrowed a lot: top open models are now competitive on many tasks. But "accessibility" cuts two ways:
- Closed-source is more accessible to **use** (sign up, get an API key, call it — the W1 flow).
- Open-source is more accessible to **own/control** (no gatekeeper can rate-limit you, change the model under you, or deprecate it).

💻 **Java analogy:** a **managed cloud service** (closed) gives you a tuned, monitored, auto-scaled system out of the box. **Self-hosting** (open) can match or beat it, but only after *you* size the servers, tune the GC/config, and keep it alive at 3 a.m.

---

## 5. Key difference #3 — Cost

### 📄 FROM THE PDF
> **3. Cost Considerations**
> - **Open-Source:** Typically free to use but may involve costs related to **training infrastructure**, deployment, and scaling.
> - **Closed-Source:** Often subscription-based or **pay-per-use**, but costs include access to optimized models and ongoing support.

### 🧠 EXPLAINED
**"Free" is the most misleading word in this whole reading.** Open-source models cost **$0 in licensing**, but that is not the same as free to *operate*. This is the difference between **price** and **Total Cost of Ownership (TCO)**.

**Open-source cost = you buy the compute.**
- **Hardware / GPU rental** — running or fine-tuning a large model needs expensive **GPUs**, whether bought or rented by the hour in the cloud. This bill runs whether or not anyone is using your app.
- **Engineering time** — someone has to deploy it, scale it, monitor it, patch it. Salaries are a cost.
- **Scaling** — traffic spikes mean provisioning more machines yourself.

**Closed-source cost = you pay per use (**`pay-per-use`**).**
- Usually **billed per token** (W1: tokens are the chunks a model reads/writes) or a monthly **subscription**. You met `max_output_tokens` in W1·SG03 precisely *because* output length = money.
- **$0 fixed cost** — idle app, idle bill. You pay only for actual calls, and support/optimization is bundled in.

🧮 **The cross-over mental model (the key intuition):**
```
              ^ total cost
              |
   closed  →  |            /   (pay-per-use: rises with every call)
              |          /
              |        /
              |______/________________  ← open-source fixed floor
              |    /   (rent the GPU 24/7 whether busy or not)
              |  /
              +--------------------------> usage volume
                        ^ break-even
```
- **Low / spiky volume → closed-source is cheaper** (no idle GPU bill; pay only when used).
- **High / steady volume → open-source can win** (once you're saturating a GPU anyway, owning it beats paying per-token forever).

💻 **Java analogy:** **serverless/Lambda (pay-per-invocation) vs. a reserved EC2 instance running 24/7.** Bursty traffic → serverless. Constant heavy traffic → the always-on box you own is cheaper per request. Same economics, exactly.

---

## 6. Key difference #4 — Community & Support

### 📄 FROM THE PDF
> **4. Community and Support**
> - **Open-Source:** Backed by active developer communities. Platforms like **GitHub** host numerous projects and forums where you can seek advice or collaborate.
> - **Closed-Source:** Support is usually provided directly by the organization, offering dedicated resources but often requiring paid plans.

### 🧠 EXPLAINED
**Where do you go when it breaks?**

- **Open-source → the community.** Documentation, forums, GitHub issues, Discord servers, and thousands of other developers who hit your problem first. It's free and often *excellent* and fast — but there's **no SLA** (no contractual guarantee anyone will answer, or by when). 💻 Like leaning on **Stack Overflow + a library's GitHub issues** for a Spring problem.
- **Closed-source → the vendor.** A dedicated support channel, account managers, uptime guarantees — but typically **behind a paid support tier**. 💻 Like an **enterprise Oracle/AWS support contract**: reliable, accountable, and billed.

> **`SLA`** = Service-Level Agreement — a contractual promise about uptime/response time. Closed vendors sell them; open-source communities don't owe you one.

**Nuance:** open-source's community is also its *superpower* — the same LLaMA base gets improved by the whole world (fine-tunes, tooling, optimizations) far faster than any single company can move. The support question ("who fixes *my* outage?") and the innovation question ("who improves the model?") point in opposite directions.

---

## 7. Pros and cons (comparison table)

### 📄 FROM THE PDF
> **🌟 Pros and Cons:**
>
> | Aspect | Open-Source | Closed-Source |
> |---|---|---|
> | **Flexibility** | High — can modify and adapt freely | Low — limited to provided features |
> | **Performance** | Varies — depends on community contributions | Consistently optimized and reliable |
> | **Cost** | Potentially free but can incur hosting costs | Pay-as-you-go; includes support |
> | **Support** | Community-driven, often excellent | Professional, but sometimes expensive |
> | **Transparency** | Complete — underlying code available | Limited — black-box approach |

### 🧠 EXPLAINED
This table is the whole reading in five rows. A memory hook — read it as **one trade-off** rather than five separate facts:

> **Open-source = you take the wheel** (flexibility, transparency, privacy, control) **and the responsibility** (ops, hardware, no SLA).
> **Closed-source = you buy a chauffeur** (polish, reliability, support, zero ops) **and give up the wheel** (black box, vendor lock-in, per-use bill).

Two things the PDF's table doesn't name explicitly but you should add mentally:
- **Privacy / data control** → a *pro* for open-source (data never leaves your servers — see [§9](#9-use-cases)).
- **Vendor lock-in & model drift** → a *con* for closed-source (the vendor can change, price, deprecate, or rate-limit the model under you; you have no frozen copy).

---

## 8. Which should you choose?

### 📄 FROM THE PDF
> **🚀 Which Should You Choose?**
> - **Beginners:** Start with closed-source models through APIs like OpenAI's **GPT** or Google's **PaLM**. They're easy to use, well-documented, and provide quick results.
> - **Intermediate Users:** Explore open-source models. Try running models like **LLaMA** or **Mistral** on local machines or cloud services to understand their capabilities and limitations.

### 🧠 EXPLAINED
The PDF frames it as a **learning ladder**, and that's exactly right for you:

1. **Start closed (you already did this in Week 1).** The ticket-triage assignment called OpenAI's API — sign up, get a key, get results in minutes, zero infrastructure. This is the fastest way to learn *prompting, structured output, and system design* without drowning in ops.
2. **Then go open to understand the machine.** Once concepts are solid, run **LLaMA** or **Mistral** yourself (locally or on a rented cloud GPU) to *feel* what "hosting a model" actually costs and involves — hardware limits, load times, quantization trade-offs.

> **`PaLM`** = Google's earlier large language model family, accessed via API. *(Note: Google's current API-served line is **Gemini** — the same one this course lets you swap in via an OpenAI-compatible endpoint. PaLM is its predecessor; the PDF is slightly dated here.)*

💡 **Real-world decision rule (beyond beginner/intermediate):** the choice is rarely about skill level — it's about **constraints**. Ask: *Is my data sensitive? Is my volume high and steady? Do I need to modify the model?* → lean **open**. *Do I need the best quality fast with no ops, at low/spiky volume?* → lean **closed**. Many production systems use **both** (closed for hard reasoning, a cheap open model for bulk/simple calls).

---

## 9. Use cases

### 📄 FROM THE PDF
> **💡 Use Cases:**
> - **Prototyping and Quick Demos:** Closed-source models often provide faster, more reliable results with minimal setup.
> - **Research and Innovation:** Open-source models allow deeper exploration, custom training, and experimentation with new architectures or data.
> - **Privacy and Compliance:** Open-source models can be deployed on **private servers**, ensuring full control over data — a crucial factor for sensitive industries.

### 🧠 EXPLAINED
Map each use case to the trade-off from [§1](#1-overview--why-this-decision-matters):

| Use case | Winner | Why |
|---|---|---|
| **Prototype / demo** | **Closed** | Speed-to-first-result beats everything; you want an answer today, not a GPU cluster. |
| **Research / innovation** | **Open** | You need to open the hood — modify architecture, train on novel data, publish reproducible results. |
| **Privacy / compliance** | **Open** | Data **never leaves your servers**. |

The **privacy** row is the one to burn into memory, because it's often a hard, non-negotiable **compliance** wall:

- With **closed-source**, your prompt (and thus your data) is **sent to the vendor's servers** to be processed. For a hospital, bank, or anyone under **GDPR** (W1·SG04) or HIPAA, that can be legally forbidden.
- With **open-source self-hosted on private servers**, the data stays inside your walls end-to-end. This single factor overrides cost and convenience for regulated industries.

> **`Self-hosting` / on-premise (on-prem) deployment** = running the model on servers *you* control (your data center or your private cloud), so no third party ever sees the inputs. This is the concrete mechanism behind the "privacy" advantage. 💻 Java analogy: keeping a database **inside your own VPC/on-prem** for compliance instead of sending records to a third-party SaaS.

> **`Compliance`** = obeying legal/regulatory rules about data (GDPR, HIPAA, etc.). Often the *deciding* factor, not a tie-breaker.

---

## 10. Getting started with open-source models

### 📄 FROM THE PDF
> **🔗 Getting Started with Open-Source Models:**
> 1. **Platforms to Explore:**
>    - **Hugging Face** 🤗 (hosts numerous pre-trained models)
>    - **GitHub** repositories (for active projects like LLaMA)
> 2. **Key Tools:**
>    - **LangChain** and **LlamaIndex** for building applications with GenAI
>    - **Transformers** library from Hugging Face for model fine-tuning

### 🧠 EXPLAINED
Your starter toolbox for the open-source world:

- **Hugging Face** 🤗 — the "GitHub of models." A **model hub/marketplace** (W1·SG02) hosting hundreds of thousands of downloadable **pre-trained models** (W1·SG02), plus datasets and demos. This is where you *find and download* open weights. 💻 Think **Maven Central, but for AI models**.
- **GitHub** — hosts the *code* and active projects (like LLaMA's repo, tooling, fine-tuning scripts).
- **Transformers library** (from Hugging Face) — the Python library that actually **loads and runs** a model's weights (and helps you **fine-tune** them). It's the workhorse that turns downloaded files into a callable model. 💻 Like the **JDBC driver + ORM** layer that turns a database into objects you can call.
- **LangChain** & **LlamaIndex** — higher-level **application frameworks** for *building things* with LLMs (open or closed): chaining calls, connecting to data, giving models tools and memory. You'll meet these properly later in the course; for now, know they sit **above** a raw model and orchestrate it. 💻 Think **Spring** for GenAI apps — the framework wiring your components together, not the model itself.

> **`Hugging Face`** = the dominant hub for finding, downloading, and sharing open models/datasets (`huggingface.co`).
> **`Transformers` (library)** = Hugging Face's Python library to load, run, and fine-tune models. ⚠️ Don't confuse the **Transformers *library*** (software) with the **Transformer *architecture*** (W1·N01, the 2017 design). The library is *named after* the architecture.
> **`LangChain` / `LlamaIndex`** = frameworks for building LLM-powered applications (orchestration, data connections, tools/memory). They wrap a model; they are not a model.

*(Not in the PDF, but worth knowing: **Ollama** and **LM Studio** are popular tools for running open models locally with almost no setup — great for your "intermediate" step in [§8](#8-which-should-you-choose).)*

---

## 11. Conclusion

### 📄 FROM THE PDF
> **🤔 Conclusion: Which Path Fits Your Journey?**
> The choice between open and closed models depends on your goals:
> - **Need something that just works?** Closed-source APIs are the way to go.
> - **Want full control and flexibility?** Dive into the open-source ecosystem.
>
> Both paths offer rich opportunities for learning and innovation. Happy coding! 🚀

### 🧠 EXPLAINED
There is **no universal winner** — there's a winner *for your constraints*. The PDF's closing line is the takeaway: **"just works" → closed; "full control" → open.** In real systems the honest answer is often **"both,"** routed by the job (recall the ticket-triage assignment already lets you swap OpenAI ⇄ Groq/Gemini via one env var — that swappability *is* this chapter made concrete: your code stays the same; the model behind it can be closed or open).

---

## 12. ⚠️ Important nuance the PDF skips: "open-weight" ≠ "open-source"

This is the one place the PDF oversimplifies, and it matters for real decisions and interviews.

The PDF says open-source means "view, modify, and distribute the **code**." Strictly, **true open-source** (as software people mean it — an OSI-approved license) would require the **training code AND the training data AND the weights**, all under a permissive license. Almost no famous "open" LLM meets that bar. What you actually get is usually just the **weights**, under a custom license — this is more precisely called **open-weight**.

| Term | What's released | Example | Catch |
|---|---|---|---|
| **Fully open-source** | Weights + training code + data, permissive license | Some Mistral models (Apache-2.0), OLMo, some others | Rare |
| **Open-weight** | Weights only, often a **restricted** license | **LLaMA** (Meta's community license restricts some commercial use; training data not released) | You can run/tune it, but you can't fully reproduce or always use it commercially without conditions |
| **Closed** | Nothing — API only | GPT-4, Claude | Black box |

**Why you must care:**
- **Licensing risk** — an "open" model may forbid your commercial use case. Always read the license.
- **Reproducibility** — without training data/code you can't fully audit *how* it was built (bias, contamination).
- **Interview gold** — saying *"LLaMA is open-weight, not strictly open-source"* signals real understanding.

The W1·SG02 glossary entry already hinted at this by pairing the terms: **"Open-source / open-weight."** Now you know why they're paired — and where they differ.

---

## 13. 🧵 Connected mental model

How this reading plugs into what you already know and what's coming:

```
        WEEK 1 (what & how)                    WEEK 2 starts here
   ┌───────────────────────────┐        ┌──────────────────────────────┐
   │ Tokens → Transformer →     │        │  THE DELIVERY DECISION:        │
   │ Pretraining → LLM →        │───────▶│  Open-source ┄┄┄ Closed-source │
   │ Fine-tuning → API call     │        │  (own it)         (rent it)    │
   └───────────────────────────┘        └───────────────┬──────────────┘
                                                         │  drives ↓
                                    ┌────────────────────┼─────────────────────┐
                                    ▼                     ▼                     ▼
                              CUSTOMIZATION           COST MODEL            PRIVACY
                          (fine-tune / prompt)    (fixed GPU / per-token)  (on-prem / vendor)
                                    │                     │                     │
                                    └──────────── all feed later topics ────────┘
                                                         ▼
                        RAG · Agents · Fine-tuning · Deployment  (rest of course)
```

**One-line thread:** `LLM (W1) → choose delivery: open vs closed (W2·SG01) → that choice sets your customization, cost, and privacy → which shapes how you build RAG/agents/fine-tunes later.`

The Week 1 model-selection guide (W1·SG04) chose *which* model on quality/benchmarks; this reading chooses *how you get* the model. **Both decisions happen together in real projects.**

---

## 14. ⚡ 60-second recap

- **The decision:** open-source (download & run the **weights** yourself) vs. closed-source (**rent** via API). It's the **control-vs-convenience** trade-off — the SaaS-vs-self-host choice, applied to models.
- **Transparency/customization:** open = change the *model* (fine-tune, edit architecture); closed = change only your *prompt/params*.
- **Performance:** closed usually leads on polish & top-end quality with zero ops; open ranges from tiny to frontier-rivaling, but *you* must make it perform.
- **Cost:** open is $0 license but **you buy the GPUs/ops** (fixed floor); closed is **pay-per-use** (idle = $0). Low/spiky volume → closed cheaper; high/steady → open can win.
- **Support:** open = community (great, no SLA); closed = paid vendor support (accountable, costs money).
- **Privacy/compliance** is the tiebreaker-that-isn't: sensitive data → **open, self-hosted on-prem** so data never leaves.
- **Ladder:** beginners start closed (fast, no ops); then run **LLaMA/Mistral** open to learn the machine.
- **Tools:** find models on **Hugging Face**; run/tune with **Transformers**; build apps with **LangChain/LlamaIndex**.
- **The nuance:** most "open" LLMs are **open-weight** (weights only, licensed), not strictly open-source (weights + code + data).

---

## 15. 🗂️ Jargon Dictionary

*(New terms introduced in this reading. Terms already defined in Week 1 — Transformer, fine-tuning, quantization, LoRA/QLoRA, GPU, guardrails, GDPR, diffusion model, architecture, frontier model, model hub, pre-trained model, prompt engineering — are reused here but not repeated.)*

| Term | Definition |
|---|---|
| **Open-source model** | A model whose weights (and often code) are published so anyone can download, run, modify, and redistribute it — you host it yourself. |
| **Closed-source model** | A proprietary model whose weights stay on the vendor's servers; you access it only via API. |
| **Proprietary** | Owned and controlled by a company, with internals kept secret (closed-source models are proprietary). |
| **Model weights** | The billions of learned numbers that *are* the trained model; shipping the weights = shipping the model. |
| **Open-weight model** | A model where only the **weights** are released (often under a restricted license) — the common real meaning of "open-source LLM"; distinct from fully open-source (weights + training code + data). |
| **Black box** | A system you can use but can't inspect the internals of (closed-source models). |
| **Inference parameters (parameter adjustments)** | Request-time dials (`temperature`, `top_p`, `max_output_tokens`) that shape output — *not* the model's internal weights. |
| **Total Cost of Ownership (TCO)** | The full cost of running something (hardware + engineering + scaling + ops), not just its licence price — key to the open-source "free ≠ free" trap. |
| **Pay-per-use / pay-as-you-go** | Billing model where you're charged per API call / per token, with no fixed idle cost (closed-source pricing). |
| **Self-hosting / on-premise (on-prem)** | Running a model on servers you control, so inputs never leave your environment — the mechanism behind open-source's privacy advantage. |
| **Compliance** | Obeying legal/regulatory rules about data (GDPR, HIPAA, etc.); often the deciding factor for open vs closed. |
| **SLA (Service-Level Agreement)** | A contractual guarantee about uptime/response time; sold by closed vendors, absent from open-source communities. |
| **Vendor lock-in** | Dependence on one provider whose model you can't freeze or move; a risk of closed-source. |
| **LLaMA** | Meta's influential family of open-weight LLMs; base for thousands of fine-tunes. |
| **Mistral** | A French lab's family of small, fast, genuinely-open (Apache-2.0) LLMs. |
| **Stable Diffusion** | The landmark open-source image-generation (diffusion) model. |
| **GPT-4** | OpenAI's frontier closed-source LLM, accessed via API. |
| **Claude** | Anthropic's family of closed-source LLMs, accessed via API. |
| **PaLM** | Google's earlier API-served LLM family (predecessor to Gemini). |
| **Hugging Face** | The dominant hub for finding, downloading, and sharing open models and datasets ("GitHub of models"). |
| **Transformers (library)** | Hugging Face's Python library to load, run, and fine-tune models — distinct from the Transformer *architecture*. |
| **LangChain** | A framework for building LLM applications (chaining calls, data, tools, memory) — wraps a model, isn't one. |
| **LlamaIndex** | A framework for connecting LLMs to your data (indexing/retrieval) to build data-aware apps. |

---

## 16. 🧠 Knowledge check

Answer these in your own words — reply with your answers and I'll grade them, explaining any mistakes rather than just giving the solution.

**Conceptual**
1. In one sentence each, define *open-source* and *closed-source* models, and name the single trade-off that underlies every difference between them.
2. The reading calls open-source models "typically free to use." Why is that misleading? What real costs replace the licence fee?
3. Explain the difference between the two meanings of "parameter" in this reading (weights vs. inference parameters). Which one can *only* open-source models change?

**Applied**
4. A startup is building a quick demo to pitch investors next week, with almost no infrastructure budget and low traffic. Open or closed? Justify using at least two of the four key differences.
5. A hospital wants an LLM to summarize patient records. Patient data legally cannot leave their premises. Which path, and what specific mechanism makes it possible?
6. At roughly what point does self-hosting an open model become *cheaper* than a pay-per-use API? Sketch the cost intuition.

**Interview-style**
7. An interviewer says: *"LLaMA is open-source, right?"* Give the more precise answer and explain the distinction.
8. Your team already ships on OpenAI's API. Give one concrete reason you might *add* a self-hosted open model rather than replace, and one risk of staying purely closed-source.

---

*End of Study Guide 02·01. Next Week 2 reading → paste it and I'll build Study Guide 02·02, extending the glossary and this mental model.*
