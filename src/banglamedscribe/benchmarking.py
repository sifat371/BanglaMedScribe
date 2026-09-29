from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from banglamedscribe.evaluation import ASRMetrics, aggregate_transcripts


@dataclass(frozen=True, slots=True)
class TaggedTranscript:
    reference: str
    hypothesis: str
    tags: tuple[str, ...] = ()


def parse_tags(value: str | None) -> tuple[str, ...]:
    if not value:
        return ()
    return tuple(
        dict.fromkeys(
            tag.strip().lower()
            for tag in value.split(";")
            if tag.strip()
        )
    )


def aggregate_by_tag(
    items: list[TaggedTranscript],
) -> dict[str, tuple[int, ASRMetrics]]:
    grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for item in items:
        for tag in item.tags:
            grouped[tag].append((item.reference, item.hypothesis))

    return {
        tag: (len(pairs), aggregate_transcripts(pairs))
        for tag, pairs in sorted(grouped.items())
    }
