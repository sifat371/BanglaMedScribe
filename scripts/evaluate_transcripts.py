#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from banglamedscribe.evaluation import aggregate_transcripts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute corpus-level WER/CER from JSONL reference/hypothesis pairs."
    )
    parser.add_argument(
        "jsonl",
        type=Path,
        help="JSONL rows with string fields: reference and hypothesis",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pairs: list[tuple[str, str]] = []

    with args.jsonl.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            try:
                reference = str(row["reference"])
                hypothesis = str(row["hypothesis"])
            except KeyError as exc:
                raise SystemExit(
                    f"Missing {exc.args[0]!r} on line {line_number}"
                ) from exc
            pairs.append((reference, hypothesis))

    metrics = aggregate_transcripts(pairs)
    print(
        json.dumps(
            {
                "utterances": len(pairs),
                "wer": round(metrics.wer.rate, 6),
                "wer_percent": round(metrics.wer.rate * 100, 2),
                "wer_errors": metrics.wer.errors,
                "wer_reference_words": metrics.wer.reference_units,
                "cer": round(metrics.cer.rate, 6),
                "cer_percent": round(metrics.cer.rate * 100, 2),
                "cer_errors": metrics.cer.errors,
                "cer_reference_characters": metrics.cer.reference_units,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
