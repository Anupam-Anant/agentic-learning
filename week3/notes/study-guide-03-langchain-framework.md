# Study Guide 03·03 — LangChain: A Framework for Language AI

> **Source:** Week 3 reading PDF #3 — *"LangChain: A Powerful Framework for Language AI"* (TMLC), plus three companion Colab notebooks (setup + simple chain · complex chain · LCEL).
> **Where it fits in the course:** This is the **"now you build it" reading.** Weeks 1–3 gave you the *parts* — LLMs and the API (W1), prompting (W2·SG02), embeddings + vector DBs + the RAG pattern (W3·SG01–02). **LangChain is the framework that wires those parts into an actual application.** If SG01 was the *blueprint* of a RAG system and SG02 was the *storage engine*, this is the *construction toolkit*. It's also the direct on-ramp to **agents** (the next big topic), because agents are built on exactly these primitives.
>
> **How to read this file:** Self-contained — you never need the original PDF. Each section pairs:
> - 📄 **`FROM THE PDF`** — original text, cleaned (spaces were stripped in the paste; the `TMLC` watermark, page-breaks, and an "Automatic Zoom" scroll artifact were removed; wording preserved).
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies and the "why."
>
> ✅ **On the code notebooks:** the three companion notebooks are now captured as runnable, local-friendly scripts in `week3/code/` — `langchain_simple_chain_demo.py`, `langchain_sequential_chain_demo.py`, `langchain_lcel_demo.py` (+ a shared `langchain_model.py`). They're walked through in [§7](#7-a-worked-mental-walkthrough-simple--complex--lcel).
>
> New terms are **bolded and defined on first use**, then collected in the 🗂️ Jargon Dictionary.

---

## 📑 Table of Contents

1. [What LangChain is (and the problem it solves)](#1-what-langchain-is-and-the-problem-it-solves)
2. [The three pillars: chains, integration, extensibility](#2-the-three-pillars-chains-integration-extensibility)
3. [Why use LangChain?](#3-why-use-langchain)
4. [Other frameworks (and when to pick which)](#4-other-frameworks-and-when-to-pick-which)
5. [Core concepts: Chains · Models · Prompts · Memory](#5-core-concepts-chains--models--prompts--memory)
6. [LCEL — the modern way to build chains](#6-lcel--the-modern-way-to-build-chains)
7. [A worked mental walkthrough: simple → complex → LCEL](#7-a-worked-mental-walkthrough-simple--complex--lcel)
8. [How LangChain builds the RAG from SG01/SG02](#8-how-langchain-builds-the-rag-from-sg01sg02)
9. [Deep dives beyond the PDF](#9-deep-dives-beyond-the-pdf)
10. [🧵 Connected mental model](#10--connected-mental-model)
11. [⚡ 60-second recap](#11--60-second-recap)
12. [🗂️ Jargon Dictionary](#12--jargon-dictionary)
13. [🧠 Knowledge check](#13--knowledge-check)

---

## 1. What LangChain is (and the problem it solves)

### 📄 FROM THE PDF
> **What is LangChain?**
> LangChain is a framework that simplifies working with LLMs by providing a structured and modular way to build complex language AI applications.

### 🧠 EXPLAINED
**LangChain** is a **framework** — a reusable scaffold with conventions and building blocks — for building applications *around* LLMs. It is **not** a model; it doesn't do the "thinking." It's the **plumbing and orchestration layer** that sits between your code and one-or-more LLMs, data sources, and tools, and makes them work together cleanly.

> 🔑 **Framework** = a pre-built structure that calls *your* code within *its* conventions (inversion of control), as opposed to a *library* you call. 💻 You know this exactly: **Spring** is a framework, `commons-lang` is a library. LangChain is "**Spring for LLM apps**."
> 🔑 **Orchestration** = coordinating multiple steps/components into one flow. 💻 Think of a service method that calls the DB, transforms the result, hits an external API, and formats a response — LangChain orchestrates the LLM equivalent of that.

**The problem it solves — why not just call the OpenAI API directly?** You already did that in W1, and for a single call it's fine. The pain shows up when a *real* app needs more than one call glued to other systems. Consider a "chat with your PDFs" feature — end to end it must:

1. Take the user's question,
2. Embed it, hit a **vector DB**, get top-K chunks (SG01/SG02),
3. Stuff those chunks into a **prompt template**,
4. Call the LLM,
5. Parse the LLM's output into a clean structure,
6. Remember the conversation so far (**memory**),
7. …and ideally swap OpenAI→Anthropic without a rewrite.

Hand-rolling all that means a tangle of string-formatting, HTTP calls, JSON parsing, provider-specific SDKs, and glue. **LangChain gives each of those steps a standard, swappable component and a clean way to connect them** — so you assemble an app from parts instead of hand-wiring every wire.

💻 **The anchor analogy — LangChain : LLM apps :: Spring : web apps.** Before Spring, a Java web app was servlets + manual JDBC + hand-managed transactions + boilerplate. Spring gave you *abstractions* (repositories, `RestTemplate`, DI) and *conventions* so you compose an app from standard beans. LangChain does the identical thing for the LLM world: standard abstractions for **models, prompts, chains, memory, retrievers, tools**, so you stop writing glue and start composing. Same instinct, new domain.

⚠️ **The honest caveat (worth knowing up front):** LangChain is powerful but has a reputation for *heavy abstraction* — sometimes it's simpler to call the API directly. The skill is knowing *when* the orchestration earns its keep (multi-step, multi-tool, memory, provider-swapping) vs when it's overkill (one prompt in, one string out). We'll flag this again in [§9](#9-deep-dives-beyond-the-pdf).

---

## 2. The three pillars: chains, integration, extensibility

### 📄 FROM THE PDF
> - **Chain-Based Design:** Chains are modular units that orchestrate the interaction of LLMs, data sources, and other tools.
> - **Integration with LLMs:** LangChain supports a wide range of LLMs, including OpenAI's GPT-3, Hugging Face models, and others.
> - **Extensibility:** LangChain is designed for customization and can be extended to include custom models, tools, and data sources.

### 🧠 EXPLAINED
These three describe *how* LangChain is architected. Take them one at a time:

**① Chain-Based Design.** The core metaphor. A **chain** is a sequence of steps where each step's output feeds the next — LLM calls, data lookups, transformations, tool calls — composed into one runnable unit.
> 🔑 **Chain** = a composable pipeline of steps (prompt → model → parse → …) treated as a single callable. 💻 Three analogies you already own: a **Servlet filter chain** (each filter processes then passes on), a **Java Stream pipeline** (`.map().filter().collect()`), and **Unix pipes** (`grep | sort | uniq`). A LangChain chain is that, with LLM steps in the pipe.

**② Integration with LLMs.** LangChain wraps *many* providers behind *one* interface. Swap OpenAI ↔ Hugging Face ↔ Anthropic ↔ local models by changing a line, not rewriting your app.
> 💻 **This is the JDBC pattern.** JDBC gives you one `Connection`/`Statement` API and hides whether it's Postgres or MySQL underneath. LangChain's model interface hides whether it's GPT, Claude, or a local Llama. You met this idea in W1 ("provider-swappable via env var") — LangChain makes it a first-class abstraction. *(Note: the PDF says "GPT-3" because it's a bit dated; today it's GPT-4o/Claude/Gemini/etc. — the pattern is unchanged.)*

**③ Extensibility.** Every piece is an interface you can implement. Custom model? Custom tool? Custom data source? Plug it in and it composes with everything else.
> 💻 **This is Spring's `@Bean` / SPI ecosystem.** You can drop in your own implementation of an interface and the framework treats it like any built-in. Extensibility is what lets the community ship hundreds of integrations (every vector DB, every API) that "just work" in a chain.

**The through-line:** *chains* are the composition model, *integration* is the breadth of parts, *extensibility* is your ability to add new parts. Together they make LangChain a **Lego kit**: standard studs (interfaces) mean any brick snaps to any other.

---

## 3. Why use LangChain?

### 📄 FROM THE PDF
> LangChain offers several advantages that make it a popular choice for developers working with LLMs.
> - **Simplified Development:** LangChain provides a high-level abstraction, making it easier to build and maintain complex LLM-based applications.
> - **Modular Design:** The modular architecture of LangChain allows you to easily combine different components and customize your application to suit specific needs.
> - **Enhanced Capabilities:** LangChain offers features like **memory**, **data augmentation**, and **tool integration**, enabling you to create advanced language AI applications.

### 🧠 EXPLAINED
The first two (simplified, modular) are the Spring-analogy benefits from §1–2. The **third is the one that actually sells LangChain** — it names three superpowers a bare LLM API doesn't give you:

- **Memory** — an LLM API call is **stateless**: it forgets everything between calls (you met this in W1 — you had to resend history or thread `previous_response_id`). **Memory** components store conversation/state and auto-inject it into the next prompt, so your bot *remembers*. 💻 It's **`HttpSession` for a stateless protocol** — the same problem HTTP has, the same fix. (Full treatment in [§5](#5-core-concepts-chains--models--prompts--memory).)
> 🔑 **Memory** = a component that persists information across interactions and feeds it back into later prompts, making the app context-aware.

- **Data augmentation** — connecting the LLM to *external data* at runtime so it answers from *your* documents, not just its frozen training. **This is literally RAG** (SG01) — and LangChain is *the* toolkit people use to build it (retrievers, document loaders, vector-store integrations). See [§8](#8-how-langchain-builds-the-rag-from-sg01sg02).
> 🔑 **Data augmentation** = enriching the model's input with retrieved external data (the "Augmented" in Retrieval-**Augmented** Generation).

- **Tool integration** — letting the LLM *use tools*: call a calculator, run a search, hit an API, query a DB. The model decides *"I need to look this up"* and the framework runs the tool and feeds the result back. 💻 Like giving your service a set of injected clients it can call on demand. **This is the seed of agents** — a model that picks and runs tools in a loop.
> 🔑 **Tool** = a function/capability (search, calculator, API call, DB query) the LLM can invoke to act on the world or fetch live facts.

**Why this matters:** bare LLM = *a brain in a jar* (fluent, but stateless, cut off from your data, unable to act). LangChain's three superpowers give it **a memory, a library card, and hands.** That's the leap from "text generator" to "application."

---

## 4. Other frameworks (and when to pick which)

### 📄 FROM THE PDF
> Other frameworks: **LlamaIndex, FlowiseAI, CrewAI**

### 🧠 EXPLAINED
LangChain isn't the only game. The PDF name-drops three; here's what each actually is, plus **LangGraph** (LangChain's own agent framework, which you'll meet soon) — because knowing the landscape is an interview favorite:

| Framework | What it's best at | 💻 Analogy | Pick it when… |
|---|---|---|---|
| **LangChain** | General-purpose orchestration of LLM apps | **Spring** (broad framework) | You're composing multi-step LLM+data+tool flows |
| **LlamaIndex** | **RAG / data indexing** specialist — ingesting, chunking, indexing, retrieving over your data | A **specialized ORM/search library** | Your app is *heavily* about retrieval over lots of documents |
| **CrewAI** | **Multi-agent** orchestration — multiple role-playing agents collaborating | A **team of workers** with an org chart | You want several agents (researcher, writer, critic) cooperating |
| **FlowiseAI** | **Low-code/visual** builder — drag-and-drop LangChain flows in a UI | **Node-RED / a visual workflow tool** | You want to prototype without writing much code |
| **LangGraph** | **Stateful, cyclic** agent workflows (graphs, loops, branches) built on LangChain | A **state machine / BPMN engine** | Your agent needs loops, branching, human-in-the-loop |

**How to hold it in your head:** **LangChain** = the general toolkit; **LlamaIndex** = go-deep-on-RAG; **CrewAI** = multi-agent teams; **FlowiseAI** = visual/no-code; **LangGraph** = complex stateful agents. They overlap and often interoperate (LangChain + LlamaIndex retrievers together is common). No single "winner" — they're different tools for different shapes of problem.

---

## 5. Core concepts: Chains · Models · Prompts · Memory

### 📄 FROM THE PDF
> LangChain is built around several core concepts that form the foundation of its architecture.
> - **Chains:** Chains are the fundamental building blocks of LangChain applications. They define the flow of data and interactions between different components.
> - **Models:** Models are the LLMs that provide the intelligence for LangChain applications. They can be used for text generation, translation, question answering, and more.
> - **Prompts:** Prompts are the instructions you provide to the LLMs. They specify the task you want the model to perform.
> - **Memory:** Memory allows chains to store and retrieve information from previous interactions, enabling more context-aware and personalized responses.

### 🧠 EXPLAINED
These four are the vocabulary of every LangChain app. Here's each with the concrete component + Java framing:

**🔗 Chains — the flow.** The pipeline that connects everything (§2①). The *simplest* useful chain is **`prompt → model → output parser`**: fill a template, call the model, parse the reply. Complex chains branch, loop, and call other chains. 💻 A chain is your **service-orchestration method**, but declarative and composable.

**🧠 Models — the intelligence.** The LLM(s). Important nuance the PDF glosses: LangChain splits models into **types**:
> 🔑 **LLM (text model)** = string in → string out. 🔑 **Chat model** = a list of role-tagged **messages** in (system/user/assistant, from W1) → a message out. **Chat models are the modern default.** 🔑 **Embedding model** = text in → vector out (W2·SG03) — the retriever's engine. Same three you've already met, now as LangChain interfaces you can swap.

**📝 Prompts — the instructions.** Rarely a raw string; usually a **`PromptTemplate`** — a parameterized template with `{placeholders}` you fill at runtime.
> 🔑 **PromptTemplate** = a reusable prompt with typed variables, e.g. `"Translate '{text}' to {language}."` 💻 **Exactly a `PreparedStatement` / `MessageFormat`** — a template with bind-parameters, not string-concatenation. Same benefits: reuse, clarity, and you don't hand-mangle strings. (It does *not* protect against "prompt injection" the way `PreparedStatement` stops SQL injection — that's a separate concern.)

**💾 Memory — the state.** Stores prior turns and injects them into the next prompt so the chain is **context-aware** across a conversation.
> Types you'll meet: **buffer memory** (keep the last N turns verbatim), **summary memory** (keep an LLM-written running summary to save tokens). 💻 **`HttpSession` for your bot** — the mechanism that turns a series of stateless calls into a coherent conversation. Without it, every message starts from amnesia.

**How the four snap together** (the mental picture):
```
   user input
      │
      ▼
   [ PROMPT template ] ← fills in {vars} (+ injects MEMORY of past turns)
      │
      ▼
   [ MODEL ] ← the LLM does the work
      │
      ▼
   [ output parser ]        ─────────►  answer
      │                                    │
      └────────── all wired by a CHAIN ────┘   (and the turn is saved back to MEMORY)
```

---

## 6. LCEL — the modern way to build chains

> *(Not in the PDF's text, but it's the subject of one of the three companion notebooks and the standard way chains are written today — you can't skip it.)*

**LCEL (LangChain Expression Language)** is LangChain's syntax for composing chains with the **pipe operator `|`**. Instead of nesting components or using older `*Chain` classes, you *pipe* one component into the next:

```python
chain = prompt | model | output_parser
result = chain.invoke({"text": "Bonjour", "language": "English"})
```

Read that `|` exactly like a **Unix pipe** or **function composition**: *"take the input, run it through `prompt`, pipe the result into `model`, pipe that into `output_parser`."*

> 🔑 **LCEL** = the `|`-based declarative syntax for building chains from **Runnables**.
> 🔑 **Runnable** = LangChain's universal interface for "a thing you can call." Every component (prompt, model, parser, retriever, even a plain function) is a Runnable, so they all share methods — `.invoke()` (one input), `.batch()` (many), `.stream()` (token-by-token), and async variants — and any Runnable can pipe into any other.
> 🔑 **Pipe operator `|`** = composes two Runnables left-to-right; the left's output becomes the right's input. 💻 Python's `|` is overloaded here just like you'd overload an operator in Java — it's syntactic sugar for `compose(a, b)`.

💻 **The Java analogy that makes LCEL click:** it's **`Function.andThen()` / Stream chaining.** In Java you write `f.andThen(g).andThen(h)` or `stream.map(f).map(g)`; LCEL writes `f | g | h`. Both are **function composition** — small, testable units snapped into a pipeline. And because *everything* is a Runnable (one interface), composition *always* type-checks structurally — the same reason Java Streams compose so freely.

**Why LCEL won** (over the older `LLMChain`/`SequentialChain` classes):
- **Streaming, batching, async — for free.** Build with `.invoke()`, and `.stream()`/`.batch()`/`ainvoke()` work automatically because every Runnable implements them.
- **Readable.** `prompt | model | parser` *is* the data flow, left to right.
- **Composable & swappable.** Swap any stage without touching the others (the modular promise, realized).

⚠️ **Version note:** LangChain moved from legacy chain classes (`LLMChain`, `SequentialChain`) to **LCEL** as the recommended style. Tutorials vary by age — if you see `LLMChain(llm=..., prompt=...)`, that's the older way; `prompt | model` is current. Both still run; prefer LCEL.

---

## 7. A worked mental walkthrough: simple → complex → LCEL

The three companion notebooks build up in difficulty. Runnable, annotated versions are in `week3/code/` (see file names below); here's the *shape* and the lesson of each.

**① Simple chain** — one template, one model call (`langchain_simple_chain_demo.py`).
The notebook builds `"Tell me a {adjective} joke"` using the **deprecated** `LLMChain` class — and running it literally prints:
> *`LangChainDeprecationWarning: The class LLMChain was deprecated … Use `prompt | llm` instead.`*
**That warning is the lesson.** The demo shows both side by side:
```python
# (A) the notebook's deprecated way — returns a dict, you dig out response['text']
chain = LLMChain(llm=model, prompt=prompt); chain.invoke("funny")["text"]
# (B) the modern LCEL way — returns the value directly, + batch/stream/async for free
chain = prompt | model | StrOutputParser(); chain.invoke({"adjective": "funny"})
```
*One prompt in, one string out.* This is the "hello world" — and the case where LangChain is arguably *optional* (§1 caveat).

**② Sequential chain** — one step's output feeds the next (**prompt chaining** from W2·SG02, as code; `langchain_sequential_chain_demo.py`):
```python
# step 1: outline a topic → step 2: expand the outline
outline_chain = outline_prompt | model | StrOutputParser()
expand_chain  = expand_prompt  | model | StrOutputParser()
chain = {"outline": outline_chain} | expand_chain   # step 2 consumes step 1's output
```
> ⚠️ **Two things the original notebook actually shows** (worth knowing): it ran a **local Mistral-7B in 4-bit quantization on a GPU** via `HuggingFacePipeline` (proof that LangChain wraps *local* models, not just APIs — but not Mac-runnable), and despite the "Sequential Chain" title the code was a *single* call whose **base-model output looped** ("…convert light energy into chemical energy." repeated) — a textbook sign of a **base (non-instruction-tuned) model** at low temperature. Our demo uses the swappable chat model and builds a *genuine* 2-step chain.

**③ LCEL fan-out/fan-in** — the mechanics of §6 (`langchain_lcel_demo.py`):
```python
# two models answer the SAME question (fan-out, parallel) → a third merges them (fan-in)
combined = {"question": RunnablePassthrough(), "answer1": chain1, "answer2": chain2} | chain3
```
This teaches the pieces that make LCEL more than straight lines: a **dict of Runnables** (fan-out, run in parallel), **`RunnablePassthrough`** (forward the raw input untouched), and **`.assign()`** (add computed keys as data flows). The notebook's own note nails the trade-off: *"LCEL … is easy for simple chains, but it can get confusing once we add complexity."*

> **The learning arc:** *simple* proves the pattern (and shows the LLMChain→LCEL shift), *sequential* shows why orchestration helps, *LCEL fan-out/fan-in* gives you the grammar for non-linear topologies. Same "one call → multi-step → composable" progression as the whole course.

---

## 8. How LangChain builds the RAG from SG01/SG02

This is the section that ties Week 3 together — **LangChain is how the RAG blueprint from SG01 actually gets built.** Map each RAG step to its LangChain component:

| RAG step (SG01) | LangChain component | What it does |
|---|---|---|
| Load your docs | **Document loader** | Read PDFs/HTML/CSV/Notion/… into a standard `Document` object |
| Chunk them | **Text splitter** | The chunking from SG01·§7.1 (size + overlap) |
| Embed + store | **Embeddings + VectorStore** | Wrap SBERT/OpenAI + Chroma/FAISS/Pinecone (SG02) behind one interface |
| Retrieve top-K | **Retriever** | The SG01 retriever — `.invoke(query)` → relevant chunks |
| Augment + generate | **Prompt \| Model** | Stuff chunks into a template, call the LLM |

As an LCEL chain, a minimal RAG is almost pseudocode:
```python
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}  # retrieve + pass the question
    | rag_prompt                                               # augment: chunks + question
    | model                                                    # generate
    | StrOutputParser()                                        # clean text out
)
rag_chain.invoke("What's our refund policy?")
```
Read it top-to-bottom and it's **literally the SG01 diagram**: retrieve → augment → generate. *That's* the "data augmentation" superpower from §3 — and why LangChain and RAG are almost always taught together. **Everything you learned in SG01–02 is the theory; this chain is the practice.**

> 🔑 **VectorStore / Retriever (LangChain)** = the framework's wrapper over a vector DB (SG02) that exposes `.as_retriever()` → a Runnable you can pipe into a chain. It's the seam where Week 3's storage engine plugs into the app.

---

## 9. Deep dives beyond the PDF

### 9.1 The ecosystem (the names you'll keep seeing)
LangChain is more than the core library:
- **`langchain-core`** — the base abstractions (Runnable, prompts, messages). **LangChain Expression Language lives here.**
- **`langchain-openai` / `langchain-anthropic` / `langchain-community`** — provider integrations, split into separate packages (so you install only what you use).
- **LangSmith** — observability/debugging/eval platform: trace every step of a chain, see the exact prompts sent and tokens used. 💻 **APM / distributed tracing (think Datadog) for your LLM app** — indispensable once chains get deep.
- **LangGraph** — stateful, cyclic agent workflows (from §4).
- **LangServe** — deploy a chain as a REST API in a few lines. 💻 **Spring Boot's embedded server for a chain.**

### 9.2 When *not* to use LangChain
The honest engineering judgment (interviewers probe this):
- **One prompt, one response, one provider?** Call the SDK directly — LangChain's abstraction is overhead you don't need.
- **You want full control / minimal deps?** Raw API or a thin wrapper may be cleaner.
- **Complex multi-step, multi-tool, multi-provider, with memory and retrieval?** *Now* LangChain (or a peer) earns its keep. The framework's value scales with your app's complexity.

### 9.3 Prompts here vs prompt engineering (W2·SG02)
W2·SG02 taught prompt *content* (zero-shot, few-shot, CoT). LangChain's `PromptTemplate` is prompt *plumbing* — how you parameterize, reuse, and inject variables/memory into those prompts. **Content vs delivery** — you need both.

### 9.4 "Chain" here vs "chain" in prompt chaining (W2·SG02)
Related but not identical: **prompt chaining** (W2) is the *technique* of feeding one LLM's output into the next prompt; a LangChain **chain** is the *mechanism* that implements that (and more — it also chains non-LLM steps like retrieval and parsing). LangChain is how you *operationalize* prompt chaining.

---

## 10. 🧵 Connected mental model

LangChain is the **assembly layer** that turns every prior concept into a running app:

```
   W1: LLM + API ───────────────┐
   W2: Prompts (0/few-shot, CoT)─┤
   W2·SG03: Embeddings ──────────┤        ┌──────────── L A N G C H A I N ───────────┐
   W3·SG02: Vector DB ───────────┼──wraps─►  Models · Prompts · Memory · Retrievers   │
   W3·SG01: RAG pattern ─────────┘        │  Tools ── all composed with CHAINS (LCEL) │
                                          └───────────────────┬──────────────────────┘
                                                              ▼
                                              a real app:  RAG chatbot, Q&A over docs
                                                              ▼
                                                    A G E N T S  (next: model + tools
                                                    in a loop; LangGraph / CrewAI)
```

**One-line thread:** `LLM (W1) + Prompts (W2) + Embeddings→VectorDB→RAG (W3) ──assembled by──► LangChain (chains · models · prompts · memory · tools, via LCEL) ──leads to──► Agents.`

Back-links: **models** = W1 LLMs/chat-roles + W2·SG03 embeddings; **prompts** = W2·SG02 techniques, now templated; **memory** solves W1's statelessness; **data augmentation** = SG01 RAG; **retriever/vector store** = SG02; **tools** = the seed of agents. **LCEL's `|`** = Java `Function.andThen()` / Stream pipelines.

---

## 11. ⚡ 60-second recap

- **LangChain = a framework (not a model)** for building apps *around* LLMs — the **orchestration/plumbing layer.** 💻 **"Spring for LLM apps."**
- **Problem it solves:** real apps need multi-step flows (retrieve → prompt → call → parse → remember → maybe swap providers). LangChain gives each step a **standard, swappable component** instead of hand-glued code.
- **Three pillars:** **chain-based design** (compose steps, like a Stream/filter chain), **integration** (many LLMs behind one interface — the JDBC pattern), **extensibility** (plug in custom parts — the SPI pattern).
- **Three superpowers over a bare API:** **memory** (state — `HttpSession` for your bot), **data augmentation** (= RAG), **tool integration** (the seed of agents). Bare LLM = brain in a jar; LangChain adds *memory, a library card, and hands.*
- **Four core concepts:** **Chains** (flow) · **Models** (LLM/chat/embedding) · **Prompts** (`PromptTemplate` = a `PreparedStatement`) · **Memory** (context across turns).
- **LCEL** = build chains with the **pipe `|`**: `prompt | model | parser`. Everything is a **Runnable** (shared `.invoke/.batch/.stream`), so composition is free. 💻 = Java `Function.andThen()`.
- **Other frameworks:** **LlamaIndex** (RAG specialist) · **CrewAI** (multi-agent) · **FlowiseAI** (visual/no-code) · **LangGraph** (stateful agents).
- **The payoff:** a RAG app is a ~5-line LCEL chain (`retriever → prompt → model → parser`) — SG01/SG02 theory becomes practice. Next stop: **agents.**

---

## 12. 🗂️ Jargon Dictionary

*(New this reading. Reused without redefining — from W1: LLM, chat roles/messages, GPT, API. From W2: prompt, zero/few-shot, chain-of-thought, Hugging Face, embedding. From W3·SG01–02: RAG, retriever, vector DB, chunking, top-K, FAISS/Chroma/Pinecone.)*

| Term | Definition |
|---|---|
| **LangChain** | A framework for building applications around LLMs — the orchestration layer connecting models, prompts, data, memory, and tools. |
| **Framework (vs library)** | A scaffold that calls *your* code within its conventions (inversion of control); you compose within it. LangChain ≈ Spring for LLM apps. |
| **Orchestration** | Coordinating multiple steps/components into one flow. |
| **Chain** | A composable pipeline of steps (prompt → model → parse → …) treated as one callable; the fundamental building block. |
| **LCEL (LangChain Expression Language)** | The `|`-based declarative syntax for composing chains from Runnables. |
| **Runnable** | LangChain's universal "callable" interface; every component implements it, sharing `.invoke()/.batch()/.stream()` + async. |
| **Pipe operator `\|`** | Composes two Runnables left-to-right (left's output → right's input); function composition. |
| **Model (LLM / Chat / Embedding)** | The intelligence. *LLM* = string→string; *Chat model* = messages→message (modern default); *Embedding* = text→vector. |
| **Prompt / PromptTemplate** | Instructions to the model; a template with `{variables}` filled at runtime (≈ a `PreparedStatement`). |
| **Output parser** | A component that turns the model's raw text into a clean structure (string, JSON, object). |
| **Memory** | A component that persists info across interactions and injects it into later prompts (≈ `HttpSession` for a bot). |
| **Data augmentation** | Enriching the model's input with retrieved external data — i.e. RAG. |
| **Tool** | A function the LLM can invoke (search, calculator, API, DB) to fetch facts or act; the basis of agents. |
| **Agent** | A model that chooses and runs tools in a loop to accomplish a goal (upcoming topic). |
| **Document loader** | Reads source data (PDF/HTML/CSV/…) into standard `Document` objects for a RAG pipeline. |
| **Text splitter** | Chunks documents (size + overlap) before embedding (SG01 chunking, as a component). |
| **VectorStore / Retriever (LangChain)** | Wrapper over a vector DB exposing `.as_retriever()` → a Runnable that returns relevant chunks. |
| **LlamaIndex** | A framework specialized in RAG / data indexing and retrieval. |
| **CrewAI** | A framework for multi-agent orchestration (role-playing agents collaborating). |
| **FlowiseAI** | A low-code/visual (drag-and-drop) builder for LangChain-style flows. |
| **LangGraph** | LangChain's framework for stateful, cyclic (loops/branches) agent workflows. |
| **LangSmith** | LangChain's observability/eval platform — tracing/debugging chains (≈ APM for LLM apps). |
| **LangServe** | Deploys a chain as a REST API in a few lines. |

---

## 13. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. In one sentence, what *is* LangChain — and what is it explicitly *not*? Why is "Spring for LLM apps" a fair analogy?
2. Name LangChain's three "enhanced capabilities" over a bare LLM API, and for each say what limitation of a raw LLM it fixes.
3. What is a `PromptTemplate`, and which Java construct is it most like? What does that analogy get right — and what does it *not* protect you from?

**Applied**
4. Rewrite this in LCEL and explain what `|` does at each step: "fill a translation prompt, call the model, return plain text."
5. Map the five RAG steps from SG01 onto their LangChain components. Which component is the seam where SG02's vector DB plugs in?
6. You're asked to build (a) a one-off "summarize this text" script, and (b) a multi-tool research assistant with conversation memory. For each, would you reach for LangChain or the raw API — and why?

**Interview-style**
7. A teammate says "LCEL is just fancy syntax — why not use the old `LLMChain` class?" Give two concrete things LCEL/Runnables give you "for free."
8. Distinguish "prompt chaining" (W2·SG02) from a LangChain "chain." How does the framework operationalize the technique?

---

*End of Study Guide 03·03. Runnable companions in `week3/code/`: `langchain_simple_chain_demo.py` · `langchain_sequential_chain_demo.py` · `langchain_lcel_demo.py` (+ shared `langchain_model.py`). Next Week 3 reading → paste it and I'll build Study Guide 03·04, extending the glossary and this mental model.*
