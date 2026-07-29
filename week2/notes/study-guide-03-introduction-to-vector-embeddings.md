# Study Guide 02·03 — Introduction to Vector Embeddings

> **Source:** Week 2 reading PDF #3 — *"Introduction to Vector Embeddings"* (TMLC).
> **Where it fits in the course:** This is a **cornerstone** reading. W1 taught you tokens & Transformers; W2·SG01–02 covered model choice and prompting. **Embeddings are the bridge from "text" to "math you can compute similarity on"** — and they are the engine behind **semantic search, recommendation systems, and (crucially) RAG**, which is coming soon. Almost everything advanced in GenAI stands on this idea. If one Week 2 concept must be rock-solid, it's this one.
>
> **How to read this file:** Self-contained — you never need the original PDF. Each section pairs:
> - 📄 **`FROM THE PDF`** — original text, cleaned (spaces were stripped in the paste; a `TMLC` watermark + page breaks removed; wording preserved). Two "click here"/"visit this link" pointers in the PDF were dead links and are noted, not invented.
> - 🧠 **`EXPLAINED`** — plain-English teaching with 💻 Java/backend analogies and the "why."
>
> New terms are **bolded and defined on first use**, then collected in the 🗂️ Jargon Dictionary.

---

## 📑 Table of Contents

1. [What is a vector embedding? (and why we need it)](#1-what-is-a-vector-embedding-and-why-we-need-it)
2. [The "apple" intuition](#2-the-apple-intuition)
3. [Vector representations — the core idea](#3-vector-representations--the-core-idea)
4. [Key concepts: vectors, embedding space, one-hot → dense](#4-key-concepts-vectors-embedding-space-one-hot--dense)
5. [The king / queen example](#5-the-king--queen-example)
6. [Techniques & models for generating embeddings](#6-techniques--models-for-generating-embeddings)
7. [Static vs contextual embeddings (the big leap)](#7-static-vs-contextual-embeddings-the-big-leap)
8. [Conclusion](#8-conclusion)
9. [Deep dives beyond the PDF](#9-deep-dives-beyond-the-pdf)
10. [🧵 Connected mental model](#10--connected-mental-model)
11. [⚡ 60-second recap](#11--60-second-recap)
12. [🗂️ Jargon Dictionary](#12--jargon-dictionary)
13. [🧠 Knowledge check](#13--knowledge-check)

---

## 1. What is a vector embedding? (and why we need it)

### 📄 FROM THE PDF
> **Introduction to Vector Embeddings**
> Vector embeddings play a foundational role in machine learning and artificial intelligence. They convert complex, high-dimensional data such as words, images, audio or user behaviours into meaningful numerical representations. These embeddings help machines understand relationships and patterns in data, paving the way for applications like natural language processing (NLP), image recognition, and recommendation systems.

### 🧠 EXPLAINED
A **vector embedding** (usually just "**embedding**") is a way to turn a piece of data — a word, sentence, image, audio clip, even a user's behavior — into a **list of numbers** (a **vector**) that **captures its meaning**, such that *similar things get similar lists of numbers.*

> **`Vector`** = an ordered list of numbers, e.g. `[0.23, -0.45, 0.91, …]`. In math it's a point (or an arrow) in space. 💻 For you: a `float[]` / `double[]` — a fixed-length array of numbers.
> **`Embedding`** = a vector *produced to represent the meaning of some input.* Same word learned in W1·SG02 ("open-weight"), but here it's the star of the show.

**The problem it solves.** Computers do math, not language. To let a machine *reason about* the word "apple," you must first turn "apple" into numbers. The naive ways are terrible:

- Assign each word an ID (`apple=1, banana=2, car=3`). But now the math lies: it implies `banana` is "twice" `apple`, and `apple + banana = car`. The numbers carry **false relationships**.
- The trick of embeddings: assign numbers so that **geometric closeness = semantic closeness.** "apple" and "banana" land near each other; "apple" and "car" land far apart. The position *means* something.

💻 **The anchor analogy — coordinates / feature vectors.** Imagine describing a house as `[sqft, bedrooms, price, latitude, longitude]`. That's a point in 5-D space, and two similar houses sit close together. An embedding is the same idea, except: (a) there are *hundreds* of dimensions, and (b) the model **learns** what the dimensions should be automatically, rather than you hand-picking "sqft, bedrooms." The result is a **learned coordinate system for meaning.**

💻 **A second analogy — `equals()` → `similarity()`.** In Java, `"king".equals("queen")` is `false` — strings are either identical or not, no in-between. Embeddings replace that hard `boolean` with a soft `double`: `similarity(king, queen) = 0.8`, `similarity(king, car) = 0.1`. Embeddings give you a **continuous notion of "how alike"**, which plain identity can't.

⚠️ **Don't confuse with `hashCode()`.** A hash function is *deliberately* designed so similar inputs scatter to *dissimilar* outputs (good hashing spreads things out to avoid collisions). Embeddings are the **exact opposite goal**: similar inputs → *nearby* outputs. So an embedding is a *similarity-preserving* fingerprint, not a hash.

---

## 2. The "apple" intuition

### 📄 FROM THE PDF
> Imagine trying to explain the concept of "apple" to a computer. Instead of using a single word or a simple numerical label, embeddings represent "apple" as a **dense vector** capturing its context — its relationship with "fruit," "red," or even "technology" (if we consider Apple Inc.). This nuanced representation allows AI systems to understand and generate more human-like responses.

### 🧠 EXPLAINED
The apple example makes two points:

1. **An embedding captures many facets at once.** "apple" isn't reduced to one label; its vector sits near *fruit*, near *red*, and (partly) near *technology*. Each of the vector's hundreds of numbers encodes some blend of learned features. You don't get clean human labels like "dimension 7 = redness" — the meaning is smeared across all dimensions — but collectively they place "apple" correctly among its neighbors.

2. **It hints at ambiguity** (the fruit vs. Apple Inc.). A *single fixed* vector for "apple" has to average those senses. Resolving *which* "apple" you mean based on the sentence is exactly what **contextual embeddings** do — see [§7](#7-static-vs-contextual-embeddings-the-big-leap).

💻 **Java analogy:** instead of representing an object by one field (`String name`), you represent it by a rich **feature struct** — a whole `float[]` of learned attributes. Comparing two objects becomes comparing their feature vectors, not just their names.

---

## 3. Vector representations — the core idea

### 📄 FROM THE PDF
> **Understanding the Concept of Vector Representations**
> At its core, vector embedding is a dense representation of data in a **continuous vector space**. Each item (word, image, or entity) is represented as a **point in this space**, and the **distance between points signifies their relationships or similarities**.

### 🧠 EXPLAINED
Picture a giant multi-dimensional map. Every word/image/item is a **pin** on that map. The rule of the map: **near = similar, far = different.** That map is the **embedding space** (a.k.a. **vector space**), and each embedding is a set of coordinates locating one pin on it.

- **"Continuous"** means the coordinates are smooth real numbers (`0.732…`), not discrete buckets — so you can move gradually from one concept toward another and measure fine-grained distances.
- **"Distance signifies similarity"** is the payoff: once meaning is coordinates, *"which items are similar?"* becomes *"which points are nearest?"* — a pure math question a computer can answer instantly. (How we measure that distance = **cosine similarity**, [§9](#9-deep-dives-beyond-the-pdf).)

💻 **Java analogy:** it's like giving every object a stable `(x, y, z, … )` position, then answering "find things like this" with a **nearest-neighbor** lookup instead of scanning text. Search stops being "does the string match?" and becomes "which points are closest?" — this is **semantic search**.

---

## 4. Key concepts: vectors, embedding space, one-hot → dense

### 📄 FROM THE PDF
> **Key Concepts:**
> - **Vectors:** Multi-dimensional arrays of numbers (e.g., `[0.23, -0.45, 0.91]`).
> - **Embedding Space:** A high-dimensional space where similar items are close together, and dissimilar ones are farther apart.
> - **From One-Hot Encoding to Dense Vectors:** One-hot encoding represents data as **sparse binary vectors**, which can be inefficient. Embeddings map items to **dense, lower-dimensional vectors**, preserving semantic meaning and reducing computational complexity.

### 🧠 EXPLAINED
The heart of the reading is the jump **from one-hot encoding to dense embeddings.** This is *the* thing to understand.

**One-hot encoding.** Suppose your vocabulary has 50,000 words. One-hot gives each word a vector of **50,000 slots, all `0` except a single `1`** marking that word:
```
apple  = [0, 0, 1, 0, 0, …, 0]   (a 1 in slot #3)
banana = [0, 1, 0, 0, 0, …, 0]   (a 1 in slot #2)
```
> **`One-hot encoding`** = represent one item out of N by an N-length vector with a single `1` and the rest `0`.
> **`Sparse vector`** = a vector that is *mostly zeros*.

Two fatal problems:
1. **Huge & wasteful.** 50,000 numbers to say one word; scale that to sentences and it explodes.
2. **No similarity — the killer flaw.** *Every* one-hot vector is equally distant from every other (they're all mutually perpendicular). So "king" is exactly as "far" from "queen" as from "car." One-hot encodes **identity but zero meaning.**

💻 **Java analogy:** one-hot is a `boolean[50000]` / `BitSet` with exactly one bit flipped, or an **enum ordinal** blown up into flags. It tells you *which* item, nothing about *what it's like*.

**Dense embeddings** fix both:
```
apple  = [0.21, -0.44, 0.87, 0.02, …]   (maybe 300 numbers, all meaningful)
banana = [0.19, -0.40, 0.83, 0.05, …]   (close to apple — both fruit)
car    = [-0.66, 0.12, -0.30, 0.91, …]  (far from both)
```
> **`Dense vector`** = a compact vector where *most values are non-zero and carry information*.
> **`Dimension / dimensionality`** = how many numbers are in the vector (its length). Typical: Word2Vec ≈ 300, BERT-base = 768, OpenAI `text-embedding-3-small` = 1536.

| | One-hot | Dense embedding |
|---|---|---|
| Length | = vocabulary size (e.g. 50,000) | small & fixed (e.g. 300–1536) |
| Values | one `1`, rest `0` (**sparse**) | all meaningful floats (**dense**) |
| Captures similarity? | ❌ everything equidistant | ✅ near = similar |
| Meaning | identity only | **semantic meaning** |
| 💻 analogy | `BitSet`, one bit set | compact learned `float[]` feature vector |

> **`Semantic`** = relating to *meaning*. **`Semantic similarity`** = closeness in meaning (not spelling). "car" and "automobile" are semantically similar though they share no letters — embeddings capture that; string matching can't.

---

## 5. The king / queen example

### 📄 FROM THE PDF
> Example: In word embeddings, the words **"king" and "queen"** will be represented by vectors that are **closer to each other** than "king" and "car," reflecting their **semantic similarity**.

### 🧠 EXPLAINED
This is the classic demonstration that embeddings encode *meaning*: `distance(king, queen) < distance(king, car)`, because king and queen share huge semantic overlap (royalty, monarch, person) while car is unrelated.

🔥 **The deeper, famous result (worth knowing for interviews).** Embeddings don't just cluster similar words — they encode **relationships as consistent directions** in the space. The canonical Word2Vec finding:
```
vector("king") − vector("man") + vector("woman") ≈ vector("queen")
```
Read it as: *"take king, remove the 'male' component, add the 'female' component → you land on queen."* The "gender" relationship is a repeatable direction; so is "capital-of" (`Paris − France + Italy ≈ Rome`). Meaning became *arithmetic*. That's the "wow" of embeddings.

💻 **Java analogy:** it's as if `king.subtract(man).add(woman)` returned an object that `.equals()`-ish matches `queen` — relationships you can literally compute with `+`/`−` on the feature vectors.

---

## 6. Techniques & models for generating embeddings

### 📄 FROM THE PDF
> **Popular Techniques and Models for Generating Embeddings**
>
> **Word Embeddings:**
> - **Word2Vec:** Generates word vectors using two main approaches: **Continuous Bag of Words (CBOW)** and **Skip-Gram**. These methods predict words from context or context from words.
> - **GloVe (Global Vectors for Word Representation):** Builds embeddings based on **word co-occurrence matrices**, capturing global statistical information about word relationships.
>
> **Contextual Embeddings:**
> - **BERT and Transformers:** Unlike static word embeddings, BERT creates **dynamic embeddings that depend on a word's context** within a sentence. This leads to richer representations and a better understanding of words.
>
> **Audio Embeddings:**
> - **Wav2Vec 2.0:** Generates speech embeddings by learning from raw audio signals. These embeddings can be fine-tuned for various speech tasks.
>
> **Image/Multimodal Embeddings:**
> - **CLIP:** Generates embeddings for both text and images, aligning them in a shared space to enable cross-modal tasks like zero-shot classification.
>
> **Custom Embeddings:**
> For domain-specific tasks, embeddings can be trained from scratch or an embeddings model can be fine-tuned according to the data. *(The PDF here links to a Word2Vec visualization and a sample code file — both dead "click here" links, omitted.)*

### 🧠 EXPLAINED
A tour of the model "zoo," grouped by what they embed:

| Model | Embeds | Type | One-line idea | 💻/context hook |
|---|---|---|---|---|
| **Word2Vec** | words | static | Learn word vectors by predicting words ↔ their neighbors | The model that made embeddings famous (Google, 2013) |
| **GloVe** | words | static | Factorize a global **word co-occurrence** count matrix | Stanford; "statistics of the whole corpus" |
| **BERT** | words *in context* | **contextual** | Transformer encoder; a word's vector depends on its sentence | You met BERT in W1·N01 — the encoder |
| **Wav2Vec 2.0** | raw audio | contextual | Speech → vectors, learned from raw waveforms | Powers speech recognition |
| **CLIP** | text **and** images | multimodal | Put images and their captions in **one shared space** | Enables text-to-image search & zero-shot vision |

**Word2Vec — CBOW vs Skip-Gram** (both "learn meaning from company kept"):
- **CBOW (Continuous Bag of Words):** given the surrounding words, **predict the missing middle word**. ("The cat ___ on the mat" → *sat*.)
- **Skip-Gram:** the reverse — given a word, **predict its surrounding context words**. (Given *sat* → predict *cat, on, mat*.)
- Both rest on the **distributional hypothesis**: *words used in similar contexts have similar meanings.* The vectors are a by-product of learning to predict context. 💻 It's unsupervised — no human labels; the raw text *is* the training signal.

**GloVe** reaches a similar place differently: instead of predicting word-by-word, it crunches a giant table of **how often each word co-occurs with each other word** across the whole corpus (a **co-occurrence matrix**) and factorizes it. Word2Vec = local/predictive; GloVe = global/statistical.

**CLIP** is the one to remember for **multimodal**: it trains text and images into the *same* embedding space, so a photo of a dog and the caption "a dog" land near each other. That shared space is what lets you search images with text, or do **zero-shot classification** (W1) — classify an image by comparing it to embedded label texts, with no task-specific training.

> **`Cross-modal`** = working across different data types (text ↔ image ↔ audio) in one shared space. CLIP is the poster child.
> **`Embedding model`** = a model whose *job* is to output embeddings (e.g. Word2Vec, BERT, OpenAI's `text-embedding-3-*`), as opposed to a generative model that outputs text.

**Custom embeddings:** for a specialized domain (legal, medical, your product catalog), you can **train an embedding model from scratch** or **fine-tune** (W1·N01) an existing one on your data — the embedding equivalent of domain-specializing a model. Ties straight back to W2·SG01: you can grab an **open-source** embedding model from Hugging Face and tune it, or call a **closed** embeddings API.

---

## 7. Static vs contextual embeddings (the big leap)

*(Not a separate PDF section, but the single most important distinction hiding inside §6 — worth isolating.)*

- **Static embeddings** (Word2Vec, GloVe): **one fixed vector per word**, forever, regardless of sentence. The word "bank" gets *one* vector that awkwardly averages "river bank" and "money bank."
- **Contextual embeddings** (BERT, Transformers): the vector for a word is **computed fresh from its whole sentence**, so "bank" in *"river bank"* and *"bank account"* get **different** vectors.

| | Static (Word2Vec/GloVe) | Contextual (BERT) |
|---|---|---|
| Vectors per word | one, fixed | one *per occurrence*, context-dependent |
| Handles ambiguity ("bank")? | ❌ averages the senses | ✅ disambiguates by context |
| Built on | shallow prediction / counts | Transformer + self-attention (W1·N01) |
| 💻 analogy | a `static final` constant | a value **computed at runtime** from surrounding args |

This is *why* the field moved from Word2Vec (2013) to Transformer-based embeddings — and it connects directly to the [§2](#2-the-apple-intuition) apple ambiguity and W1's attention mechanism.

---

## 8. Conclusion

### 📄 FROM THE PDF
> **Conclusion**
> Vector embeddings have revolutionized how machines understand and process complex data, enabling applications ranging from NLP to computer vision and recommendation systems. They not only enhance model performance but also open up new possibilities for creating more intelligent, context-aware systems.

### 🧠 EXPLAINED
The takeaway: **embeddings are the universal "meaning → numbers" adapter.** Once *anything* (text, image, audio, user behavior) is an embedding, you can do math on meaning — measure similarity, cluster, recommend, search, classify — with the same toolbox. That universality is why the next things you'll learn (**vector databases** and **RAG**) are basically "store lots of embeddings, then find the nearest ones fast."

---

## 9. Deep dives beyond the PDF

**A) How do you actually measure "distance"? → Cosine similarity.**
The standard metric for text embeddings is **cosine similarity**: it measures the **angle** between two vectors (ignoring their length), i.e. "are they pointing the same way?"
- `cos = 1` → same direction → very similar. `cos = 0` → perpendicular → unrelated. `cos = −1` → opposite.
- Formula: `cos(A,B) = (A · B) / (|A| · |B|)` — dot product over the product of magnitudes.
> **`Cosine similarity`** = similarity as the cosine of the angle between two vectors; the go-to metric for comparing embeddings. (Euclidean straight-line distance is also used, but cosine is most common for text.)

> ❓ **Q: Why *cosine* — can't we use sine or tangent to measure vector similarity?**
>
> **A: No — and it's not arbitrary; sine and tangent are actually *broken* for this.** We want a function of the angle θ that (1) is **maximal at 0°** (same direction = most similar), (2) **decreases monotonically** to 180° (bigger angle ⇒ always less similar), and (3) **tells identical (0°) apart from opposite (180°)**. Check each function:
>
> | angle θ | meaning | **cos** | sin | tan |
> |---|---|---|---|---|
> | 0° | identical | **+1** | 0 | 0 |
> | 30° | very similar | **+0.87** | 0.5 | 0.58 |
> | 90° | unrelated | **0** | 1 | ∞ (undefined) |
> | 150° | nearly opposite | **−0.87** | 0.5 | −0.58 |
> | 180° | opposite | **−1** | 0 | 0 |
>
> - **Cosine** slides cleanly `+1 → 0 → −1`: bounded, monotonic, one score per angle. Passes all three. ✅
> - **Sine is ambiguous & backwards:** `sin(30°) = sin(150°) = 0.5` (can't tell "almost same" from "almost opposite"), and `sin(0°) = sin(180°) = 0` (confuses identical with opposite). It peaks at 90° — it measures how *perpendicular* vectors are, the opposite of what we want. ❌
> - **Tangent explodes:** `tan(90°)` is **undefined (→∞)** — and 90° (unrelated) is a totally normal case — plus it's unbounded and sign-flips. Numerically unusable. ❌
>
> **The deeper reason cosine is *natural*:** the dot product is defined as `A · B = |A|·|B|·cos(θ)`, so `cos(θ) = (A·B)/(|A||B|)` is just **the dot product with length divided out** — cheap (multiply-and-sum, no trig call at runtime) and defined in *any* number of dimensions. Sine belongs to the **cross product**, which is only a clean scalar in 3-D — there's no usable "sine" in a 1536-D embedding space. So cosine isn't merely convenient; it's the only one of the three that even *generalizes* to high-dimensional vectors. **One-liner:** we want "same direction = most similar," and cosine is the function that both tracks that monotonically *and* falls straight out of the dot product.

**B) A concrete taste (OpenAI embeddings API).** *Not from the PDF — added so it's tangible. This is the course's OpenAI stack from W1.*
```python
from openai import OpenAI
client = OpenAI()

def embed(text):
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding          # a 1536-number vector

# compare cosine similarity of the three words
import numpy as np
def cos(a, b): return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

k, q, c = embed("king"), embed("queen"), embed("car")
print(cos(k, q))   # high  (~0.5–0.6): king ↔ queen
print(cos(k, c))   # lower           : king ↔ car
```
Same pattern as W1's client, but the call is `client.embeddings.create(...)` and you read `resp.data[0].embedding`. *(Want this as a runnable file in `week2/code/`? Say the word — see the offer at the end.)*

**C) Tokens vs embeddings — don't conflate them.** A **token** (W1) is a *chunk of text* the model reads. An **embedding** is the *vector of numbers* representing meaning. Pipeline order: **text → tokens → embeddings**. Tokens are the input units; embeddings are the numeric meaning derived from them.

**D) Where this goes next — the RAG preview.** Semantic search = embed your documents once, store the vectors in a **vector database**, then at query time embed the question and retrieve the **nearest** document vectors. Feeding those retrieved chunks into an LLM prompt *is* **Retrieval-Augmented Generation (RAG)** — the marquee technique you're building toward. Embeddings are step one of RAG.
> **`Vector database`** = a datastore built to hold embeddings and find nearest neighbors fast (e.g. Pinecone, Weaviate, FAISS, Chroma, pgvector). 💻 Like an index optimized for "closest points" instead of "exact key match."
> **`Semantic search`** = search by *meaning* (nearest embeddings) rather than keyword matching.

**E) Dimensionality trade-off.** More dimensions = richer meaning but more storage/compute. Common sizes: 300 (Word2Vec) → 768 (BERT-base) → 1536 (OpenAI `text-embedding-3-small`). Bigger isn't always better; it's a cost/accuracy dial.

---

## 10. 🧵 Connected mental model

Embeddings are the hinge the whole course turns on — this is the CLAUDE.md master chain, now earned:

```
   TEXT
    │  (W1: tokenizer)
    ▼
  TOKENS ── numeric ids for text chunks
    │  (this reading: an embedding model — Word2Vec / BERT / OpenAI)
    ▼
  EMBEDDINGS ── meaning as coordinates in a vector space
    │            similar meaning → nearby points  (cosine similarity)
    ├────────────► similarity / clustering / recommendation
    │  (store many; find nearest)
    ▼
  VECTOR DATABASE ── fast nearest-neighbor search  ⇒  SEMANTIC SEARCH
    │  (retrieve relevant chunks, stuff into a prompt)
    ▼
  RAG ── Retrieval-Augmented Generation
    │
    ▼
  AGENTS ── models that plan, retrieve, and act
```

**One-line thread:** `Text → Tokens → Embeddings (meaning as vectors) → Vector DB (nearest-neighbor) → Semantic search → RAG → Agents.`

Back-links: **BERT** = the W1 encoder producing contextual embeddings; **contextual embeddings** rely on W1 **self-attention**; **custom/open embedding models** are the W2·SG01 open-vs-closed choice applied to embeddings; **few-shot vs fine-tuning** (W2·SG02) reappears as "use a pretrained embedding model vs fine-tune one."

---

## 11. ⚡ 60-second recap

- **Embedding** = turn data (word/image/audio/behavior) into a **vector of numbers** that captures **meaning**, so **near = similar, far = different.**
- **Why:** computers need numbers, and naive numbering invents false relationships; embeddings make **geometry = semantics.** Think **learned coordinates**, or `equals()` upgraded to a continuous `similarity()`.
- **One-hot → dense:** one-hot is a giant mostly-zero vector with a single `1` — big, and treats *all* words as equally different (no meaning). Dense embeddings are short, all-meaningful vectors where similarity is baked in.
- **king − man + woman ≈ queen:** relationships are consistent **directions**; meaning becomes arithmetic.
- **Models:** *static* — Word2Vec (CBOW/Skip-Gram), GloVe (co-occurrence). *Contextual* — BERT/Transformers (vector depends on the sentence → disambiguates "bank"). *Audio* — Wav2Vec 2.0. *Multimodal* — CLIP (text+image in one shared space, **cross-modal**).
- **Static vs contextual** is the key leap: one fixed vector per word vs a fresh vector per context.
- **Measure similarity** with **cosine similarity** (angle between vectors).
- **Where it leads:** embeddings → **vector database** → **semantic search** → **RAG** → agents. This reading is step one of RAG.

---

## 12. 🗂️ Jargon Dictionary

*(New this reading. Reused from earlier weeks without redefining: NLP, Transformer, BERT, encoder, self-attention, token, fine-tuning, zero-shot, multimodal, open-source.)*

| Term | Definition |
|---|---|
| **Vector** | An ordered list of numbers, e.g. `[0.23, -0.45, 0.91]`; a point/arrow in space. (💻 a `float[]`.) |
| **Vector embedding (embedding)** | A vector produced to represent the *meaning* of an input, so similar inputs get nearby vectors. |
| **Embedding space / vector space** | The high-dimensional space embeddings live in; near = similar, far = dissimilar. |
| **Dimension / dimensionality** | The length of a vector (how many numbers). Typical: 300 (Word2Vec), 768 (BERT), 1536 (OpenAI). |
| **Continuous vector space** | A space with smooth real-number coordinates (fine-grained distances), not discrete buckets. |
| **One-hot encoding** | Representing one of N items as an N-length vector with a single `1` and the rest `0`. |
| **Sparse vector** | A vector that is mostly zeros (e.g. one-hot). |
| **Dense vector** | A compact vector where most values are non-zero and carry information (an embedding). |
| **Semantic** | Relating to meaning. |
| **Semantic similarity** | Closeness in *meaning* (not spelling); e.g. "car" ≈ "automobile". |
| **Cosine similarity** | Similarity measured as the cosine of the angle between two vectors; the standard metric for embeddings. |
| **Word embedding** | An embedding representing a single word. |
| **Static embedding** | One fixed vector per word regardless of context (Word2Vec, GloVe). |
| **Contextual embedding** | A word's vector computed from its whole sentence, so it varies by context (BERT). |
| **Word2Vec** | 2013 model that learns word vectors by predicting words ↔ context (CBOW / Skip-Gram). |
| **CBOW (Continuous Bag of Words)** | Word2Vec mode: predict the missing center word from its surrounding context. |
| **Skip-Gram** | Word2Vec mode: predict the surrounding context words from a given word. |
| **GloVe** | Word-embedding model built from a global word **co-occurrence matrix** (statistical, not predictive). |
| **Co-occurrence matrix** | A table counting how often each word appears near each other word across a corpus. |
| **Distributional hypothesis** | The idea that words used in similar contexts have similar meanings (basis of learned embeddings). |
| **Wav2Vec 2.0** | Model that produces speech/audio embeddings learned from raw waveforms. |
| **CLIP** | Model that embeds text *and* images into one shared space, enabling cross-modal & zero-shot tasks. |
| **Cross-modal** | Operating across different data types (text ↔ image ↔ audio) in a shared space. |
| **Embedding model** | A model whose output is embeddings (vs a generative model that outputs text). |
| **Vector database** | A datastore for embeddings optimized for fast nearest-neighbor search (Pinecone, FAISS, Chroma, pgvector…). |
| **Semantic search** | Search by meaning (nearest embeddings) rather than keyword matching. |
| **Nearest-neighbor search** | Finding the points closest to a query point in vector space. |

---

## 13. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. In one sentence, what is a vector embedding, and what single property makes it more useful than assigning each word an ID number (`apple=1, banana=2`)?
2. Explain the two fatal problems with one-hot encoding that dense embeddings solve.
3. What is the difference between a *static* and a *contextual* embedding? Give a word whose correct vector *must* depend on context, and say why.

**Applied**
4. You have 1,000,000 product reviews and want to find the 10 most similar to a given review. Sketch the pipeline using embeddings, and name the metric you'd compare with.
5. Why can embeddings match "car" to "automobile" when a classic keyword search (`WHERE text LIKE '%car%'`) cannot?
6. `vector("Paris") − vector("France") + vector("Italy") ≈ ?` — what's the expected result, and what property of embedding spaces makes this work?

**Interview-style**
7. A teammate says "embeddings are basically a hash of the text." Correct them precisely.
8. Explain, in two sentences, how embeddings are the *first step* of RAG.

---

*End of Study Guide 02·03. Next Week 2 reading → paste it and I'll build Study Guide 02·04, extending the glossary and this mental model. (Or ask me to drop the embeddings similarity demo into `week2/code/`.)*
