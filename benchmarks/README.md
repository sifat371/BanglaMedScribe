# ASR evaluation

This directory is the reproducible evaluation boundary for the project.

The repository currently provides **evaluation tooling, not a clinical accuracy claim**. Do not
publish WER/CER numbers until the corresponding audio and reference transcripts have been manually
reviewed and the evaluation manifest is committed or otherwise versioned.

## JSONL scoring format

Each line contains:

```json
{"id":"demo-001","reference":"আমার তিন দিন ধরে জ্বর","hypothesis":"আমার তিন দিন ধরে জ্বর"}
```

Score a completed run with:

```bash
python scripts/evaluate_transcripts.py benchmarks/example_pairs.jsonl
```

## Planned benchmark dimensions

A useful first benchmark should report corpus-level WER/CER plus slices for:

- Bangla-only speech
- Bangla-English code switching
- medication names and clinical terminology
- numbers, doses, and units
- clean audio
- controlled noisy audio

The benchmark must distinguish synthetic/scripted evaluation from real clinical data. Real patient
audio requires appropriate consent, governance, privacy controls, and review.
