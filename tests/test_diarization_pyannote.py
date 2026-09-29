from dataclasses import dataclass

from banglamedscribe.diarization_pyannote import _annotation_to_turns


@dataclass
class FakeSegment:
    start: float
    end: float


class FakeAnnotation:
    def itertracks(self, *, yield_label: bool):
        assert yield_label is True
        yield FakeSegment(0.0, 1.25), "track-0", "SPEAKER_00"
        yield FakeSegment(1.25, 2.5), "track-1", "SPEAKER_01"


def test_annotation_to_turns_supports_itertracks() -> None:
    turns = _annotation_to_turns(FakeAnnotation())

    assert len(turns) == 2
    assert turns[0].speaker == "SPEAKER_00"
    assert turns[0].start == 0.0
    assert turns[1].end == 2.5
