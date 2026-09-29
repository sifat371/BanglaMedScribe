# BanglaMedScribe

> Working codename for a Bangla/Banglish clinical speech research and documentation prototype.

The project is being matured around a measurable speech-processing core:

**consultation audio → reproducible ASR → quantitative evaluation → speaker attribution → downstream clinical structure**

The current codebase is a research/engineering prototype, not a validated clinical system.

## What is implemented

- 16 kHz mono audio preprocessing with ffmpeg
- pluggable `ASRProvider` abstraction
- local multilingual transcription through `faster-whisper`
- Bangla-oriented defaults with Banglish/English preserved by the multilingual model
- segment and optional word timestamps
- typed Pydantic transcript schemas
- CLI and FastAPI inference surfaces
- corpus-level WER/CER scoring
- end-to-end benchmark runner producing per-utterance results and aggregate WER/CER/RTF
- model-agnostic `DiarizationProvider` boundary
- deterministic alignment of ASR segments with diarization turns
- unit tests, Ruff linting, and GitHub Actions CI

## What is not claimed yet

The repository does **not** currently claim:

- a representative Bengali clinical-speech WER/CER;
- a validated speaker-diarization model or DER result;
- doctor/patient role-identification accuracy;
- clinical deployment readiness;
- diagnostic or prescribing capability.

Those require reviewed benchmark data and explicit evaluation.

## Requirements

- Python 3.11+
- ffmpeg
- a machine capable of running the selected Whisper model

## Setup

```bash
git clone https://github.com/sifat371/BanglaMedScribe.git
cd BanglaMedScribe

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[asr,dev]"
cp .env.example .env
```

The default ASR model is `large-v3`. Change `BMS_ASR_MODEL` in `.env` when benchmarking other configurations.

## Run transcription

```bash
python run_pipeline.py --audio path/to/consultation.wav
```

or:

```bash
bms-transcribe --audio path/to/consultation.wav
```

## Run the API

```bash
uvicorn banglamedscribe.api:app --reload
```

- `GET /health`
- `POST /v1/transcribe` with multipart field `audio`

## Evaluate ASR

For already generated reference/hypothesis pairs:

```bash
python scripts/evaluate_transcripts.py benchmarks/example_pairs.jsonl
```

For a reviewed audio manifest:

```bash
python scripts/run_asr_benchmark.py benchmarks/manifest.csv
```

The benchmark runner writes per-utterance hypotheses plus corpus-level **WER, CER, and real-time factor (RTF)**.

See `docs/EVALUATION.md` for the evaluation protocol. No benchmark number should be reported without a reviewed reference set and documented scope.

## Diarization

`src/banglamedscribe/diarization.py` defines a provider-agnostic diarization contract and deterministic ASR-turn alignment.

A concrete pyannote/NeMo/local backend still needs to be implemented and evaluated before claiming speaker-diarization performance. Anonymous speaker labels are intentionally kept separate from doctor/patient role identification.

See `docs/DIARIZATION.md`.

## Test

```bash
ruff check .
pytest
```

CI avoids model downloads by testing provider-independent logic with injected fixtures.

## Research maturity roadmap

1. **Reviewed Bangla/Banglish clinical-style evaluation set**
2. **ASR baselines** — WER/CER/RTF across model/configuration choices
3. **Noise and code-switching slices**
4. **Concrete diarization backend** — DER and speaker-attribution evaluation
5. **Clinical terminology / medication / numeric error analysis**
6. **Only then:** domain adaptation or fine-tuning where the benchmark justifies it

## Safety boundary

Use synthetic, scripted, public, or appropriately consented audio during development. Real patient data requires appropriate governance, privacy controls, retention policy, and clinical review.

The project is not an autonomous diagnostic or prescribing system.
