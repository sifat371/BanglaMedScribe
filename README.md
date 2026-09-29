# BanglaMedScribe

[![CI](https://github.com/sifat371/BanglaMedScribe/actions/workflows/ci.yml/badge.svg)](https://github.com/sifat371/BanglaMedScribe/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](CHANGELOG.md)

> Bangla/Banglish clinical speech processing and documentation research prototype.

BanglaMedScribe is being developed around a measurable speech-processing core:

**consultation audio → reproducible ASR → quantitative evaluation → speaker diarization/alignment → downstream clinical structure**

The repository is a research/engineering prototype, not a validated clinical system.

## Current maturity

| Capability | Status |
| --- | --- |
| 16 kHz audio preprocessing | Implemented |
| faster-whisper ASR | Implemented |
| Word/segment timestamps | Implemented |
| FastAPI + CLI inference | Implemented |
| WER/CER scoring | Implemented |
| End-to-end WER/CER/RTF benchmark runner | Implemented |
| Tag-based clinical error slices | Implemented |
| pyannote Community-1 adapter | Implemented, not yet clinically benchmarked |
| ASR/diarization temporal alignment | Implemented |
| Diarization DER benchmark | Pending reviewed multi-speaker data |
| Doctor/patient role identification | Pending |
| Clinical fact extraction / note generation | Pending |

## Speech pipeline

- ffmpeg preprocessing to 16 kHz mono PCM WAV;
- pluggable `ASRProvider` abstraction;
- local multilingual transcription through `faster-whisper`;
- Bangla-oriented defaults while preserving Banglish/English output from the multilingual model;
- segment and optional word timestamps;
- typed Pydantic transcript schemas;
- CLI and FastAPI inference;
- corpus-level WER/CER scoring;
- benchmark runner with WER/CER/RTF, runtime configuration capture, and tag-based error slices;
- model-independent diarization contract;
- optional local pyannote Community-1 adapter;
- deterministic ASR-segment / diarization-turn alignment;
- Python 3.11/3.12 CI, tests, linting, console-entry checks, and package-build verification.

## What is not claimed

The repository does **not** currently claim:

- representative Bengali clinical-speech WER/CER;
- a Bengali clinical diarization DER;
- doctor/patient role-identification accuracy;
- clinical deployment readiness;
- diagnostic or prescribing capability.

Those require reviewed benchmark data and explicit evaluation.

## Setup

Requirements: Python 3.11+, ffmpeg, and suitable compute for the selected speech model.

```bash
git clone https://github.com/sifat371/BanglaMedScribe.git
cd BanglaMedScribe

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[asr,dev]"
cp .env.example .env
```

For optional local speaker diarization:

```bash
python -m pip install -e ".[asr,diarization,dev]"
```

The default ASR model is `large-v3`. Runtime settings are documented in `.env.example`.

## Transcribe

```bash
bms-transcribe --audio path/to/consultation.wav
```

The FastAPI service exposes:

- `GET /health`
- `POST /v1/transcribe` with multipart field `audio`

Run locally with:

```bash
uvicorn banglamedscribe.api:app --reload
```

## Benchmark ASR

Build a manually reviewed manifest using `benchmarks/manifest.example.csv`, then run:

```bash
python scripts/run_asr_benchmark.py benchmarks/manifest.csv
```

Outputs include:

- per-utterance reference/hypothesis records;
- WER and CER;
- real-time factor (RTF);
- model/runtime settings;
- slice-level WER/CER for tags such as `code-switch`, `medication`, `dose-number`, and `noisy`.

See [Evaluation protocol](docs/EVALUATION.md).

No benchmark number should be reported without a reviewed reference set and documented scope.

## Speaker diarization

The optional pyannote adapter uses the open Community-1 diarization pipeline and prefers exclusive
speaker turns when available for easier reconciliation with ASR timestamps.

```bash
export BMS_DIARIZATION_HF_TOKEN=...
bms-diarize path/to/conversation.wav
```

The project intentionally separates anonymous labels such as `SPEAKER_00` from semantic roles such
as doctor and patient. Role assignment needs its own evaluation.

See [Diarization](docs/DIARIZATION.md).

## Test and build

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m build
```

CI runs the provider-independent test suite on Python 3.11 and 3.12 without downloading ASR or
diarization model weights.

## Research maturity roadmap

1. **Reviewed Bangla/Banglish clinical-style evaluation set**
2. **ASR baseline table** — model/configuration WER, CER, and RTF
3. **Noise, code-switching, medication, and dose-number slices**
4. **Multi-speaker benchmark** — DER and speaker-attribution analysis
5. **Clinical terminology error analysis**
6. **Domain adaptation/fine-tuning only after the benchmark identifies a justified target**

## Safety and privacy

Use synthetic, scripted, public, de-identified, or appropriately consented audio during development.
Real patient data requires appropriate governance, privacy controls, retention policy, and clinical
review.

See [Security and privacy](SECURITY.md) and [development safety boundary](docs/SAFETY.md).

BanglaMedScribe is not an autonomous diagnostic or prescribing system.
