import json
import shutil
import tempfile
from pathlib import Path
from uuid import uuid4

from banglamedscribe.asr import ASRProvider, build_asr_provider
from banglamedscribe.audio import prepare_audio, validate_audio_path
from banglamedscribe.config import Settings, get_settings
from banglamedscribe.schemas import ASRMetadata, AudioMetadata, TranscriptDocument


class TranscriptionPipeline:
    def __init__(
        self,
        settings: Settings | None = None,
        provider: ASRProvider | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.provider = provider or build_asr_provider(self.settings)

    def transcribe(
        self,
        audio_path: str | Path,
        *,
        preprocess: bool = True,
    ) -> TranscriptDocument:
        source = Path(audio_path)
        validate_audio_path(source)

        with tempfile.TemporaryDirectory(prefix="banglamedscribe_") as temp_dir_name:
            temp_dir = Path(temp_dir_name)

            if preprocess:
                prepared_path = temp_dir / "audio.wav"
                audio_metadata = prepare_audio(source, prepared_path)
            else:
                prepared_path = source
                audio_metadata = AudioMetadata(original_filename=source.name)

            result = self.provider.transcribe(prepared_path)

            if audio_metadata.duration_seconds is None:
                audio_metadata.duration_seconds = result.duration_seconds

            return TranscriptDocument(
                consultation_id=f"consult_{uuid4().hex[:12]}",
                audio=audio_metadata,
                asr=ASRMetadata(
                    provider=self.provider.provider_name,
                    model=self.provider.model_name,
                    requested_language=self.provider.requested_language,
                    detected_language=result.detected_language,
                    language_probability=result.language_probability,
                ),
                segments=result.segments,
            )

    def run(
        self,
        audio_path: str | Path,
        output_dir: str | Path | None = None,
    ) -> tuple[TranscriptDocument, Path]:
        source = Path(audio_path)
        validate_audio_path(source)

        destination = (
            Path(output_dir)
            if output_dir
            else self.settings.output_dir / source.stem
        )
        destination.mkdir(parents=True, exist_ok=True)

        if self.settings.keep_processed_audio:
            with tempfile.TemporaryDirectory(prefix="banglamedscribe_") as temp_dir_name:
                prepared_path = Path(temp_dir_name) / "audio.wav"
                audio_metadata = prepare_audio(source, prepared_path)
                result = self.provider.transcribe(prepared_path)
                shutil.copy2(prepared_path, destination / "audio.wav")

                transcript = TranscriptDocument(
                    consultation_id=f"consult_{uuid4().hex[:12]}",
                    audio=audio_metadata,
                    asr=ASRMetadata(
                        provider=self.provider.provider_name,
                        model=self.provider.model_name,
                        requested_language=self.provider.requested_language,
                        detected_language=result.detected_language,
                        language_probability=result.language_probability,
                    ),
                    segments=result.segments,
                )
        else:
            transcript = self.transcribe(source)

        transcript_path = destination / "transcript.json"
        transcript_path.write_text(
            json.dumps(
                transcript.model_dump(mode="json"),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        return transcript, transcript_path
