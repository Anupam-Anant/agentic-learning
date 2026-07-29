"""
Week 2 · Study Guide 04 companion — Using BERT for simple NLP tasks
===================================================================
Runnable version of the three tasks from the Week 2 PDF #4, via Hugging Face
`transformers` pipelines:
  1. Text classification (sentiment)  — default model: DistilBERT (SST-2)
  2. Named Entity Recognition (NER)    — dbmdz/bert-large-cased-finetuned-conll03-english
  3. Question answering (extractive)   — default DistilBERT (SQuAD)

Unlike week1/ (which called the OpenAI *API*), this runs an OPEN-SOURCE model
*locally*: `transformers` downloads the weights from the Hugging Face Hub on the
first run and executes them via PyTorch (`torch`). No API key needed — this is
the "open-source / self-hosted" path from Study Guide 02·01, made concrete.

NOTES (differences from the PDF, so the script runs anywhere):
  * The PDF's QA example passed device="cuda" (NVIDIA GPU). That raises an error
    on a machine without a CUDA GPU (e.g. a Mac), so it's omitted here — the
    pipeline runs on CPU by default. (On Apple Silicon you may pass device="mps".)
  * The PDF's QA question has a typo ("deafeated"); fixed to "defeated" below.
  * First run downloads a few hundred MB of model weights per pipeline.

Run:
    pip install transformers torch
    python bert_tasks_demo.py
"""

from transformers import pipeline


def task1_text_classification():
    """Sentiment: text -> POSITIVE/NEGATIVE + confidence score."""
    # No model argument -> the pipeline picks a DEFAULT model:
    # DistilBERT fine-tuned on SST-2 (distilbert-base-uncased-finetuned-sst-2-english).
    classifier = pipeline("sentiment-analysis")
    text = "I love using BERT for natural language processing tasks!"
    print("1) Sentiment:", classifier(text))
    # => [{'label': 'POSITIVE', 'score': 0.9998...}]


def task2_named_entity_recognition():
    """NER: tag each token as a person / location / organization / etc."""
    # Here we DO pass an explicit fine-tuned model (BERT-large, CoNLL-03 English).
    ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
    text = "India lay down the gauntlet to Australia with 295-run thrashing."
    print("2) Entities:")
    for entity in ner(text):
        print("   ", entity)
    # 'India' -> I-LOC, 'Australia' -> I-LOC   (I-LOC = inside a LOCation span)


def task3_question_answering():
    """Extractive QA: return the SPAN of the context that answers the question."""
    # PDF used device="cuda"; omitted so this runs on CPU anywhere.
    qa = pipeline("question-answering")
    context = "India won the first test against Australia"
    question = "Who defeated Australia in first test?"   # PDF typo "deafeated" fixed
    print("3) Answer:", qa({"context": context, "question": question}))
    # => {'score': 0.59..., 'start': 0, 'end': 42, 'answer': 'India won the first test against Australia'}


if __name__ == "__main__":
    task1_text_classification()
    task2_named_entity_recognition()
    task3_question_answering()
