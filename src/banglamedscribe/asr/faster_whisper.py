from pathlib import Path

from banglamedscribe.asr.base import ASRProvider, ASRResult
from banglamedscribe.config import Settings
from banglamedscribe.schemas import SpeakerRole, TranscriptSegment, WordTimestamp


class FasterWhisperProvider(ASRProvider):
    """Adapter around faster-whisper for local transcription."""

    def __init__(self, settings: Settings) -> None:
        try:
            from faster_whisper import WhisperModel
        except ImportError as exc:
            raise RuntimeError(
                "faster-whisper is not installed. Run: pip install -e '.[asr]'"
            ) from exc

        self._settings = settings
        self._model = WhisperModel(
            settings.asr_model,
            device=settings.asr_device,
            compute_type=settings.asr_compute_type,
        )

    @property
    def provider_name(self) -> str:
        return "faster-whisper"

    @property
    def model_name(self) -> str:
        return self._settings.asr_model

    @property
    def requested_language(self) -> str | None:
        return self._settings.asr_language

    def transcribe(self, audio_path: Path) -> ASRResult:
        segments_iter, info = self._model.transcribe(
            str(audio_path),
            language=self._settings.asr_language,
            beam_size=self._settings.asr_beam_size,
            vad_filter=self._settings.asr_vad_filter,
            word_timestamps=self._settings.asr_word_timestamps,
        )

        segments: list[TranscriptSegment] = []

        for index, segment in enumerate(segments_iter):
            text = segment.text.strip()
            if not text:
                continue

            words: list[WordTimestamp] = []
            for word in segment.words or []:
                word_text = word.word.strip()
                if not word_text:
                    continue
                words.append(
                    WordTimestamp(
                        start=float(word.start),
                        end=float(word.end),
                        text=word_text,
                        probability=(
                            float(word.probability)
                            if word.probability is not None
                            else None
                        ),
                    )
                )

            segments.append(
                TranscriptSegment(
                    id=f"seg_{index:04d}",
                    start=float(segment.start),
                    end=float(segment.end),
                    speaker=SpeakerRole.UNKNOWN,
                    text=text,
                    words=words,
                )
            )

        return ASRResult(
            segments=segments,
            detected_language=getattr(info, "language", None),
            language_probability=getattr(info, "language_probability", None),
            duration_seconds=getattr(info, "duration", None),
        )
