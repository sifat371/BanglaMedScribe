# Sprint 1 — Foundation and ASR

## Goal

Turn one consultation audio file into a reproducible, timestamped transcript JSON document.

## Scope

- Python package and configuration
- audio validation and ffmpeg preprocessing
- pluggable ASR provider interface
- faster-whisper provider
- Bengali/Banglish-oriented default configuration
- word/segment timestamps
- typed transcript schema
- CLI entry point
- minimal FastAPI endpoint
- tests that do not require model downloads
- CI lint/test workflow

## Definition of done

Running:

```bash
python run_pipeline.py --audio samples/demo.wav
```

creates:

```text
outputs/demo/
└── transcript.json
```

The JSON includes consultation/audio/ASR metadata, timestamped segments, optional word timestamps,
and a speaker placeholder set to `UNKNOWN`.

Speaker diarization and doctor/patient role assignment are intentionally Sprint 2.

## Safety boundary

Sprint 1 is for synthetic, scripted, public, or appropriately consented demonstration audio.
Do not use uncontrolled real patient data in the public pre-pilot.
