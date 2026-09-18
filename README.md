# BanglaMedScribe

> Working codename for a showcaseable Bangla/Banglish clinical documentation assistant.

BanglaMedScribe V1 is being built around one product experience:

**consultation audio → timestamped transcript → clinical facts → evidence-linked clinical note → clinician review**

The project is currently in **Sprint 1: Foundation + ASR**.

## Product boundary

BanglaMedScribe is a **clinical documentation assistant**. It is not an autonomous diagnostic or prescribing system. During the showcase/pre-pilot phase, use synthetic, scripted, public, or appropriately consented demonstration audio only.

## Sprint 1

The current branch implements:

- 16 kHz mono audio preprocessing with ffmpeg
- a pluggable `ASRProvider` interface
- local transcription through `faster-whisper`
- Bangla-oriented defaults with Banglish/English preserved by the multilingual model
- timestamped segments and optional word timestamps
- typed Pydantic transcript schemas
- a CLI runner
- a minimal FastAPI transcription endpoint
- tests that do not require model downloads
- GitHub Actions lint/test CI

Speaker diarization and doctor/patient role assignment come next.

## Requirements

- Python 3.11+
- ffmpeg
- a machine capable of running your selected Whisper model

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

The default ASR model is `large-v3`. Change `BMS_ASR_MODEL` in `.env` if you want a smaller model during development.

## Run the Sprint 1 pipeline

```bash
python run_pipeline.py --audio path/to/consultation.wav
```

Output:

```text
outputs/
└── consultation/
    └── transcript.json
```

The same command is available after installation as:

```bash
bms-transcribe --audio path/to/consultation.wav
```

## Run the API

```bash
uvicorn banglamedscribe.api:app --reload
```

Health check:

```text
GET /health
```

Transcription:

```text
POST /v1/transcribe
Content-Type: multipart/form-data
field: audio
```

The first transcription request loads the configured ASR model.

## Test

```bash
ruff check .
pytest
```

The test suite uses an injected fake ASR provider, so CI does not download Whisper weights.

## Planned V1 milestones

1. **Foundation + ASR** — audio → timestamped transcript
2. **Diarization** — transcript → doctor/patient turns
3. **Clinical extraction** — transcript → structured clinical facts
4. **Grounded note** — facts → evidence-linked clinical note
5. **Showcase UI** — record/upload → review → edit → export

See `docs/SPRINT_1.md`, `docs/ARCHITECTURE.md`, and `docs/SAFETY.md` for the current engineering boundary.
