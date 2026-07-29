# Week 1 — Code (OpenAI Responses API)

Clean, runnable versions of the examples from **Study Guide 03**. The PDF's code was OCR-scrambled; these are the corrected files.

## Setup

```bash
pip install openai pydantic
```

Make your API key available as an environment variable:

- **Google Colab:** add a secret named `OPENAI_API_KEY` (Secrets/key icon in the left sidebar) and enable notebook access. `openai_client.py` reads it automatically.
- **Locally:** `export OPENAI_API_KEY=sk-...` before running.

> 🔐 Never hardcode the key or commit it to git. If it leaks, revoke & rotate it on the OpenAI dashboard.

## Files

| File | Shows |
|---|---|
| `openai_client.py` | Reusable configured client + `OPENAI_MODEL` constant. Imported by the others. |
| `01_basic_and_multiturn.py` | Basic call, multi-message (roles), and follow-up via `previous_response_id`. |
| `02_structured_output.py` | Schema-safe JSON via a Pydantic model and via a manual JSON Schema. |
| `03_streaming.py` | Incremental streaming with `stream=True` and event handling. |

## Run

```bash
python 01_basic_and_multiturn.py
python 02_structured_output.py
python 03_streaming.py
```

> Note: these call the live OpenAI API and will consume a small amount of API credit each run.
