from banglamedscribe.diarization import SpeakerTurn, assign_speakers_by_overlap
from banglamedscribe.schemas import SpeakerRole, TranscriptSegment


def test_alignment_uses_maximum_overlap() -> None:
    segments = [
        TranscriptSegment(id="s1", start=0.0, end=2.0, text="hello"),
        TranscriptSegment(id="s2", start=2.0, end=4.0, text="world"),
    ]
    turns = [
        SpeakerTurn(start=0.0, end=2.4, speaker="SPEAKER_00"),
        SpeakerTurn(start=2.4, end=4.0, speaker="SPEAKER_01"),
    ]

    aligned = assign_speakers_by_overlap(
        segments,
        turns,
        role_map={
            "SPEAKER_00": SpeakerRole.DOCTOR,
            "SPEAKER_01": SpeakerRole.PATIENT,
        },
    )

    assert aligned[0].speaker is SpeakerRole.DOCTOR
    assert aligned[1].speaker is SpeakerRole.PATIENT


def test_nonoverlapping_segment_stays_unknown() -> None:
    segment = TranscriptSegment(id="s1", start=5.0, end=6.0, text="hello")
    aligned = assign_speakers_by_overlap(
        [segment],
        [SpeakerTurn(start=0.0, end=1.0, speaker="SPEAKER_00")],
    )
    assert aligned[0].speaker is SpeakerRole.UNKNOWN
