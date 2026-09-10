# Study Guide 03·04 — Retrieval Optimization (Pre, During & Post)

> **Source:** Week 3 reading PDF #4 — *"Retrieval Optimization: Pre, During, and Post Retrieval"* (TMLC).
> **Where it fits in the course:** This is the **"make RAG actually good" reading.** SG01 gave you the RAG blueprint (retrieve → augment → generate) and even flagged some of these very techniques as *"Advanced RAG, coming later"* (SG01·§7.5); SG02 built the vector-DB engine and named **hybrid search** and **re-ranking** as future upgrades (SG02·§9). **This reading delivers on those promises.** A naive RAG that just embeds → top-K → generates often returns mediocre chunks; the techniques here are *how real systems fix that.* This is the difference between a demo and a product.
>
> **How to read this file:** Self-contained — you never need the original PDF. Each section pairs:
> - 📄 **`FROM THE PDF`** — original text, cleaned (spaces were stripped in the paste; the `TMLC` watermark, page-breaks, and a "90%" scroll artifact were removed; wording preserved).
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies and the "why."
>
> New terms are **bolded and defined on first use**, then collected in the 🗂️ Jargon Dictionary.

---

## 📑 Table of Contents

1. [The big idea: three stages of retrieval optimization](#1-the-big-idea-three-stages-of-retrieval-optimization)
2. [Foundation: precision vs recall (the goal metrics)](#2-foundation-precision-vs-recall-the-goal-metrics)
3. [Pre-retrieval ①: Sentence Window](#3-pre-retrieval--sentence-window)
4. [Pre-retrieval ②: Query Expansion](#4-pre-retrieval--query-expansion)
5. [Pre-retrieval ③: Query Rewriting](#5-pre-retrieval--query-rewriting)
6. [During retrieval: Hybrid Search](#6-during-retrieval-hybrid-search)
7. [Post-retrieval: Reranking](#7-post-retrieval-reranking)
8. [Deep dives beyond the PDF](#8-deep-dives-beyond-the-pdf)
9. [🧵 Connected mental model](#9--connected-mental-model)
10. [⚡ 60-second recap](#10--60-second-recap)
11. [🗂️ Jargon Dictionary](#11--jargon-dictionary)
12. [🧠 Knowledge check](#12--knowledge-check)

---

## 1. The big idea: three stages of retrieval optimization

### 📄 FROM THE PDF
> Information retrieval is a critical process in systems designed to search and extract relevant information from vast datasets. Effective retrieval requires fine-tuned optimization at different stages—**before, during, and after retrieval**—to ensure that results are accurate and meaningful. Here, we'll explore strategies for optimization at each stage: pre-retrieval, retrieval, and post-retrieval.

### 🧠 EXPLAINED
> 🔑 **Information Retrieval (IR)** = the field of finding relevant items (documents/chunks) from a large collection in response to a query. Search engines, RAG retrievers, recommendation systems — all IR. This reading is *applied IR for RAG.*

The key framing: **retrieval isn't one step you either do or don't — it's a pipeline with three places to intervene.** A naive RAG only touches the middle. This reading says: optimize *before* you search, *during* the search, and *after* you get results.

```
        ┌─────────────── PRE ───────────────┐   ┌── DURING ──┐   ┌────── POST ──────┐
  user  │ better chunks (sentence window)    │   │  hybrid    │   │  rerank the      │  →  best
  query │ better query (expand + rewrite)    │──►│  search    │──►│  top results     │  chunks → LLM
        └────────────────────────────────────┘   └────────────┘   └──────────────────┘
        fix the INPUT                             do the SEARCH well  fix the OUTPUT
```

💻 **The anchor analogy — a request pipeline with pre/post filters.** You already build exactly this shape. A **Servlet filter chain** (or Spring's `HandlerInterceptor`) has a `preHandle` (mutate/validate the incoming request), the **handler** (do the work), and `postHandle` (transform the response before it ships). Retrieval optimization is the same three-phase pattern: **pre-retrieval = preHandle** (clean up the query + how docs are indexed), **retrieval = the handler** (run the search well), **post-retrieval = postHandle** (reorder results before sending to the LLM). Same instinct, applied to search.

**Why bother?** Because the generator LLM is only as good as what it's fed (SG01's "garbage-in-context → garbage-out"). Every technique here exists to put *better chunks* in front of the model.

---

## 2. Foundation: precision vs recall (the goal metrics)

> *(Not a section in the PDF, but the PDF repeatedly says techniques "improve recall" and "balance precision and recall." You can't understand the reading without these two words — so let's nail them first.)*

Two metrics measure "was my retrieval any good?" They pull in opposite directions:

> 🔑 **Precision** = of the results I *returned*, what fraction were actually relevant? *"Did I return junk?"*
> 🔑 **Recall** = of all the relevant results that *exist*, what fraction did I *return*? *"Did I miss anything?"*

The classic picture — you searched and got some results:

|  | **Actually relevant** | **Actually irrelevant** |
|---|---|---|
| **You returned it** | ✅ true positive | ❌ false positive (hurts *precision*) |
| **You didn't return it** | ⚠️ false negative (hurts *recall*) | ✅ true negative |

- **High precision, low recall:** everything you returned is good, but you missed a lot. (Cautious.)
- **High recall, low precision:** you caught everything relevant, but buried it in junk. (Greedy.)

💻 **The tension, concretely.** Widen a search (add synonyms, loosen matching) → you catch more relevant docs (**recall ↑**) but also drag in more irrelevant ones (**precision ↓**). Narrow it → the reverse. **You can't max both;** IR is the art of trading them. 💻 It's the **sensitivity vs specificity** dial you know from monitoring/alerting: alert on everything (never miss an incident, drown in false pages) vs alert conservatively (quiet, but miss a real one).

**Why this frames the whole reading:** each technique targets one side —
- **Sentence window, hybrid search, query expansion** → mostly boost **recall** (find more relevant material).
- **Reranking** → boosts **precision** (push the junk back down, surface the best).
- Good RAG = **cast a wide net (recall), then filter hard (precision).** Keep that phrase; it's the strategy behind every section below.

---

## 3. Pre-retrieval ①: Sentence Window

### 📄 FROM THE PDF
> **Pre-retrieval optimization** focuses on refining the input to maximize the efficiency and accuracy of the retrieval process. Here are some key techniques:
> **1. Sentence Window**
> A sentence window approach involves segmenting larger documents or texts into manageable windows or chunks, typically one or more sentences long. By creating a **sliding window** of sentences, search engines can:
> - Enhance focus on smaller, contextually rich segments.
> - Improve recall rates by preventing over-reliance on large, broad documents.
> - Enable more precise matching for nuanced queries.
> **Example:** When searching for "early Renaissance techniques for light and perspective," breaking down long academic articles into sentence windows allows for better pinpointing of sections discussing specific techniques.

### 🧠 EXPLAINED
This is **chunking, upgraded** (recall SG01·§7.1 — chunking is the make-or-break step). The insight: **the granularity you *search* at should be small and precise, so matches are pinpoint.**

> 🔑 **Sentence window / sliding window** = split documents into small units (one or a few sentences) using a window that slides across the text, optionally overlapping, so each searchable unit is tight and focused.

**Why small units help retrieval** (the PDF's three bullets, explained):
- **Focus:** a single relevant sentence embeds into a *clean* vector. A whole 10-page doc embeds into a *muddy average* of many topics — its vector is "about everything," so it matches *nothing* sharply. Small = sharp.
- **Recall ↑:** if you only index big docs, a niche query ("light and perspective techniques") may not surface the one paragraph that answers it, because it's diluted. Small windows expose those buried gems.
- **Precise matching:** the query matches the *exact* sentence, not a vaguely-related document.

⚠️ **But there's a catch the PDF's name hints at — the "window."** A lone sentence is great for *matching* but often too little *context* for the LLM to answer well. The fix (and the real technique behind the name) is **sentence-window retrieval, a.k.a. "small-to-big":** *search* on the tiny sentence, but *return to the LLM* that sentence **plus its neighbors** (the surrounding window). **Match small, feed big.** See [§8.2](#8-deep-dives-beyond-the-pdf) — this is how LlamaIndex/LangChain actually implement it.

💻 **Java analogy:** it's an **index-granularity decision**, like choosing to index individual log *lines* instead of whole log *files* — you can pinpoint the exact line that matches, then show ±5 lines around it for context. Fine-grained index, context-padded result.

---

## 4. Pre-retrieval ②: Query Expansion

### 📄 FROM THE PDF
> **2. Query Expansion**
> Query expansion enriches the initial user query by adding synonyms, related terms, or broader concepts. This helps in:
> - Broadening the scope to capture relevant information that may use different terminology.
> - Addressing the issue of **vocabulary mismatch** between user queries and indexed content.
> **Technique:** Synonym-based and **knowledge graph**-based expansions can be applied to extend user input.
> **Example:** A search for "laptop" might expand to include "notebook," "portable computer," and other related terms.

### 🧠 EXPLAINED
The problem this solves has a name:
> 🔑 **Vocabulary mismatch** = the searcher and the document use *different words for the same thing* ("laptop" vs "notebook" vs "portable computer"). Keyword search fails here; even semantic search can miss edge cases.

> 🔑 **Query expansion** = automatically *adding* terms (synonyms, related concepts, broader terms) to the query before searching, so you catch documents that phrase the idea differently. **Pure recall play:** more terms → wider net → more relevant hits.

**The two techniques the PDF names:**
- **Synonym-based** — expand via a thesaurus/synonym list ("laptop" → +"notebook", +"portable computer").
- 🔑 **Knowledge graph-based** — a **knowledge graph** is a network of entities and their relationships (Apple —makes→ MacBook —is-a→ laptop). Expanding via a knowledge graph pulls in *related entities*, not just synonyms — richer than a flat thesaurus.

💻 **Backend analogy:** this is the **search-synonyms/analyzer** feature you'd configure in Elasticsearch (synonym token filters), or query-time fuzzy expansion. You've seen the idea: a user searches "TV," you also match "television." Query expansion automates that for *meaning*, not just spelling.

**Modern twist (worth knowing):** today expansion is often done by an **LLM** — "rewrite this query 3 ways / list related terms" — or by **HyDE** (generate a fake ideal answer and search with *its* embedding). See [§8.4](#8-deep-dives-beyond-the-pdf). ⚠️ **Trade-off:** more expansion = higher recall but can *lower precision* (you drag in loosely-related stuff) — which is exactly why **reranking** (§7) exists downstream to clean it back up.

---

## 5. Pre-retrieval ③: Query Rewriting

### 📄 FROM THE PDF
> **3. Query Rewriting**
> Query rewriting refines the original query to make it more search-friendly. This can involve:
> - Reordering words for clarity.
> - Correcting typos or ambiguous phrasing.
> - Adjusting terms based on user intent.
> **Example:** The query "weather Tokyo tomorrow" could be rewritten to "Tokyo weather forecast for tomorrow" for better retrieval results.

### 🧠 EXPLAINED
> 🔑 **Query rewriting** = *transforming* the user's query into a cleaner, better-formed version before searching — fixing typos, reordering, disambiguating, aligning to how the corpus phrases things.

**Expansion vs rewriting — don't confuse them** (a favorite exam trap):
- **Query expansion** *adds* terms → the query gets **bigger** (wider net, recall).
- **Query rewriting** *reshapes* the same intent → the query gets **cleaner** (better-formed, precision/clarity).

The PDF's three moves: reorder for clarity, fix typos/ambiguity, adjust to user intent. `"weather Tokyo tomorrow"` → `"Tokyo weather forecast for tomorrow"` reads more like how a real document/title is written, so it matches better.

**The killer modern use-case: conversational rewriting.** In a chatbot, users ask follow-ups that only make sense in context:
```
User: "Tell me about the Photosynthesis study guide."
User: "who wrote it?"        ← "it" = ??? a bare retriever has no idea
```
A rewriting step turns *"who wrote it?"* into *"who wrote the Photosynthesis study guide?"* — a **standalone query** the retriever can actually use. This is essential for RAG chatbots with **memory** (SG03 §5). 💻 It's **query normalization/canonicalization** — the same reason you normalize inputs (trim, lowercase, resolve aliases) before hitting a cache or DB, so equivalent requests map to the same clean form.

---

## 6. During retrieval: Hybrid Search

### 📄 FROM THE PDF
> During the retrieval phase, it's crucial to employ techniques that **balance precision and recall**, ensuring results are relevant and comprehensive.
> **1. Hybrid Search**
> Hybrid search combines two main types of retrieval methods—**semantic** and traditional **keyword-based (syntax)** searches—to deliver:
> - Broader coverage by integrating **lexical matching** with semantic understanding.
> - Enhanced relevance through deeper contextual analysis.
> **How it Works:** The system might first use a **BM25** or **TF-IDF** approach for surface-level matching and then apply **semantic vector embeddings** for deeper meaning-based refinement.
> **Example:** Searching for "ways to improve sleep quality" can return results that match exact phrases as well as contextually related content like "better rest habits."

### 🧠 EXPLAINED
You met **hybrid search** as a one-liner in SG02·§9 — here's the full picture. It fuses the two families of search, because **each fails where the other wins:**

| | **Keyword / lexical search** (BM25, TF-IDF) | **Semantic search** (embeddings, SG02) |
|---|---|---|
| Matches by | Exact words/tokens | Meaning |
| Nails | Exact strings: names, codes, `ERR-4021`, part numbers | Concepts: "sleep quality" ≈ "better rest habits" |
| Fumbles | Synonyms/paraphrases ("car" ≠ "automobile") | Exact tokens (blurs precise IDs) |

> 🔑 **Lexical / keyword search** = matching on the literal words. 🔑 **TF-IDF** (Term Frequency–Inverse Document Frequency) = classic scoring: a word matters more if it's *frequent in this doc* (TF) but *rare across all docs* (IDF) — so "the" scores low, "photosynthesis" scores high. 🔑 **BM25** = the modern, better-tuned successor to TF-IDF (the standard lexical ranker; you met it in SG02). Both are *keyword* methods — no notion of meaning.

**Why fuse them:** the PDF's example is perfect — "ways to improve sleep quality" should match the *exact phrase* (lexical) **and** "better rest habits" (semantic). Neither method alone gets both; hybrid does. 💻 **This is the SG02·§9 point, now mechanical:** run *both* an **inverted index** (Elasticsearch/BM25) and a **vector index** (SG02), then **merge the two ranked lists.**

> ⚙️ **How the merge works (the missing piece):** you can't directly compare a BM25 score (unbounded) to a cosine score (0–1). The standard fix is **Reciprocal Rank Fusion (RRF)** — combine by each doc's *rank* in each list, not its raw score. See [§8.3](#8-deep-dives-beyond-the-pdf).

⚠️ **Note the PDF's "first BM25 then semantic" phrasing.** True hybrid search usually runs both **in parallel** and fuses; the PDF's "surface-level first, then refine" describes one valid *pipeline* variant (cheap filter → expensive refine). Both exist; don't over-index on the ordering.

---

## 7. Post-retrieval: Reranking

### 📄 FROM THE PDF
> **Post-retrieval Optimization**
> **1. Reranking**
> Reranking involves applying additional algorithms to reorder the initial set of retrieved documents:
> - **Approach:** Use machine learning models or heuristic rules to prioritize documents based on metrics like **click-through rates**, content freshness, or user engagement.
> - **Outcome:** Boosts the prominence of higher-quality and more relevant documents.
> **Example:** After retrieving documents about "XYZ query" a reranking system will re-rank the retrieved contexts according to the query with an algorithm that is designed for re-ranking.

### 🧠 EXPLAINED
The final polish. You flagged this in SG01·§7.5 and SG02·§9 — here's how and why.

> 🔑 **Reranking** = take the top-N results from the first retrieval and **reorder them with a second, smarter (slower) model or rule**, so the *very best* rise to the top before you hand them to the LLM.

**The two-stage pattern is the whole point** — and it's an efficiency pattern you already use:
```
   ①  RETRIEVE (fast, approximate):  vector/hybrid search over MILLIONS → top ~50 candidates
   ②  RERANK  (slow, precise):       a heavy model scores those 50 → keep the best ~5 → LLM
```
💻 **The anchor analogy — cheap pre-filter, expensive precise re-check.** This is *exactly* how you optimize an expensive query: a **coarse index scan** cheaply narrows millions to a handful, then an **expensive exact predicate** runs only on that handful. You'd never run the expensive check on all million rows. Reranking is that: fast retrieval casts the wide net (**recall**), then a costly reranker sorts the catch precisely (**precision**). *Cast wide, then filter hard* — §2's strategy, realized.

**What does the reranking?** The PDF lists two flavors:
- **Heuristic/signal-based** — reorder by business signals: **click-through rate (CTR)**, freshness, popularity, engagement. 💻 A custom `Comparator`.
- **ML model-based** — the modern RAG default is a **cross-encoder** (a model that reads the query and a document *together* and scores their true relevance). It's far more accurate than the first-pass vector match — and far too slow to run on the whole corpus, which is *why* it only runs on the top-N. This bi-encoder-vs-cross-encoder distinction is the single most useful thing to understand here → [§8.1](#8-deep-dives-beyond-the-pdf).

> 🔑 **Click-through rate (CTR)** = fraction of users who clicked a result when shown it; a relevance/quality signal for heuristic reranking.

---

## 8. Deep dives beyond the PDF

### 8.1 Bi-encoder vs cross-encoder — *why* reranking is a separate, second stage
This is the concept that makes reranking click, and it's a top interview question.
- **Bi-encoder** (what the first-pass retrieval uses): embeds the query and each document **separately**, into independent vectors, then compares by cosine (SG02). Because doc vectors are **precomputed and indexed**, this is *fast* — you compare against millions instantly. But encoding them apart means it never sees query and doc *together*, so it's less precise.
- **Cross-encoder** (what a reranker uses): feeds the query **and** a document **together** into the model, which attends across both and outputs one relevance score. Far more accurate — but it must run *per (query, doc) pair* at query time, so it *can't* be precomputed and is *far* too slow for millions.

> 🔑 **Bi-encoder** = encode query and doc separately → fast, indexable, less precise (first-pass retrieval). 🔑 **Cross-encoder** = encode query+doc jointly → slow, unindexable, very precise (reranking).

**The resolution is the two-stage pipeline:** bi-encoder retrieves top-50 cheaply → cross-encoder reranks those 50 precisely. You get *both* speed and accuracy by using each where it's strong. This is the deep "why" behind §7.

### 8.2 Sentence-window / "small-to-big" retrieval (what §3 is really about)
Match on a tiny unit, but return a bigger context to the LLM. Two common forms:
- **Sentence-window retrieval:** index single sentences; on a hit, expand to the sentence ± *k* neighbors before sending to the model.
- **Parent-document retrieval:** index small child chunks; on a hit, return the larger *parent* chunk/document.
Both resolve §3's tension: **small is best for *matching*, big is best for *answering*.** (LlamaIndex's `SentenceWindowNodeParser` and LangChain's `ParentDocumentRetriever` implement these.)

### 8.3 Reciprocal Rank Fusion (RRF) — how hybrid actually merges (§6)
You can't add a BM25 score to a cosine score — different scales. **RRF** ignores raw scores and fuses by **rank**: each doc gets `Σ 1/(k + rank_in_each_list)`, summed across the lexical and semantic result lists; sort by that. Simple, scale-free, and the de-facto standard (used by Elasticsearch, Weaviate, etc.).
> 🔑 **Reciprocal Rank Fusion (RRF)** = combine multiple ranked lists by summing `1/(k+rank)` per item — merges lexical + semantic results without comparing incompatible scores.

### 8.4 HyDE — query expansion's clever cousin
> 🔑 **HyDE (Hypothetical Document Embeddings)** = ask an LLM to *write a fake ideal answer* to the query, then embed **that** and search with it. A hypothetical answer "looks like" the real documents you want, so its vector often retrieves better than the bare question's vector. A modern, LLM-era form of query expansion.

### 8.5 The cost/latency ladder (when to add each)
Every technique adds latency and/or cost. Add them **in order of ROI**, not all at once:
1. **Better chunking / sentence window** — free at query time, huge quality lift. *Do first.*
2. **Hybrid search** — one extra index; big win when exact terms matter.
3. **Reranking** — an extra model call on top-N; the biggest precision win, modest added latency.
4. **Query rewriting/expansion (LLM-based)** — an extra LLM call *before* retrieval; adds latency, great for conversational/ambiguous queries.
⚠️ **No free lunch:** measure retrieval quality (precision/recall on a test set) before and after each — don't stack techniques blindly.

---

## 9. 🧵 Connected mental model

This reading is a zoom-in on the single word **"retrieve"** from SG01's pipeline:

```
                         ┌──────────── RETRIEVAL OPTIMIZATION (this reading) ───────────┐
   user query ──────────►│  PRE:  sentence-window chunking · query expansion · rewriting│
                         │  DURING: HYBRID SEARCH  = BM25/TF-IDF (lexical)  +  vectors   │
                         │  POST: RERANK (cross-encoder / signals) the top-N            │
                         └───────────────────────────────┬──────────────────────────────┘
                                                         ▼
   SG01 RAG:   query → [ RETRIEVE ]───────────────────► augment → generate → answer
                          ▲                                 ▲
              SG02 vector DB (the engine)      SG03 LangChain (retriever/reranker as Runnables)
```

**One-line thread:** `Embeddings (W2) → Vector DB (SG02) → the RETRIEVE step of RAG (SG01) → made GOOD by pre/during/post optimization (this reading) → assembled in LangChain (SG03) → agents.`

Back-links: **precision/recall** are the metrics behind SG01's "reduced hallucination" (better chunks → better grounding); **hybrid search & BM25** were promised in SG02·§9; **reranking** was flagged in SG01·§7.5 / SG02·§9; **query rewriting** pairs with SG03 **memory** for chatbots; **bi- vs cross-encoder** builds on SG02's embeddings + W1 attention.

---

## 10. ⚡ 60-second recap

- **Retrieval is a 3-stage pipeline you can optimize** — **pre** (fix the input), **during** (search well), **post** (fix the output). 💻 Like a Servlet filter chain: preHandle → handler → postHandle.
- **Goal metrics = precision vs recall.** Precision = "did I return junk?"; recall = "did I miss anything?" They trade off. Winning strategy: **cast a wide net (recall), then filter hard (precision).**
- **Pre — Sentence Window:** chunk small (sentences) so matches are sharp; but *return* the surrounding window/parent to the LLM ("**match small, feed big**" / small-to-big).
- **Pre — Query Expansion:** *add* synonyms/related terms (thesaurus, knowledge graph, LLM, HyDE) to beat **vocabulary mismatch** → recall ↑.
- **Pre — Query Rewriting:** *reshape* the query — fix typos, reorder, and (big one) turn conversational follow-ups into **standalone queries** using memory.
- **During — Hybrid Search:** fuse **lexical** (BM25/TF-IDF — exact words, IDs) + **semantic** (embeddings — meaning), merged with **RRF**. Each covers the other's blind spot.
- **Post — Reranking:** reorder the top-N with a slower, smarter **cross-encoder** (or signals like CTR/freshness) → precision ↑. Two-stage = **bi-encoder retrieves fast, cross-encoder reranks precise** (cheap pre-filter → expensive re-check).
- **Add techniques by ROI, and measure** precision/recall each time — don't stack blindly.

---

## 11. 🗂️ Jargon Dictionary

*(New this reading. Reused without redefining — from SG01–03: RAG, retriever, chunking, top-K, embeddings, semantic search, vector DB, hybrid search, re-ranking, BM25, memory, Runnable.)*

| Term | Definition |
|---|---|
| **Information Retrieval (IR)** | Finding relevant items from a large collection in response to a query (search, RAG, recommendations). |
| **Pre- / during- / post-retrieval optimization** | The three stages you can tune: refine the input · run the search well · refine the output. |
| **Precision** | Of the results returned, the fraction that are relevant ("did I return junk?"). |
| **Recall** | Of all relevant results that exist, the fraction returned ("did I miss anything?"). |
| **Precision–recall trade-off** | Widening search raises recall but lowers precision, and vice versa; you balance them. |
| **Sentence window / sliding window** | Splitting text into small (1–few sentence) units via a sliding window for sharp, focused matching. |
| **Sentence-window / small-to-big / parent-document retrieval** | Match on a tiny unit but return a larger surrounding context to the LLM. |
| **Query expansion** | Adding synonyms/related/broader terms to the query before searching → recall ↑. |
| **Vocabulary mismatch** | Searcher and document use different words for the same idea ("laptop" vs "notebook"). |
| **Knowledge graph** | A network of entities and their relationships; a source for related-term expansion. |
| **Query rewriting** | Transforming the query into a cleaner, better-formed, standalone version (typos, order, intent, context). |
| **Lexical / keyword search** | Matching on literal words/tokens (no notion of meaning). |
| **TF-IDF** | Classic lexical scoring: term frequency × inverse document frequency (frequent-here-but-rare-overall = important). |
| **Reranking** | Reordering the first-pass top-N with a slower, smarter model/rule to surface the best → precision ↑. |
| **Bi-encoder** | Encodes query and doc separately → fast, indexable, less precise (first-pass retrieval). |
| **Cross-encoder** | Encodes query + doc jointly → slow, unindexable, very precise (used for reranking). |
| **Reciprocal Rank Fusion (RRF)** | Merges multiple ranked lists by summing `1/(k+rank)` per item — fuses lexical + semantic without comparing raw scores. |
| **HyDE (Hypothetical Document Embeddings)** | Generate a fake ideal answer with an LLM, embed *that*, and search with it. |
| **Click-through rate (CTR)** | Fraction of users who clicked a shown result; a signal for heuristic reranking. |

---

## 12. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. Define precision and recall in one sentence each, then explain why you can't simply maximize both. Which does *reranking* mainly improve, and which does *query expansion* mainly improve?
2. Name the three stages of retrieval optimization and give one technique from each. What's the Servlet-filter analogy?
3. Query *expansion* vs query *rewriting* — what's the core difference, and what does each mainly help (recall vs clarity)?

**Applied**
4. A user asks a RAG chatbot: "Summarize the LangChain guide," then follows up "does it cover LCEL?" Which pre-retrieval technique makes that follow-up retrievable, and what would the transformed query look like?
5. Someone searches your docs for error code `ERR-4021` and semantic search returns conceptually-similar-but-wrong pages. Which *during-retrieval* technique fixes this, and why does pure vector search fail on exact codes?
6. Explain the two-stage "retrieve then rerank" pipeline using the bi-encoder/cross-encoder distinction. Why not just use the cross-encoder on all documents?

**Interview-style**
7. Your naive RAG has poor answer quality. You can add sentence-window chunking, hybrid search, and reranking. In what order would you add them and why — and how would you *know* each helped?
8. Explain "cast a wide net, then filter hard" and map each half to a specific technique from this reading.

---

*End of Study Guide 03·04. Next Week 3 reading → paste it and I'll build Study Guide 03·05, extending the glossary and this mental model. (Or ask me to add an "advanced RAG" demo to `week3/code/` — e.g. hybrid search + a cross-encoder reranker over the ChromaDB collection.)*
