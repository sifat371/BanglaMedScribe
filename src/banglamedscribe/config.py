from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from BMS_* environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="BMS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    asr_provider: str = "faster-whisper"
    asr_model: str = "large-v3"
    asr_language: str | None = "bn"
    asr_device: str = "auto"
    asr_compute_type: str = "auto"
    asr_beam_size: int = Field(default=5, ge=1, le=20)
    asr_vad_filter: bool = True
    asr_word_timestamps: bool = True

    output_dir: Path = Path("outputs")
    keep_processed_audio: bool = False
    max_upload_mb: int = Field(default=100, ge=1, le=2048)


def get_settings() -> Settings:
    return Settings()
