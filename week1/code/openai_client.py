"""
Reusable OpenAI client module.

Import this from the other example scripts:
    from openai_client import client, OPENAI_MODEL

Setup:
  1. pip install openai
  2. Make your API key available as the OPENAI_API_KEY environment variable.
     - In Google Colab: store it in Colab Secrets (name = OPENAI_API_KEY),
       and the block below reads it automatically.
     - Locally: export OPENAI_API_KEY=sk-...   (or use a .env loader)

Never hardcode the key in source or commit it to git.
"""

import os
from openai import OpenAI

# Centralize the model choice in ONE place so you can swap models easily.
# "mini" = smaller, cheaper, faster. Swap up only where you need more capability.
OPENAI_MODEL = "gpt-4.1-mini"

# --- Read the key from Colab Secrets when running in Google Colab ---
try:
    from google.colab import userdata  # only exists inside Colab
    os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
except ImportError:
    # Running locally: assume OPENAI_API_KEY is already in the environment.
    pass

# With no arguments, the client auto-reads OPENAI_API_KEY from the environment.
client = OpenAI()

# Equivalent explicit form:
# client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
