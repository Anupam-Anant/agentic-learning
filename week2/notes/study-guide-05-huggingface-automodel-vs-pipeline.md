# Study Guide 02·05 — Hugging Face: `AutoModel` vs `pipeline`

> **Source:** Week 2 notebook — `HuggingFace_Pipeline.ipynb` (provided locally). Unlike the earlier readings, the source here is a **Jupyter notebook**, so the original-text blocks below are labelled **`📓 FROM THE NOTEBOOK`** and reproduce the actual cell code + its real output.
> **Where it fits in the course:** This is the **capstone of the Hugging Face thread.** SG04 used the one-line `pipeline()` and I noted *"under it sit an `AutoTokenizer` and an `AutoModelFor…` class… `pipeline()` is the on-ramp, not the ceiling."* **This notebook shows both floors of the building side by side:** the manual `AutoModel` path (you drive tokenize → generate → decode yourself) *and* the `pipeline` facade. It also runs **Phi-3, a generative *decoder* model**, so it's the concrete counterpart to BERT (an encoder, SG04) and a live demo of **autoregressive** generation.
>
> **How to read this file:** Self-contained. Each section pairs:
> - 📓 **`FROM THE NOTEBOOK`** — the real cell code/output (trimmed download-progress noise).
> - 🧠 **`EXPLAINED`** — line-by-line teaching, 💻 Java/backend analogies, and the "why."
>
> **Three faithfulness notes** (per our repo rule to flag anything):
> 1. Cell 12's comment `# Translate sentences from Hindi to English` is a **leftover/wrong comment** — the code is English **sentiment classification**, not translation. Flagged in [§B2](#b2--run-it).
> 2. `device_map="cuda"` (cells 4–5) needs an **NVIDIA GPU** — it errors on a Mac. Fixes in [§9](#9-deep-dives-beyond-the-notebook).
> 3. The notebook's own output shows `temperature` was **ignored** during generation — a real subtlety explained in [§A6](#a6--run-predict-and-the-temperature-warning).

---

## 📑 Table of Contents

- **Part A — Using `AutoModel` (the manual path)**
  1. [Imports & setup](#a1--imports--setup)
  2. [Load the model — Phi-3](#a2--load-the-model--phi-3)
  3. [Load the tokenizer](#a3--load-the-tokenizer)
  4. [The `messages` chat format](#a4--the-messages-chat-format)
  5. [Peeking inside the tokenizer](#a5--peeking-inside-the-tokenizer)
  6. [The `predict()` function + the temperature warning](#a6--the-predict-function--and-the-temperature-warning)
- **Part B — Using `pipeline` (the facade)**
  1. [Load the pipeline](#b1--load-the-pipeline)
  2. [Run it](#b2--run-it)
- [The core lesson: `AutoModel` vs `pipeline`](#7-the-core-lesson-automodel-vs-pipeline)
- [Encoder vs decoder, revisited (Phi-3 vs BERT)](#8-encoder-vs-decoder-revisited-phi-3-vs-bert)
- [Deep dives beyond the notebook](#9-deep-dives-beyond-the-notebook)
- [🧵 Connected mental model](#10--connected-mental-model)
- [⚡ 60-second recap](#11--60-second-recap)
- [🗂️ Jargon Dictionary](#12--jargon-dictionary)
- [🧠 Knowledge check](#13--knowledge-check)

---

# Part A — Using `AutoModel` (the manual path)

## A1 · Imports & setup

### 📓 FROM THE NOTEBOOK
```python
# !pip install transformers
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import warnings
warnings.filterwarnings("ignore")

# Set the random seed for reproducibility
torch.random.manual_seed(0)   # -> <torch._C.Generator at 0x...>
```

### 🧠 EXPLAINED
- `import torch` — **PyTorch** (W2·SG04), the numeric engine everything runs on.
- `from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline` — three key imports:
  - **`AutoModelForCausalLM`** — loads a **causal language model** (a generative, *autoregressive* decoder — see [§8](#8-encoder-vs-decoder-revisited-phi-3-vs-bert)).
  - **`AutoTokenizer`** — loads the matching tokenizer.
  - **`pipeline`** — the high-level facade from SG04 (used in Part B).
- `warnings.filterwarnings("ignore")` — silence noisy deprecation/info warnings (cosmetic).
- `torch.random.manual_seed(0)` — fix the **random seed** so any randomness (e.g. sampling) is **reproducible** run-to-run. Same seed → same "random" choices.
  > **`Random seed`** = the starting number for a pseudo-random generator; fixing it makes stochastic output repeatable. 💻 Like `new Random(0)` in Java — same seed, same sequence.

> **The `Auto*` classes are a factory pattern.** `AutoModelForCausalLM.from_pretrained("...")` doesn't hard-code *which* model class to build — it **reads the model's `config.json` and instantiates the correct concrete class** (Phi-3's, Llama's, Mistral's…) for you. 💻 Exactly Java's **Factory / `Class.forName()` + reflection / `ServiceLoader`**: you ask for "the model for this id," and the framework resolves the right implementation from config. This is why the *same two lines* load almost any model on the Hub.

---

## A2 · Load the model — Phi-3

### 📓 FROM THE NOTEBOOK
```python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",      # comment to use CPU
    torch_dtype="auto",     # Automatically selects the appropriate data type
    # trust_remote_code=True,
)
# downloads: config.json, model.safetensors(.index.json), generation_config.json ...
```

### 🧠 EXPLAINED
`from_pretrained(...)` downloads the weights from the **Hugging Face Hub** (W2·SG04) and builds the model in memory. Decoding what's here:

- **Model ID `microsoft/Phi-3-mini-4k-instruct`** — read it the SG04 way:
  - `microsoft` — owner/org on the Hub.
  - `Phi-3` — Microsoft's family of **Small Language Models (SLMs)**.
  - `mini` — the smallest size (~3.8B parameters).
  - `4k` — a **4096-token context window** (W1·N01 — how much it can attend to at once).
  - `instruct` — **instruction-tuned**: fine-tuned to follow instructions / chat (vs a raw "base" model that only autocompletes). This is why you can talk to it.
  > **`Small Language Model (SLM)`** = a compact LLM (a few billion params) meant to run cheaply, even locally. The open-source, "own-it" side of W2·SG01, at laptop scale.
  > **`Instruction-tuned (instruct) model`** = a base LLM further fine-tuned on instruction/response (and often chat) data so it follows requests helpfully.
- `device_map="cuda"` — place the model on the **GPU** (W1·SG02 / SG04 `CUDA`). ⚠️ **Errors without an NVIDIA GPU.** The inline comment even says *"comment to use CPU."* On a Mac, drop it (CPU) or try `device_map="mps"` (Apple Silicon). *(Also note Phi-3-mini is several GB to download.)*
- `torch_dtype="auto"` — pick the numeric **precision** automatically (e.g. `bfloat16` on GPU vs `float32` on CPU). Lower precision = less memory + faster — the same idea as **quantization** (W1·SG04), here just choosing the storage type.
  > **`torch_dtype` / dtype** = the numeric type weights are stored/computed in (float32/float16/bfloat16). Trades precision for speed & memory.
- `# trust_remote_code=True` (commented) — some models ship custom Python on the Hub; this flag would allow running it. Left off here.
- **`.safetensors`** (in the download list) = the modern, safe file format for weights (can't execute arbitrary code on load, unlike old pickle files).

---

## A3 · Load the tokenizer

### 📓 FROM THE NOTEBOOK
```python
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct", device_map="cuda")
# downloads: tokenizer_config.json, tokenizer.json, tokenizer.model,
#            added_tokens.json, special_tokens_map.json
```

### 🧠 EXPLAINED
A model can't read text — it reads **numbers**. The **tokenizer** is the translator between the two, and it must **match the model** (each model was trained with its own vocabulary), which is why you load it from the *same* ID.

> **`Tokenizer`** = the component that converts text ↔ **token IDs** (integers). 💻 Think a **codec / serializer**: `String` → `int[]` on the way in, `int[]` → `String` on the way out. Text → tokens → IDs is the W1 pipeline made literal.

The downloaded files define the vocabulary and rules: `tokenizer.model`/`tokenizer.json` hold the vocab & merge rules; `special_tokens_map.json` and `added_tokens.json` define **special tokens** (like end-of-text, or chat markers `<|user|>`/`<|assistant|>` — see [§A6](#a6--the-predict-function--and-the-temperature-warning)).
> **`Special tokens`** = reserved tokens that aren't ordinary words — they mark structure (start/end, turn boundaries, padding).

---

## A4 · The `messages` chat format

### 📓 FROM THE NOTEBOOK
```python
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
    {"role": "assistant", "content": "Sure! Here are some ways ... 1. smoothie ... 2. salad ..."},
    {"role": "user", "content": "What about solving a 2x + 3 = 7 equation?"},
]
```

### 🧠 EXPLAINED
This is the **roles format** from W1·SG03 (`system` / `user` / `assistant`), here as a plain Python list of dicts. It encodes a **multi-turn conversation**: a system instruction, a prior user question, the assistant's prior answer, then a new user question. Including the earlier turns is how the model gets **conversation history** (contrast Week 1's server-side `previous_response_id` — here *you* hold the history in a list).

⚠️ But a raw model can't consume this list directly — it needs the turns flattened into **one specially-formatted string** with the model's own chat markers. That conversion is the job of the **chat template** in `predict()` below. (This particular `messages` block is illustrative; the `predict()` function builds its own.)

> 🧩 **Callout — why the model can't just read the `messages` list (the part that trips everyone up)**
>
> **The one fact that unlocks it:** a language model understands exactly *one* kind of input — **a single flat sequence of tokens.** Its interface is effectively `String generate(String oneFlatPrompt)`. There is **no parameter for "a list of messages"** and it has no concept of `role`. So a structured conversation *must* be converted into one string first.
>
> 💻 **Java analogy — serialization / wire format.** You have a clean `List<Message>` of DTOs in code, but you can't push Java objects down a socket — you **serialize** them to a specific wire format (JSON, protobuf…) that the other end expects. Same here:
> - `messages` list = your structured **DTOs** (convenient for *you*).
> - the model's "wire format" = **one flat string with special marker tokens**.
> - `apply_chat_template` = the **serializer** that flattens one into the other.
>
> **Before → after** (`apply_chat_template` on Phi-3 produces roughly):
> ```
> <|system|>
> You are a helpful assistant.<|end|>
> <|user|>
> What about solving 2x + 3 = 7?<|end|>
> <|assistant|>
> ```
> Those `<|system|>`/`<|user|>`/`<|assistant|>`/`<|end|>` markers are the **delimiters that preserve "who said what"** once the list is flattened — exactly like `\r\n` + the blank line separate headers from body in a raw HTTP request. Strip them and the model just sees a mushy blob with no turn boundaries.
>
> **Why the model obeys the markers:** it was **trained** on text containing them, so it learned "after `<|assistant|>`, it's my turn." That's also **why the template is model-specific** — Phi-3 uses `<|user|>`, Llama uses `[INST]…[/INST]`, Mistral differs again — so you let `apply_chat_template` read the model's own template rather than hand-writing markers. The trailing `<|assistant|>` (with nothing after it) is the "your turn now" cue that `add_generation_prompt=True` adds.
>
> **Why Week 1 never made you think about this:** you sent `messages` to the OpenAI *API* and it applied the chat template **server-side, invisibly**. Running a raw model locally, *you* are the infrastructure — `apply_chat_template` is you doing that hidden step by hand.

---

## A5 · Peeking inside the tokenizer

### 📓 FROM THE NOTEBOOK
```python
tokenizer("What about solving a 2x + 3 = 7 equation?")
# {'input_ids': [1724, 1048, 17069, 263, 29871, 29906, 29916, 718, 29871,
#                29941, 353, 29871, 29955, 6306, 29973],
#  'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}
```

### 🧠 EXPLAINED
This one line demystifies "tokenization." Calling the tokenizer on a string returns a dict:

- **`input_ids`** — the text as a list of **token IDs** (integers indexing the model's vocabulary). The 8-word sentence became **15 tokens** — more tokens than words, because tokenizers split on **subwords** (e.g. `2x` and punctuation become their own pieces). Each number is "the vocabulary index of this piece."
  > **`Token ID` / `input_ids`** = the integer indices the model actually consumes; the tokenizer's output.
- **`attention_mask`** — a list of `1`s (and `0`s) marking which positions are **real tokens vs padding**. All `1`s here = no padding, every token is real. When you batch sentences of different lengths, shorter ones get padded and those positions get `0` so the model **ignores** them.
  > **`attention_mask`** = a 0/1 vector telling the model which tokens to pay attention to (1) vs ignore as padding (0). 💻 Like a validity bitmask over a fixed-length buffer.

---

## A6 · The `predict()` function — and the temperature warning

### 📓 FROM THE NOTEBOOK
```python
def predict(input_prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that assists users to find the correct methods/approach for security within an organization."},
        {"role": "user", "content": input_prompt}
    ]

    # 1) format messages into the model's chat string
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)

    # 2) tokenize to PyTorch tensors, move to the model's device
    model_inputs = tokenizer([text], return_tensors="pt")
    model_inputs = {k: v.to(model.device) for k, v in model_inputs.items()}

    # 3) autoregressive generation
    generated_ids = model.generate(**model_inputs, max_new_tokens=4096, temperature=0.2)

    # 4) slice off the prompt tokens, keep only the new ones
    generated_ids = [out[len(inp):] for inp, out in zip(model_inputs["input_ids"], generated_ids)]

    # 5) decode IDs back to text
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

print(predict("What about solving a 2x + 3 = 7 equation?"))
```
Real output (abridged):
```
[transformers] The following generation flags are not valid and may be ignored: ['temperature'].
To solve the linear equation 2x + 3 = 7, follow these steps:
1. Subtract 3 from both sides: 2x = 4
2. Divide both sides by 2: x = 2
So, the solution ... is x = 2.
```

### 🧠 EXPLAINED
**This function *is* everything `pipeline()` hides — done by hand.** Five steps:

**1) `apply_chat_template(messages, tokenize=False, add_generation_prompt=True)`** — turns the list of role/content dicts into the **one formatted string** Phi-3 expects, inserting the model's **special chat tokens** around each turn (Phi-3 uses markers like `<|system|> … <|end|> <|user|> … <|end|> <|assistant|>`).
- `tokenize=False` → return the *string* (not IDs yet), so you can see/inspect it.
- `add_generation_prompt=True` → append the opening `<|assistant|>` marker so the model knows **"now it's your turn to speak."** Without it, the model might not start a fresh answer.
  > **`Chat template`** = the model-specific rule that serializes a `messages` list into the exact prompt string (with special tokens) the model was trained on. 💻 Like serializing DTOs into the precise wire format an API requires — every model family has its own "protocol."

**2) Tokenize → tensors → device.**
- `tokenizer([text], return_tensors="pt")` → the `input_ids`/`attention_mask` from [§A5](#a5--peeking-inside-the-tokenizer), but as **PyTorch tensors** (`"pt"`) instead of plain lists, because the model consumes tensors.
  > **`Tensor`** = an n-dimensional array (the fundamental data unit in PyTorch). `return_tensors="pt"` = "give me PyTorch tensors."
- `{k: v.to(model.device) ...}` → move the input tensors onto the **same device** (GPU/CPU) as the model, or the math can't run.

**3) `model.generate(**model_inputs, max_new_tokens=4096, temperature=0.2)`** — the **autoregressive loop** you just learned: predict next token → append → repeat, up to **`max_new_tokens=4096`** new tokens (or until an end token).
  > **`max_new_tokens`** = cap on how many tokens to *generate* (distinct from the total context). ≈ W1's `max_output_tokens`.

  ⚠️ **The temperature warning — a real lesson.** The output literally says `temperature ... may be ignored`. Why? By default `generate()` does **greedy decoding** — it always takes the single most-likely next token (deterministic). **`temperature` only matters when sampling is on** (`do_sample=True`). Passing `temperature=0.2` *without* `do_sample=True` → it's ignored, and you get greedy output.
  > **`Greedy decoding`** = always pick the highest-probability next token (deterministic). **`Sampling` (`do_sample=True`)** = draw the next token *randomly* from the probability distribution; **`temperature`** then scales how adventurous that draw is (low = safe/greedy-ish, high = creative/wild). To actually use `temperature=0.2` here you'd pass `do_sample=True`.
  This is the flip side of the **autoregressive** picture: at each step the model produces a probability distribution; greedy vs sampling is *how you pick* from it.

**4) Slice off the prompt.** `generate()` returns the **whole sequence = input prompt tokens + newly generated tokens**. `out[len(inp):]` drops the echoed prompt so you keep only the new completion. 💻 Like the response echoing your request back — you `substring` past it to get just the answer.

**5) `batch_decode(..., skip_special_tokens=True)`** — turn the output token IDs **back into a string** (the tokenizer in reverse), dropping special tokens like `<|end|>`. `[0]` takes the first (only) result.

**The payoff:** the model, given "solve 2x + 3 = 7," produced a clean step-by-step solution ending `x = 2`. Notice it laid out the steps itself — instruction-tuned models tend to "show their work" (a natural, un-prompted flavor of the **Chain-of-Thought** from SG02).

---

# Part B — Using `pipeline` (the facade)

## B1 · Load the pipeline

### 📓 FROM THE NOTEBOOK
```python
classifier = pipeline("text-classification",
                      model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
```

### 🧠 EXPLAINED
Now the **contrast**. This is the SG04 one-liner: pick a task (`"text-classification"`) and a model, and `pipeline()` internally does the *entire* Part-A dance for you — load model **and** tokenizer, tokenize, run, post-process. Here the model is passed **explicitly** (`distilbert-base-uncased-finetuned-sst-2-english` — DistilBERT fine-tuned on SST-2 sentiment), rather than relying on the default as in SG04. `"text-classification"` and `"sentiment-analysis"` map to the same underlying task.

---

## B2 · Run it

### 📓 FROM THE NOTEBOOK
```python
# Translate sentences from Hindi to English      # <-- leftover/wrong comment (see note)
print(classifier("This movie is disgustingly good !"))
print(classifier("Director tried too much."))
# [{'label': 'POSITIVE', 'score': 0.9998536109924316}]
# [{'label': 'NEGATIVE', 'score': 0.9963768124580383}]
```

### 🧠 EXPLAINED
One call each, and out comes `label` + confidence `score` — no tokenizing, generating, slicing, or decoding in *your* code. That's the whole point of the facade.

- `"This movie is disgustingly good !"` → **POSITIVE (0.9998)** — a nice demo of *contextual* understanding: "disgustingly" is negative in isolation, but the model reads "disgustingly good" as intense praise (contextual embeddings, W2·SG03, at work).
- `"Director tried too much."` → **NEGATIVE (0.996)**.

⚠️ **Faithfulness flag:** the comment `# Translate sentences from Hindi to English` is **wrong** — a copy-paste leftover. This code does **English sentiment classification**, not translation, and the sentences are English. Ignore the comment.

---

## 7. The core lesson: `AutoModel` vs `pipeline`

Part A and Part B do fundamentally the same thing (run a model on text) at **two levels of abstraction** — this is *the* takeaway of the notebook:

| | **`AutoModel` (Part A, manual)** | **`pipeline` (Part B, facade)** |
|---|---|---|
| Lines of your code | ~6 steps (template → tokenize → generate → slice → decode) | ~2 (create, call) |
| Control | **Full** — every knob: chat template, `max_new_tokens`, sampling, device, batching | **Limited** — sensible defaults, few knobs |
| You must know about | tokens, tensors, devices, generation params, decoding | almost nothing |
| Best for | custom generation, research, production tuning, non-standard flows | quick standard tasks, prototypes |
| 💻 Java analogy | **hand-wiring beans / using the raw SDK** | **Spring Boot starter / auto-configuration** |

**Rule of thumb:** reach for **`pipeline`** first (it's the on-ramp); drop to **`AutoModel`** when you need control `pipeline` won't give you — exactly the "convenience vs control" spectrum from W2·SG01, now inside one library. `pipeline()` is literally `AutoModel` + `AutoTokenizer` + pre/post-processing bundled together.

---

## 8. Encoder vs decoder, revisited (Phi-3 vs BERT)

The notebook quietly demonstrates **both halves of the Transformer** (W1·N01, SG04 §8):

| | **Phi-3** (Part A) | **DistilBERT** (Part B) |
|---|---|---|
| Loaded via | `AutoModelForCausalLM` | `pipeline("text-classification")` (a BERT encoder) |
| Transformer half | **Decoder** | **Encoder** |
| Objective | **Causal LM** = predict next token, **autoregressive**, left-to-right | Understand text → a label |
| Does | **generates** new text (the math solution) | **classifies** (POSITIVE/NEGATIVE) |

> **`Causal language modeling (Causal LM)`** = training/using a model to predict the **next** token from previous tokens only — the **autoregressive**, generative objective. `AutoModelForCausalLM` = "load the autoregressive generator." ("Causal" = a token may only depend on the *past*, never the future — the left-to-right constraint you learned makes generation possible.)

So the class name you import tells you the model's *nature*: `...ForCausalLM` → a GPT-style **generator**; a `text-classification` pipeline → a BERT-style **understander**. Same library, opposite jobs — the encoder/decoder split, in code.

---

## 9. Deep dives beyond the notebook

- **Run it on a Mac (no CUDA).** Remove `device_map="cuda"` from cells 4–5 (defaults to CPU), or use `device_map="mps"` on Apple Silicon. Phi-3-mini is a multi-GB download and slow on CPU — for a light local test, the Part-B DistilBERT pipeline is far cheaper.
- **The temperature gotcha, generalized.** `model.generate(...)` defaults to **greedy** (deterministic). Sampling params (`temperature`, `top_p`, `top_k`) do nothing unless `do_sample=True`. If you *want* varied output, set `do_sample=True`; if you want repeatable output, greedy (or `temperature` unused) is fine and the `manual_seed(0)` guards any remaining randomness.
- **Why load the tokenizer separately from the model?** They're a matched pair but distinct objects: the tokenizer is pure text↔ID logic (fast, CPU), the model is the heavy neural net. `pipeline` just hides that they're two pieces.
- **Chat templates are model-specific.** Phi-3, Llama, and Mistral each use different special-token formats. `apply_chat_template` reads the template shipped with the tokenizer so you don't hard-code any of it — do **not** hand-build these strings.
- **`AutoModelFor…` variants.** There's a family: `AutoModelForCausalLM` (generation), `AutoModelForSequenceClassification` (classification), `AutoModelForTokenClassification` (NER), `AutoModelForQuestionAnswering` (extractive QA). Each is the manual-path counterpart of an SG04 `pipeline` task.
- **This is still the open-source / self-hosted path (W2·SG01).** No API, no key; weights on your disk; your compute. The cost is the multi-GB download and needing a GPU for comfort.

---

## 10. 🧵 Connected mental model

```
  Hugging Face `transformers`
        │
        ├── HIGH LEVEL:  pipeline("task")            ← SG04, and Part B here
        │        (facade: load model+tokenizer → tokenize → run → post-process)
        │
        └── LOW LEVEL:   AutoModelFor… + AutoTokenizer ← Part A here
                 └─ you do it by hand:
                    messages ─apply_chat_template─▶ text
                       └─tokenizer─▶ input_ids + attention_mask (tensors, on device)
                            └─model.generate (AUTOREGRESSIVE loop, greedy/sampled)─▶ ids
                                 └─slice off prompt ─ batch_decode ─▶ text

  Model NATURE decides the class:
     AutoModelForCausalLM  → DECODER  → Phi-3 → GENERATE  (autoregressive)   [Part A]
     text-classification   → ENCODER  → BERT  → CLASSIFY                     [Part B]
```

**One-line thread:** `pipeline() is AutoModel + AutoTokenizer + glue. Manual path = template → tokenize → generate → slice → decode. CausalLM = decoder = autoregressive generation (Phi-3); classification = encoder (BERT).`

Back-links: **pipeline / transformers / local self-hosting** (SG04, SG01), **roles/messages** (W1·SG03), **tokens/tokenizer** (W1), **autoregressive / encoder-decoder** (W1·N01 + your autoregressive Q), **temperature/sampling** (W2·SG02), **context window & fine-tuning/instruct** (W1), **quantization ≈ dtype** (W1·SG04).

---

## 11. ⚡ 60-second recap

- **Two levels to run a model:** low-level **`AutoModel` + `AutoTokenizer`** (you drive every step) vs high-level **`pipeline`** (facade doing it all). `pipeline` = `AutoModel` + tokenizer + pre/post-processing. Java: **raw SDK vs Spring Boot starter.**
- **`Auto*` = factory pattern:** `from_pretrained(id)` reads the model's config and builds the right class, so two lines load almost any model.
- **Part A runs Phi-3** — a **Small Language Model**, **instruction-tuned**, loaded via **`AutoModelForCausalLM`** = a **decoder** doing **causal LM = autoregressive** generation.
- **Manual generation flow:** `messages` → **`apply_chat_template`** (adds model-specific special tokens; `add_generation_prompt=True`) → tokenize to **tensors** (`input_ids` + `attention_mask`) on the model **device** → **`model.generate`** (autoregressive, `max_new_tokens`) → **slice off the prompt** → **decode**.
- **Tokenizer peek:** text → `input_ids` (subword integer IDs; 8 words → 15 tokens) + `attention_mask` (1 = real, 0 = padding).
- **Temperature was ignored** because `generate()` defaults to **greedy**; sampling params need **`do_sample=True`**.
- **Part B `pipeline("text-classification", model=distilbert-…sst-2)`** does the same dance in one call → sentiment `POSITIVE/NEGATIVE` + score.
- **Class name = model nature:** `…ForCausalLM` → generator (decoder); `text-classification` → understander (encoder).
- ⚠️ `device_map="cuda"` needs a GPU; the "Hindi to English" comment is a wrong leftover (it's sentiment classification).

---

## 12. 🗂️ Jargon Dictionary

*(New this reading. Reused without redefining: pipeline, transformers, PyTorch, DistilBERT, text classification, Hugging Face Hub, tokens, roles/system/user/assistant, autoregressive, encoder/decoder, temperature, context window, fine-tuning, quantization.)*

| Term | Definition |
|---|---|
| **`AutoModel` / `AutoModelForCausalLM`** | Factory classes that load the correct model class from a Hub id; `…ForCausalLM` loads an autoregressive (generative) decoder. |
| **`AutoTokenizer`** | Factory class that loads the tokenizer matching a given model id. |
| **Auto classes (factory)** | The `Auto*` pattern: `from_pretrained(id)` reads config and instantiates the right concrete class. |
| **Tokenizer** | Converts text ↔ token IDs; must match the model. (💻 a codec: `String` ↔ `int[]`.) |
| **Token ID / `input_ids`** | The integer vocabulary indices the model consumes (the tokenizer's numeric output). |
| **`attention_mask`** | 0/1 vector marking real tokens (1) vs padding to ignore (0). |
| **Special tokens** | Reserved non-word tokens marking structure (end-of-text, chat-turn markers, padding). |
| **Chat template / `apply_chat_template`** | Model-specific rule serializing a `messages` list into the exact prompt string (with special tokens) the model expects. |
| **`add_generation_prompt`** | Flag that appends the assistant-turn marker so the model starts a new reply. |
| **Causal language modeling (Causal LM)** | Predicting the next token from previous tokens only — the autoregressive, generative objective. |
| **Small Language Model (SLM)** | A compact LLM (few-billion params) meant to run cheaply/locally (e.g. Phi-3-mini). |
| **Instruction-tuned (instruct) model** | A base LLM fine-tuned to follow instructions/chat (vs a raw autocomplete base model). |
| **Tensor / `return_tensors="pt"`** | An n-dimensional array (PyTorch's data unit); `"pt"` returns PyTorch tensors. |
| **`device_map` / device** | Where the model/tensors run — `"cuda"` (NVIDIA GPU), `"mps"` (Apple), or CPU. |
| **`torch_dtype` (dtype)** | Numeric precision of weights/compute (float32/float16/bfloat16); trades precision for speed & memory. |
| **`model.generate()`** | The method that runs the autoregressive generation loop. |
| **`max_new_tokens`** | Cap on how many *new* tokens to generate. |
| **Greedy decoding** | Always pick the most-likely next token (deterministic; `generate`'s default). |
| **Sampling / `do_sample=True`** | Draw the next token randomly from the distribution; enables `temperature`/`top_p`/`top_k`. |
| **Random seed (`manual_seed`)** | Fixes the pseudo-random generator so stochastic output is reproducible. |
| **safetensors** | Modern, safe weight-file format (no arbitrary code execution on load). |
| **Phi-3** | Microsoft's family of small, instruction-tuned open LLMs (this notebook uses `Phi-3-mini-4k-instruct`). |

---

## 13. 🧠 Knowledge check

Answer in your own words — reply and I'll grade, explaining mistakes rather than just giving answers.

**Conceptual**
1. In one sentence each, what do `pipeline` and `AutoModel` give you, and what's the trade-off between them?
2. What does `AutoModelForCausalLM` tell you about the *kind* of model Phi-3 is, and how does that differ from the DistilBERT used in Part B?
3. Why does the manual path need `apply_chat_template` at all — why can't you pass the `messages` list straight to `model.generate`?

**Applied**
4. List, in order, the five things `predict()` does that `pipeline()` would otherwise hide.
5. The notebook printed a warning that `temperature` was ignored, yet still produced a correct answer. Explain *why* it was ignored and what one change would make `temperature=0.2` take effect.
6. You run cell 4 on your MacBook and it errors. Which argument is the culprit and what are two ways to fix it?

**Interview-style**
7. Tokenizing "What about solving a 2x + 3 = 7 equation?" gave 15 `input_ids` for an 8-word sentence. Explain why there are more IDs than words, and what `attention_mask` all-`1`s means.
8. A teammate hand-builds the Phi-3 prompt string with `<|user|>`/`<|assistant|>` markers themselves. Why is that fragile, and what should they use instead?

---

*End of Study Guide 02·05. Next Week 2 material → paste it (PDF text, notebook path, or screenshots) and I'll build Study Guide 02·06, extending the glossary and this mental model.*
