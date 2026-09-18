from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from banglamedscribe.schemas import TranscriptSegment


@dataclass(slots=True)
class ASRResult:
    segments: list[TranscriptSegment]
    detected_language: str | None = None
    language_probability: float | None = None
    duration_seconds: float | None = None


class ASRProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def requested_language(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def transcribe(self, audio_path: Path) -> ASRResult:
        raise NotImplementedError
