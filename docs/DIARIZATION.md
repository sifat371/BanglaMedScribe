# Diarization boundary

Speaker diarization is a required research milestone, but the repository does **not** yet claim a
validated diarization model.

The current code introduces two stable pieces:

1. DiarizationProvider — a model-agnostic interface for future pyannote/NeMo/local providers.
2. Deterministic overlap-based alignment from diarization turns to ASR transcript segments.

This deliberately separates three different problems:

    audio
      |-- ASR -> timestamped words/segments
      |-- diarization -> anonymous speaker turns
                             |
                             v
                    temporal alignment
                             |
                             v
                  speaker-attributed ASR
                             |
                             v
                 role identification
                 (doctor/patient/etc.)

Diarization labels such as SPEAKER_00 are **not automatically equivalent** to doctor/patient
roles. Role identification must be evaluated separately rather than inferred by speaker index.

## Before making a CV/result claim

A concrete diarization backend should be implemented and evaluated on reviewed multi-speaker audio.
Report at least the benchmark scope and a diarization metric such as DER, together with the
speaker-attribution protocol.
