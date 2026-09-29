from __future__ import annotations

from pathlib import Path
from typing import Any

from banglamedscribe.config import Settings
from banglamedscribe.diarization import (
    DiarizationProvider,
    DiarizationResult,
    SpeakerTurn,
)


def _annotation_to_turns(annotation: Any) -> list[SpeakerTurn]:
    turns: list[SpeakerTurn] = []

    if hasattr(annotation, "itertracks"):
        for segment, _track, speaker in annotation.itertracks(yield_label=True):
            turns.append(
                SpeakerTurn(
                    start=float(segment.start),
                    end=float(segment.end),
                    speaker=str(speaker),
                )
            )
        return turns

    for item in annotation:
        if len(item) != 2:
            raise RuntimeError("Unsupported pyannote diarization item shape")
        segment, speaker = item
        turns.append(
            SpeakerTurn(
                start=float(segment.start),
                end=float(segment.end),
                speaker=str(speaker),
            )
        )
    return turns


class PyannoteDiarizationProvider(DiarizationProvider):
    """Local pyannote.audio Community-1 diarization adapter."""

    def __init__(self, settings: Settings) -> None:
        try:
            from pyannote.audio import Pipeline
        except ImportError as exc:
            raise RuntimeError(
                "pyannote.audio is not installed. Run: pip install -e '.[diarization]'"
            ) from exc

        token = (
            settings.diarization_hf_token.get_secret_value()
            if settings.diarization_hf_token is not None
            else None
        )

        self._settings = settings
        self._pipeline = Pipeline.from_pretrained(
            settings.diarization_model,
            token=token,
        )

        if settings.diarization_device != "auto":
            try:
                import torch
            except ImportError as exc:
                raise RuntimeError(
                    "PyTorch is required to select a diarization device explicitly."
                ) from exc
            self._pipeline.to(torch.device(settings.diarization_device))

    @property
    def provider_name(self) -> str:
        return "pyannote"

    @property
    def model_name(self) -> str:
        return self._settings.diarization_model

    def diarize(self, audio_path: Path) -> DiarizationResult:
        output = self._pipeline(str(audio_path))

        annotation = None
        if self._settings.diarization_use_exclusive:
            annotation = getattr(output, "exclusive_speaker_diarization", None)
        if annotation is None:
            annotation = getattr(output, "speaker_diarization", None)
        if annotation is None:
            raise RuntimeError("pyannote output did not expose diarization turns")

        return DiarizationResult(
            turns=_annotation_to_turns(annotation),
            provider=self.provider_name,
            model=self.model_name,
        )
