# RAGBench

Evaluate saved RAG outputs: retrieval Recall/MRR/nDCG and reference-based answer scores.

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
python -m ragbench
python -m unittest discover -s tests -v
```

`--data path.json` accepts the schema in `examples/input.json`.
`--output path.json` sets the report location (default: `results/report.json`).
Source: `ragbench/core.py`; checks: `tests/`; inputs: `examples/`.

Consumes saved outputs; does not call a model or judge. Token overlap is not semantic correctness; citation ID precision checks membership, not factual support. Unanswerable rows are excluded from retrieval means.

The checked-in report is an executed demonstration, not a real-world benchmark.
Seed: 42 where randomness is used. Python 3.12.
