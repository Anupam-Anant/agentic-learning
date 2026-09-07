# 7-Week Generative AI Program — Learning Workspace

This workspace holds my notes, code, assignments, and revision material for a 7-week guided GenAI program. Each week lives in its own folder so material never gets mixed up.

## Folder Convention

```
L1/
├── README.md              <- this index (course-wide)
├── week1/                  <- Week 1: Building LLMs using Playgrounds
│   ├── notes/              <- teaching notes (chapter-by-chapter explanations of the PDF)
│   ├── code/               <- hands-on code, experiments, snippets
│   ├── assignments/        <- the weekly project/assignment work
│   └── revision/           <- cheat sheets, glossary, interview Q&A, concept maps
├── week2/ ... week7/       <- same structure, created as we go
```

## Week Index

| Week | Topic | Status |
|------|-------|--------|
| 1 | Building LLMs using Playgrounds | 🟢 Complete — 4 study guides + assignment (Ticket Triage System) |
| 2 | Open/Closed Models · Prompt Engineering · Embeddings · BERT · Hugging Face | 🟡 In progress — study guides 01–05 + 2 code demos |
| 3 | RAG · Vector Databases · LangChain | 🟡 In progress — study guides 01–03 (RAG · vector DBs · LangChain) + 4 code demos |
| 4 | _TBD_ | ⚪ Not started |
| 5 | _TBD_ | ⚪ Not started |
| 6 | _TBD_ | ⚪ Not started |
| 7 | _TBD_ | ⚪ Not started |

### Week 1 files
- **`notes/study-guide-01-transformers-to-llms.md`** ⭐ Reading 01 — self-contained: full PDF text + inline explanations + jargon dictionary.
- **`notes/study-guide-02-introduction-to-genai.md`** ⭐ Reading 02 — What is GenAI, how it works, how to access it, models, ethics. Self-contained.
- **`notes/study-guide-03-openai-api-usage.md`** ⭐ Reading 03 — OpenAI Responses API, Structured Outputs, Streaming. Self-contained + line-by-line code.
- **`notes/study-guide-04-choosing-a-genai-model.md`** ⭐ Reading 04 — model types, 9 selection criteria, benchmarks, decision framework. Self-contained.
- `notes/01-evolution-of-transformers-to-llms.md` — companion teaching breakdown for Reading 01 + **knowledge-check quiz**.
- `code/` — runnable OpenAI API examples (client + basic/multi-turn, structured output, streaming).
- `revision/glossary.md` — running glossary across all weeks (~253 terms so far).
- **`assignments/project1-ticket-triage/`** ⭐ **Week 1 assignment** — AI Support Ticket Triage System (Colab notebook + CLI + dataset + README).

### Week 2 files
- **`notes/study-guide-01-open-source-vs-closed-source.md`** ⭐ Reading 01 — open-source vs closed-source models: the control-vs-convenience trade-off across transparency, performance, cost, and support; decision framework, use cases, tooling (Hugging Face / Transformers / LangChain / LlamaIndex), and the open-weight ≠ open-source nuance. Self-contained + knowledge check.
- **`notes/study-guide-02-basic-prompt-engineering.md`** ⭐ Reading 02 — 4 core prompt techniques (zero-shot, few-shot, prompt chaining, chain-of-thought): what each is, when to use it, line-by-line code, in-context learning vs fine-tuning, and the Chat Completions vs Responses API bridge. Self-contained + knowledge check.
- **`notes/study-guide-03-introduction-to-vector-embeddings.md`** ⭐ Reading 03 — vector embeddings: meaning as coordinates, one-hot vs dense, king−man+woman, static vs contextual (Word2Vec/GloVe/BERT/CLIP), cosine similarity, and the path to vector DBs & RAG. Self-contained + knowledge check.
- **`notes/study-guide-04-using-bert-for-simple-tasks.md`** ⭐ Reading 04 — using BERT locally via Hugging Face `transformers` for text classification, NER, and extractive QA; the `pipeline()` abstraction, encoder-vs-decoder, IOB tagging, extractive-vs-generative QA, and running open-source models on your own machine. Self-contained + line-by-line code + knowledge check.
- `code/prompt_engineering_demo.py` — runnable demo of all 4 prompt techniques (Chat Completions API); see `code/README.md`.
- `code/bert_tasks_demo.py` — runnable demo of BERT for 3 NLP tasks, run locally via Hugging Face `transformers` (no API key); see `code/README.md`.
- **`notes/study-guide-05-huggingface-automodel-vs-pipeline.md`** ⭐ Reading 05 (notebook `HuggingFace_Pipeline.ipynb`) — the two ways to run a HF model: low-level `AutoModel`+`AutoTokenizer` (manual tokenize→generate→decode with Phi-3, a causal/autoregressive decoder) vs high-level `pipeline` (DistilBERT sentiment); chat templates, tensors, greedy-vs-sampling, and the `Auto*` factory pattern. Self-contained + line-by-line + knowledge check.

### Week 3 files
- **`notes/study-guide-01-retrieval-augmented-generation.md`** ⭐ Reading 01 — Retrieval Augmented Generation: the Retrieve → Augment → Generate pattern; retriever (embeddings + vector DB, "librarian") vs generator (LLM, "writer"); why bare LLMs go stale & hallucinate; RAG vs fine-tuning (knowledge-in-DB vs knowledge-in-weights); the 4-step query flow + hidden indexing step; chunking, context window, top-K, FAISS/ChromaDB. Self-contained + knowledge check.
- **`notes/study-guide-02-introduction-to-vector-databases.md`** ⭐ Reading 02 — Vector databases (the engine behind RAG's retriever): why B-tree DBs can't do similarity search ("Elasticsearch for meaning"); the 4 components; distance metrics (cosine vs Euclidean vs dot product); ANN & the accuracy/speed trade-off with HNSW ("skip-list for geometry"); tools by deployment model (FAISS/Chroma/Qdrant/Pinecone/pgvector); the ingest→index→query→post-process lifecycle; the ChromaDB sample-code walkthrough + hybrid search. Self-contained + knowledge check.
- `code/chromadb_tutorial_demo.py` — runnable ChromaDB tour (the SG02 PDF's "sample code"): SBERT embeddings + cosine similarity, add/query (semantic search), persistence, distance-metric choice, metadata filtering, full CRUD. Runs **locally, no API key**; see `code/README.md`.
- **`notes/study-guide-03-langchain-framework.md`** ⭐ Reading 03 — LangChain, the framework that assembles W1–W3 into a real app ("Spring for LLM apps"): the problem it solves; chains/integration/extensibility; the memory/data-augmentation/tool superpowers; core concepts (Chains · Models · Prompts · Memory); **LCEL** and the pipe `|`; other frameworks (LlamaIndex/CrewAI/FlowiseAI/LangGraph); and how a RAG app is a ~5-line LCEL chain. Self-contained + knowledge check.
- **`notes/study-guide-03b-langchain-notebooks-walkthrough.md`** — cell-by-cell walkthrough of the three original LangChain notebooks (`Setup_and_Simple_Chain` · `Chains` · `LCEL`): every meaningful line explained, incl. quantization/4-bit, tokenizer padding, the base-model repetition bug, and the LCEL fan-out/fan-in. Companion to SG03.
- `code/langchain_*_demo.py` (+ shared `langchain_model.py`) — the 3 LangChain companion notebooks made runnable: **simple chain** (deprecated `LLMChain` vs modern LCEL), **sequential chain** (topic→outline→expand), and **LCEL fan-out/fan-in** (two models answer, a third merges). Provider-swappable (Cohere/OpenAI); see `code/README.md`.

## How the notes are built

For each week's PDF, the notes follow a consistent teaching workflow:
1. High-level overview (what & why)
2. Chapter-by-chapter deep teaching
3. Intuition (analogies + mental models)
4. Deep dives beyond the PDF
5. Glossary of key terms
6. How everything connects
7. Practical/industry perspective
8. Knowledge-check questions
9. Revision notes & cheat sheet
10. Assignment plan

---
*Legend: 🟢 Complete · 🟡 In progress · ⚪ Not started*
