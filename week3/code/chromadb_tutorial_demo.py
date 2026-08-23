"""
chromadb_tutorial_demo.py
=========================
Runnable, locally-friendly version of the **ChromaDB tutorial notebook** referenced by
Week 3 Study Guide 02 ("Introduction to Vector Databases"). It exercises almost every
concept from SG02 as executable code.

WHAT IT SHOWS (each part maps to an SG02 section):
  Part 1  Embeddings + cosine similarity intuition   -> SG02 §4  (distance metrics)
  Part 2  Basic collection: client -> add -> query   -> SG02 §7  (ingest/index/query)
  Part 3  Persistent storage (data survives restart) -> SG02 §6  (Chroma as a server/DB)
  Part 4  Plugging in a custom embedding function     -> SG02 §7① (SBERT ingestion)
  Part 5  Distance metric choice + metadata           -> SG02 §4, §5 (cosine vs L2, HNSW)
  Part 6  Pre-computed vectors + metadata filtering    -> SG02 §7④ (metadata filtering)
  Part 7  Upsert + delete (full CRUD)                  -> SG02 §3  (querying/lifecycle)

RUNS LOCALLY, NO API KEY. Everything (the SBERT model AND Chroma's default embedder)
runs on your machine via open-source models — same "local, no key" pattern as Week 2's
`bert_tasks_demo.py`. First run downloads a small model (~90 MB) to
`~/.cache/huggingface` and `~/.cache/chroma`; later runs are offline and fast.

SETUP:
    pip install "chromadb" "sentence-transformers>=3.0"
    python week3/code/chromadb_tutorial_demo.py

FAITHFUL CHANGES vs the Colab notebook (kept minimal, all noted here):
  * The notebook's `PersistentClient(path="/content/my_chroma_db")` used a Colab-only
    path. Here it's a local `./chroma_db_demo` folder (git-ignored) so it runs anywhere.
  * Wrapped each notebook section in a function + a `main()` so it runs top-to-bottom
    as one script instead of cell-by-cell.
  * Used `get_or_create_collection(...)` in a couple of spots the notebook used
    `create_collection(...)`, so re-running the script doesn't crash on "collection
    already exists". (Best-practice note called out inline.)
  * Added print labels so you can see what each step returns.
Behavior and API calls are otherwise identical to the notebook.
"""

import os
import shutil

# `reset()` (Part 3) is disabled by default in Chroma as a safety measure; this env var
# opts in. MUST be set BEFORE importing/creating any client. (Notebook cell 1.)
os.environ["ALLOW_RESET"] = "True"

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Same open-source embedding model used throughout the notebook. 384-dimensional,
# fast, CPU-friendly. This is a Sentence-BERT (SBERT) model -> SG02 §7① / glossary.
MODEL_NAME = "all-MiniLM-L6-v2"

# Local folder for the persistent DB (Part 3). Git-ignored; deleted at the end so
# repeated runs start clean.
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_demo")


# ---------------------------------------------------------------------------
# PART 1 — Embeddings + cosine similarity, BY HAND (before Chroma enters)
# Notebook cells 2-3.  Teaches SG02 §4: "similarity" is just a number computed
# from two vectors. Chroma will do all of this for you later; here we peek under
# the hood so the vector DB isn't a black box.
# ---------------------------------------------------------------------------
def part1_embedding_intuition():
    print("\n=== PART 1: embeddings + cosine similarity (raw SBERT) ===")

    model = SentenceTransformer(MODEL_NAME)   # downloads weights on first run

    sentences = [
        "The weather is lovely today.",
        "It's so sunny outside!",
        "He drove to the stadium.",
    ]

    # model.encode() turns each sentence into a 384-number vector (the embedding).
    embeddings = model.encode(sentences)
    print("embeddings.shape =", embeddings.shape)   # (3, 384): 3 sentences x 384 dims

    # .similarity() computes cosine similarity between every pair -> a 3x3 matrix.
    # Diagonal = 1.0 (each sentence with itself). Higher = more similar in MEANING.
    similarities = model.similarity(embeddings, embeddings)

    # Pretty-print the matrix so the semantics jump out.
    for i, s1 in enumerate(sentences):
        print(s1)
        for j, s2 in enumerate(sentences):
            print(f"   - {s2:<32}: {similarities[i][j]:.4f}")
    # EXPECT: sentence 0 ("weather...") ~ sentence 1 ("sunny...") ~0.67  (both weather),
    # but both ~0.10 vs sentence 2 ("stadium") -> unrelated. Meaning = geometry. (SG02 §1/§4)


# ---------------------------------------------------------------------------
# PART 2 — The core vector-DB loop: client -> collection -> add -> query
# Notebook cells 4-8. This is SG02 §7's lifecycle in 4 calls.
# ---------------------------------------------------------------------------
def part2_basic_collection():
    print("\n=== PART 2: basic collection (add + query) ===")

    # chromadb.Client() = an EPHEMERAL, in-memory client (data gone when the process
    # ends). Great for demos/tests. (~ an in-memory H2 DB in Java.)
    chroma_client = chromadb.Client()

    # A "collection" ~ a table/index dedicated to one set of vectors.
    # NOTE: notebook used create_collection(); get_or_create_ is re-run-safe.
    collection = chroma_client.get_or_create_collection(name="my_collection")

    # DATA INGESTION (SG02 §7①). We pass raw TEXT and NO embedding function, so Chroma
    # uses its DEFAULT embedder (an ONNX build of all-MiniLM-L6-v2 — same family as
    # Part 1) to embed for us. This is the "convenience" payoff from SG02 §8.
    collection.add(
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges",
        ],
        ids=["id1", "id2"],
    )

    # QUERY EXECUTION (SG02 §7③). Chroma embeds the query text, then returns the
    # top-K nearest stored docs by distance. n_results = top-K (SG01/SG02).
    results = collection.query(
        query_texts=["This is a query document about hawaii"],  # Chroma embeds this
        n_results=2,
    )
    print("query 'hawaii' -> documents:", results["documents"])
    print("distances (smaller = closer):", results["distances"])
    # EXPECT: 'pineapple' ranks ABOVE 'oranges' — Hawaii<->pineapple is the stronger
    # semantic link, even though the word "hawaii" appears in NEITHER document. That is
    # semantic search: matching by MEANING, not keywords. (SG02 §1)

    # The stored vectors are excluded from query output by default (they're big).
    # Ask for them explicitly with include=[...].
    got = collection.get(include=["embeddings"])
    first_vec = got["embeddings"][0]
    print(f"stored vector length = {len(first_vec)} (a 384-dim embedding)")


# ---------------------------------------------------------------------------
# PART 3 — Persistent storage: the DB survives a restart
# Notebook cells 10-12. Ephemeral Client() forgets everything; PersistentClient
# writes to disk and reloads on start — this is what makes Chroma a real DB, not
# just an in-memory FAISS-style index. (SG02 §6 deployment models.)
# ---------------------------------------------------------------------------
def part3_persistent_client():
    print("\n=== PART 3: persistent client ===")

    client = chromadb.PersistentClient(path=PERSIST_DIR)  # writes to ./chroma_db_demo

    # heartbeat() -> a nanosecond timestamp; a cheap "is the DB alive?" ping.
    print("heartbeat (ns):", client.heartbeat())

    # reset() WIPES the entire database. Destructive + irreversible — it only works
    # because we set ALLOW_RESET=True at the top. (Notebook cell 12.)
    client.reset()
    print("client.reset() -> database emptied")

    return client


# ---------------------------------------------------------------------------
# PART 4 — Supplying your OWN embedding function explicitly
# Notebook cells 13-17. Instead of Chroma's default embedder, hand it a specific
# SentenceTransformer. Also shows housekeeping ops: peek/count/modify.
# ---------------------------------------------------------------------------
def part4_custom_embedding_function(client):
    print("\n=== PART 4: custom embedding function + housekeeping ===")

    # Wrap our chosen SBERT model as a Chroma "embedding function". Now every add()/
    # query() on this collection routes text through THIS model. Pinning the embedder
    # matters: query vectors and stored vectors must come from the SAME model (SG02 §4).
    sbert_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )

    collection = client.get_or_create_collection(
        name="my_collection_2", embedding_function=sbert_ef
    )

    print("peek() ->", collection.peek())   # first 10 items (empty here)
    print("count() ->", collection.count())  # number of items -> 0
    collection.modify(name="vect-db")        # rename the collection
    print("renamed collection to:", collection.name)


# ---------------------------------------------------------------------------
# PART 5 — Choosing the DISTANCE METRIC (cosine vs L2) + metadata on add
# Notebook cells 18-21. The metric is set at collection-creation via the
# "hnsw:space" metadata key. This is SG02 §4 (metric) + §5 (HNSW index) made real.
# ---------------------------------------------------------------------------
def part5_metric_and_metadata(client):
    print("\n=== PART 5: distance metric (cosine) + metadata ===")

    # metadata={"hnsw:space": "cosine"} tells the HNSW index to rank by COSINE distance.
    # Default is "l2" (squared Euclidean). Options: "cosine", "l2", "ip" (inner product).
    # -> SG02 §4. You choose this ONCE, at creation; changing it later means re-indexing.
    collection = client.get_or_create_collection(
        name="KnowledgeBase",
        metadata={"hnsw:space": "cosine"},
    )

    # Each document carries a metadata dict — arbitrary structured fields you can later
    # FILTER on (SG02 §7④). Here: chapter/verse tags.
    collection.add(
        documents=["lorem ipsum...", "doc2", "doc3"],
        metadatas=[
            {"chapter": "3", "verse": "16"},
            {"chapter": "3", "verse": "5"},
            {"chapter": "29", "verse": "11"},
        ],
        ids=["id1", "id2", "id3"],
    )
    print("count() ->", collection.count())  # 3


# ---------------------------------------------------------------------------
# PART 6 — Pre-computed vectors + metadata FILTERING (the WHERE clause)
# Notebook cells 23-28. Two big ideas:
#   (a) You can store vectors you computed ELSEWHERE (pass embeddings=, not documents=).
#       Then Chroma's embedding_function is bypassed entirely.
#   (b) where={...} filters results by metadata — "nearest neighbors, BUT only these".
# ---------------------------------------------------------------------------
def part6_precomputed_and_filtering(client):
    print("\n=== PART 6: pre-computed embeddings + metadata filtering ===")

    # Fresh collection. (An embedding_function is set but will be UNUSED here because we
    # pass embeddings= directly — a subtle but important point, see below.)
    sbert_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=MODEL_NAME
    )
    collection = client.get_or_create_collection(
        name="Test1", embedding_function=sbert_ef
    )

    # (a) Supply 3-dim vectors DIRECTLY. When you pass `embeddings=`, Chroma stores them
    # as-is and never calls the embedding function — so these toy 3-dim vectors are fine
    # even though the SBERT model is 384-dim. The only rule: query vectors must match the
    # STORED dimensionality (here, 3). This mirrors SG02's "store vectors computed by an
    # external model" note.
    collection.upsert(   # upsert = insert-or-update; re-run-safe (notebook used add())
        embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2]],
        metadatas=[
            {"chapter": "3", "verse": "16"},
            {"chapter": "3", "verse": "5"},
            {"chapter": "29", "verse": "11"},
        ],
        ids=["id1", "id2", "id3"],
    )

    # Plain nearest-neighbor query with a raw 3-dim query vector.
    res = collection.query(query_embeddings=[[11.1, 12.1, 13.1]], n_results=10)
    print("nearest ids (no filter):", res["ids"])

    # (b) SAME query, now with a metadata filter: only chapter == "3".
    # This is the vector-DB "WHERE clause" (SG02 §7④): similarity search + structured
    # filter combined — essential for per-tenant / permissioned RAG.
    res_filtered = collection.query(
        query_embeddings=[[11.1, 12.1, 13.1]],
        n_results=10,
        where={"chapter": "3"},
    )
    print("nearest ids (chapter=3 only):", res_filtered["ids"])

    # Richer filter operators (notebook cell 28):
    #   $eq / $ne  equal / not-equal      $gt / $gte / $lt / $lte  numeric compares
    #   $in / $nin  in / not-in a list
    res_in = collection.query(
        query_embeddings=[[11.1, 12.1, 13.1]],
        n_results=10,
        where={"chapter": {"$in": ["3", "29"]}},
    )
    print("nearest ids (chapter in {3,29}):", res_in["ids"])

    return collection


# ---------------------------------------------------------------------------
# PART 7 — Upsert + delete = the rest of CRUD
# Notebook cells 29-31. Vector DBs aren't write-once; they support live updates and
# deletes (with the same metadata filters).
# ---------------------------------------------------------------------------
def part7_upsert_and_delete(collection):
    print("\n=== PART 7: upsert + delete (CRUD) ===")

    # upsert: update these ids if present, else insert. Idempotent — the safe way to
    # keep a knowledge base in sync as source docs change (SG02 §3 lifecycle).
    collection.upsert(
        ids=["id1", "id2", "id3"],
        embeddings=[[1.1, 2.3, 3.2], [4.5, 6.9, 4.4], [1.1, 2.3, 3.2]],
        metadatas=[
            {"chapter": "3", "verse": "16"},
            {"chapter": "3", "verse": "5"},
            {"chapter": "29", "verse": "11"},
        ],
        documents=["doc1", "doc2", "doc3"],
    )

    # delete by ids + a metadata filter. BOTH must match: here ids are id1..id3 but only
    # the one with verse == "5" is removed -> exactly 1 deleted.
    collection.delete(ids=["id1", "id2", "id3"], where={"verse": "5"})
    remaining = collection.get(ids=["id1", "id2", "id3"])
    print("remaining ids after delete(verse=5):", remaining["ids"])  # -> id1, id3


def main():
    part1_embedding_intuition()
    part2_basic_collection()
    client = part3_persistent_client()
    part4_custom_embedding_function(client)
    part5_metric_and_metadata(client)
    collection = part6_precomputed_and_filtering(client)
    part7_upsert_and_delete(collection)

    # Clean up the on-disk demo DB so re-runs start fresh and nothing is committed.
    if os.path.isdir(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
    print("\nDone. (temp DB at ./chroma_db_demo removed)")


if __name__ == "__main__":
    main()
