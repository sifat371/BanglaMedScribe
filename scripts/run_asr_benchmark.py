#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from banglamedscribe.evaluation import aggregate_transcripts, score_transcript
from banglamedscribe.pipeline import TranscriptionPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the configured ASR system over a reviewed benchmark manifest."
    )
    parser.add_argument(
        "manifest",
        type=Path,
        help="CSV with columns: id,audio_path,reference",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("benchmarks/results"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    with args.manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    required = {"id", "audio_path", "reference"}
    if not rows:
        raise SystemExit("Benchmark manifest is empty.")
    missing = required - set(rows[0])
    if missing:
        raise SystemExit(f"Manifest is missing columns: {', '.join(sorted(missing))}")

    pipeline = TranscriptionPipeline()
    pairs: list[tuple[str, str]] = []
    utterance_results: list[dict[str, object]] = []
    total_audio_seconds = 0.0
    total_inference_seconds = 0.0
    provider = model = None

    for row in rows:
        audio_path = Path(row["audio_path"])
        reference = row["reference"]

        started = time.perf_counter()
        transcript = pipeline.transcribe(audio_path)
        elapsed = time.perf_counter() - started

        hypothesis = " ".join(segment.text for segment in transcript.segments).strip()
        metrics = score_transcript(reference, hypothesis)
        duration = float(transcript.audio.duration_seconds or 0.0)
        rtf = elapsed / duration if duration > 0 else None

        provider = transcript.asr.provider
        model = transcript.asr.model
        total_audio_seconds += duration
        total_inference_seconds += elapsed
        pairs.append((reference, hypothesis))

        utterance_results.append(
            {
                "id": row["id"],
                "audio_path": str(audio_path),
                "reference": reference,
                "hypothesis": hypothesis,
                "duration_seconds": round(duration, 4),
                "inference_seconds": round(elapsed, 4),
                "rtf": round(rtf, 6) if rtf is not None else None,
                "wer": round(metrics.wer.rate, 6),
                "cer": round(metrics.cer.rate, 6),
            }
        )

    aggregate = aggregate_transcripts(pairs)
    overall_rtf = (
        total_inference_seconds / total_audio_seconds
        if total_audio_seconds > 0
        else None
    )

    jsonl_path = args.output_dir / "utterances.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in utterance_results:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    summary = {
        "utterances": len(utterance_results),
        "provider": provider,
        "model": model,
        "audio_seconds": round(total_audio_seconds, 3),
        "inference_seconds": round(total_inference_seconds, 3),
        "rtf": round(overall_rtf, 6) if overall_rtf is not None else None,
        "wer": round(aggregate.wer.rate, 6),
        "wer_percent": round(aggregate.wer.rate * 100, 2),
        "cer": round(aggregate.cer.rate, 6),
        "cer_percent": round(aggregate.cer.rate * 100, 2),
    }

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote: {jsonl_path}")
    print(f"Wrote: {summary_path}")


if __name__ == "__main__":
    main()
