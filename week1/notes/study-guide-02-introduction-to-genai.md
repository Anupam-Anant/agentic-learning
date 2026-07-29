# 📘 Week 1 · Study Guide 02 — Introduction to Generative AI (GenAI)

> **Self-contained document.** Contains the **complete original PDF text** *plus* first-principles explanations of every concept and piece of jargon. You do **not** need to open the PDF.
>
> **How to read:** 📄 **`FROM THE PDF`** = exact original text · 🧠 **`EXPLAINED`** = plain-English teaching · 🔑 **bold jargon** defined on first use and again in the **Jargon Dictionary** at the end. Written for a **Java/backend engineer** new to AI.
>
> *(The source PDF repeats pages 4–5 verbatim — an OCR artifact. This guide presents each idea once, cleanly.)*

---

## 📑 Table of Contents

1. [What GenAI Has Become (2026 framing)](#page-1-2--what-genai-has-become)
2. [What is Generative AI?](#page-2--what-is-generative-ai)
3. [How Does Generative AI Work? (the 6-stage pipeline)](#page-3-4--how-does-generative-ai-work)
4. [How to Access & Use GenAI Models (5 ways)](#page-4-7--how-can-genai-models-be-accessed--used)
5. [Popular GenAI Models](#page-8--popular-genai-models)
6. [Ethical Considerations & Future](#page-9--ethical-considerations--future)
7. [🗂️ Full Jargon Dictionary](#-full-jargon-dictionary)
8. [📊 Key Comparison Tables](#-key-comparison-tables)
9. [🧵 Connected Mental Model](#-connected-mental-model)
10. [⚡ 60-Second Recap](#-60-second-recap)

---

## Page 1–2 — What GenAI Has Become

> 📄 **FROM THE PDF**
> **✨ Introduction to Generative AI (GenAI)**
>
> In the ever-evolving world of artificial intelligence, one term is making waves across industries and sparking imaginations: Generative AI. Imagine machines that can write stories, compose music, or even create stunning artworks. Sound futuristic? It's happening right now, and GenAI is the engine behind it.
>
> By 2026, GenAI is no longer only about writing stories, generating images, or answering questions. It has become a **full-stack technology layer** used for reasoning, coding, automation, document understanding, image analysis, video generation, voice interaction, enterprise workflows, and AI agents. That means modern AI systems can understand and generate text, images, audio, video, code, documents, screens, charts, and tools. They can also plan tasks, call APIs, search databases, use software, write code, review files, and assist humans in real business workflows.

### 🧠 EXPLAINED

This is the "why should you care" opener. The key phrase is **"full-stack technology layer."**

- 🔑 **Full-stack technology layer:** the PDF is saying GenAI is no longer a single feature ("a chatbot") but a *foundational layer* you build entire systems on — the way you think of a *database* or an *operating system* as infrastructure. As a backend engineer, picture it like this: you already treat "the database layer" or "the auth layer" as reusable infrastructure. By 2026, "the AI layer" joins them — something many features call into.

- **The leap being described:** early GenAI (2020–2022) mostly *generated content* (text, images). Modern GenAI also **takes actions** — it can `call APIs`, `search databases`, `use software`, and `complete multi-step tasks`. That shift, from *"generate text"* to *"do things,"* is the single biggest theme of this whole reading, and it's what the word **agent** captures (defined below).

- 🔑 **Multimodal** *(introduced by the long list of media types):* able to work with **more than one type of data ("modality")** — text, images, audio, video, documents, even screenshots and charts. A model that can look at an image *and* answer a text question about it is multimodal. (Contrast: older models were *unimodal* — text only, or image only.)

---

## Page 2 — What is Generative AI?

> 📄 **FROM THE PDF**
> Generative AI refers to a category of artificial intelligence models designed to generate new content. Unlike traditional AI systems that focus on **classification or prediction**, GenAI creates outputs such as text, images, music, and more.
>
> It leverages complex algorithms — particularly **neural networks** — to learn patterns from vast datasets and generate original content based on those learnings. This ability sets GenAI apart from conventional AI, which primarily interprets data rather than creating it.

### 🧠 EXPLAINED

This is the **core definition**. The best way to understand "Generative" AI is to contrast it with the older "traditional" kind.

- 🔑 **Traditional / Discriminative AI:** AI that *interprets or labels existing data* — it answers "which category?" or "what number?" It **discriminates between options**. Examples: spam-or-not (classification), house-price estimate (prediction/regression), is-this-a-cat (image classification).

- 🔑 **Generative AI:** AI that *creates new data* that didn't exist before — a paragraph, an image, a melody, a block of code. It answers "produce something new that fits this request."

| | Traditional (Discriminative) AI | Generative AI |
|---|---|---|
| **Question it answers** | "Which label / what value?" | "Create something new that fits." |
| **Output** | A category or number | New content (text, image, audio, code) |
| **Example** | "This email is **spam**." | "**Write** me a polite reply to this email." |
| **Mindset** | Interprets data | Produces data |

- 🔑 **Neural network** *(recap from Study Guide 01):* a model made of layers of simple math units connected by **weights** (tunable numbers), loosely inspired by brain neurons. It learns by adjusting those weights over lots of examples. GenAI models are (very large) neural networks.

- 🔑 **Dataset:** the collection of examples a model learns from. "Vast datasets" = huge amounts of text/images/etc. (often much of the public internet).

> **One-line takeaway:** *Traditional AI reads and labels; Generative AI writes and creates.*

---

## Page 3–4 — How Does Generative AI Work?

> 📄 **FROM THE PDF**
> At the core of GenAI are **foundation models**. These are large models trained on massive datasets so they can perform many different tasks.
>
> The most common model families include:
> - **Transformer models** for text, code, reasoning, and multimodal understanding
> - **Diffusion models** for image, audio, and video generation
> - **Multimodal models** that combine text, image, audio, video, and document understanding
> - **Reasoning models** that spend more computation on complex problem-solving
> - **Agents** that can plan, use tools, and complete multi-step tasks
>
> Here's a simplified view of the process:
> 1. **Training Phase:** the model is trained on large datasets (text, code, images, audio, videos, documents, structured data). It learns patterns, grammar, facts, styles, visual structures, programming logic, and relationships between concepts.
> 2. **Pattern Learning:** the model does not simply memorize. It learns **statistical and semantic patterns** — for text, how words and ideas connect; for images, shapes/textures/objects/styles; for code, syntax/logic/libraries/patterns.
> 3. **Prompt or Input Phase:** the user gives an instruction, question, document, image, audio clip, or workflow request. This input is converted into **tokens** or internal representations the model can process.
> 4. **Generation Phase:** the model predicts and generates the most suitable output based on the input, training, context, and system instructions. Output may be text, code, image, video, audio, JSON, or a tool action.
> 5. **Feedback and Alignment:** modern models are improved using feedback, safety training, preference tuning, reinforcement learning, evaluation pipelines, and human review — making outputs more useful, safe, accurate, and aligned with user intent.
> 6. **Tool Use and Agents:** by 2026, many GenAI systems connect with tools such as search engines, databases, calendars, CRMs, ERPs, code editors, browsers, and APIs — so they can not only answer questions but also perform actions.

### 🧠 EXPLAINED

#### The central concept: Foundation Models

- 🔑 **Foundation model:** one **big, general-purpose** model, pretrained on enormous data, that serves as the *foundation* for **many** downstream tasks. Instead of training a separate model per task (one for translation, one for summarizing…), you train **one** foundation model and adapt it. LLMs (like GPT/Claude) are foundation models for language. The name (coined at Stanford) captures the idea: it's the base layer everything else is built on.

> 💻 **Engineering analogy:** a foundation model is like a **base class / shared library / platform SDK**. You don't rewrite it per project — you *import it and extend it* (via prompting, fine-tuning, or tools) for your specific need.

#### The five model families (know these — common interview question)

| Family | What it's for | How to think about it |
|---|---|---|
| 🔑 **Transformer models** | Text, code, reasoning, multimodal | The architecture from Study Guide 01 — the workhorse for language. |
| 🔑 **Diffusion models** | Image, audio, video **generation** | Start from pure random **noise** and repeatedly *remove* noise until a coherent image emerges (like sculpting a photo out of static). Powers tools like Stable Diffusion, Midjourney, DALL·E. |
| 🔑 **Multimodal models** | Combine text + image + audio + video + docs | One model that "sees" and "reads" and "hears." E.g., ask a question about a photo. |
| 🔑 **Reasoning models** | Hard, multi-step problems | Deliberately **spend more computation at answer-time** ("thinking longer") before responding — trading speed for correctness on math, logic, coding. Also called *test-time compute*. |
| 🔑 **Agents** | Plan + use tools + multi-step tasks | Not just generate — *act*. Break a goal into steps, call tools/APIs, observe results, continue. (The big 2026 theme.) |

#### The 6-stage pipeline — how a GenAI system actually runs

Think of stages 1–2 as **"build the model" (done once, by big labs)** and stages 3–4 as **"use the model" (every time you send a prompt)**. Stages 5–6 are **"make it safe and capable of acting."**

```
[ BUILD ONCE (expensive, done by OpenAI/Google/etc.) ]
 1. TRAINING ─────► 2. PATTERN LEARNING
    feed huge data      learns statistical + semantic patterns (not memorization)

[ USE IT (every request) ]
 3. PROMPT/INPUT ─► 4. GENERATION
    your text/image      predicts best output token-by-token
    → converted to       → text / code / image / JSON / tool action
      TOKENS

[ IMPROVE & EMPOWER ]
 5. FEEDBACK & ALIGNMENT ── humans + RL make it helpful/safe/aligned
 6. TOOL USE & AGENTS ────── connects to search, DBs, APIs → performs actions
```

- 🔑 **Pattern learning (statistical vs semantic):** the model doesn't store a giant lookup table of your training text. It learns **statistical patterns** ("after 'thank', 'you' is very likely") *and* **semantic patterns** (that "king" and "queen" are *related in meaning*). This is why it can generalize to things it never saw exactly.

- 🔑 **Token:** the unit of text a model actually reads/writes — roughly a word or word-piece (e.g., "unbelievable" → `un` + `believ` + `able`). Your prompt is chopped into tokens before processing, and output is produced one token at a time. **You'll care about tokens constantly** because API pricing and the **context window** limit are both measured in tokens.

- 🔑 **Internal representation / embedding:** after tokenizing, each token is turned into a list of numbers (a **vector**) capturing its meaning, so the math can operate on it. (Deep-dived in a later RAG module.)

- 🔑 **System instructions (system prompt):** hidden setup instructions that define the model's role/rules for a session (e.g., "You are a helpful customer-support agent; never reveal internal pricing"). You'll set these in Playgrounds. Separate from the *user* prompt.

- 🔑 **Feedback & Alignment:** the process of shaping a raw model to be helpful, honest, and harmless. Includes:
  - 🔑 **RLHF (Reinforcement Learning from Human Feedback)** / **preference tuning:** humans rank outputs; the model is tuned to prefer the better ones.
  - 🔑 **Evaluation pipelines ("evals"):** automated test suites that score model quality/safety before release (your QA/CI mindset, applied to models).

- 🔑 **Tool use / function calling:** giving the model the ability to call external functions/APIs (search the web, query a DB, hit a CRM). The model decides *when* to call a tool and with *what arguments*, then uses the result. This is what turns a "text generator" into an **agent** that gets real work done. (`CRM` = Customer Relationship Management system like Salesforce; `ERP` = Enterprise Resource Planning system like SAP — the business software agents plug into.)

---

## Page 4–7 — How Can GenAI Models Be Accessed & Used?

> 📄 **FROM THE PDF**
> Generative AI models have become more accessible than ever. Here's an overview of how you can access and utilize these powerful tools:
>
> **1. Pre-trained Models via APIs** — Access: many AI companies offer **APIs (Application Programming Interfaces)** to interact with pre-trained models. Providers: OpenAI, Google, Anthropic, Microsoft (cloud-based APIs for text, image, audio). Usage: text generation (chatbots, content tools, code assistants), image creation, audio synthesis. **Benefits:** no need for extensive computational resources or deep-learning expertise; focus on application development.
>
> **2. Open-Source Models** — Access: many models available as open-source on platforms like GitHub. Examples: Stable Diffusion, various transformer implementations. Usage: download and run locally or on a cloud instance; **fine-tune** on your dataset. **Benefits:** flexibility and transparency; modify the code, train for unique applications.
>
> **3. Cloud Platforms** — Access: AWS, Google Cloud, Azure offer services to deploy/run models. Tools: integrated training, deployment, monitoring. Usage: deploy in scalable environments; use cloud **GPUs/TPUs** to speed up training and **inference**. **Benefits:** scalable infrastructure without on-premise hardware.
>
> **4. Custom Model Development** — Access: build your own models using frameworks like **PyTorch, TensorFlow, or Keras**. Usage: train from scratch on domain-specific data; customize **architecture and hyperparameters**. **Benefits:** complete control; tailored solutions.
>
> **5. Model Marketplaces** — Access: online marketplaces offer pre-trained models and datasets. Examples: **Hugging Face Model Hub**, TensorFlow Hub, AWS Bedrock catalog, Azure AI Foundry, Google Vertex AI Model Garden, NVIDIA NIM. Usage: explore models for different tasks; deploy directly or fine-tune. **Benefits:** quick access to many models, saving time and resources.

### 🧠 EXPLAINED

These are the **5 ways to get your hands on a GenAI model**, ordered roughly from *easiest/least control* to *hardest/most control*. As a backend dev, map this to a familiar spectrum: *"call a managed SaaS API"* → *"self-host an open-source library"* → *"build it yourself."*

- 🔑 **API (Application Programming Interface):** a defined way for your code to talk to a service over the network — you send a request (your prompt), you get a response (the model's output). You already use APIs daily; here the API *is* the model. **This is how you'll build 95% of real GenAI apps** — you never touch the model weights, you just call an endpoint. (Anthropic, OpenAI, Google, etc.)

- 🔑 **Pre-trained model:** a model someone else already trained; you just *use* it. (You're not paying the huge training cost.)

- 🔑 **Open-source vs open-weight:** *open-source* models let you download and run them yourself (e.g., **Stable Diffusion**, **Llama**). ⚠️ Nuance: many "open" models are technically **open-weight** — you get the trained weights to run/fine-tune, but not necessarily the training data or full training code. Either way: **you control where it runs** (great for privacy/cost/customization).

- 🔑 **Inference:** *using* a trained model to produce an output (as opposed to **training**, which is *building* it). Every time you send a prompt and get a response, that's one inference. Inference is what you pay for per-use; training is the big one-time cost.

- 🔑 **GPU / TPU:** specialized chips for the massive parallel math that AI needs. **GPU** = Graphics Processing Unit (NVIDIA dominates); **TPU** = Tensor Processing Unit (Google's custom AI chip). Recall from Study Guide 01: Transformers parallelize → they *need* these parallel chips.

- 🔑 **Cloud platform (AWS / Google Cloud / Azure):** rent scalable compute instead of buying servers. You deploy models there and scale up/down on demand.

- 🔑 **Deep learning framework (PyTorch / TensorFlow / Keras):** software libraries for building and training neural networks. **PyTorch** (Meta) dominates research; **TensorFlow** (Google) is common in production; **Keras** is a friendly high-level layer on top. (Think: the "Spring/Hibernate" of AI — the frameworks you code models in.)

- 🔑 **Architecture:** the structural design of a model (how many layers, how they connect). 🔑 **Hyperparameters:** the *dials you set before training* that control *how* it learns (e.g., learning rate, batch size) — as opposed to *parameters/weights*, which the model *learns by itself*. **Hyperparameters = you choose; parameters = model learns.**

- 🔑 **Model marketplace / hub:** an app-store-like catalog of ready-made models. **Hugging Face** is the giant here — the "GitHub of AI models." Cloud vendors have their own (**AWS Bedrock**, **Azure AI Foundry**, **Google Vertex AI Model Garden**, **NVIDIA NIM**).

> **Which will *you* use in this course?** Overwhelmingly **#1 (APIs)** and **#5 (hubs/Playgrounds)**. Options #3 and #4 (cloud training, custom models from scratch) are for teams with big budgets and specialized needs — good to *know*, rarely where you *start*.

---

## Page 8 — Popular GenAI Models

> 📄 **FROM THE PDF**
> - **OpenAI GPT Models:** widely used for reasoning, coding, business automation, multimodal apps, structured output, tool use, and agentic workflows. The GPT-5.x family is positioned for professional work, coding, complex reasoning, and multimodal use cases.
> - **Google Gemini:** strong in multimodal reasoning, long-context processing, coding, visual understanding, and integration across Google's AI ecosystem. Gemini 3 and Gemini 3.1 Pro represent Google's newer generation.
> - **Anthropic Claude:** known for strong writing, reasoning, coding, safety-focused design, long-context work, and agentic task handling. Claude Opus 4.8 and related Claude 4.x models represent Anthropic's 2026 generation.
> - **Meta Llama:** major role in **open-weight** AI adoption. Llama 4 introduced natively multimodal open-weight models — important for developers wanting control over deployment and customization.
> - **Gemma, Qwen, DeepSeek, Phi and other open-source models:** smaller, efficient models useful for fine-tuning, private deployment, coding, local inference, and domain-specific apps. Not every business needs the biggest **frontier** model. Many production systems mix small, medium, and large models based on **cost, latency, and accuracy** needs.

### 🧠 EXPLAINED

The exact version numbers will keep changing — **don't memorize them.** Instead, learn the *landscape* and the *decision framework*:

| Provider | Model family | Access model | Known for |
|---|---|---|---|
| **OpenAI** | GPT | Closed (API only) | Reasoning, coding, tool use, agents |
| **Google** | Gemini | Closed (API only) | Multimodal, long context, Google ecosystem |
| **Anthropic** | Claude | Closed (API only) | Writing, reasoning, coding, **safety**, agents |
| **Meta** | Llama | **Open-weight** | Self-hosting, customization, control |
| **Others** | Gemma, Qwen, DeepSeek, Phi | Mostly open-weight | Small, cheap, efficient, private/local |

- 🔑 **Frontier model:** the biggest, most capable (and most expensive) models at the cutting edge — e.g., top GPT/Gemini/Claude models.

- **The single most important business idea on this page** 👇
  > 🔑 **The cost / latency / accuracy trade-off:** you rarely want the biggest model for *everything*. Bigger models are more accurate but slower (**latency**) and pricier (**cost**). Real production systems **route** work to different sizes: a tiny cheap model for simple classification, a frontier model only for the hard reasoning. As an engineer, treating "which model?" as an *architecture decision* (like choosing a cache tier) is a mark of maturity.

- 🔑 **Latency:** how long the model takes to respond. Critical for user-facing apps (nobody waits 30s for a chatbot).

> **Fun fact for context:** these notes you're reading are being written *by* Claude (Anthropic's model family mentioned above) — so you're seeing one of these "popular models" in action right now. 🙂

---

## Page 9 — Ethical Considerations & Future

> 📄 **FROM THE PDF**
> **Ethical Considerations & Challenges** — With great power comes great responsibility. GenAI's ability to generate realistic content raises several ethical concerns:
> - **Bias:** AI models can perpetuate or amplify biases in training data.
> - **Misinformation:** realistic deepfakes and fake news pose risks to society.
> - **Intellectual Property:** determining ownership of AI-generated content is still a grey area.
>
> Ensuring responsible development and use of GenAI is crucial. Human oversight, transparency, and ethical guidelines are essential.
>
> **Future of Generative AI** — Industries will continue integrating GenAI to enhance creativity, optimize processes, and personalize experiences. As AI advances, collaboration between humans and AI will redefine possibilities, making innovation more accessible and powerful.

### 🧠 EXPLAINED

These aren't just "nice to mention" — they show up in system design reviews, compliance, and interviews about *responsible AI*.

- 🔑 **Bias:** if the training data over-represents certain groups/views, the model reproduces (and can amplify) those skews. Example: a resume-screening model trained on biased historical hiring data may unfairly rank candidates. **Mitigation:** diverse data, testing for fairness, human review.

- 🔑 **Misinformation & deepfakes:** GenAI can produce convincing fake text, images, audio, or video (a 🔑 **deepfake** = synthetic media that realistically impersonates a real person). Risk: fraud, propaganda, reputational harm. **Mitigation:** provenance/watermarking, verification, guardrails.

- 🔑 **Intellectual Property (IP):** who owns AI-generated content, and was the *training data* used with permission? Legally unsettled ("grey area"). Matters for any commercial product you ship.

- 🔑 **Human oversight / transparency:** keep a human "in the loop" for consequential decisions, and be open about when/how AI is used. This is the practical backbone of "responsible AI."

> 💻 **Engineer's takeaway:** treat these like **non-functional requirements** (security, reliability). You wouldn't ship a backend without auth and error handling; don't ship a GenAI feature without thinking about bias, hallucination/misinformation, IP, and human review.

**The future** the PDF describes = deeper human–AI collaboration across every industry. The durable trend to hold: **from AI that *generates* → to AI that *acts* (agents) → working alongside humans in real workflows.**

---

## 🗂️ Full Jargon Dictionary

> New terms introduced in this reading (terms already defined in Study Guide 01 — Transformer, LLM, parameter, fine-tuning, RLHF, token, context window — are in `revision/glossary.md`).

| Term | Definition | Why it matters |
|---|---|---|
| **Agent** | A GenAI system that plans, uses tools/APIs, and completes multi-step tasks — it *acts*, not just generates. | The defining 2026 capability; a later course module. |
| **Alignment** | Shaping a model to be helpful, honest, and harmless, matching user intent. | The safety goal behind modern models. |
| **API (Application Programming Interface)** | A network endpoint your code calls to send a prompt and get a model's output. | How most real GenAI apps are built. |
| **Architecture** | The structural design of a model (layers and how they connect). | You choose it when building custom models. |
| **Bias** | Skewed model behavior inherited/amplified from skewed training data. | Fairness, compliance, responsible AI. |
| **Cloud platform** | Rentable scalable compute (AWS/GCP/Azure) to train/deploy/run models. | Where models run at scale. |
| **Cost/latency/accuracy trade-off** | Bigger models = more accurate but slower & pricier; pick the right size per task. | Core production design decision. |
| **CRM / ERP** | Business software (customer relations / enterprise resource planning) agents integrate with. | Real-world tool-use targets. |
| **Deepfake** | Synthetic media realistically impersonating a real person. | Misinformation risk. |
| **Deep learning framework** | Libraries to build/train neural nets: PyTorch, TensorFlow, Keras. | The "coding tools" of AI. |
| **Diffusion model** | Generates images/audio/video by starting from noise and iteratively denoising. | Powers image generators (Stable Diffusion, etc.). |
| **Discriminative (traditional) AI** | AI that classifies/predicts (labels existing data) rather than creating. | The contrast that defines "generative." |
| **Evaluation pipeline (evals)** | Automated tests scoring model quality/safety before release. | QA/CI for models. |
| **Foundation model** | One large, general, pretrained model reused as the base for many tasks. | The central concept of modern AI. |
| **Frontier model** | The largest, most capable, most expensive cutting-edge models. | Top of the capability/cost curve. |
| **Full-stack technology layer** | GenAI treated as reusable infrastructure, like a DB or OS. | Framing for how pervasive AI has become. |
| **Generative AI** | AI models that create new content (text/image/audio/code). | The subject of the whole field. |
| **GPU / TPU** | Specialized parallel chips for AI math (NVIDIA GPUs / Google TPUs). | Hardware that makes training/inference feasible. |
| **Hyperparameter** | A dial *you* set before training (learning rate, batch size); controls *how* it learns. | Vs. parameters, which the model learns. |
| **Inference** | *Using* a trained model to produce output (vs. training = building it). | What you pay for per request. |
| **Intellectual Property (IP)** | Ownership of AI-generated content / training data rights — legally unsettled. | Commercial/legal risk. |
| **Model marketplace / hub** | Catalog of ready-made models (Hugging Face, Bedrock, Vertex, Azure AI Foundry, NVIDIA NIM). | Where you find and grab models. |
| **Multimodal** | Works with multiple data types (text, image, audio, video, docs) in one model. | The modern default for top models. |
| **Open-source / open-weight** | Models you can download and run yourself (weights available; open-source also implies code). | Control, privacy, customization. |
| **Pattern learning (statistical + semantic)** | Learning how things relate, not memorizing data. | Why models generalize. |
| **Pre-trained model** | A model already trained by someone else that you just use. | You skip the huge training cost. |
| **Reasoning model** | Spends extra compute at answer-time ("thinks longer") for hard problems. | Better math/logic/coding accuracy. |
| **System instructions / system prompt** | Hidden setup rules defining the model's role/behavior for a session. | You'll set these in Playgrounds. |
| **Tool use / function calling** | Model calling external functions/APIs and using the results. | Turns a generator into an agent. |
| **Training** | Building a model by adjusting weights over huge data (expensive, done once). | The costly build phase. |

---

## 📊 Key Comparison Tables

### The 5 access methods — control vs effort

| Method | Control | Effort/Cost to you | Best when... |
|---|---|---|---|
| **1. Pre-trained via API** | Low | Lowest | You want to ship fast; no ML expertise needed. ← *most apps* |
| **2. Open-source (self-host)** | High | Medium | You need privacy, customization, or lower per-call cost at scale. |
| **3. Cloud platforms** | Medium | Medium | You need scalable infra to deploy/run models. |
| **4. Custom model from scratch** | Highest | Highest | You have unique needs, data, and a big budget/team. ← *rare* |
| **5. Model marketplaces/hubs** | Varies | Low | You want to browse/grab a ready model quickly. |

### The 5 model families

| Family | Generates / Does | Example use |
|---|---|---|
| **Transformer** | Text, code, reasoning | Chatbots, code assistants |
| **Diffusion** | Images, audio, video | Midjourney, Stable Diffusion |
| **Multimodal** | Understands mixed media | "Describe this photo," analyze a chart |
| **Reasoning** | Hard multi-step problems | Math proofs, complex coding |
| **Agents** | Plans + acts with tools | Auto-book a meeting, run a workflow |

---

## 🧵 Connected Mental Model

```
                         GENERATIVE AI
              (creates new content; opposite of
               traditional/discriminative AI)
                             │
                    built on FOUNDATION MODELS
                             │
      ┌──────────┬───────────┼───────────┬──────────┐
   Transformer Diffusion  Multimodal  Reasoning   Agents
    (text/code) (img/vid)  (mixed)    (thinks +)  (acts +tools)
                             │
     ── HOW IT RUNS ──────────────────────────────────
     Train ▶ Pattern-learn ▶ Prompt(→tokens) ▶ Generate ▶ Align ▶ Tools/Agents
                             │
     ── HOW YOU ACCESS IT ────────────────────────────
     API · Open-source · Cloud · Custom-build · Marketplace
                             │
     ── WHO MAKES IT ─────────────────────────────────
     OpenAI(GPT) · Google(Gemini) · Anthropic(Claude) · Meta(Llama) · open models
                             │
     ── WATCH OUT FOR ────────────────────────────────
     Bias · Misinformation/Deepfakes · IP · (need human oversight)
```

**Ties back to Study Guide 01:** the *Transformer* you learned about is just **one** of the five families here, and the *LLM* is a **Transformer-based foundation model**. This reading zooms out to the whole GenAI picture around it.

---

## ⚡ 60-Second Recap

- **Generative AI = creates new content** (text/image/audio/code); traditional AI just **labels/predicts**.
- Built on **foundation models** — big general pretrained models reused for many tasks.
- **5 families:** Transformer (text), Diffusion (images), Multimodal (mixed), Reasoning (thinks longer), **Agents (acts + tools)**.
- **How it works (6 stages):** Train → Pattern-learn → Prompt (→tokens) → Generate → Align (RLHF) → Tool use/Agents.
- **5 ways to access:** API (easiest, most apps) · Open-source · Cloud · Custom-build · Marketplace (Hugging Face).
- **Players:** OpenAI (GPT), Google (Gemini), Anthropic (Claude), Meta (Llama, open-weight), + small open models (Gemma/Qwen/DeepSeek/Phi).
- **Pick models by cost / latency / accuracy** — not always the biggest.
- **Ethics:** bias, misinformation/deepfakes, IP → need human oversight & transparency.
- **The 2026 theme:** AI moved from *generating content* → *taking actions* (agents).

---

*This is your complete Week 1 Reading 02. Next: hands-on with LLM Playgrounds — where you'll access a model (method #1/#5 above) and try prompting it yourself.*
