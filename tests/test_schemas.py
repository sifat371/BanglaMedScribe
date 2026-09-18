import pytest
from pydantic import ValidationError

from banglamedscribe.schemas import SpeakerRole, TranscriptSegment, WordTimestamp


def test_transcript_segment_accepts_bangla_text() -> None:
    segment = TranscriptSegment(
        id="seg_0001",
        start=1.0,
        end=2.5,
        speaker=SpeakerRole.PATIENT,
        text="তিন দিন ধরে জ্বর",
    )

    assert segment.text == "তিন দিন ধরে জ্বর"
    assert segment.speaker is SpeakerRole.PATIENT


def test_segment_rejects_reversed_timestamps() -> None:
    with pytest.raises(ValidationError):
        TranscriptSegment(
            id="seg_bad",
            start=5.0,
            end=2.0,
            text="invalid",
        )


def test_word_probability_is_bounded() -> None:
    with pytest.raises(ValidationError):
        WordTimestamp(start=0, end=1, text="জ্বর", probability=1.2)
