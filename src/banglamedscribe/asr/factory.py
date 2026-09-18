from banglamedscribe.asr.base import ASRProvider
from banglamedscribe.config import Settings


def build_asr_provider(settings: Settings) -> ASRProvider:
    provider = settings.asr_provider.strip().lower()

    if provider == "faster-whisper":
        from banglamedscribe.asr.faster_whisper import FasterWhisperProvider

        return FasterWhisperProvider(settings)

    raise ValueError(
        f"Unsupported ASR provider '{settings.asr_provider}'. "
        "Currently supported: faster-whisper"
    )
