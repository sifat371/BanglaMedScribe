# Evaluation protocol

The project separates **inference capability** from **measured ASR evidence**.

## 1. Build a reviewed manifest

Create a CSV with one utterance per row:

```csv
id,audio_path,reference
case-001,/data/case-001.wav,ম্যানুয়ালি যাচাই করা রেফারেন্স ট্রান্সক্রিপ্ট
```

References should be manually reviewed. Do not use model-generated transcripts as ground truth.

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

The summary contains corpus-level WER, CER, total audio/inference time, and real-time factor (RTF).

## 3. Report benchmark scope

Any public result should state:

- how audio was obtained (synthetic/scripted/public/consented);
- total duration and number of speakers/utterances;
- language mix (Bangla-only vs. code-switched);
- recording conditions;
- model and compute configuration;
- normalization/scoring policy;
- whether the result is development-only or held-out.

## 4. Recommended error slices

For clinical-style speech, maintain tags or separate manifests for:

- medical terminology;
- medication names;
- numbers, doses, and units;
- Bangla-English code switching;
- clean vs. controlled noisy audio.

Do not describe a small development set as representative of real clinical deployment.
