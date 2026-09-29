from banglamedscribe.evaluation import aggregate_transcripts, normalize_text, score_transcript


def test_normalization_preserves_bangla_and_collapses_whitespace() -> None:
    assert normalize_text("  আমার,   জ্বর!  ") == "আমার জ্বর"


def test_exact_match_has_zero_error() -> None:
    metrics = score_transcript("আমার তিন দিন ধরে জ্বর", "আমার তিন দিন ধরে জ্বর")
    assert metrics.wer.rate == 0.0
    assert metrics.cer.rate == 0.0


def test_single_word_substitution_is_counted() -> None:
    metrics = score_transcript("আমার জ্বর আছে", "আমার ব্যথা আছে")
    assert metrics.wer.errors == 1
    assert metrics.wer.reference_units == 3


def test_corpus_metrics_micro_aggregate_counts() -> None:
    metrics = aggregate_transcripts(
        [
            ("আমি ভালো আছি", "আমি ভালো আছি"),
            ("আজ জ্বর আছে", "আজ ব্যথা আছে"),
        ]
    )
    assert metrics.wer.errors == 1
    assert metrics.wer.reference_units == 6
