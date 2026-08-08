# Study Guide 03·01 — Retrieval Augmented Generation (RAG)

> **Source:** Week 3 reading PDF #1 — *"Retrieval Augmented Generation (RAG)"* (TMLC).
> **Where it fits in the course:** This is the **payoff reading** the whole course has been building toward. W1 taught tokens & Transformers; W2 taught model choice, prompting, and — crucially — **embeddings, vector databases, and semantic search** (W2·SG03). RAG is where all of that **snaps together into a system**: you *embed* your documents, store them in a *vector DB*, *retrieve* the relevant ones by *semantic search*, and hand them to an *LLM* to write the answer. Every serious "chat with your docs / your data / your company knowledge base" product is RAG. It is also the direct on-ramp to Week 3's later readings and (eventually) **agents**.
>
> **How to read this file:** Self-contained — you never need the original PDF. Each section pairs:
> - 📄 **`FROM THE PDF`** — original text, cleaned (spaces were stripped in the paste; the `TMLC` watermark, a page-break, and a "90%" scroll artifact were removed; wording preserved).
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies and the "why."
>
> New terms are **bolded and defined on first use**, then collected in the 🗂️ Jargon Dictionary.

---

## 📑 Table of Contents

1. [What RAG is — and the one-line intuition](#1-what-rag-is--and-the-one-line-intuition)
2. [The two components: retriever + generator](#2-the-two-components-retriever--generator)
3. [Why RAG exists: the problem with a bare LLM](#3-why-rag-exists-the-problem-with-a-bare-llm)
4. [RAG vs. Fine-Tuning](#4-rag-vs-fine-tuning)
5. [Advantages of RAG](#5-advantages-of-rag)
6. [How RAG works: the simplified flow](#6-how-rag-works-the-simplified-flow)
7. [Deep dives beyond the PDF](#7-deep-dives-beyond-the-pdf)
8. [🧵 Connected mental model](#8--connected-mental-model)
9. [⚡ 60-second recap](#9--60-second-recap)
10. [🗂️ Jargon Dictionary](#10--jargon-dictionary)
11. [🧠 Knowledge check](#11--knowledge-check)

---

## 1. What RAG is — and the one-line intuition

### 📄 FROM THE PDF
> 🚀 **Retrieval Augmented Generation (RAG)** has become a buzzword in the world of Generative AI. It's an innovative method that combines the prowess of generative models with the accuracy of retrieval systems. But what exactly is RAG, and why is it such a game-changer? Let's dive in!
>
> **🌟 What is Retrieval Augmented Generation (RAG)?**
> At its core, RAG is a technique that blends two powerful components:
> 1. **Retrieval System:** Think of this as a librarian that fetches the most relevant documents or pieces of information from a vast knowledge base.
> 2. **Generative Model:** This is the creative writer, crafting meaningful responses or content based on the retrieved information.
>
> Instead of relying solely on a generative model's internal knowledge (which may be outdated or limited), RAG ensures the model has access to up-to-date, relevant data during inference. This is achieved by retrieving external information in real-time, making the responses more accurate and contextually rich.

### 🧠 EXPLAINED
**Retrieval Augmented Generation (RAG)** is a pattern where, *before* you ask an LLM to answer, you first **look up relevant information** and **paste it into the prompt** alongside the question. The model then answers using that supplied text instead of relying only on what it memorized during training.

The name decodes exactly into the mechanism:
- **Retrieval** — go *fetch* relevant documents from your own data.
- **Augmented** — *add* those documents to the prompt (you "augment," i.e. enrich, the question with context).
- **Generation** — the LLM *writes* the final answer.

So: **Retrieve → Augment the prompt → Generate.**

💻 **The anchor analogy — open-book vs closed-book exam.** A plain LLM answering from memory is a student taking a **closed-book exam**: whatever they crammed months ago (during training) is all they've got, and they'll confidently guess when unsure. RAG turns it into an **open-book exam**: right before answering, the student is handed the *exact pages* relevant to the question and told "answer from these." Same student (same model), dramatically more accurate answers — because the facts are now *in front of them*, not dredged from fuzzy memory.

💻 **A backend analogy — cache/DB lookup before compute.** You already do this instinctively. A stateless service doesn't hardcode customer data into the binary; on each request it **queries the database** for the relevant rows, then runs its logic on *fresh* data. RAG is the same shape: the LLM is the stateless compute layer, your vector DB is the datastore, and every question triggers a **lookup → then process**. Retraining the model to add a new fact would be like recompiling and redeploying your service every time a customer's address changes — absurd. You query instead. That's RAG.

> 🔑 **Knowledge base** = the external collection of documents RAG can draw from (your PDFs, wiki pages, tickets, product docs…). It lives *outside* the model and can be updated any time without touching the model.
> 🔑 **Inference** = the moment you actually *run* the model to get an answer (as opposed to *training* it). "During inference" = "at question time, live." 💻 Think **request-handling time**, not build time.

---

## 2. The two components: retriever + generator

### 📄 FROM THE PDF
> At its core, RAG is a technique that blends two powerful components:
> 1. **Retrieval System:** … a librarian that fetches the most relevant documents … from a vast knowledge base.
> 2. **Generative Model:** … the creative writer, crafting meaningful responses … based on the retrieved information.

### 🧠 EXPLAINED
RAG is literally two subsystems wired in series. Keep them distinct in your head — they use *different* models and do *different* jobs:

| | **Retriever** (the librarian) | **Generator** (the writer) |
|---|---|---|
| **Job** | *Find* the right facts | *Phrase* the answer |
| **Model type** | An **embedding model** (encoder, e.g. BERT-family / OpenAI `text-embedding-3`) | A **generative LLM** (decoder, e.g. GPT) |
| **Output** | A shortlist of relevant text chunks | Natural-language answer |
| **W2 link** | This is **semantic search** (W2·SG03) | This is the **decoder / GPT** from W1 |
| **Skill it needs** | *Precision* — get the truly relevant docs | *Fluency* — read docs, write a coherent reply |

The retriever finds *what's true and relevant*; the generator makes it *readable*. Neither alone is enough: a search engine returns links but won't compose an answer; a bare LLM writes fluently but may invent facts. RAG gets **both** — grounded *and* fluent.

💻 **Java analogy — two beans, one pipeline.** Picture a `RetrieverService` (does the vector-DB nearest-neighbor query) feeding a `GeneratorService` (calls the LLM). The orchestrator wires them: `answer = generator.write(question, retriever.find(question))`. Classic separation of concerns — the "find" logic and the "phrase" logic are independently swappable. Want a better search? Swap the retriever. Want nicer prose? Swap the LLM. The seam between them is just **text chunks passed as context**.

> 🔑 **Retriever** = the component that searches the knowledge base and returns the most relevant chunks. Under the hood it's the embeddings + vector-DB machinery from W2.
> 🔑 **Generator** = the LLM that reads the retrieved chunks + the question and produces the final worded answer.
> 🔑 **Context** = the retrieved text that gets injected into the prompt for the generator to read. (Also why the model's input limit is called the **context window** — see [§7](#7-deep-dives-beyond-the-pdf).)

---

## 3. Why RAG exists: the problem with a bare LLM

### 📄 FROM THE PDF
> Instead of relying solely on a generative model's internal knowledge (which may be outdated or limited), RAG ensures the model has access to up-to-date, relevant data during inference.

### 🧠 EXPLAINED
This one sentence names the **two fatal limits of a bare LLM** that RAG fixes. Both matter, so let's make them concrete:

**1. Its knowledge is *frozen* (outdated).** An LLM only "knows" what was in its training data, which was collected up to some cutoff date. Ask about anything newer — this quarter's numbers, yesterday's release, a policy changed last week — and the model has genuinely never seen it. 💻 It's a **binary compiled months ago**: no amount of asking nicely makes it aware of data created after the build.

**2. Its knowledge is *generic* (limited).** The model was trained on the public internet. It has **no idea about your private, internal data** — your company's runbooks, your customer's contract, your product's specific config. That information was never in the training set, so the model can't have memorized it.

When a bare LLM hits a question it can't actually answer from memory, it doesn't say "I don't know." It **hallucinates** — produces a fluent, confident, *plausible-sounding* answer that is simply wrong.

> 🔑 **Hallucination** = when an LLM generates false information stated with total confidence. It happens because the model is fundamentally a *next-word predictor* optimizing for *plausible-sounding* text, not for *true* text — so when it lacks the fact, it fills the gap with something that merely *sounds* right.

**RAG attacks the root cause of both problems at once:** it stops asking the model to *remember* and instead *hands it the facts at question time*. Frozen knowledge? Doesn't matter — the retrieved docs are current. Private data? Fine — it's in your knowledge base, retrieved and pasted in. Hallucination? Sharply reduced — the model is now **grounding** its answer in real text it can see, not guessing from memory.

> 🔑 **Grounding** = tying the model's answer to specific, provided source text, so its claims are backed by real evidence rather than invented. RAG is the most common grounding technique.

💻 **Backend framing:** a bare LLM is a service with a **giant, stale, read-only in-memory cache and no database connection.** RAG gives it the database connection back. You'd never ship the former on purpose.

---

## 4. RAG vs. Fine-Tuning

### 📄 FROM THE PDF
> **RAG vs. Fine-Tuning 💡**
> Fine-tuning and RAG serve different purposes, and their use depends on the scenario.
>
> | Aspect | Fine-Tuning | RAG |
> |---|---|---|
> | **Data Dependence** | Requires a large amount of labelled data for training. | Leverages external knowledge without retraining. |
> | **Flexibility** | Model updates require retraining with new data. | Dynamic; retrieves updated information instantly. |
> | **Cost** | Computationally expensive to fine-tune and deploy. | Lightweight and cost-effective for updates. |
> | **Accuracy** | Can overfit or hallucinate outdated information. | Provides accurate and context-aware responses. |
>
> For example, while fine-tuning is great for domain-specific tasks (like medical diagnosis), RAG shines in applications where data is vast, dynamic, or frequently updated.

### 🧠 EXPLAINED
This is the single most important comparison in applied GenAI, and interviewers love it. First, the definition:

> 🔑 **Fine-tuning** = continuing to *train* a pretrained model on your own examples, so its **weights** (the model's internal numbers) permanently absorb new behavior or knowledge. (You met this in W2·SG02 as the heavyweight alternative to prompting.)

The crux is **where the new knowledge lives:**

- **Fine-tuning bakes knowledge *into the model's weights*.** To change what it knows, you re-train and redeploy. 💻 It's like **hardcoding data into the compiled binary** — to update one fact you rebuild and ship a new artifact.
- **RAG keeps knowledge *outside the model*, in the knowledge base.** To change what it knows, you edit a document. 💻 It's like **reading from a database at runtime** — update a row and the very next request sees it, no redeploy.

That single distinction drives every row of the PDF's table:

| Aspect | Fine-Tuning (knowledge in *weights*) | RAG (knowledge in *knowledge base*) |
|---|---|---|
| **Updating a fact** | Re-train + redeploy the model | Edit/add a document — live instantly |
| **Data needed** | Lots of curated **labelled** examples | Just your raw documents, no labels |
| **Cost profile** | High *upfront* (GPU training) + per-update | Low upfront; pay per query (retrieval + LLM call) |
| **Freshness** | Stale until the next retrain | Always as fresh as the knowledge base |
| **What it's for** | Teaching a new **skill / style / format / behavior** | Supplying **facts / knowledge** |
| **Failure mode** | Overfit; confidently recite outdated training data | Only as good as what the retriever finds |

**The mental rule that actually sticks:**
> **Fine-tuning changes *how* the model behaves. RAG changes *what* the model knows.**

- Need the model to always reply in your legal team's tone, or output a specific JSON shape, or reason like a radiologist? That's a **skill/style** → **fine-tune.**
- Need the model to answer questions about documents that change weekly? That's **knowledge** → **RAG.**

And they're **not mutually exclusive** — real systems often do both: fine-tune a model for domain *style/behavior*, then use RAG to feed it current *facts*. The PDF's own example captures the split: fine-tune for the *skill* of medical diagnosis; use RAG when the *data* is vast and changes constantly.

> ⚠️ **Nuance on the PDF's "hallucinate outdated information" (Fine-Tuning row):** the point isn't that fine-tuning *causes* hallucination — it's that fine-tuning **freezes** knowledge at training time, so as the world moves on, the model keeps confidently reciting now-stale facts. RAG sidesteps this because its facts are fetched live.

---

## 5. Advantages of RAG

### 📄 FROM THE PDF
> **Advantages of RAG ✅**
> ✅ **Up-to-Date Knowledge:** RAG dynamically retrieves the latest information, ensuring responses remain relevant.
> ✅ **Reduced Hallucination:** Generative models often "hallucinate" facts. RAG mitigates this by grounding outputs in retrieved data.
> ✅ **Cost Efficiency:** No need for expensive fine-tuning or retraining for every data update.
> ✅ **Scalability:** Easy to scale across different domains by simply changing the knowledge base.

### 🧠 EXPLAINED
Each "advantage" is really the flip side of a bare-LLM weakness from [§3](#3-why-rag-exists-the-problem-with-a-bare-llm) and [§4](#4-rag-vs-fine-tuning). Read them as *"RAG fixes X":*

- **Up-to-Date Knowledge** ← fixes *frozen weights.* The answer is as current as your documents, because facts are fetched at inference, not memorized at training.
- **Reduced Hallucination** ← fixes *confident guessing.* With real source text in front of it, the model **grounds** its answer instead of inventing one. (Note: *reduced*, not *eliminated* — see the caveat below.)
- **Cost Efficiency** ← fixes *expensive retraining.* Updating knowledge = editing a file (cheap), not running a GPU training job (expensive). New info goes live immediately.
- **Scalability** ← fixes *one-model-per-domain.* Point the same RAG system at a legal knowledge base and it's a legal assistant; swap in medical docs and it's a medical assistant. The *code stays the same*; only the **knowledge base** changes. 💻 Like a generic service parameterized by which database it connects to.

**A bonus advantage the PDF doesn't list but interviewers do:**
- **Traceability / citations.** Because you *know which chunks* were retrieved, you can show the user *"here's the source."* A fine-tuned model can't cite where a memorized fact came from; RAG can point at the exact document. Huge for trust, compliance, and debugging.

> ⚠️ **Honest caveat — "reduced," not "solved."** RAG's answer is only as good as what the retriever hands over. Two failure modes remain: (1) **retrieval misses** — the right doc isn't fetched, so the model is back to guessing; (2) the model may still **ignore or misread** correct context. RAG dramatically *reduces* hallucination; it does not *eliminate* it. Garbage-in-context → garbage-out.

---

## 6. How RAG works: the simplified flow

### 📄 FROM THE PDF
> **How RAG Works: A Simplified Flow**
> 1. **Input Query:** The user provides a question or request.
> 2. **Retrieve Phase:** A retrieval system (e.g., **ChromaDB** or **FAISS**) fetches the **top-K** relevant documents from the knowledge base.
> 3. **Generate Phase:** A generative model (e.g., GPT) processes the retrieved documents and crafts a coherent response.
> 4. **Output Response:** The final answer is delivered, blending retrieved knowledge with generative reasoning.

### 🧠 EXPLAINED
Here is the full pipeline as a text diagram — memorize this shape, everything else is detail:

```
                          ┌─────────────────────────────────────────────┐
                          │  (done ONCE, ahead of time — "indexing")     │
                          │  docs → split into chunks → embed each chunk │
                          │       → store vectors in a VECTOR DB         │
                          └─────────────────────────────────────────────┘
                                              │
  ① USER QUERY  ─────►  ② RETRIEVE  ─────►  ③ GENERATE  ─────►  ④ RESPONSE
   "What's our      embed the query,      LLM reads the        grounded,
    refund policy?"  find top-K nearest    chunks + question    cited answer
                     chunks in vector DB   → writes answer
```

Walking the four runtime steps:

**① Input Query.** The user asks something. 💻 An incoming request.

**② Retrieve Phase.** The system **embeds the query** into a vector (same embedding model used for the docs), then asks the **vector database** for the **top-K** most similar chunks by **nearest-neighbor search** (ranked by **cosine similarity** — all straight from W2·SG03).
- 🔑 **top-K** = "give me the K best matches" (K is a small number you choose, e.g. 3–5). 💻 Exactly a `LIMIT K` on a similarity-ordered query. Too small → you miss relevant context; too large → you stuff the prompt with noise and pay for more tokens.
- 🔑 **Vector database** = a datastore built for fast nearest-neighbor search over embeddings. The PDF names two: **FAISS** (Facebook AI Similarity Search — a blazing-fast *library* you run in-process) and **ChromaDB** (an easy, developer-friendly vector *database*). Others you'll hear: Pinecone, Weaviate, Milvus, pgvector.

**③ Generate Phase.** The retrieved chunks are **stitched into the prompt** as context, typically with a template like:
```
Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know.

Context:
{chunk 1}
{chunk 2}
{chunk 3}

Question: {user query}
```
The **generator LLM** reads all of that and writes the answer. *This* is the "augment" step made concrete — the prompt is **augmented** with retrieved context. The "answer only from context / say you don't know" instruction is the guardrail that turns retrieval into reduced hallucination.

**④ Output Response.** The final answer is returned — "blending retrieved knowledge with generative reasoning," i.e. *facts from your data* + *fluent phrasing from the LLM.* Often the retrieved chunks are returned too, as **citations**.

> 🔎 **The hidden step-zero: indexing.** The PDF's flow is the *query-time* path, but none of it works until the knowledge base has been **indexed** ahead of time — documents **chunked**, each chunk **embedded**, and the vectors **stored** in the vector DB. This is the top box in the diagram. Do it once (and re-run when docs change). See [§7](#7-deep-dives-beyond-the-pdf) for chunking, which is where beginners most often go wrong.

💻 **The whole thing as one backend request handler:**
```java
// (index once, offline): for each chunk -> vectorDb.upsert(embed(chunk))

String answer(String query) {
    float[] q      = embed(query);                 // ② embed the question
    List<Chunk> ctx = vectorDb.topK(q, 4);         // ② nearest-neighbor lookup (LIMIT 4)
    String prompt  = template(query, ctx);         // ③ augment: stitch context in
    return llm.generate(prompt);                   // ③–④ generate + return
}
```
That five-line method *is* RAG. Everything advanced (better chunking, re-ranking, hybrid search, query rewriting) is a refinement of one of those lines.

---

## 7. Deep dives beyond the PDF

These aren't in the PDF but you *cannot* build RAG without them — they're the parts that decide whether your system actually works.

### 7.1 Chunking — the make-or-break step
You don't embed whole documents; you split them into **chunks** (passages of, say, 200–800 tokens) and embed *each*. Why:
- **Precision.** Retrieving a tight, relevant paragraph beats retrieving a 40-page PDF where the answer is one buried line.
- **Context-window limits.** You can only fit so much text into the prompt (the **context window**), so you must send *small, relevant* pieces, not whole books.

> 🔑 **Chunk / chunking** = splitting documents into smaller passages before embedding, so retrieval returns focused snippets. 🔑 **Chunk overlap** = letting consecutive chunks share a few sentences, so an idea split across a boundary isn't lost.

⚠️ **Bad chunking is the #1 reason RAG systems underperform.** Chunks too big → noisy, imprecise retrieval and wasted tokens; too small → each chunk lacks enough context to be meaningful. This is a real tuning knob, not an afterthought.

### 7.2 The context window — why we can't just "send everything"
> 🔑 **Context window** = the maximum amount of text (measured in **tokens**) a model can consider at once — prompt + retrieved context + answer, all together. 💻 Think of it as a **fixed-size buffer / method-argument limit**: exceed it and content gets truncated or rejected. This hard cap is *the* reason RAG retrieves a *top-K few* chunks instead of dumping the entire knowledge base into the prompt.

Even as context windows grow huge, RAG stays essential: sending *only relevant* chunks is **cheaper** (fewer tokens = less money + latency) and **more accurate** (models get distracted and "lose" facts buried in a giant prompt — the "lost in the middle" effect). Retrieval is about sending the model *the right little*, not *the most*.

### 7.3 Query-time vs index-time — the two phases
RAG has two clocks, and conflating them causes confusion:
- **Index time (offline, once):** chunk → embed → store. Slow, batch, done ahead. 💻 A **build/ETL job**.
- **Query time (online, per request):** embed query → retrieve top-K → generate. Fast, live. 💻 **Request handling**.
The *same* embedding model must be used in both phases — query vectors and doc vectors have to live in the **same vector space** or nearest-neighbor comparison is meaningless.

### 7.4 Where RAG sits on the "give the model knowledge" spectrum
| Approach | How new knowledge gets in | Best for | Update cost |
|---|---|---|---|
| **Prompting only** | Typed into the prompt by hand | One-off, tiny context | — |
| **RAG** | Retrieved from a knowledge base at query time | **Large, changing, factual** knowledge | Edit a doc (cheap) |
| **Fine-tuning** | Baked into weights via training | New **skill / style / behavior** | Retrain (expensive) |
| **Pretraining** | Learned from scratch on web-scale data | Building a base model | Astronomical |

RAG is the sweet spot for the most common real need: *"make the model answer questions about my specific, up-to-date data."*

### 7.5 A note on "Advanced RAG"
The PDF shows **naive RAG** (embed → top-K → generate). Production systems layer on: **re-ranking** (a second, sharper model reorders the top-K), **hybrid search** (combine semantic + keyword/BM25), **query rewriting** (expand or clarify the user's question before retrieval), and **metadata filtering** (restrict retrieval by date/author/tenant). You don't need these yet — but know the naive flow is the *floor*, not the ceiling.

---

## 8. 🧵 Connected mental model

RAG is where the W1→W2 chain finally becomes a working product. Everything upstream was a part; this is the assembled machine:

```
   TEXT
    │  (W1: tokenizer → tokens)
    ▼
  EMBEDDINGS ── meaning as coordinates            (W2·SG03)
    │            similar meaning → nearby points  (cosine similarity)
    ▼
  VECTOR DATABASE ── fast nearest-neighbor search  ⇒  SEMANTIC SEARCH   (W2·SG03)
    │
    │   ┌──────────────── R A G  (this reading) ────────────────┐
    │   │                                                        │
    └───► ① query → ② RETRIEVE top-K → ③ GENERATE (LLM) → ④ answer
        │        (semantic search)      (W1 decoder / GPT)       │
        └────────────────────────────────────────────────────────┘
                              │
                              ▼
                          AGENTS ── models that plan, retrieve, and act
                                    (RAG's retrieve step becomes one "tool")
```

**One-line thread:** `Text → Tokens → Embeddings → Vector DB → Semantic search → RAG (retrieve + generate) → Agents.`

Back-links: the **retriever** *is* W2·SG03 semantic search; the **generator** *is* the W1 GPT-style **decoder**; **RAG vs fine-tuning** extends the W2·SG02 *few-shot vs fine-tune* trade-off from "how to teach behavior" to "how to supply knowledge"; **hallucination** and **grounding** are the problem/solution pair that motivates the entire pattern.

---

## 9. ⚡ 60-second recap

- **RAG = Retrieve → Augment → Generate.** Look up relevant docs, paste them into the prompt, let the LLM answer from them. **Open-book exam** for an LLM.
- **Two parts:** a **retriever** (embedding model + vector DB doing semantic search — the librarian) and a **generator** (an LLM — the writer). *Find* the facts, then *phrase* the answer.
- **Why it exists:** a bare LLM's knowledge is **frozen** (stale) and **generic** (doesn't know your private data), so it **hallucinates**. RAG hands it fresh, specific facts at **inference** time instead.
- **RAG vs fine-tuning:** fine-tuning bakes knowledge into **weights** (change behavior/style, expensive to update); RAG keeps knowledge in an external **knowledge base** (change facts, cheap/instant). **Fine-tuning changes *how* it behaves; RAG changes *what* it knows.** Often used together.
- **Advantages:** up-to-date, **reduced** hallucination (via **grounding**), cost-efficient updates, scalable across domains (just swap the knowledge base), plus **citations**.
- **The flow:** ① query → ② retrieve **top-K** chunks from a **vector DB** (FAISS / ChromaDB) by cosine similarity → ③ LLM generates from chunks + question → ④ answer. Hidden **step-zero: index** the docs first (chunk → embed → store).
- **Make-or-break detail:** **chunking**. Send the model *the right little*, not *the most* — bounded by the **context window**.

---

## 10. 🗂️ Jargon Dictionary

*(New this reading. Reused from earlier weeks without redefining: token, embedding, embedding model, vector, vector database, cosine similarity, nearest-neighbor search, semantic search, encoder, decoder, BERT, GPT, LLM, fine-tuning, few-shot, prompt.)*

| Term | Definition |
|---|---|
| **RAG (Retrieval Augmented Generation)** | Pattern that retrieves relevant documents and adds them to the prompt so an LLM answers from supplied facts, not just memory. |
| **Retriever / Retrieval system** | The component that searches the knowledge base and returns the most relevant chunks (embeddings + vector-DB search under the hood). |
| **Generator / Generative model** | The LLM that reads the retrieved chunks + question and writes the final natural-language answer. |
| **Knowledge base** | The external collection of documents RAG draws from; lives outside the model and can be updated freely. |
| **Inference** | Running a trained model to get an answer (as opposed to training it); "at inference" = at question time, live. |
| **Grounding** | Tying the model's answer to specific provided source text, so claims are backed by evidence. RAG is the main grounding technique. |
| **Hallucination** | An LLM confidently stating false information; happens when it lacks a fact and fills the gap with plausible-sounding text. |
| **Fine-tuning** | Further-training a model on your examples so new behavior/knowledge is baked into its weights (heavyweight; needs retraining to update). |
| **Context** | The retrieved text injected into the prompt for the generator to read. |
| **Context window** | The max text (in tokens) a model can consider at once — prompt + context + answer combined; a hard size cap. |
| **top-K** | Retrieve the K best-matching chunks (K = a small chosen number); like `LIMIT K` on a similarity-ordered query. |
| **Chunk / Chunking** | Splitting documents into smaller passages before embedding, so retrieval returns focused snippets. |
| **Chunk overlap** | Letting consecutive chunks share some text so ideas spanning a boundary aren't lost. |
| **Indexing (index time)** | The offline, one-time prep: chunk → embed → store vectors in the DB, so query-time retrieval is possible. |
| **FAISS** | Facebook AI Similarity Search — a fast in-process library for nearest-neighbor search over vectors. |
| **ChromaDB (Chroma)** | A developer-friendly open-source vector database, popular for RAG prototypes. |
| **Re-ranking** | (Advanced) A second, sharper model reorders the initially retrieved top-K for better precision. |
| **Hybrid search** | (Advanced) Combining semantic (embedding) search with keyword search (e.g. BM25). |

---

## 11. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. Expand the acronym RAG and, in one sentence each, say what the "Retrieval," "Augmented," and "Generation" steps do.
2. A bare LLM has two knowledge limitations that RAG fixes. Name both, and explain how retrieving-at-inference addresses each.
3. Complete and justify the rule: "Fine-tuning changes ___; RAG changes ___." Give one concrete scenario that clearly calls for each.

**Applied**
4. Your company's HR policies change every few months. Would you fine-tune a model on them or use RAG? Why — and what specifically would you have to do each time the policy changes, under your chosen approach?
5. Sketch the query-time RAG flow for the question *"How many vacation days do I get?"* — name each phase, the role of `top-K`, and which W2 concept powers the "retrieve" step.
6. A colleague builds RAG but retrieval keeps returning irrelevant passages. Give two distinct likely causes rooted in the *indexing/chunking* stage, and how you'd check each.

**Interview-style**
7. "If context windows are getting huge, RAG is obsolete — just paste all the docs into the prompt." Give two solid reasons this is wrong.
8. RAG "reduces" hallucination but doesn't eliminate it. Describe one realistic way a RAG system still produces a wrong answer, and which component is at fault.

---

*End of Study Guide 03·01. Next Week 3 reading → paste it and I'll build Study Guide 03·02, extending the glossary and this mental model. (Or ask me to drop a minimal end-to-end RAG demo into `week3/code/` — chunk → embed → Chroma/FAISS → retrieve → generate.)*
