import shutil
import subprocess
import wave
from pathlib import Path

from banglamedscribe.schemas import AudioMetadata

SUPPORTED_AUDIO_SUFFIXES = {
    ".wav",
    ".mp3",
    ".m4a",
    ".flac",
    ".ogg",
    ".webm",
    ".mp4",
}


def validate_audio_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Audio path is not a file: {path}")
    if path.suffix.lower() not in SUPPORTED_AUDIO_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_AUDIO_SUFFIXES))
        raise ValueError(f"Unsupported audio format '{path.suffix}'. Supported: {supported}")


def prepare_audio(input_path: Path, output_path: Path) -> AudioMetadata:
    """Convert input audio to 16 kHz mono PCM WAV using ffmpeg."""

    validate_audio_path(input_path)

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError(
            "ffmpeg is required for audio preprocessing. Install ffmpeg and ensure it is in PATH."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        error = exc.stderr.strip() or "unknown ffmpeg error"
        raise RuntimeError(f"Failed to preprocess audio: {error}") from exc

    with wave.open(str(output_path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        frames = wav_file.getnframes()
        duration = frames / sample_rate if sample_rate else None

    return AudioMetadata(
        original_filename=input_path.name,
        duration_seconds=duration,
        sample_rate_hz=sample_rate,
        channels=channels,
    )
