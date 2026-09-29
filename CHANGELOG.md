# Changelog

## 0.2.0-alpha — research-maturity branch

### Added
- corpus-level WER/CER scoring;
- end-to-end ASR benchmark runner with RTF reporting;
- tag-based benchmark slices for code-switching, medication, noise, and other error categories;
- model/runtime configuration capture in benchmark summaries;
- provider-independent diarization contracts and ASR-turn alignment;
- optional pyannote Community-1 diarization adapter and CLI;
- diarization/evaluation regression tests;
- multi-version CI, package-build checks, project metadata, licensing, citation, and contribution guidance.

### Changed
- reframed the README around measurable speech-processing evidence;
- clarified that representative clinical ASR/diarization performance has not yet been established.

## 0.1.0

Initial Foundation + ASR implementation:
- ffmpeg preprocessing;
- faster-whisper provider;
- timestamped transcript schema;
- CLI and FastAPI inference;
- lightweight tests and CI.
