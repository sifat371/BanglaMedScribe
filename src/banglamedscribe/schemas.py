from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SpeakerRole(StrEnum):
    UNKNOWN = "UNKNOWN"
    DOCTOR = "DOCTOR"
    PATIENT = "PATIENT"
    OTHER = "OTHER"


class WordTimestamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start: float = Field(ge=0)
    end: float = Field(ge=0)
    text: str = Field(min_length=1)
    probability: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode="after")
    def validate_time_order(self) -> "WordTimestamp":
        if self.end < self.start:
            raise ValueError("word end time must be greater than or equal to start time")
        return self


class TranscriptSegment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    start: float = Field(ge=0)
    end: float = Field(ge=0)
    speaker: SpeakerRole = SpeakerRole.UNKNOWN
    text: str = Field(min_length=1)
    words: list[WordTimestamp] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_time_order(self) -> "TranscriptSegment":
        if self.end < self.start:
            raise ValueError("segment end time must be greater than or equal to start time")
        return self


class AudioMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    original_filename: str
    duration_seconds: float | None = Field(default=None, ge=0)
    sample_rate_hz: int | None = Field(default=None, gt=0)
    channels: int | None = Field(default=None, gt=0)


class ASRMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str
    requested_language: str | None = None
    detected_language: str | None = None
    language_probability: float | None = Field(default=None, ge=0, le=1)


class TranscriptDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: str = "1.0"
    consultation_id: str
    audio: AudioMetadata
    asr: ASRMetadata
    segments: list[TranscriptSegment]

    @property
    def text(self) -> str:
        return " ".join(segment.text for segment in self.segments).strip()
