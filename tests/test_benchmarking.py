from banglamedscribe.benchmarking import (
    TaggedTranscript,
    aggregate_by_tag,
    parse_tags,
)


def test_parse_tags_normalizes_and_deduplicates() -> None:
    assert parse_tags("Bangla; medical-term ;bangla") == (
        "bangla",
        "medical-term",
    )


def test_aggregate_by_tag_reports_micro_metrics() -> None:
    items = [
        TaggedTranscript(
            reference="আমার জ্বর আছে",
            hypothesis="আমার জ্বর আছে",
            tags=("bangla", "clean"),
        ),
        TaggedTranscript(
            reference="আজ জ্বর আছে",
            hypothesis="আজ ব্যথা আছে",
            tags=("bangla", "noisy"),
        ),
    ]

    slices = aggregate_by_tag(items)

    count, metrics = slices["bangla"]
    assert count == 2
    assert metrics.wer.errors == 1
    assert metrics.wer.reference_units == 6

    clean_count, clean_metrics = slices["clean"]
    assert clean_count == 1
    assert clean_metrics.wer.rate == 0.0
