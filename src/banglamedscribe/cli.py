import argparse
import sys
from pathlib import Path

from banglamedscribe.pipeline import TranscriptionPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Transcribe a Bangla/Banglish consultation into timestamped JSON."
    )
    parser.add_argument("--audio", required=True, type=Path, help="Path to consultation audio")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to outputs/<audio-stem>/",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        pipeline = TranscriptionPipeline()
        transcript, transcript_path = pipeline.run(args.audio, args.output_dir)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    print(f"consultation_id: {transcript.consultation_id}")
    print(f"segments: {len(transcript.segments)}")
    print(f"transcript: {transcript_path}")


if __name__ == "__main__":
    main()
