import tempfile
from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool

from banglamedscribe.audio import SUPPORTED_AUDIO_SUFFIXES
from banglamedscribe.config import Settings, get_settings
from banglamedscribe.pipeline import TranscriptionPipeline
from banglamedscribe.schemas import TranscriptDocument

app = FastAPI(
    title="BanglaMedScribe API",
    version="0.1.0",
    description="V1 clinical documentation pipeline API.",
)


@lru_cache(maxsize=1)
def get_pipeline() -> TranscriptionPipeline:
    return TranscriptionPipeline()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "banglamedscribe"}


@app.post("/v1/transcribe", response_model=TranscriptDocument)
async def transcribe(
    audio: UploadFile = File(...),
    pipeline: TranscriptionPipeline = Depends(get_pipeline),
    settings: Settings = Depends(get_settings),
) -> TranscriptDocument:
    filename = audio.filename or "consultation.wav"
    suffix = Path(filename).suffix.lower()

    if suffix not in SUPPORTED_AUDIO_SUFFIXES:
        raise HTTPException(status_code=415, detail="Unsupported audio format")

    max_bytes = settings.max_upload_mb * 1024 * 1024
    total_bytes = 0

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        try:
            while chunk := await audio.read(1024 * 1024):
                total_bytes += len(chunk)
                if total_bytes > max_bytes:
                    raise HTTPException(status_code=413, detail="Audio upload is too large")
                temp_file.write(chunk)
        except Exception:
            temp_path.unlink(missing_ok=True)
            raise

    try:
        return await run_in_threadpool(pipeline.transcribe, temp_path)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        temp_path.unlink(missing_ok=True)
        await audio.close()
