"""Sequence-level graph features for *recognized* major/minor triads.

``None`` denotes an unknown or unsupported chord and BREAKS a transition. Never
connect chords across a missing event. Consecutive repeats count as observable
adjacencies but are excluded from harmonic *change* statistics so the latter
are not diluted by repeated beat-level segmentation of the same chord.

Inputs contain ordered chord events, not raw MIDI notes or time durations.
All distances are descriptive structural features, not emotional scores.
"""

from __future__ import annotations

from collections.abc import Iterable
from math import fsum

from research.graphs import (
    Chord,
    chord_pitch_classes,
    graph_voice_discordance,
    is_hexatonic_pole,
    plr_distance,
    voice_leading_distance,
)


def _mean(values: list[int | float]) -> float | None:
    return fsum(values) / len(values) if values else None


def extract_progression_features(
    sequence: Iterable[Chord | None],
) -> dict[str, int | float | None]:
    """Summarize adjacent harmonic changes without bridging unrecognized events.

    ``None`` is the ONLY missing-chord sentinel; an unsupported quality (e.g.
    diminished) must be mapped to None upstream, deliberately. Otherwise bad
    inputs raise ValueError rather than quietly corrupting research results.

    The mean distances, pole frequency and discordance statistics use only
    adjacent recognized *changes* (a != b). Missing-chord coverage is reported
    separately. Means/rates with zero observations are None, NOT numeric zero.
    """
    chords = tuple(sequence)
    for index, chord in enumerate(chords):
        if chord is not None:
            try:
                chord_pitch_classes(chord)  # Validate root and major/minor quality.
            except ValueError as exc:
                raise ValueError(
                    f"Invalid chord at index {index}: {chord!r}; "
                    "use None for unknown/unsupported chords"
                ) from exc

    total_adjacent = max(0, len(chords) - 1)
    valid_adjacent = [
        (a, b) for a, b in zip(chords, chords[1:])
        if a is not None and b is not None
    ]
    changed = [(a, b) for a, b in valid_adjacent if a != b]
    graph_distances = [plr_distance(a, b) for a, b in changed]
    voice_distances = [voice_leading_distance(a, b) for a, b in changed]
    discordances = [graph_voice_discordance(a, b) for a, b in changed]
    poles = sum(is_hexatonic_pole(a, b) for a, b in changed)
    n_changed = len(changed)
    n_recognized = sum(chord is not None for chord in chords)

    return {
        "n_events": len(chords),
        "n_recognized_events": n_recognized,
        "n_distinct_recognized_chords": len({c for c in chords if c is not None}),
        "recognized_event_fraction": n_recognized / len(chords) if chords else None,
        "n_adjacent_pairs": total_adjacent,
        "n_valid_adjacent_pairs": len(valid_adjacent),
        "valid_adjacent_fraction": (
            len(valid_adjacent) / total_adjacent if total_adjacent else None
        ),
        "n_changed_transitions": n_changed,
        "n_repeated_adjacent_pairs": len(valid_adjacent) - n_changed,
        "n_hexatonic_poles": poles,
        "mean_plr_distance": _mean(graph_distances),
        "mean_voice_leading_distance": _mean(voice_distances),
        "mean_discordance": _mean(discordances),
        "mean_absolute_discordance": _mean([abs(d) for d in discordances]),
        "positive_discordance_fraction": (
            sum(d > 1e-12 for d in discordances) / n_changed
            if n_changed else None
        ),
        "hexatonic_pole_fraction": poles / n_changed if n_changed else None,
    }
