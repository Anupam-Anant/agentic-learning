# Week 2 — Code

Runnable examples that accompany the Week 2 study guides.

## Setup

```bash
pip install openai
export OPENAI_API_KEY=sk-...        # or use Colab Secrets in a notebook
```

## Files

| File | Study guide | What it shows | Run |
|---|---|---|---|
| `prompt_engineering_demo.py` | `notes/study-guide-02-basic-prompt-engineering.md` | The 4 basic prompt-engineering techniques — zero-shot, few-shot, prompt chaining, chain-of-thought | `python prompt_engineering_demo.py` |
| `bert_tasks_demo.py` | `notes/study-guide-04-using-bert-for-simple-tasks.md` | Running BERT **locally** via Hugging Face `transformers` for 3 understanding tasks — sentiment classification, NER, extractive QA | `python bert_tasks_demo.py` |

### Notes on `bert_tasks_demo.py`
- **Original Colab notebook** (from the PDF): https://colab.research.google.com/drive/19JHeS3NBrtXEnDOtHPMlDCb5MAqLEn1- (may require Google sign-in). This local script is the runnable equivalent.
- **Different dependencies** from the OpenAI examples: `pip install transformers torch` — and **no API key**. It runs an open-source model **locally** (weights download from the Hugging Face Hub on first run and are cached under `~/.cache/huggingface`).
- **First run downloads a few hundred MB** of model weights per pipeline; later runs are offline and fast.
- The PDF's QA example passed `device="cuda"` (NVIDIA GPU) — that **errors without a CUDA GPU** (e.g. on a Mac), so the runnable file omits it and uses CPU. On Apple Silicon you can try `device="mps"`.
- Faithful fixes vs the PDF: the "deafeated" typo → "defeated"; the backwards default-model comment corrected. See the study guide for details.

### Notes on `prompt_engineering_demo.py`
- Uses the OpenAI **Chat Completions** API (`client.chat.completions.create`, `gpt-4o-mini`) to stay faithful to the PDF — this differs from `week1/code/`, which uses the newer **Responses API**. The techniques are API-agnostic; the study guide shows the Responses-API equivalent.
- The PDF's snippet omitted the client setup and mislabels technique #2 as "One Shot" (it is actually **few-shot** — three examples). Both are noted in the file header.
- Each run makes **5 live API calls** (zero-shot ×1, few-shot ×1, chaining ×2, CoT ×1), so it costs a few tokens. Outputs are non-deterministic (no `temperature=0` here) — expect wording to vary run to run.
