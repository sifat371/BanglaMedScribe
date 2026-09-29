from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from banglamedscribe.schemas import SpeakerRole, TranscriptSegment


@dataclass(frozen=True, slots=True)
class SpeakerTurn:
    start: float
    end: float
    speaker: str

    def __post_init__(self) -> None:
        if self.start < 0 or self.end < 0:
            raise ValueError("speaker-turn timestamps must be non-negative")
        if self.end < self.start:
            raise ValueError("speaker-turn end must be >= start")
        if not self.speaker.strip():
            raise ValueError("speaker label must be non-empty")


@dataclass(frozen=True, slots=True)
class DiarizationResult:
    turns: list[SpeakerTurn]
    provider: str
    model: str


class DiarizationProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def diarize(self, audio_path: Path) -> DiarizationResult:
        raise NotImplementedError


def _overlap_seconds(segment: TranscriptSegment, turn: SpeakerTurn) -> float:
    return max(0.0, min(segment.end, turn.end) - max(segment.start, turn.start))


def assign_speakers_by_overlap(
    segments: list[TranscriptSegment],
    turns: list[SpeakerTurn],
    *,
    role_map: dict[str, SpeakerRole] | None = None,
) -> list[TranscriptSegment]:
    """Assign each ASR segment the diarization label with maximum temporal overlap.

    role_map may map diarization labels such as SPEAKER_00/SPEAKER_01 to
    domain roles such as DOCTOR/PATIENT after a separate role-identification step.
    Unmapped or non-overlapping segments remain UNKNOWN.
    """
    role_map = role_map or {}
    aligned: list[TranscriptSegment] = []

    for segment in segments:
        best_turn = None
        best_overlap = 0.0
        for turn in turns:
            overlap = _overlap_seconds(segment, turn)
            if overlap > best_overlap:
                best_overlap = overlap
                best_turn = turn

        speaker = (
            role_map.get(best_turn.speaker, SpeakerRole.OTHER)
            if best_turn is not None
            else SpeakerRole.UNKNOWN
        )
        aligned.append(segment.model_copy(update={"speaker": speaker}))

    return aligned
