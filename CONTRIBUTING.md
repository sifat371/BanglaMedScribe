# Contributing

BanglaMedScribe is an early research/engineering project. Contributions should improve measurable
speech-processing capability, reproducibility, or safety rather than add unsupported product claims.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m build
```

ASR and diarization backends are optional:

```bash
python -m pip install -e ".[asr,diarization,dev]"
```

## Expectations

- keep model-specific code behind provider interfaces;
- add tests for provider-independent logic;
- document any benchmark dataset and scoring policy;
- never report unreviewed model output as ground truth;
- do not commit private patient data or credentials;
- distinguish implemented features from planned work;
- include limitations when adding evaluation results.

## Benchmark changes

A benchmark PR should identify the data source, duration, language mix, speaker composition,
recording conditions, reference-review method, model/runtime configuration, and evaluation metric.
