#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from banglamedscribe.config import get_settings
from banglamedscribe.diarization import build_diarization_provider


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the configured speaker diarization provider."
    )
    parser.add_argument("audio", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    provider = build_diarization_provider(settings)
    result = provider.diarize(args.audio)

    payload = {
        "provider": result.provider,
        "model": result.model,
        "turns": [
            {
                "start": round(turn.start, 4),
                "end": round(turn.end, 4),
                "speaker": turn.speaker,
            }
            for turn in result.turns
        ],
    }

    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"Wrote: {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
