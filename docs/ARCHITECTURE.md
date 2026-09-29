# Architecture

BanglaMedScribe is organized as a modular speech-processing pipeline. Model-specific components live
behind provider interfaces so inference backends can be compared or replaced without changing
downstream contracts.

```text
Audio
  |
  v
Audio preprocessing
16 kHz mono PCM WAV
  |
  +---------------------------+
  |                           |
  v                           v
ASRProvider               DiarizationProvider
  |                           |
  v                           v
timestamped transcript     anonymous speaker turns
  |                           |
  +------------+--------------+
               |
               v
      temporal speaker alignment
               |
               v
      speaker-attributed transcript
               |
               v
      [future] role identification
               |
               v
      [future] clinical extraction
```

## Stable contracts

- `TranscriptDocument` is the stable ASR output boundary.
- `ASRProvider` isolates model-specific transcription code.
- `DiarizationProvider` isolates future speaker-diarization backends.
- WER/CER evaluation is provider-independent.
- Role identification is explicitly separate from anonymous speaker diarization.

## Evaluation boundary

`scripts/run_asr_benchmark.py` executes the configured ASR pipeline against a reviewed manifest and
writes per-utterance hypotheses plus corpus-level WER/CER/RTF.

The repository should not publish clinical accuracy claims unless the benchmark source, duration,
speaker composition, recording conditions, reference-review process, model configuration, and
scoring policy are documented.

## Why provider adapters?

The best ASR or diarization model may change as Bangla/Banglish clinical-style accuracy is measured.
Stable provider contracts let the project compare Whisper-family, Bengali-specific, local, or hosted
systems without rewriting evaluation or downstream processing.
