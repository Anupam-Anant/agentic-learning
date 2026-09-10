# Running Glossary — GenAI Program

> Terms are added as we encounter them, week by week. Use this as your quick-reference lookup.

## Week 1

| Term | Definition | First seen |
|---|---|---|
| **NLP** | Natural Language Processing — getting computers to work with human language. | W1·N01 |
| **RNN** | Recurrent Neural Network — reads text sequentially, one word at a time, keeping a memory. | W1·N01 |
| **LSTM** | Long Short-Term Memory — an improved RNN that remembers longer, but still sequential. | W1·N01 |
| **Transformer** | 2017 architecture based entirely on attention; processes all words in parallel. Foundation of every modern LLM. | W1·N01 |
| **Self-attention** | Mechanism that weighs how much each word relates to every other word in the input. | W1·N01 |
| **Positional encoding** | A signal added to each token so word order is preserved despite parallel processing. | W1·N01 |
| **Encoder** | The half of a Transformer that reads/understands input (BERT-style). | W1·N01 |
| **Decoder** | The half that generates output token-by-token (GPT-style). All chat LLMs are decoders. | W1·N01 |
| **BERT** | Google 2018 — bidirectional encoder; great for understanding/classification/search. | W1·N01 |
| **GPT** | OpenAI — autoregressive decoder family; great for generation; basis of ChatGPT. | W1·N01 |
| **Autoregressive** | Predicting the next token from all previous tokens. | W1·N01 |
| **Parameter** | A single learnable weight in the network; "model size" = parameter count (e.g., 175B). | W1·N01 |
| **LLM** | Large Language Model — a very large pretrained Transformer. | W1·N01 |
| **Zero-shot** | Doing a task from only an instruction, with no examples. | W1·N01 |
| **Few-shot** | Doing a task after being shown a few examples inside the prompt. | W1·N01 |
| **Pretraining** | Learning general language from massive text, once, expensively (the "P" in GPT/BERT). | W1·N01 |
| **Fine-tuning** | Cheaply specializing a pretrained model on a smaller, targeted dataset. | W1·N01 |
| **RLHF** | Reinforcement Learning from Human Feedback — aligning a model to be helpful/honest/harmless. | W1·N01 |
| **Context window** | The maximum number of tokens a model can attend to at once. | W1·N01 |
| **Generative AI** | AI that creates new content (text/image/audio/code); opposite of discriminative AI. | W1·SG02 |
| **Discriminative / traditional AI** | AI that classifies or predicts (labels existing data) rather than creating. | W1·SG02 |
| **Foundation model** | One large general pretrained model reused as the base for many tasks. | W1·SG02 |
| **Diffusion model** | Generates images/audio/video by iteratively removing noise. | W1·SG02 |
| **Multimodal** | Works with multiple data types (text, image, audio, video, docs) in one model. | W1·SG02 |
| **Reasoning model** | Spends extra compute at answer-time ("thinks longer") for hard problems. | W1·SG02 |
| **Agent** | GenAI system that plans, uses tools/APIs, and completes multi-step tasks (acts, not just generates). | W1·SG02 |
| **Tool use / function calling** | Model calling external functions/APIs and using the results. | W1·SG02 |
| **API** | A network endpoint your code calls to send a prompt and get model output. | W1·SG02 |
| **Inference** | Using a trained model to produce output (vs. training = building it). | W1·SG02 |
| **Training** | Building a model by adjusting weights over huge data (expensive, one-time). | W1·SG02 |
| **GPU / TPU** | Specialized parallel chips for AI math (NVIDIA GPUs / Google TPUs). | W1·SG02 |
| **Open-source / open-weight** | Models you can download and run yourself. | W1·SG02 |
| **Pre-trained model** | A model already trained by someone else that you just use. | W1·SG02 |
| **Hyperparameter** | A dial you set before training (learning rate, batch size); controls how it learns. | W1·SG02 |
| **Architecture** | The structural design of a model (layers and how they connect). | W1·SG02 |
| **Deep learning framework** | Libraries to build/train neural nets: PyTorch, TensorFlow, Keras. | W1·SG02 |
| **Model marketplace / hub** | Catalog of ready-made models (Hugging Face, Bedrock, Vertex, Azure AI Foundry). | W1·SG02 |
| **Frontier model** | The largest, most capable, most expensive cutting-edge models. | W1·SG02 |
| **Latency** | How long a model takes to respond. | W1·SG02 |
| **System prompt / instructions** | Hidden setup rules defining the model's role/behavior for a session. | W1·SG02 |
| **Bias** | Skewed model behavior inherited/amplified from skewed training data. | W1·SG02 |
| **Deepfake** | Synthetic media realistically impersonating a real person. | W1·SG02 |
| **Intellectual Property (IP)** | Ownership of AI-generated content / training-data rights — legally unsettled. | W1·SG02 |
| **Evaluation pipeline (evals)** | Automated tests scoring model quality/safety before release. | W1·SG02 |
| **API key** | Secret credential (`sk-…`) authenticating requests to your billing account. | W1·SG03 |
| **SDK** | Library wrapping the raw HTTP API in native function calls (the `openai` package). | W1·SG03 |
| **Responses API** | OpenAI's primary endpoint (`POST /v1/responses`) for generating responses. | W1·SG03 |
| **Chat Completions API** | OpenAI's original stateless interface (`/v1/chat/completions`); you manage history/tools. | W1·SG03 |
| **Function calling** | Model requests a function; you execute it and return the result (client-run tool). | W1·SG03 |
| **Hosted tools** | Tools OpenAI runs server-side (web/file search, code interpreter, computer use); Responses-only. | W1·SG03 |
| **`instructions` (system prompt)** | Developer-set behavior/rules for the model. | W1·SG03 |
| **`input`** | The user message(s)/task sent to the model. | W1·SG03 |
| **`max_output_tokens`** | Cap on output length — controls cost & latency. | W1·SG03 |
| **`previous_response_id`** | Server-side pointer to continue a prior response (multi-turn). | W1·SG03 |
| **Role (system/user/assistant)** | Labels on messages defining who said what. | W1·SG03 |
| **Structured Outputs** | Guarantees the reply matches a JSON Schema you define. | W1·SG03 |
| **JSON Schema** | Formal description of required fields/types/allowed values. | W1·SG03 |
| **JSON mode** | Guarantees valid JSON but not your specific fields (weaker than Structured Outputs). | W1·SG03 |
| **Pydantic / BaseModel** | Python typed-data-model + validation library; your DTO/POJO for schemas. | W1·SG03 |
| **`output_parsed` / `output_text`** | The typed parsed object / the plain-text reply accessor. | W1·SG03 |
| **Streaming / SSE** | Sending the reply incrementally as events (`output_text.delta`). | W1·SG03 |
| **Delta** | An incremental chunk of streamed output. | W1·SG03 |
| **Refusal** | The model declines a request (e.g., safety) — detect before parsing. | W1·SG03 |
| **Incomplete response** | A truncated reply (often hit `max_output_tokens`); check `status`/`incomplete_details`. | W1·SG03 |
| **Perceived latency** | How slow a response *feels*; streaming improves it. | W1·SG03 |
| **Colab / Colab Secrets** | Google's cloud notebook + its secret store for keys. | W1·SG03 |
| **Governance** | Rules/policies/accountability for how AI is used. | W1·SG04 |
| **Domain-specific model** | Model pre-trained/tuned on one field (e.g., BioGPT). | W1·SG04 |
| **Distillation / DistilGPT** | Training a small "student" to mimic a big "teacher" model. | W1·SG04 |
| **LoRA** | Fine-tune tiny extra weights while base model stays frozen. | W1·SG04 |
| **QLoRA** | LoRA applied on a quantized (compressed) model. | W1·SG04 |
| **PEFT** | Parameter-Efficient Fine-Tuning (LoRA/QLoRA family). | W1·SG04 |
| **Quantization** | Storing weights at lower precision (e.g., 4-bit) to shrink a model. | W1·SG04 |
| **Open vs closed source model** | Self-hostable (privacy/control) vs API-only (convenience/scale). | W1·SG04 |
| **Hallucination** | Confidently stated falsehoods from a model. | W1·SG04 |
| **Guardrails** | Built-in safety filters against harmful/biased output. | W1·SG04 |
| **GDPR** | EU data-protection law; a compliance gate. | W1·SG04 |
| **MMLU** | 57-subject knowledge exam benchmark ("general smarts"). | W1·SG04 |
| **HellaSwag** | Commonsense sentence-completion benchmark. | W1·SG04 |
| **WinoGrande** | Pronoun/ambiguity commonsense-reasoning benchmark. | W1·SG04 |
| **OpenLLM Leaderboard** | Public ranking comparing open LLMs. | W1·SG04 |
| **Benchmark contamination** | Test data leaking into training, inflating scores. | W1·SG04 |
| **Inpainting** | Editing/filling part of an image. | W1·SG04 |
| **Segmentation / SAM** | Outlining objects in an image pixel-by-pixel (Meta's SAM). | W1·SG04 |
| **TTS** | Text-to-speech synthesis (WaveNet/VALL-E/Tacotron). | W1·SG04 |
| **Monitoring** | Ongoing tracking of quality/latency/cost/feedback post-deploy. | W1·SG04 |

## Week 2

| Term | Definition | First seen |
|---|---|---|
| **Open-source model** | Weights (and often code) published so anyone can download, run, modify, and self-host it. | W2·SG01 |
| **Closed-source model** | Proprietary model whose weights stay on the vendor's servers; accessed only via API. | W2·SG01 |
| **Proprietary** | Owned/controlled by a company with internals kept secret (closed-source models). | W2·SG01 |
| **Model weights** | The billions of learned numbers that *are* the trained model; shipping them = shipping the model. | W2·SG01 |
| **Open-weight model** | Only the weights are released (often restricted license) — the common real meaning of "open-source LLM"; distinct from fully open-source (weights + code + data). | W2·SG01 |
| **Black box** | A system you can use but can't inspect inside (closed-source models). | W2·SG01 |
| **Inference parameters** | Request-time dials (`temperature`, `top_p`, `max_output_tokens`) — not the internal weights; both open and closed expose these. | W2·SG01 |
| **Total Cost of Ownership (TCO)** | Full cost of running something (hardware + engineering + scaling + ops), not just licence price — the open-source "free ≠ free" trap. | W2·SG01 |
| **Pay-per-use / pay-as-you-go** | Billing per API call / per token with no idle fixed cost (closed-source pricing). | W2·SG01 |
| **Self-hosting / on-premise (on-prem)** | Running a model on servers you control so inputs never leave your environment — basis of open-source's privacy edge. | W2·SG01 |
| **Compliance** | Obeying legal/regulatory data rules (GDPR, HIPAA…); often the deciding factor for open vs closed. | W2·SG01 |
| **SLA** | Service-Level Agreement — contractual uptime/response guarantee; sold by closed vendors, absent in open communities. | W2·SG01 |
| **Vendor lock-in** | Dependence on one provider whose model you can't freeze or move; a closed-source risk. | W2·SG01 |
| **LLaMA** | Meta's influential family of open-weight LLMs; base for thousands of fine-tunes. | W2·SG01 |
| **Mistral** | French lab's small, fast, genuinely-open (Apache-2.0) LLM family. | W2·SG01 |
| **Stable Diffusion** | Landmark open-source image-generation (diffusion) model. | W2·SG01 |
| **GPT-4** | OpenAI's frontier closed-source LLM (API-only). | W2·SG01 |
| **Claude** | Anthropic's family of closed-source LLMs (API-only). | W2·SG01 |
| **PaLM** | Google's earlier API-served LLM family (predecessor to Gemini). | W2·SG01 |
| **Hugging Face** | Dominant hub to find/download/share open models and datasets ("GitHub of models"). | W2·SG01 |
| **Transformers (library)** | Hugging Face's Python library to load/run/fine-tune models — distinct from the Transformer *architecture*. | W2·SG01 |
| **LangChain** | Framework for building LLM apps (chaining calls, data, tools, memory) — wraps a model, isn't one. | W2·SG01 |
| **LlamaIndex** | Framework connecting LLMs to your data (indexing/retrieval) for data-aware apps. | W2·SG01 |
| **Prompt engineering** | Deliberately crafting the input text sent to an LLM so it reliably produces the desired output — "programming in natural language." | W2·SG02 |
| **Prompt** | The text you send the model (the `input` + any `instructions`). | W2·SG02 |
| **In-context learning (ICL)** | The model learning a task from examples/instructions in the prompt at inference time, with no change to its weights — the mechanism behind few-shot. | W2·SG02 |
| **Inference time** | The moment a finished model is run to answer an input (per API call, cheap; weights frozen) — vs *training time* when weights are built (once, offline). All prompt techniques act at inference time. | W2·SG02 |
| **One-shot prompting** | Prompting with exactly one worked example (between zero-shot and few-shot). | W2·SG02 |
| **Prompt chaining** | Breaking a complex task into a sequence of LLM calls where each output feeds the next call's input. | W2·SG02 |
| **Chain-of-Thought (CoT)** | Prompting the model to reason step by step before answering, improving accuracy on multi-step problems. | W2·SG02 |
| **"Let's think step by step"** | The canonical trigger phrase that elicits CoT reasoning from a standard chat model. | W2·SG02 |
| **gpt-4o-mini** | A small, fast, low-cost OpenAI chat model used in the prompt-engineering demo. | W2·SG02 |
| **Cohere** | Another closed-source LLM provider (API), a drop-in alternative to OpenAI. | W2·SG02 |
| **Vector** | An ordered list of numbers, e.g. `[0.23, -0.45, 0.91]`; a point/arrow in space (≈ a `float[]`). | W2·SG03 |
| **Vector embedding (embedding)** | A vector produced to represent the *meaning* of an input, so similar inputs get nearby vectors. | W2·SG03 |
| **Embedding space / vector space** | The high-dimensional space embeddings live in; near = similar, far = dissimilar. | W2·SG03 |
| **Dimension / dimensionality** | The length of a vector (how many numbers). Typical: 300 (Word2Vec), 768 (BERT), 1536 (OpenAI). | W2·SG03 |
| **One-hot encoding** | Representing one of N items as an N-length vector with a single `1` and the rest `0`. | W2·SG03 |
| **Sparse vector** | A vector that is mostly zeros (e.g. one-hot). | W2·SG03 |
| **Dense vector** | A compact vector where most values are non-zero and carry information (an embedding). | W2·SG03 |
| **Semantic** | Relating to meaning. | W2·SG03 |
| **Semantic similarity** | Closeness in *meaning* (not spelling); e.g. "car" ≈ "automobile". | W2·SG03 |
| **Cosine similarity** | Similarity as the cosine of the angle between two vectors; the standard metric for embeddings. | W2·SG03 |
| **Word embedding** | An embedding representing a single word. | W2·SG03 |
| **Static embedding** | One fixed vector per word regardless of context (Word2Vec, GloVe). | W2·SG03 |
| **Contextual embedding** | A word's vector computed from its whole sentence, so it varies by context (BERT). | W2·SG03 |
| **Word2Vec** | 2013 model that learns word vectors by predicting words ↔ context (CBOW / Skip-Gram). | W2·SG03 |
| **CBOW / Skip-Gram** | Word2Vec modes: predict the center word from context (CBOW), or context from the word (Skip-Gram). | W2·SG03 |
| **GloVe** | Word-embedding model built from a global word co-occurrence matrix (statistical, not predictive). | W2·SG03 |
| **Co-occurrence matrix** | A table counting how often each word appears near each other word across a corpus. | W2·SG03 |
| **Distributional hypothesis** | Words used in similar contexts have similar meanings — the basis of learned embeddings. | W2·SG03 |
| **Wav2Vec 2.0** | Model producing speech/audio embeddings learned from raw waveforms. | W2·SG03 |
| **CLIP** | Model embedding text *and* images into one shared space; enables cross-modal & zero-shot tasks. | W2·SG03 |
| **Cross-modal** | Operating across different data types (text ↔ image ↔ audio) in a shared space. | W2·SG03 |
| **Embedding model** | A model whose output is embeddings (vs a generative model that outputs text). | W2·SG03 |
| **Vector database** | Datastore for embeddings optimized for fast nearest-neighbor search (Pinecone, FAISS, Chroma, pgvector). | W2·SG03 |
| **Semantic search** | Search by meaning (nearest embeddings) rather than keyword matching. | W2·SG03 |
| **Nearest-neighbor search** | Finding the points closest to a query point in vector space. | W2·SG03 |
| **Bidirectional** | Reading a word's context from both left and right at once (BERT); vs left-to-right only (GPT). | W2·SG04 |
| **transformers (library)** | Hugging Face's Python library to download and run pre-trained models. | W2·SG04 |
| **PyTorch (torch)** | Deep-learning framework (tensors + GPU math) that models run on; `transformers` sits on top of it. | W2·SG04 |
| **Hugging Face Hub** | The online registry model weights are downloaded/cached from (`huggingface.co`). | W2·SG04 |
| **pipeline (Hugging Face)** | High-level helper bundling tokenizer + model + pre/post-processing for a named task (~2 lines to run). | W2·SG04 |
| **DistilBERT** | A distilled (smaller/faster, ~97% quality) version of BERT; default in several pipelines. | W2·SG04 |
| **Text classification** | Assigning a whole piece of text to a category/label. | W2·SG04 |
| **Sentiment analysis** | Text classification where labels are emotional polarity (positive/negative/neutral). | W2·SG04 |
| **Named entity** | A real-world proper noun — a specific person, place, organization, date, etc. | W2·SG04 |
| **Named Entity Recognition (NER)** | Detecting named entities in text and labeling their type (PER/LOC/ORG/MISC). | W2·SG04 |
| **Token classification** | Assigning a label to *each token* (as in NER), vs one label for the whole text. | W2·SG04 |
| **IOB / BIO tagging** | Span-labeling scheme: Begin / Inside / Outside; lets per-token labels represent multi-word entities (e.g. `I-LOC`). | W2·SG04 |
| **CoNLL-2003** | Standard English NER benchmark dataset (people/locations/orgs/misc). | W2·SG04 |
| **Question answering (QA)** | Answering a question about a text. | W2·SG04 |
| **Extractive QA** | The answer is a span pulled verbatim from the provided context (predict start/end). | W2·SG04 |
| **Abstractive / generative QA** | The model *writes* a fresh answer in its own words (GPT-style), not copied from context. | W2·SG04 |
| **CUDA** | NVIDIA's GPU compute platform; `device="cuda"` runs a pipeline on the GPU. | W2·SG04 |
| **SQuAD** | Standard extractive-QA benchmark dataset (Stanford Question Answering Dataset). | W2·SG04 |
| **AutoModel / AutoModelForCausalLM** | Factory classes that load the right model class from a Hub id; `…ForCausalLM` loads an autoregressive (generative) decoder. | W2·SG05 |
| **AutoTokenizer** | Factory class that loads the tokenizer matching a given model id. | W2·SG05 |
| **Auto classes (factory)** | The `Auto*` pattern: `from_pretrained(id)` reads config and instantiates the right concrete class. | W2·SG05 |
| **Tokenizer** | Converts text ↔ token IDs; must match the model (≈ a codec: `String` ↔ `int[]`). | W2·SG05 |
| **Token ID / input_ids** | The integer vocabulary indices the model consumes (tokenizer's numeric output). | W2·SG05 |
| **attention_mask** | 0/1 vector marking real tokens (1) vs padding to ignore (0). | W2·SG05 |
| **Special tokens** | Reserved non-word tokens marking structure (end-of-text, chat-turn markers, padding). | W2·SG05 |
| **Chat template / apply_chat_template** | Model-specific rule serializing a `messages` list into the exact prompt string (with special tokens) the model expects. | W2·SG05 |
| **Causal language modeling (Causal LM)** | Predicting the next token from previous tokens only — the autoregressive, generative objective. | W2·SG05 |
| **Small Language Model (SLM)** | A compact LLM (few-billion params) meant to run cheaply/locally (e.g. Phi-3-mini). | W2·SG05 |
| **Instruction-tuned (instruct) model** | A base LLM fine-tuned to follow instructions/chat (vs a raw autocomplete base). | W2·SG05 |
| **Tensor / return_tensors="pt"** | An n-dimensional array (PyTorch's data unit); `"pt"` returns PyTorch tensors. | W2·SG05 |
| **device_map** | Where the model/tensors run — `"cuda"` (NVIDIA GPU), `"mps"` (Apple), or CPU. | W2·SG05 |
| **torch_dtype (dtype)** | Numeric precision of weights/compute (float32/float16/bfloat16); trades precision for speed & memory. | W2·SG05 |
| **model.generate()** | The method that runs the autoregressive generation loop. | W2·SG05 |
| **max_new_tokens** | Cap on how many *new* tokens to generate. | W2·SG05 |
| **Greedy decoding** | Always pick the most-likely next token (deterministic; `generate`'s default). | W2·SG05 |
| **Sampling / do_sample** | Draw the next token randomly from the distribution; enables `temperature`/`top_p`/`top_k`. | W2·SG05 |
| **Random seed (manual_seed)** | Fixes the pseudo-random generator so stochastic output is reproducible. | W2·SG05 |
| **safetensors** | Modern, safe weight-file format (no arbitrary code execution on load). | W2·SG05 |
| **Phi-3** | Microsoft's family of small, instruction-tuned open LLMs (notebook uses `Phi-3-mini-4k-instruct`). | W2·SG05 |

## Week 3

| Term | Definition | First seen |
|---|---|---|
| **RAG (Retrieval Augmented Generation)** | Pattern that retrieves relevant documents and adds them to the prompt so an LLM answers from supplied facts, not just memory. Retrieve → Augment → Generate. | W3·SG01 |
| **Retriever / Retrieval system** | The component that searches the knowledge base and returns the most relevant chunks (embeddings + vector-DB search under the hood). "The librarian." | W3·SG01 |
| **Generator / Generative model** | The LLM that reads the retrieved chunks + question and writes the final natural-language answer. "The writer." | W3·SG01 |
| **Knowledge base** | The external collection of documents RAG draws from; lives outside the model and can be updated freely without retraining. | W3·SG01 |
| **Inference** | Running a trained model to get an answer (vs training it); "at inference" = at question time, live. | W3·SG01 |
| **Grounding** | Tying the model's answer to specific provided source text, so claims are backed by evidence rather than invented. RAG is the main grounding technique. | W3·SG01 |
| **Hallucination** | An LLM confidently stating false information; happens when it lacks a fact and fills the gap with plausible-sounding text. | W3·SG01 |
| **Context (retrieved)** | The retrieved text injected into the prompt for the generator to read. | W3·SG01 |
| **Context window** | The max text (in tokens) a model can consider at once — prompt + context + answer combined; a hard size cap. | W3·SG01 |
| **top-K** | Retrieve the K best-matching chunks (K = a small chosen number); like `LIMIT K` on a similarity-ordered query. | W3·SG01 |
| **Chunk / Chunking** | Splitting documents into smaller passages before embedding, so retrieval returns focused snippets. | W3·SG01 |
| **Chunk overlap** | Letting consecutive chunks share some text so ideas spanning a boundary aren't lost. | W3·SG01 |
| **Indexing (index time)** | The offline, one-time prep: chunk → embed → store vectors in the DB, enabling query-time retrieval. | W3·SG01 |
| **FAISS** | Facebook AI Similarity Search — a fast in-process library for nearest-neighbor search over vectors. | W3·SG01 |
| **ChromaDB (Chroma)** | A developer-friendly open-source vector database, popular for RAG prototypes. | W3·SG01 |
| **Re-ranking** | (Advanced RAG) A second, sharper model reorders the initially retrieved top-K for better precision. | W3·SG01 |
| **Hybrid search** | (Advanced RAG) Combining semantic (embedding) search with keyword search (e.g. BM25). | W3·SG01 |
| **Unstructured data** | Data with no fixed table schema — free text, images, audio, video. | W3·SG02 |
| **BLOB (Binary Large Object)** | A DB column holding a whole file's raw bytes (image/PDF/audio); the DB can store it but can't search by its *content*, only by structured labels — the limitation vector DBs undo. (💻 Java `byte[]`.) | W3·SG02 |
| **High-dimensional vector** | A vector with hundreds/thousands of numbers (e.g. 1,536-dim); one point in that many-D space. | W3·SG02 |
| **Distance metric / similarity metric** | The formula scoring how alike two vectors are; results are ranked by it. | W3·SG02 |
| **Euclidean distance (L2)** | Straight-line distance between two points, `√Σ(aᵢ−bᵢ)²`; smaller = more similar. | W3·SG02 |
| **Dot product** | Similarity combining direction and magnitude (rewards longer vectors); used when vectors aren't normalized. | W3·SG02 |
| **Normalized vector** | A vector scaled to length 1; makes cosine and Euclidean rank results identically. | W3·SG02 |
| **Exact / brute-force k-NN** | Compare the query to all N vectors for the true K closest — accurate but O(N), too slow at scale. | W3·SG02 |
| **Approximate Nearest Neighbor (ANN)** | Index that returns probably-closest vectors while checking a tiny fraction of data — trades a little accuracy for huge speed. | W3·SG02 |
| **Recall (ANN)** | Fraction of the true nearest neighbors the approximate search returned; the accuracy⇄speed knob. | W3·SG02 |
| **HNSW (Hierarchical Navigable Small World)** | The dominant ANN index: a layered proximity graph ("skip-list for geometry") giving ~O(log N) search. | W3·SG02 |
| **IVF (Inverted File Index)** | ANN approach that clusters vectors and searches only the nearest clusters. | W3·SG02 |
| **Curse of dimensionality** | In high-D space points become near-equidistant and space-partitioning trees fail — the reason ANN graphs are needed. | W3·SG02 |
| **Upsert** | Insert-or-update in one operation; the standard vector-DB write. | W3·SG02 |
| **SBERT (Sentence-BERT)** | BERT variant fine-tuned to produce one strong embedding per sentence/passage; a go-to text embedder for retrieval. | W3·SG02 |
| **Metadata filtering** | Narrowing similarity results by structured attributes (tenant, date, source) — a `WHERE` clause on nearest-neighbor search. | W3·SG02 |
| **Post-processing (vector DB)** | Refining raw hits: filtering, re-ranking, dedup, formatting. | W3·SG02 |
| **Data ingestion** | The pipeline of generating embeddings and loading them (with metadata) into the DB. | W3·SG02 |
| **Qdrant** | Open-source, production-grade vector database (self-hosted server). | W3·SG02 |
| **Managed vs self-hosted vs embedded** | Deployment axis: Pinecone (managed cloud) · Qdrant/Chroma-server (self-hosted) · FAISS/SQLite-like (embedded library). | W3·SG02 |
| **BM25** | Classic keyword-ranking algorithm; the "lexical" half of hybrid search. | W3·SG02 |
| **LangChain** | A framework for building applications around LLMs — the orchestration layer wiring models, prompts, data, memory, and tools. ("Spring for LLM apps.") | W3·SG03 |
| **Framework (vs library)** | A scaffold that calls *your* code within its conventions (inversion of control); you compose within it. | W3·SG03 |
| **Orchestration** | Coordinating multiple steps/components into one flow. | W3·SG03 |
| **Chain (LangChain)** | A composable pipeline of steps (prompt → model → parse → …) treated as one callable; the fundamental building block. | W3·SG03 |
| **LCEL (LangChain Expression Language)** | The `\|`-based declarative syntax for composing chains from Runnables. | W3·SG03 |
| **Runnable** | LangChain's universal "callable" interface; every component implements it, sharing `.invoke()/.batch()/.stream()` + async. | W3·SG03 |
| **Pipe operator `\|` (LCEL)** | Composes two Runnables left-to-right (left's output → right's input); function composition (≈ Java `Function.andThen()`). | W3·SG03 |
| **RunnablePassthrough** | An LCEL Runnable that forwards its input unchanged; `.assign()` adds computed keys while keeping existing ones. | W3·SG03 |
| **Chat model (vs LLM text model)** | LangChain model type taking role-tagged messages → a message (modern default); an *LLM* is string→string. | W3·SG03 |
| **PromptTemplate** | A reusable prompt with typed `{variables}` filled at runtime (≈ a `PreparedStatement` / `MessageFormat`). | W3·SG03 |
| **Output parser** | A component that turns the model's raw text into a clean structure (string, JSON, object); e.g. `StrOutputParser`. | W3·SG03 |
| **Memory (LangChain)** | A component that persists info across interactions and injects it into later prompts (≈ `HttpSession` for a bot). | W3·SG03 |
| **Data augmentation** | Enriching the model's input with retrieved external data — i.e. RAG. | W3·SG03 |
| **Tool (LangChain)** | A function the LLM can invoke (search, calculator, API, DB) to fetch facts or act; the basis of agents. | W3·SG03 |
| **Agent** | A model that chooses and runs tools in a loop to accomplish a goal (upcoming topic). | W3·SG03 |
| **VectorStore / Retriever (LangChain)** | Wrapper over a vector DB (SG02) exposing `.as_retriever()` → a Runnable returning relevant chunks. | W3·SG03 |
| **Document loader** | Reads source data (PDF/HTML/CSV/…) into standard `Document` objects for a RAG pipeline. | W3·SG03 |
| **Text splitter** | Chunks documents (size + overlap) before embedding (SG01 chunking, as a component). | W3·SG03 |
| **HuggingFacePipeline** | LangChain wrapper that runs a *local* Hugging Face model as a chain's LLM (vs an API model). | W3·SG03 |
| **Quantization (4-bit / NF4)** | Compressing model weights to lower precision (e.g. 4-bit `nf4` via bitsandbytes) so a big model fits/loads on limited GPU memory. | W3·SG03 |
| **LlamaIndex** | A framework specialized in RAG / data indexing and retrieval. | W3·SG03 |
| **CrewAI** | A framework for multi-agent orchestration (role-playing agents collaborating). | W3·SG03 |
| **FlowiseAI** | A low-code/visual (drag-and-drop) builder for LangChain-style flows. | W3·SG03 |
| **LangGraph** | LangChain's framework for stateful, cyclic (loops/branches) agent workflows. | W3·SG03 |
| **LangSmith** | LangChain's observability/eval platform — tracing/debugging chains (≈ APM for LLM apps). | W3·SG03 |
| **LangServe** | Deploys a chain as a REST API in a few lines. | W3·SG03 |
| **ChatPromptTemplate** | A prompt template that outputs role-tagged chat **messages** (vs `PromptTemplate`'s plain string); use with chat models. | W3·SG03b |
| **StrOutputParser** | Output parser that extracts the plain string from a chat model's message object. | W3·SG03b |
| **RunnableLambda** | Wraps an arbitrary Python function as a Runnable so it composes in an LCEL chain. | W3·SG03b |
| **Fan-out / fan-in** | Run several branches from one input (a dict of Runnables, in parallel), then merge them into one step. | W3·SG03b |
| **Gated model** | A Hugging Face Hub model requiring license acceptance / auth (an `HF_TOKEN`) before download. | W3·SG03b |
| **pad_token / padding_side** | A filler token + which side to pad, so batched inputs share one length (Mistral reuses `eos_token` as pad). | W3·SG03b |
| **Information Retrieval (IR)** | Finding relevant items from a large collection in response to a query (search, RAG, recommendations). | W3·SG04 |
| **Pre- / during- / post-retrieval optimization** | The three stages you can tune: refine the input · run the search well · refine the output. | W3·SG04 |
| **Precision** | Of the results returned, the fraction that are relevant ("did I return junk?"). | W3·SG04 |
| **Recall (IR)** | Of all relevant results that exist, the fraction returned ("did I miss anything?"). | W3·SG04 |
| **Precision–recall trade-off** | Widening search raises recall but lowers precision, and vice versa; you balance them. | W3·SG04 |
| **Sentence window / sliding window** | Splitting text into small (1–few sentence) units via a sliding window for sharp, focused matching. | W3·SG04 |
| **Small-to-big / sentence-window / parent-document retrieval** | Match on a tiny unit but return a larger surrounding context to the LLM. | W3·SG04 |
| **Query expansion** | Adding synonyms/related/broader terms to the query before searching → recall ↑. | W3·SG04 |
| **Vocabulary mismatch** | Searcher and document use different words for the same idea ("laptop" vs "notebook"). | W3·SG04 |
| **Knowledge graph** | A network of entities and their relationships; a source for related-term expansion. | W3·SG04 |
| **Query rewriting** | Transforming the query into a cleaner, better-formed, standalone version (typos, order, intent, conversational context). | W3·SG04 |
| **Lexical / keyword search** | Matching on literal words/tokens (no notion of meaning). | W3·SG04 |
| **TF-IDF** | Classic lexical scoring: term frequency × inverse document frequency (frequent-here-but-rare-overall = important). | W3·SG04 |
| **Bi-encoder** | Encodes query and doc separately → fast, indexable, less precise (first-pass retrieval). | W3·SG04 |
| **Cross-encoder** | Encodes query + doc jointly → slow, unindexable, very precise (used for reranking). | W3·SG04 |
| **Reciprocal Rank Fusion (RRF)** | Merges multiple ranked lists by summing `1/(k+rank)` per item — fuses lexical + semantic without comparing raw scores. | W3·SG04 |
| **HyDE (Hypothetical Document Embeddings)** | Generate a fake ideal answer with an LLM, embed *that*, and search with it (LLM-era query expansion). | W3·SG04 |
| **Click-through rate (CTR)** | Fraction of users who clicked a shown result; a signal for heuristic reranking. | W3·SG04 |
