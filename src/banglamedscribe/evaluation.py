from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Iterable

_PUNCTUATION_RE = re.compile(r"[^\w\s\u0980-\u09FF]", flags=re.UNICODE)


@dataclass(frozen=True, slots=True)
class ErrorRate:
    errors: int
    reference_units: int

    @property
    def rate(self) -> float:
        if self.reference_units == 0:
            return 0.0 if self.errors == 0 else 1.0
        return self.errors / self.reference_units


@dataclass(frozen=True, slots=True)
class ASRMetrics:
    wer: ErrorRate
    cer: ErrorRate


def normalize_text(text: str, *, strip_punctuation: bool = True) -> str:
    """Conservative Unicode/whitespace normalization for Bangla/Banglish ASR scoring."""
    normalized = unicodedata.normalize("NFKC", text).strip()
    normalized = re.sub(r"\s+", " ", normalized)
    if strip_punctuation:
        normalized = _PUNCTUATION_RE.sub(" ", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _edit_distance(reference: list[str], hypothesis: list[str]) -> int:
    previous = list(range(len(hypothesis) + 1))
    for i, ref_unit in enumerate(reference, start=1):
        current = [i]
        for j, hyp_unit in enumerate(hypothesis, start=1):
            substitution = previous[j - 1] + (ref_unit != hyp_unit)
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1
            current.append(min(substitution, insertion, deletion))
        previous = current
    return previous[-1]


def _score(reference: list[str], hypothesis: list[str]) -> ErrorRate:
    return ErrorRate(
        errors=_edit_distance(reference, hypothesis),
        reference_units=len(reference),
    )


def score_transcript(reference: str, hypothesis: str) -> ASRMetrics:
    ref = normalize_text(reference)
    hyp = normalize_text(hypothesis)

    ref_words = ref.split() if ref else []
    hyp_words = hyp.split() if hyp else []

    ref_chars = list(ref.replace(" ", ""))
    hyp_chars = list(hyp.replace(" ", ""))

    return ASRMetrics(
        wer=_score(ref_words, hyp_words),
        cer=_score(ref_chars, hyp_chars),
    )


def aggregate_transcripts(pairs: Iterable[tuple[str, str]]) -> ASRMetrics:
    wer_errors = wer_units = 0
    cer_errors = cer_units = 0

    for reference, hypothesis in pairs:
        metrics = score_transcript(reference, hypothesis)
        wer_errors += metrics.wer.errors
        wer_units += metrics.wer.reference_units
        cer_errors += metrics.cer.errors
        cer_units += metrics.cer.reference_units

    return ASRMetrics(
        wer=ErrorRate(wer_errors, wer_units),
        cer=ErrorRate(cer_errors, cer_units),
    )
