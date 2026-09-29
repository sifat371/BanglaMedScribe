# Evaluation protocol

The project separates **inference capability** from **measured ASR evidence**.

## 1. Build a reviewed manifest

Create a CSV with one utterance per row:

```csv
id,audio_path,reference,tags
case-001,/data/case-001.wav,ম্যানুয়ালি যাচাই করা রেফারেন্স ট্রান্সক্রিপ্ট,bangla;clean;symptom
```

Required columns are `id`, `audio_path`, and `reference`. The optional `tags` column accepts
semicolon-separated labels and enables slice-level reporting.

References should be manually reviewed. Do not use model-generated transcripts as ground truth.

Recommended tags include:

- `bangla`
- `code-switch`
- `medical-term`
- `medication`
- `dose-number`
- `clean`
- `noisy`

## 2. Run the configured ASR benchmark

Install the ASR extra and ensure ffmpeg is available:

```bash
python -m pip install -e ".[asr,dev]"
python scripts/run_asr_benchmark.py benchmarks/manifest.csv
```

The run writes:

```text
benchmarks/results/
├── utterances.jsonl
└── summary.json
```

The summary contains:

- corpus-level WER and CER;
- total inference time and real-time factor (RTF);
- the actual ASR model/runtime configuration;
- WER/CER by every manifest tag.

This makes it possible to distinguish, for example, overall performance from code-switched,
medication-name, dose-number, and noisy-speech performance.

## 3. Report benchmark scope

Any public result should state:

- how audio was obtained (synthetic/scripted/public/consented);
- total duration and number of speakers/utterances;
- language mix (Bangla-only vs. code-switched);
- recording conditions;
- model and compute configuration;
- normalization/scoring policy;
- whether the result is development-only or held-out.

## 4. Clinical-style error slices

A single headline WER can hide the errors that matter most in a documentation setting. At minimum,
report separate slices where the data supports them for:

- medical terminology;
- medication names;
- numbers, doses, and units;
- Bangla-English code switching;
- clean vs. controlled noisy audio.

Do not describe a small development set as representative of real clinical deployment.
