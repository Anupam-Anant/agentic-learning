# Study Guide 02·04 — How to Use BERT for Simple Tasks

> **Source:** Week 2 reading PDF #4 — *"How to use BERT for simple tasks"* (TMLC).
> **Where it fits in the course:** This is the reading where theory becomes **hands-on**. You met **BERT** in W1·N01 (the bidirectional *encoder*) and again in W2·SG03 (it makes *contextual embeddings*). You met the **Hugging Face `transformers` library** in W2·SG01 (open-source tooling). Now you *use* them together — and, importantly, this is the **first time the course runs a model locally on your own machine instead of calling an API.** That makes the "open-source / self-hosted" path from SG01 real.
>
> **How to read this file:** Self-contained — you don't need the PDF. Each section pairs:
> - 📄 **`FROM THE PDF`** — original text/code, cleaned (spaces were stripped in the paste; `TMLC` watermark + page breaks removed; wording/code preserved).
> - 🧠 **`EXPLAINED`** — line-by-line teaching, 💻 Java/backend analogies, and the "why."
>
> **Three faithfulness notes** (per our repo rule to flag repairs):
> 1. The sentiment comment in the PDF reads *"if a model is passed then it will pick DistilBERT by default"* — that's **logically backwards**. It should be *"if **no** model is passed, it defaults to DistilBERT."* Corrected in the explanation.
> 2. The QA example's question has a typo — *"deafeated"*. Preserved in the PDF block; fixed in the runnable code.
> 3. The QA code passes `device="cuda"` (NVIDIA GPU). That errors on a machine without a CUDA GPU (e.g. a Mac), so the runnable file omits it (CPU default).
>
> **Runnable code:** `week2/code/bert_tasks_demo.py` (+ entry in `week2/code/README.md`).

---

## 📑 Table of Contents

1. [What BERT is, and why "bidirectional" matters](#1-what-bert-is-and-why-bidirectional-matters)
2. [Setup — the library, and running a model locally](#2-setup--the-library-and-running-a-model-locally)
3. [The `pipeline()` abstraction — the whole trick](#3-the-pipeline-abstraction--the-whole-trick)
4. [Task 1 — Text classification (sentiment)](#4-task-1--text-classification-sentiment)
5. [Task 2 — Named Entity Recognition (NER)](#5-task-2--named-entity-recognition-ner)
6. [Task 3 — Question answering (extractive)](#6-task-3--question-answering-extractive)
7. [Conclusion](#7-conclusion)
8. [The unifying idea: encoder tasks vs decoder tasks](#8-the-unifying-idea-encoder-tasks-vs-decoder-tasks)
9. [Deep dives beyond the PDF](#9-deep-dives-beyond-the-pdf)
10. [🧵 Connected mental model](#10--connected-mental-model)
11. [⚡ 60-second recap](#11--60-second-recap)
12. [🗂️ Jargon Dictionary](#12--jargon-dictionary)
13. [🧠 Knowledge check](#13--knowledge-check)

---

## 1. What BERT is, and why "bidirectional" matters

### 📄 FROM THE PDF
> The power of **BERT (Bidirectional Encoder Representations from Transformers)** has revolutionized the way we process natural language. BERT's transformer-based architecture understands context from **both the left and right** of a word in a sentence, making it incredibly effective for a variety of NLP tasks. While BERT may sound complex, it's actually pretty simple to use, thanks to tools like Hugging Face's `transformers` library. In this article, we'll walk you through how to use BERT for simple NLP tasks such as text classification, named entity recognition (NER), and question answering.
>
> *Note: Access the colab notebook here.* → https://colab.research.google.com/drive/19JHeS3NBrtXEnDOtHPMlDCb5MAqLEn1- *(the "here" link from the PDF; it opens in Google Colab and may require sign-in. A local, runnable equivalent is in `week2/code/bert_tasks_demo.py`.)*

### 🧠 EXPLAINED
Let's decode the acronym, because every word earns its place:

- **B**idirectional — BERT looks at a word's context on **both sides** at once. In *"I deposited cash at the **bank**,"* it uses both "deposited cash" (left) and any right-side words to decide "bank" = financial, not river.
- **E**ncoder **R**epresentations — BERT is an **encoder** (W1·N01): its job is to *read and understand* text into rich numeric representations (**contextual embeddings**, W2·SG03), **not** to generate new text.
- from **T**ransformers — it's built on the Transformer architecture and its **self-attention** (W1·N01).

🔑 **The one contrast that explains everything in this reading — BERT (encoder) vs GPT (decoder):**

| | **BERT** (this reading) | **GPT** (Week 1 / ChatGPT) |
|---|---|---|
| Half of the Transformer | **Encoder** | **Decoder** |
| Reads context | **Bidirectional** (both sides at once) | **Left-to-right** only (**autoregressive**, W1·N01) |
| Built for | **Understanding** — classify, tag, extract, search | **Generating** — write the next tokens |
| Output | labels / spans / embeddings | new text |
| The three tasks here | ✅ all understanding tasks | (GPT would *generate* answers instead) |

💻 **Java analogy:** BERT is a **parser/analyzer** — it reads input and hands you a structured understanding (like parsing a request into a typed DTO). GPT is a **generator** — it *produces* new output token by token. Why does bidirectional make BERT better at *understanding*? Because to classify or tag a word you can use the *whole* sentence; but to *generate* text left-to-right you must **not** peek at future words (that would be cheating — the future isn't written yet). Different jobs → different designs.

---

## 2. Setup — the library, and running a model locally

### 📄 FROM THE PDF
> **Setting Up the Environment**
> Before diving into the code, let's set up our environment. If you haven't installed the `transformers` and `torch` libraries, you can do so with the following command:
> ```bash
> pip install transformers torch
> ```

### 🧠 EXPLAINED
Two libraries, and this is a **bigger deal than it looks**:

- **`transformers`** — Hugging Face's library (W2·SG01) to download and run thousands of open models. It's the workhorse that turns downloaded weights into a callable model.
- **`torch`** — **PyTorch**, the deep-learning framework (W1·SG02) that actually does the tensor math on CPU/GPU. `transformers` runs *on top of* PyTorch.

> **`PyTorch` (`torch`)** = the numerical engine (tensors + autograd + GPU support) that neural networks run on. 💻 Think of it as the low-level runtime; `transformers` is the high-level framework built on it — roughly **JVM : Spring**.

🌟 **The conceptual milestone:** in Week 1 you *rented* a model over an API (send text → get JSON back; the weights live on OpenAI's servers). Here, `transformers` **downloads the model weights to your machine** (from the **Hugging Face Hub**) and runs them **locally** via PyTorch. **No API key. No network call at inference time. Your data never leaves your box.**

This is *literally* the **open-source, self-hosted** path from W2·SG01 — now concrete. Trade-offs from that guide show up immediately: the first run downloads hundreds of MB of weights, and it's your CPU/GPU doing the work (slower without a GPU) — the "you own the ops/compute" side of the ledger.

> **`Hugging Face Hub`** = the online registry the weights are pulled from (`huggingface.co`). 💻 Like Maven Central resolving a dependency on first build — downloaded and cached locally.

---

## 3. The `pipeline()` abstraction — the whole trick

*(Not a separate PDF section, but the single idea that makes all three tasks one-liners — worth isolating before the tasks.)*

Every task below is just:
```python
from transformers import pipeline
some_task = pipeline("<task-name>")   # or pipeline("<task-name>", model="<id>")
result = some_task(your_input)
```

**`pipeline()` is a facade** that hides the entire messy stack behind one call. When you call it, it silently does **four** things:
1. **Downloads** the right pre-trained model + its tokenizer from the Hub (first time only; cached after).
2. **Tokenizes** your text → token IDs (W1: tokens).
3. **Runs** the model forward pass (via PyTorch) → raw numbers (logits).
4. **Post-processes** those numbers into a **human-friendly result** (a label, a list of entities, an answer string).

💻 **Java analogy:** `pipeline("sentiment-analysis")` is **Spring Boot auto-configuration / a "starter" dependency** — one line wires up a whole preconfigured stack with sensible defaults (convention over configuration). Or a **Facade** pattern hiding the tokenizer + model + decoder subsystems. You *can* drop down and assemble those pieces manually; `pipeline()` is the "just make it work" front door.

> **`pipeline` (Hugging Face)** = a high-level helper that bundles tokenizer + model + pre/post-processing for a named task, so a task takes ~2 lines.

---

## 4. Task 1 — Text classification (sentiment)

### 📄 FROM THE PDF
> **Task 1: Text Classification with BERT**
> Let's start with the most common NLP task: text classification. For this task, we'll use a model to classify whether a sentence expresses a positive or negative sentiment.
> ```python
> from transformers import pipeline
>
> # Load a pre-trained sentiment analysis pipeline
> classifier = pipeline('sentiment-analysis')  # if a model is passed then it will pick DistilBERT by default
>
> # Sample text
> text = "I love using BERT for natural language processing tasks!"
>
> # Get prediction
> result = classifier(text)
> print(result)
> # Output => [{'label': 'POSITIVE', 'score': 0.999876916885376}]
> ```
> In this example, **DistilBERT** (a version of BERT) is used to classify the text as "positive." The `pipeline` function from Hugging Face abstracts away a lot of the complexity, so you only need a few lines of code to get started!

### 🧠 EXPLAINED
**What the task is:** **text classification** = assign a whole piece of text to a category. Here the categories are `POSITIVE` / `NEGATIVE` — that specific flavor is called **sentiment analysis**. This is a *discriminative* task (pick a label), the classic NLP workhorse — and exactly what your Week 1 ticket-triage assignment did for ticket categories (there via an LLM API; here via a local BERT).

**Line by line:**
- `classifier = pipeline('sentiment-analysis')` — no `model=` given, so the pipeline loads its **default**: **DistilBERT** fine-tuned on the SST-2 sentiment dataset (`distilbert-base-uncased-finetuned-sst-2-english`).
  > ⚠️ **Correction:** the PDF's comment says *"if a model is passed then it will pick DistilBERT by default."* That's backwards. The truth: **if you pass *no* model, it falls back to a default (DistilBERT); if you *do* pass one, it uses yours.**
- `result = classifier(text)` — runs the 4 pipeline steps and returns a list of dicts.
- Output `[{'label': 'POSITIVE', 'score': 0.9998...}]` — the predicted **label** plus a **confidence score** in `[0,1]`. `0.9998` = extremely confident it's positive.

> **`DistilBERT`** = a **distilled** (W1·SG04 — a small "student" trained to mimic a big "teacher") version of BERT: ~40% smaller and ~60% faster, keeping ~97% of the quality. It's the default for many pipelines because it's light enough to run comfortably on a CPU.
> **`Sentiment analysis`** = text classification where the labels are emotional polarity (positive/negative/neutral).

---

## 5. Task 2 — Named Entity Recognition (NER)

### 📄 FROM THE PDF
> **Task 2: Named Entity Recognition (NER) with Finetuned BERT**
> Next, let's explore **Named Entity Recognition (NER)**, a task where we identify and classify named entities (like names of people, organizations, or locations) in a text.
> ```python
> # Load a pre-trained NER pipeline
> ner = pipeline('ner', model='dbmdz/bert-large-cased-finetuned-conll03-english')
>
> # Sample text
> text = "India lay down the gauntlet to Australia with 295-run thrashing."
>
> # Get named entities
> entities = ner(text)
> for entity in entities:
>     print(entity)
> """
> Output =>
> {'entity': 'I-LOC', 'score': 0.99978846, 'index': 1, 'word': 'India', 'start': 0, 'end': 5}
> {'entity': 'I-LOC', 'score': 0.99982905, 'index': 9, 'word': 'Australia', 'start': 31, 'end': 40}
> """
> ```
> Here, we have passed a finetuned model by **dbmdz**. The model accurately identifies **India** and **Australia** as **locations**.

### 🧠 EXPLAINED
**What the task is:** **NER** finds the **named entities** in text and labels *what kind* each is — Person (PER), Location (LOC), Organization (ORG), Miscellaneous (MISC). Unlike Task 1 (one label for the *whole* sentence), NER is **token classification**: it labels *each word*. Output: "India" → LOC, "Australia" → LOC.

> **`Named entity`** = a real-world proper noun (a specific person, place, organization, date…). **`NER`** = detecting and typing them. **`Token classification`** = assigning a label to *every token*, not the whole text.

**Reading the output dict:**
- `'word': 'India'` — the token; `'start': 0, 'end': 5` — its character span in the input (`India` occupies chars 0–5); `'index': 1` — its token position; `'score'` — confidence.
- `'entity': 'I-LOC'` — the label. The `I-` prefix is the **IOB/BIO tagging scheme**: `B-` = **B**eginning of an entity, `I-` = **I**nside/continuation, `O` = **O**utside (not an entity). So `I-LOC` = "part of a LOCation span." Multi-word entities like "New York" would tag as `B-LOC` ("New") then `I-LOC` ("York").
  > **`IOB / BIO tagging`** = the labeling convention for spans: Begin / Inside / Outside. It lets a per-token classifier represent multi-word entities.

**Why `model=` is explicit this time:** there's no universally "default" NER model as convenient as the sentiment one, so the reading names a specific fine-tuned model. Decode the ID `dbmdz/bert-large-cased-finetuned-conll03-english`:
- `dbmdz/` — the **owner/org** on the Hub (a Bavarian library's ML team).
- `bert-large` — architecture + size (BERT-large, more parameters than base).
- `cased` — it preserves capitalization (crucial for NER — "Apple" ≠ "apple").
- `finetuned-conll03` — **fine-tuned** (W1·N01) on **CoNLL-2003**, the standard English NER benchmark dataset.
- `english` — the language.
> Reading Hub model IDs is a real skill: `owner / architecture-size-casing-finetunedOn-dataset-language`. It tells you what a model is at a glance.

This is W2·SG02's "few-shot vs fine-tuning" made concrete: NER needs a model whose **weights were actually fine-tuned** on labeled entity data — you couldn't reliably get these exact span tags from prompting alone.

---

## 6. Task 3 — Question answering (extractive)

### 📄 FROM THE PDF
> **Task 3: Question Answering with BERT**
> Now, let's move to question answering, where **DistilBERT** is used to answer a question based on a given context.
> ```python
> # Load a pre-trained question-answering pipeline
> qa = pipeline('question-answering', device="cuda")
>
> # Sample context and question
> context = "India won the first test against Australia"
> question = "Who deafeated Australia in first test?"   # (PDF typo: "deafeated")
>
> # Get the answer
> answer = qa({'context': context, 'question': question})
> print(answer)
> # Output => {'score': 0.5933823585510254, 'start': 0, 'end': 42, 'answer': 'India won the first test against Australia'}
> ```
> Here, the model correctly answers that India won the test, based on the context we provided. Also to use the GPU you can pass `device="cuda"`.

### 🧠 EXPLAINED
**What the task is — and the crucial distinction.** This is **extractive question answering**: given a **context** passage and a **question**, the model **finds and returns the span of the context that answers it.** It does **not** write a new sentence — it **copies a substring** out of the context.

> **`Extractive QA`** = the answer is a *span pulled verbatim from the provided context* (the model predicts a start position and an end position). Contrast **`abstractive / generative QA`** = the model *writes* a fresh answer in its own words (what ChatGPT does).

**Line by line:**
- `qa = pipeline('question-answering', device="cuda")` — loads the default QA model (DistilBERT fine-tuned on the **SQuAD** QA dataset). `device="cuda"` asks it to run on an NVIDIA **GPU**.
  > ⚠️ **Caveat:** `device="cuda"` **errors if you don't have a CUDA GPU** (e.g. on a Mac). Omit it to run on CPU (the runnable file does), or use `device="mps"` on Apple Silicon. `device` selects the hardware; it has nothing to do with the answer.
  > **`CUDA`** = NVIDIA's GPU compute platform; `device="cuda"` = "run on the GPU." (W1·SG02: GPUs are the parallel chips for AI math.)
- `qa({'context': ..., 'question': ...})` — note QA takes a **dict** with both fields, not a bare string.
- Output `{'score': 0.59, 'start': 0, 'end': 42, 'answer': 'India won the first test against Australia'}` — `start`/`end` are **character offsets into the context** (0→42 = the *entire* 42-char context), and `answer` is that exact slice. The model literally pointed at chars 0–42 and said "the answer is there."

**Why the answer is the whole context:** the context is a single short fact, so the best answering span *is* the whole thing — a nice illustration that extractive QA returns *locations in the source*, not composed prose. (The `0.59` score being lower than the near-1.0 scores in Tasks 1–2 reflects that the model is less certain exactly *where* to draw the span, partly because the question's typo "deafeated" makes the match fuzzier.)

💻 **Java analogy:** extractive QA is like `String.substring(start, end)` where a model chose `start`/`end` — it can only ever return text *already present* in the context. Generative QA is like building a brand-new `String` from scratch.

---

## 7. Conclusion

### 📄 FROM THE PDF
> **Conclusion**
> BERT is incredibly easy to use, especially with Hugging Face's `transformers` library. In this article, we've explored three simple tasks with BERT:
> 1. **Text classification** – Identifying the sentiment of a text.
> 2. **Named Entity Recognition (NER)** – Identifying entities like people, locations, and organizations.
> 3. **Question answering** – Extracting specific answers from a provided context.
>
> These tasks are just the beginning of what BERT can do. With Hugging Face, applying state-of-the-art NLP models is as simple as loading a pre-trained pipeline and calling it with your data. The best part? You can **fine-tune** these models to suit your own specific needs.

### 🧠 EXPLAINED
The reading's real lesson isn't the three tasks — it's the **workflow**: *pick a task → load a pre-trained pipeline → call it.* Two lines of code stand on the shoulders of a huge open-source model. And the closing note points to the next level: when a pre-trained model isn't quite right for your domain, you **fine-tune** it (W1·N01) on your own labeled data — exactly what `dbmdz` did to make the NER model.

---

## 8. The unifying idea: encoder tasks vs decoder tasks

Step back: **why is BERT the right tool for *all three* of these tasks?** Because classification, NER, and extractive QA are all **understanding** tasks — they analyze existing text and output labels or spans. That's the **encoder's** wheelhouse. None of them *generate* new prose, which is where you'd reach for a **decoder** (GPT).

| Task | What it outputs | Understanding or generation? | Natural model |
|---|---|---|---|
| Sentiment / text classification | a label | understanding | **encoder (BERT)** |
| NER | per-token labels (spans) | understanding | **encoder (BERT)** |
| Extractive QA | a span from the context | understanding | **encoder (BERT)** |
| Chat / summarize / write code | new text | generation | **decoder (GPT)** |
| Abstractive QA / free-form answers | new text | generation | **decoder (GPT)** |

**Rule of thumb:** *reading/labeling/extracting → encoder (BERT). Writing/creating → decoder (GPT).* Modern practice increasingly uses big decoder LLMs for everything (they can classify too, via prompting), but a small fine-tuned BERT is often **faster, cheaper, and more reliable** for a fixed understanding task at scale — a direct echo of the W2·SG01 trade-offs.

---

## 9. Deep dives beyond the PDF

- **Why not just prompt GPT for these?** You could (that's what Week 1 did for triage). But a specialized BERT is smaller, runs locally with no API cost, gives calibrated confidence scores, and is deterministic — great when you run millions of classifications. GPT wins when you need flexibility, generation, or zero setup. It's the classic *specialist vs generalist* / open-local vs API choice.
- **`pipeline()` hides real complexity.** Under it sit an `AutoTokenizer` and an `AutoModelFor…` class. For control (batching, custom pre/post-processing, truncation), you instantiate those directly. `pipeline()` is the on-ramp, not the ceiling.
- **First-run cost & caching.** The initial call downloads weights to `~/.cache/huggingface`. Subsequent runs are offline and fast. BERT-large (NER model) is several hundred MB — the "storage/ops" cost of self-hosting, live.
- **Confidence scores are per-model, not comparable across tasks.** The `0.9998` sentiment score and the `0.59` QA score come from different heads/objectives — don't compare them directly.
- **Fine-tuning is the sequel.** Every model here is BERT + a small task-specific "head" fine-tuned on a dataset (SST-2, CoNLL-03, SQuAD). Your own domain (legal, medical, your product) → fine-tune the same way. This is the concrete version of W1's fine-tuning and W2·SG03's "custom embeddings."

---

## 10. 🧵 Connected mental model

```
  W1·N01: Transformer ──► Encoder (BERT)      vs   Decoder (GPT)
                              │ understands            │ generates
                              ▼
  W2·SG03: BERT makes CONTEXTUAL EMBEDDINGS (meaning as vectors)
                              │
  W2·SG01: open-source + Hugging Face `transformers`
                              │  pipeline() = download + tokenize + run + post-process
                              ▼
  THIS READING: run BERT LOCALLY (no API) for 3 understanding tasks
       ├─ text classification (sentiment)   → one label for the text
       ├─ NER (token classification, IOB)   → label each token (India→LOC)
       └─ extractive QA (span from context) → substring, not new prose
                              │
                              ▼
  next level: FINE-TUNE (W1) on your own data  →  domain-specific models
```

**One-line thread:** `Transformer → BERT is the encoder (understanding) → it makes contextual embeddings → Hugging Face pipeline() runs it locally → classification / NER / extractive-QA → fine-tune for your domain.`

Back-links: **bidirectional/encoder** (W1·N01), **contextual embeddings** (W2·SG03), **Hugging Face / open-source / self-hosted** (W2·SG01), **distillation → DistilBERT** (W1·SG04), **fine-tuning vs prompting** (W1, W2·SG02), **GPU** (W1·SG02), and text classification mirrors your **Week 1 ticket-triage** task (LLM-API version).

---

## 11. ⚡ 60-second recap

- **BERT = Bidirectional Encoder Representations from Transformers** — an **encoder** that reads context from **both sides** to *understand* text. Encoder = understanding; **GPT/decoder = generation.**
- **Hugging Face `transformers` + `torch`** let you run BERT **locally** — weights download from the **Hub**, run on **PyTorch**, **no API/key**. This is the open-source, self-hosted path from SG01 in action.
- **`pipeline("task")`** is a facade that downloads the model + tokenizes + runs + post-processes in one line (≈ Spring Boot auto-config). No model arg → sensible default (often **DistilBERT**, a distilled = smaller/faster BERT).
- **Task 1 — text classification / sentiment:** whole text → one label + score.
- **Task 2 — NER (token classification):** label *each* token; `I-LOC`/`B-…` = **IOB** span tags; model ID decodes as owner/arch-size-casing-finetunedOn-dataset-lang (`dbmdz/bert-large-cased-finetuned-conll03-english`).
- **Task 3 — extractive QA:** returns a **span (start/end) copied from the context**, not new prose (≈ `substring`). Contrast generative/abstractive QA (GPT). `device="cuda"` = run on GPU (errors without one).
- **All three are *understanding* tasks → BERT's strength.** Need generation → use a decoder. Need a domain fit → **fine-tune**.

---

## 12. 🗂️ Jargon Dictionary

*(New this reading. Reused from earlier without redefining: BERT, Transformer, encoder/decoder, self-attention, autoregressive, fine-tuning, contextual embedding, Hugging Face, GPU, distillation, token, NLP.)*

| Term | Definition |
|---|---|
| **Bidirectional** | Reading a word's context from *both* left and right simultaneously (BERT); vs left-to-right only (GPT). |
| **`transformers` (library)** | Hugging Face's Python library to download and run pre-trained models. |
| **PyTorch (`torch`)** | The deep-learning framework (tensors + GPU math) that models run on; `transformers` sits on top of it. |
| **Hugging Face Hub** | The online registry weights are downloaded/cached from (`huggingface.co`). |
| **`pipeline` (Hugging Face)** | High-level helper bundling tokenizer + model + pre/post-processing for a named task (~2 lines to run). |
| **DistilBERT** | A distilled (smaller/faster, ~97% quality) version of BERT; default in several pipelines. |
| **Text classification** | Assigning a whole piece of text to a category/label. |
| **Sentiment analysis** | Text classification where labels are emotional polarity (positive/negative/neutral). |
| **Named entity** | A real-world proper noun — a specific person, place, organization, date, etc. |
| **Named Entity Recognition (NER)** | Detecting named entities in text and labeling their type (PER/LOC/ORG/MISC). |
| **Token classification** | Assigning a label to *each token* (as in NER), vs one label for the whole text. |
| **IOB / BIO tagging** | Span-labeling scheme: **B**egin / **I**nside / **O**utside; lets per-token labels represent multi-word entities (e.g. `I-LOC`). |
| **CoNLL-2003** | Standard English NER benchmark dataset (people/locations/orgs/misc). |
| **Question answering (QA)** | Answering a question about a text. |
| **Extractive QA** | The answer is a span pulled *verbatim* from the provided context (predict start/end). |
| **Abstractive / generative QA** | The model *writes* a fresh answer in its own words (GPT-style), not copied from context. |
| **CUDA** | NVIDIA's GPU compute platform; `device="cuda"` runs a pipeline on the GPU. |
| **SQuAD** | Standard extractive-QA benchmark dataset (Stanford Question Answering Dataset). |

---

## 13. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. What does the "B" in BERT stand for, and why is that property helpful for *understanding* tasks but *not* used for left-to-right text generation?
2. In one sentence each, what does `pipeline()` do, and why is passing no `model=` still enough to run Task 1?
3. What's the difference between text classification and NER in terms of *what gets a label*?

**Applied**
4. In the NER output, `India` is tagged `I-LOC`. Explain what `I-LOC` means and how the tag for the first word of "New York" would differ.
5. Extractive QA returned the *entire* context as the answer with `start:0, end:42`. Explain why, and how this would differ if ChatGPT (a decoder) answered the same question.
6. You run `bert_tasks_demo.py` on your Mac and Task 3 crashes. Given the code, what's the most likely line, and what's the fix?

**Interview-style**
7. When would you choose a small fine-tuned BERT over prompting GPT-4 for a classification task, and vice-versa? Tie it to the open-vs-closed trade-offs from SG01.
8. Decode the model ID `dbmdz/bert-large-cased-finetuned-conll03-english` piece by piece.

---

*End of Study Guide 02·04. Next Week 2 reading → paste it and I'll build Study Guide 02·05, extending the glossary and this mental model.*
