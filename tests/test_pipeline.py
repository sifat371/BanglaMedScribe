from pathlib import Path

from banglamedscribe.asr.base import ASRProvider, ASRResult
from banglamedscribe.config import Settings
from banglamedscribe.pipeline import TranscriptionPipeline
from banglamedscribe.schemas import SpeakerRole, TranscriptSegment


class FakeASRProvider(ASRProvider):
    @property
    def provider_name(self) -> str:
        return "fake"

    @property
    def model_name(self) -> str:
        return "fake-model"

    @property
    def requested_language(self) -> str | None:
        return "bn"

    def transcribe(self, audio_path: Path) -> ASRResult:
        return ASRResult(
            segments=[
                TranscriptSegment(
                    id="seg_0000",
                    start=0.0,
                    end=1.5,
                    speaker=SpeakerRole.UNKNOWN,
                    text="আমার তিন দিন ধরে জ্বর",
                )
            ],
            detected_language="bn",
            language_probability=0.99,
            duration_seconds=1.5,
        )


def test_pipeline_can_run_with_injected_provider_without_model_download(tmp_path: Path) -> None:
    audio_path = tmp_path / "sample.wav"
    audio_path.write_bytes(b"test-audio-placeholder")

    settings = Settings(asr_provider="fake")
    pipeline = TranscriptionPipeline(settings=settings, provider=FakeASRProvider())

    transcript = pipeline.transcribe(audio_path, preprocess=False)

    assert transcript.asr.provider == "fake"
    assert transcript.audio.duration_seconds == 1.5
    assert transcript.segments[0].text == "আমার তিন দিন ধরে জ্বর"
