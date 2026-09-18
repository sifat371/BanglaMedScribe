# V1 Architecture

BanglaMedScribe is a modular pipeline. Model-specific code lives behind provider interfaces so components can be replaced without changing the product contract.

```text
Audio
  ↓
Audio preprocessing (16 kHz mono WAV)
  ↓
ASRProvider
  ↓
TranscriptDocument
  ↓
[Sprint 2] diarization + role assignment
  ↓
[Sprint 3] clinical facts
  ↓
[Sprint 4] evidence-linked clinical note
  ↓
Clinician review
```

## Stable V1 contract

The first stable artifact is `TranscriptDocument`, defined in
`src/banglamedscribe/schemas.py`.

Downstream components should depend on this schema rather than on faster-whisper objects directly.

## Why provider adapters?

The ASR model will likely change as Bangla/Banglish clinical accuracy is benchmarked. Keeping an
`ASRProvider` boundary lets us compare or replace Whisper-family, Bengali-specific, local, or hosted
ASR implementations without rewriting the downstream pipeline.
