# Study Guide 03·03b — LangChain Notebooks: Cell-by-Cell Walkthrough

> **Source:** The three Colab notebooks that accompany Week 3 Reading 03 (LangChain):
> `Langchain_Setup_and_Simple_Chain.ipynb` · `Langchain_Chains.ipynb` · `Langchain_LCEL.ipynb`.
> **Where it fits:** Companion to **[Study Guide 03·03 (LangChain)](study-guide-03-langchain-framework.md)** — that guide teaches the *concepts*; this file explains the *original notebook code*, every meaningful line. The **runnable, local-friendly** versions live in `week3/code/` (`langchain_simple_chain_demo.py`, `langchain_sequential_chain_demo.py`, `langchain_lcel_demo.py`, + shared `langchain_model.py`).
>
> **How to read this file:** Self-contained. For each notebook we go cell by cell:
> - 📓 **`CELL`** — the original code, cleaned.
> - 🧠 **`EXPLAINED`** — what each line does, why, and 💻 Java/backend analogies.
>
> New terms are **bolded and defined on first use**; most were introduced in [SG03](study-guide-03-langchain-framework.md) or W2·SG05 (Hugging Face) — this file adds the notebook-specific ones (quantization, tokenizer padding, etc.).

---

## 📑 Table of Contents

1. [Notebook 1 — Setup & Simple Chain](#1-notebook-1--setup--simple-chain)
2. [Notebook 2 — "Sequential" Chain (local quantized model)](#2-notebook-2--sequential-chain-local-quantized-model)
3. [Notebook 3 — LCEL (fan-out / fan-in)](#3-notebook-3--lcel-fan-out--fan-in)
4. [The three notebooks as one arc](#4-the-three-notebooks-as-one-arc)
5. [🗂️ New jargon from the notebooks](#5--new-jargon-from-the-notebooks)

---

## 1. Notebook 1 — Setup & Simple Chain

The "hello world" of LangChain: fill a prompt template, call a model, print the reply.

### Cell 0 — install
```python
!pip install langchain cohere langchain_community langchain-cohere langchain-classic
```
🧠 The `!` prefix runs a **shell command** from inside a notebook cell. Why so many packages — and why LangChain is split up:

| Package | What it is |
|---|---|
| `langchain` | Umbrella package (chains, high-level helpers) |
| `cohere` | Cohere's **own** SDK (the raw client LangChain wraps) |
| `langchain_community` | Community-maintained integrations |
| `langchain-cohere` | The **Cohere ↔ LangChain adapter** (gives you `ChatCohere`) |
| `langchain-classic` | Where the **deprecated** `LLMChain` now lives (moved out of core) |

💻 The split mirrors Spring's `spring-core` vs `spring-web` vs `spring-data-*` — install only the integrations you use. That `LLMChain` was exiled to `langchain-classic` is your first hint it's legacy.

### Cell 1 — imports
```python
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere
```
🧠
- **`LLMChain`** — the old, pre-LCEL way to bind a prompt + model into one callable. Deprecated.
- **`PromptTemplate`** — a parameterized prompt (`{variables}` filled at runtime); lives in `langchain_core` as a foundational abstraction.
- **`ChatCohere`** — LangChain's wrapper around Cohere's chat model. The **JDBC-driver** pattern from [SG03 §2](study-guide-03-langchain-framework.md): swap `ChatCohere`→`ChatOpenAI`, same interface.

### Cell 2 — the secret
```python
from google.colab import userdata
```
🧠 **`userdata`** is **Colab's secret store** (the 🔑 icon in Colab's sidebar); `userdata.get('COHERE_KEY')` fetches a saved API key without hardcoding it. 💻 Colab's version of an **environment variable / secrets manager** — same reason you `export OPENAI_API_KEY` locally. *(The runnable version swaps this for an env var, since `google.colab` doesn't exist off Colab.)*

### Cell 3 — build the chain
```python
prompt_template = "Tell me a {adjective} joke"
prompt = PromptTemplate(input_variables=["adjective"], template=prompt_template)
llm = LLMChain(
    llm=ChatCohere(cohere_api_key=userdata.get('COHERE_KEY'), model="command-a-03-2025"),
    prompt=prompt, verbose=True)
```
🧠
- `{adjective}` is a **placeholder**; `input_variables=["adjective"]` declares it. 💻 A `PreparedStatement` with one bind-parameter.
- `ChatCohere(..., model="command-a-03-2025")` builds the model client for a specific Cohere model.
- `LLMChain(llm=..., prompt=..., verbose=True)` binds prompt + model. **`verbose=True`** prints the filled prompt before each call (handy for debugging).
- ⚠️ **This fires the key teaching moment** — running it prints:
  > *`LangChainDeprecationWarning: The class LLMChain was deprecated in LangChain 0.1.17 ... Use `prompt | llm` instead.`*
- Naming nit: the variable is `llm` but it's a **chain**, not a model. Mildly confusing.

### Cell 4 — invoke
```python
response = llm.invoke("funny")
```
🧠 `.invoke("funny")` fills `{adjective}` → `"Tell me a funny joke"` → calls Cohere. With `verbose=True` you see the `> Entering new LLMChain chain...` trace. ⚠️ **Gotcha:** `LLMChain.invoke` returns a **`dict`** (`{'adjective': 'funny', 'text': '...'}`), not a string.

### Cell 5 — get the text
```python
print(response['text'])
# -> "Why don't skeletons fight each other? Because they don't have the guts!"
```
🧠 You must **dig the answer out** of `response['text']`. That awkward indexing is a big reason LCEL replaced this — `prompt | model | StrOutputParser()` hands you the string directly.

**📌 Notebook 1 in one line:** the classic `LLMChain` works but is deprecated, returns a clumsy dict, and pushes you toward LCEL.

---

## 2. Notebook 2 — "Sequential" Chain (local quantized model)

Titled "Sequential Chain," but its real content is **running LangChain on a local, quantized open-source model**. The densest notebook — the most new terminology.

### Cell 0 — install
```python
!pip install langchain cohere langchain-huggingface bitsandbytes langchain-classic
```
🧠 **`langchain-huggingface`** = the HF ↔ LangChain adapter (gives `HuggingFacePipeline`). **`bitsandbytes`** = the library that performs **quantization** (loading models in 4-bit).

### Cell 1 — Hugging Face login
```python
from huggingface_hub import login
login(userdata.get('HF_TOKEN'))
```
🧠 Unlike Cohere (an API you *call*), here you **download the model weights** and run them yourself. Some models are **gated** (require accepting a license), so you authenticate with an **`HF_TOKEN`**. 💻 Like `docker login` before pulling a private image — authenticating to pull an artifact, not to call a service.

### Cell 2 — imports
```python
import torch, transformers
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
from langchain_huggingface.llms import HuggingFacePipeline
```
🧠
- **`torch`** = PyTorch (the deep-learning runtime); **`transformers`** = Hugging Face's model library (W2·SG05).
- **`AutoModelForCausalLM`** = factory that loads a generative (decoder) model — "Causal LM" = predict the next token (W2·SG05).
- **`HuggingFacePipeline`** = wraps a *local* HF model so LangChain treats it like any other LLM. **The whole point of the notebook** — LangChain isn't only for cloud APIs.

### Cell 3 — load a quantized model (slow down here)

**Tokenizer setup:**
```python
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"
```
🧠
- **Tokenizer** (W2·SG05) = converts text ↔ token IDs.
- **`pad_token = eos_token`** — batching inputs of different lengths requires **padding** shorter ones to equal length. Mistral has no dedicated pad token, so they reuse the **`eos_token`** (end-of-sequence marker) as filler. 💻 Right-padding a fixed-width column.
- **`padding_side = "right"`** — put the padding on the right end.

**Quantization config (the important new concept):**
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=False,
)
```
🧠
- 🔑 **Quantization** = storing model weights at **lower numeric precision** to save memory. A 7-billion-param model at full 32-bit needs ~28 GB of GPU RAM; at **4-bit** it's ~4 GB — the difference between "won't load" and "fits on a free Colab GPU."
- **`load_in_4bit=True`** — load weights as 4-bit numbers.
- **`nf4`** (NormalFloat4) — a 4-bit format tuned to how neural-net weights are distributed (more accurate than plain int4).
- **`compute_dtype=float16`** — *store* in 4-bit but *compute* in 16-bit (a precision/speed balance).
- 💻 **Mental model:** quantization is **lossy compression for weights** — like a 320 kbps MP3 vs a WAV. Lose a sliver of fidelity to be far smaller/faster. It's the same **accuracy-for-resource trade** as ANN in [SG02 §5](study-guide-02-introduction-to-vector-databases.md), applied to weights instead of search.

**GPU capability check:**
```python
if compute_dtype == torch.float16 and use_4bit:
    major, _ = torch.cuda.get_device_capability()
    if major >= 8:
        print("Your GPU supports bfloat16 ...")
```
🧠 Probes the NVIDIA GPU's **compute capability** (≥ 8 = Ampere or newer) to advise a better dtype. **`torch.cuda...`** needs an **NVIDIA GPU** — precisely why this notebook won't run on a Mac.

**Load model + build a generation pipeline:**
```python
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
text_generation_pipeline = transformers.pipeline(
    model=model, tokenizer=tokenizer, task="text-generation",
    temperature=0.1, max_new_tokens=512, output_scores=True)
mistral_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
```
🧠
- `from_pretrained(..., quantization_config=bnb_config)` downloads & loads `mistralai/Mistral-7B-v0.1` in 4-bit.
- **`pipeline(task="text-generation", ...)`** — the high-level HF pipeline (W2·SG05):
  - **`temperature=0.1`** — near-deterministic; low randomness (this matters for the bug below).
  - **`max_new_tokens=512`** — cap the reply at 512 new tokens.
  - **`output_scores=True`** — also return per-token probabilities (ignored here; the run log even warns it's an invalid flag for this path).
- **`HuggingFacePipeline(pipeline=...)`** — wrap it so LangChain sees a standard LLM.

### Cell 4 — markdown: `## Sequential Chain`
🧠 A heading promising a multi-step chain. ⚠️ **The code never delivers one** — the next cells build a *single* chain. Flag this.

### Cell 5 — a single chain
```python
template = "\nI want you to act as a expert who can generate details on the given scientific process {topic}.\n"
prompt_template = PromptTemplate(input_variables=["topic"], template=template)
chain = LLMChain(llm=mistral_llm, prompt=prompt_template)   # deprecation warning again
```
🧠 Same deprecated `LLMChain`, now wrapping the **local** Mistral. Note the *chain code is identical* whether the model is Cohere or local Mistral — LangChain's provider abstraction paying off.

### Cell 6 — preview the filled prompt
```python
description = "Photosynthesis"
prompt_template.format(topic=description)
# -> '\nI want you to act as a expert ... process Photosynthesis.\n'
```
🧠 **`.format(...)`** fills the template and returns the string **without** calling the model — a dry run to see exactly what will be sent. 💻 Like logging your final SQL before executing it.

### Cell 7 — run it (and the bug)
```python
print(chain.invoke(input={'topic': description}))
```
🧠 The output is stuck in a **repetition loop**:
> *"The process of photosynthesis is a process that is used to convert light energy into chemical energy."* — repeated ~15×.

**Why? Two compounding causes (great teaching moment):**
1. **`Mistral-7B-v0.1` is a BASE model, not instruction-tuned** (W2·SG05). It *autocompletes*; it doesn't *follow instructions* like "act as an expert." Base models are prone to looping.
2. **`temperature=0.1`** makes it greedily pick the same high-probability continuation every step → it falls into a loop and can't escape.

**The fix** would be an **instruct** model (e.g. `Mistral-7B-Instruct`) and/or higher temperature + `repetition_penalty`. This is the base-vs-instruct lesson from W2·SG05, seen failing in the wild.

**📌 Notebook 2 in one line:** LangChain wraps *local, quantized* models with the same chain code — but a *base* model at low temperature loops, and the "Sequential Chain" title was never actually implemented. (`week3/code/langchain_sequential_chain_demo.py` builds the real 2-step thing.)

---

## 3. Notebook 3 — LCEL (fan-out / fan-in)

The modern, elegant one.

### Cell 0 — markdown (a caveat worth heeding)
> *"LCEL simplifies syntax and it's easy to use for simple chains, but it can get confusing once we add complexity."*

🧠 Honest and correct — LCEL is delightful for pipelines, but deeply nested `RunnableParallel`/`assign` graphs get hard to read. (This is why **LangGraph** exists for *really* complex flows.)

### Cell 2 — imports
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_cohere import ChatCohere
```
🧠
- **`ChatPromptTemplate`** vs notebook 1's `PromptTemplate`: `ChatPromptTemplate` produces **chat messages** (system/user/assistant roles, W1) — what **chat models** expect. `PromptTemplate` produces a plain string. Use `ChatPromptTemplate` with chat models.
- **`StrOutputParser`** — pulls the plain string out of the model's message object (no more `response['text']` digging).
- **`RunnablePassthrough`** — forwards input unchanged. **`RunnableLambda`** — wraps any plain Python function as a Runnable (imported but unused here).

### Cell 3 — two prompts
```python
prompt = ChatPromptTemplate.from_template("{question}")
combine_answers_prompt = ChatPromptTemplate.from_template(
"""Given the question: {question} and the below two answers:
Answer 1:
{answer1}

Answer 2:
{answer2}

Combine the viewpoints of two answers and form a coherent combined answer.""")
```
🧠 `prompt` just forwards the question. `combine_answers_prompt` has **three** variables (`question`, `answer1`, `answer2`) — the **merge** step. Remember these names: the fan-out dict must produce exactly these keys.

### Cell 4 — three sub-chains
```python
model1 = ChatCohere(cohere_api_key=..., temperature=0.2)   # (×3: model1/2/3)
chain1 = prompt | model1 | StrOutputParser()
chain2 = prompt | model2 | StrOutputParser()
chain3 = combine_answers_prompt | model3 | StrOutputParser()
```
🧠 **Here's LCEL.** Read `prompt | model1 | StrOutputParser()` as *"question → fill prompt → call model → extract string."* Three separate model instances keep the two answerers and the combiner independent. Each `chainN` is itself a **Runnable**, so it can be piped into bigger chains — the whole trick.

### Cells 5–11 — run it manually first
```python
question = "What's the best way to stay up to date with latest LLM news? ... 3 bullet points."
answer1_output = chain1.invoke(question)   # model A's answer
answer2_output = chain2.invoke(question)   # model B's answer
combined_answer_output = chain3.invoke(
    {"question": question, "answer1": answer1_output, "answer2": answer2_output})
```
🧠 The notebook first does it **by hand** — invoke each sub-chain, manually pass results into `chain3`. This makes the data flow visible: two independent 3-bullet answers get merged into one. `chain3.invoke(...)` takes a **dict** because its prompt has multiple variables.

### Cells 12–13 — compose it into ONE chain (the payoff)
```python
combined_chain = {
    "question": RunnablePassthrough(),
    "answer1": chain1,
    "answer2": chain2,
} | chain3
combined_answer = combined_chain.invoke(question)
```
🧠 The heart of the notebook. On `.invoke(question)`:
- The **dict is a fan-out** (a `RunnableParallel` under the hood):
  - `RunnablePassthrough()` → copies `question` through unchanged,
  - `chain1` → runs model A on `question`,
  - `chain2` → runs model B on `question`,
  - all three **in parallel**, producing `{"question":…, "answer1":…, "answer2":…}`.
- Those keys are **exactly** the variables `chain3`'s prompt needs, so `| chain3` (the **fan-in**) merges them.
- 💻 **Java analogy:** `CompletableFuture.supplyAsync(chain1)` + `supplyAsync(chain2)` joined with `thenCombine(...)` — parallel branches, then a merge — but declarative.

### Cells 14–15 — the same chain, `.assign()` style + inspecting it
```python
combined_chain = (
    {"question": RunnablePassthrough()}
    | RunnablePassthrough.assign(answer1=chain1)
    | RunnablePassthrough.assign(answer2=chain2)
    | chain3)
print(combined_chain)
```
🧠
- **`.assign(key=runnable)`** *adds* a key to the dict flowing through, keeping what's already there. The dict grows: `{question}` → `{question, answer1}` → `{question, answer1, answer2}` → into `chain3`.
- Functionally the same as cell 12; different style (sequential accretion vs one parallel dict).
- **`print(combined_chain)`** dumps LCEL's internal structure — `first=... middle=[RunnableAssign(...), RunnableAssign(...)] last=StrOutputParser()` — confirming a chain is just an introspectable tree of composed Runnables.

**📌 Notebook 3 in one line:** LCEL composes small `prompt | model | parser` Runnables into a **parallel fan-out + merge** — expressed two equivalent ways (dict vs `.assign()`).

---

## 4. The three notebooks as one arc

| # | Notebook | Real lesson | Style |
|---|---|---|---|
| 1 | Simple chain | The **deprecated `LLMChain`** (returns a dict; nudges you to LCEL) | Legacy |
| 2 | "Sequential" chain | LangChain wraps a **local, 4-bit-quantized** model — and a **base model loops** | Legacy + local models |
| 3 | LCEL | Modern **`\|` composition** with **fan-out / fan-in** | Current ✅ |

The progression is *old → old-with-local-models → modern*. What the whole set is really teaching:
**learn LCEL (notebook 3), recognize `LLMChain` as legacy (notebooks 1–2), and know a base model at low temperature will disappoint you (notebook 2).**

Runnable, annotated equivalents (provider-swappable Cohere/OpenAI, Mac-friendly):
- `week3/code/langchain_simple_chain_demo.py` — LLMChain **vs** LCEL, side by side
- `week3/code/langchain_sequential_chain_demo.py` — a **true** 2-step chain
- `week3/code/langchain_lcel_demo.py` — the fan-out/fan-in, three ways
- `week3/code/langchain_model.py` — shared provider factory

---

## 5. 🗂️ New jargon from the notebooks

*(Concepts introduced by the notebook code specifically. Most LangChain terms — chain, LCEL, Runnable, pipe `|`, PromptTemplate, output parser, RunnablePassthrough — are defined in [SG03](study-guide-03-langchain-framework.md); Hugging Face terms — tokenizer, pipeline, Causal LM, base vs instruct, temperature, max_new_tokens — in W2·SG05.)*

| Term | Definition |
|---|---|
| **`!` (bang) in a notebook** | Runs the rest of the line as a shell command (e.g. `!pip install ...`). |
| **Colab `userdata` / Secrets** | Colab's secret store for API keys; `userdata.get('X')` reads one without hardcoding it. (≈ env var / secrets manager.) |
| **`HF_TOKEN` / HF login** | Auth token to download (possibly gated) model weights from the Hugging Face Hub. |
| **Gated model** | A Hub model requiring license acceptance / auth before download. |
| **Quantization** | Storing model weights at lower numeric precision (e.g. 4-bit) to cut memory; a lossy accuracy-for-size trade. |
| **4-bit / NF4** | A 4-bit weight format (`nf4` = NormalFloat4) tuned to weight distributions; via `bitsandbytes`. |
| **`bitsandbytes`** | The library implementing 4-/8-bit quantization for Transformers. |
| **`compute_dtype` (float16)** | Store weights in 4-bit but run math in 16-bit — precision/speed balance. |
| **pad_token / padding_side** | Filler token + which side to pad, so batched inputs share one length; Mistral reuses `eos_token` as pad. |
| **compute capability** | An NVIDIA GPU's feature/version level (`torch.cuda.get_device_capability()`); ≥8 = Ampere+ (supports bfloat16). |
| **`HuggingFacePipeline`** | LangChain wrapper that runs a *local* HF pipeline as a chain's LLM. |
| **`ChatPromptTemplate`** | A prompt template that outputs role-tagged chat **messages** (vs `PromptTemplate`'s plain string). |
| **`StrOutputParser`** | Output parser that extracts the plain string from a chat model's message object. |
| **`RunnableLambda`** | Wraps an arbitrary Python function as a Runnable so it composes in a chain. |
| **`.assign()` (RunnablePassthrough)** | Adds a computed key to the dict flowing through a chain, keeping existing keys. |
| **Fan-out / fan-in** | Run several branches from one input (a dict of Runnables, in parallel), then merge them into one step. |

---

*End of Study Guide 03·03b. Concept guide → [SG03 (LangChain)](study-guide-03-langchain-framework.md). Runnable code → `week3/code/langchain_*`. Next Week 3 reading → paste it and I'll build Study Guide 03·04.*
