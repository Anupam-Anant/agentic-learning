# Week 3 — Code

Runnable examples that accompany the Week 3 study guides.

## Setup

```bash
pip install "chromadb" "sentence-transformers>=3.0"
```

**No API key needed.** Everything runs **locally** on open-source models — same pattern as
Week 2's `bert_tasks_demo.py`. First run downloads a small (~90 MB) embedding model to
`~/.cache/huggingface` and `~/.cache/chroma`; later runs are offline and fast.

## Files

| File | Study guide | What it shows | Run |
|---|---|---|---|
| `chromadb_tutorial_demo.py` | `notes/study-guide-02-introduction-to-vector-databases.md` | End-to-end **ChromaDB** tour — SBERT embeddings + cosine similarity, collections, add/query (semantic search), persistent storage, custom embedding function, distance-metric choice (`hnsw:space`), metadata filtering, and full CRUD (upsert/delete) | `python chromadb_tutorial_demo.py` |

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
