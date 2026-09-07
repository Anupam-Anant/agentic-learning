# Week 3 — Code

Runnable examples that accompany the Week 3 study guides.

## Setup

**ChromaDB demo — no API key, runs fully locally:**
```bash
pip install "chromadb" "sentence-transformers>=3.0"
```
Everything runs **locally** on open-source models — same pattern as Week 2's
`bert_tasks_demo.py`. First run downloads a small (~90 MB) embedding model to
`~/.cache/huggingface` and `~/.cache/chroma`; later runs are offline and fast.

**LangChain demos — need an API key + one provider package:**
```bash
pip install langchain langchain-core langchain-classic
pip install langchain-cohere && export COHERE_API_KEY=...   # free tier at cohere.com
# or:  pip install langchain-openai && export OPENAI_API_KEY=...
```

## Files

| File | Study guide | What it shows | Run |
|---|---|---|---|
| `chromadb_tutorial_demo.py` | `notes/study-guide-02-introduction-to-vector-databases.md` | End-to-end **ChromaDB** tour — SBERT embeddings + cosine similarity, collections, add/query (semantic search), persistent storage, custom embedding function, distance-metric choice (`hnsw:space`), metadata filtering, and full CRUD (upsert/delete) | `python chromadb_tutorial_demo.py` |
| `langchain_model.py` | `notes/study-guide-03-langchain-framework.md` | **Shared module (not an entry point).** A provider-swappable `get_chat_model()` factory (Cohere or OpenAI via env var) that the three LangChain demos import — like `week1/code/openai_client.py`. | *(imported)* |
| `langchain_simple_chain_demo.py` | SG03 §5–6 | Simplest chain (`prompt → model → text`) shown **two ways**: the notebook's deprecated `LLMChain` vs the modern **LCEL** `prompt \| model \| StrOutputParser()`. | `python langchain_simple_chain_demo.py` |
| `langchain_sequential_chain_demo.py` | SG03 §5–7 | A **true sequential chain** (topic → outline → expand) — step 1's output feeds step 2. Delivers what the notebook's "Sequential Chain" heading promised. | `python langchain_sequential_chain_demo.py` |
| `langchain_lcel_demo.py` | SG03 §6 | The star **LCEL fan-out/fan-in**: two models answer in parallel, a third merges them. Covers `\|`, dict-of-Runnables, `RunnablePassthrough`, `.assign()`. | `python langchain_lcel_demo.py` |

### Notes on the LangChain demos (`langchain_*`)
- **These are the three Week 3 companion notebooks** (`Langchain_Setup_and_Simple_Chain`,
  `Langchain_Chains`, `Langchain_LCEL`), made locally runnable.
- **Needs an API key + one provider package** (unlike the local-only ChromaDB demo):
  ```bash
  pip install langchain langchain-core langchain-classic
  pip install langchain-cohere  && export COHERE_API_KEY=...   # free tier at cohere.com (faithful to the notebooks)
  # or
  pip install langchain-openai  && export OPENAI_API_KEY=...   # the key you already have from Week 1
  ```
  `langchain_model.py` picks Cohere if `COHERE_API_KEY` is set, else OpenAI — no code change.
- **Faithful divergences** (all noted in each file header):
  - `langchain_simple_chain_demo.py` keeps the notebook's deprecated `LLMChain` **on purpose**, next to the LCEL equivalent, so you see *why* LangChain moved to LCEL (running the old class prints a `LangChainDeprecationWarning`).
  - `langchain_sequential_chain_demo.py` — the original ran a **local Mistral-7B in 4-bit quantization on a CUDA GPU** (`HuggingFacePipeline` + bitsandbytes), which won't run on a Mac, and its "Sequential Chain" heading sat over a *single* call whose base-model output looped. This file uses the swappable chat model and builds a **genuine 2-step** chain instead.
  - `langchain_lcel_demo.py` mirrors the notebook's fan-out/fan-in exactly; Colab `userdata` secret lookups dropped for env vars.

### Notes on `chromadb_tutorial_demo.py`
- **This is the "Sample Code: ChromaDB tutorial code" the SG02 PDF referenced.** It's the
  runnable, locally-friendly version of the original Colab notebook
  (`Copy_of_ChromaDB_tutorial.ipynb`).
- **Maps 1:1 onto SG02.** Each `partN_*()` function is labelled with the SG02 section it
  demonstrates (§4 distance metrics, §5 HNSW/ANN, §7 the ingest→index→query→post-process
  lifecycle, §7④ metadata filtering). Read the guide and the code side by side.
- **Two embedders, same family.** When you pass `documents=` with no embedding function,
  Chroma uses its **default** ONNX build of `all-MiniLM-L6-v2`; Part 4 shows pinning your
  **own** `SentenceTransformerEmbeddingFunction` explicitly. Both are the same 384-dim SBERT
  model — so results are consistent.
- **Faithful changes vs the notebook** (all noted in the file header): the Colab-only
  `PersistentClient(path="/content/…")` path → a local git-ignored `./chroma_db_demo`
  folder (auto-deleted at the end); cells wrapped in functions + a `main()`; a couple of
  `create_collection()` calls switched to `get_or_create_collection()` / `add`→`upsert` so
  re-running the script doesn't crash on "already exists". API calls are otherwise identical.
- **`ALLOW_RESET`.** The script sets `os.environ["ALLOW_RESET"] = "True"` *before* importing
  Chroma so Part 3's destructive `client.reset()` is permitted (off by default as a safety
  guard).
