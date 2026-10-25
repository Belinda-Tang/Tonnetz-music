"""Graph-theoretic measures for major/minor triads in 12-tone equal temperament.

This module is deliberately independent of MIDI segmentation and visualization.
It operates on (pitch_class, quality) tuples, e.g. (0, 'major') for C major.
Only the 24 major/minor triads are nodes in the PLR graph. Distances here are
structural descriptions, NOT direct measurements of tension or emotion.
"""

from __future__ import annotations

from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, permutations
from math import sqrt

Chord = tuple[int, str]
QUALITIES = ("major", "minor")
OPERATIONS = ("P", "L", "R")
CHORDS: tuple[Chord, ...] = tuple(
    (root, quality) for root in range(12) for quality in QUALITIES
)


def _validate_chord(chord: Chord) -> Chord:
    """Require a canonical pitch-class root and supported triad quality."""
    if (
        not isinstance(chord, tuple)
        or len(chord) != 2
        or type(chord[0]) is not int
        or not 0 <= chord[0] < 12
        or chord[1] not in QUALITIES
    ):
        raise ValueError(
            "Expected (root, quality), with root in 0..11 and "
            "quality 'major' or 'minor'"
        )
    return chord


def plr_transform(chord: Chord, operation: str) -> Chord:
    """Apply a standard Neo-Riemannian P, L or R involution.

    Major root r: P -> minor r; L -> minor r+4; R -> minor r+9.
    Minor root r: P -> major r; L -> major r+8; R -> major r+3.
    All root arithmetic is modulo 12.
    """
    root, quality = _validate_chord(chord)
    if operation not in OPERATIONS:
        raise ValueError(f"Operation must be one of {OPERATIONS}")
    if operation == "P":
        return root, "minor" if quality == "major" else "major"
    if operation == "L":
        return ((root + (4 if quality == "major" else 8)) % 12,
                "minor" if quality == "major" else "major")
    return ((root + (9 if quality == "major" else 3)) % 12,
            "minor" if quality == "major" else "major")


def build_plr_graph() -> dict[Chord, dict[str, Chord]]:
    """Return the 24-node, undirected, labeled PLR adjacency graph."""
    return {
        chord: {op: plr_transform(chord, op) for op in OPERATIONS}
        for chord in CHORDS
    }


PLR_GRAPH = build_plr_graph()


def shortest_plr_path(source: Chord, target: Chord) -> tuple[Chord, ...]:
    """Shortest unweighted path (including endpoints), found using BFS.

    Ties are broken deterministically in P, L, R neighbor order.
    """
    # Validate BEFORE caching: True and 1 compare equal in Python cache keys.
    return _shortest_plr_path_cached(_validate_chord(source), _validate_chord(target))


@lru_cache(maxsize=None)
def _shortest_plr_path_cached(source: Chord, target: Chord) -> tuple[Chord, ...]:
    if source == target:
        return (source,)
    queue = deque([source])
    parent: dict[Chord, Chord | None] = {source: None}
    while queue:
        node = queue.popleft()
        for neighbor in PLR_GRAPH[node].values():
            if neighbor in parent:
                continue
            parent[neighbor] = node
            if neighbor == target:
                path: list[Chord] = [target]
                current = target
                while parent[current] is not None:
                    current = parent[current]  # type: ignore[assignment]
                    path.append(current)
                return tuple(reversed(path))
            queue.append(neighbor)
    raise RuntimeError("PLR graph is unexpectedly disconnected")


def plr_distance(source: Chord, target: Chord) -> int:
    """Unweighted shortest-path length in the PLR graph (number of edges)."""
    return len(shortest_plr_path(source, target)) - 1


def chord_pitch_classes(chord: Chord) -> tuple[int, int, int]:
    """Pitch-class SET of a major/minor triad (not an octave-specific voicing)."""
    root, quality = _validate_chord(chord)
    third = 4 if quality == "major" else 3
    return tuple(sorted((root, (root + third) % 12, (root + 7) % 12)))


def _pc_distance(a: int, b: int) -> int:
    delta = abs(a - b)
    return min(delta, 12 - delta)


def voice_leading_distance(source: Chord, target: Chord) -> int:
    """Minimum sum of circular pitch-class semitone distances over 3! matchings.

    This octave-independent distance does NOT model physical finger movement,
    register, voice identities, or the specific voicing of a MIDI performance.
    """
    a = chord_pitch_classes(source)
    b = chord_pitch_classes(target)
    return min(sum(_pc_distance(x, y) for x, y in zip(a, perm))
               for perm in permutations(b))


def is_hexatonic_pole(source: Chord, target: Chord) -> bool:
    """True for complementary hexatonic poles, e.g. C major <-> Ab minor."""
    root_a, quality_a = _validate_chord(source)
    root_b, quality_b = _validate_chord(target)
    if quality_a == quality_b:
        return False
    if quality_a == "major":
        return root_b == (root_a + 8) % 12
    return root_b == (root_a + 4) % 12


@lru_cache(maxsize=1)
def theoretical_pairs() -> tuple[tuple[Chord, Chord], ...]:
    """All 276 DISTINCT, unordered pairs of the 24 triads (excludes self)."""
    return tuple(combinations(CHORDS, 2))


@lru_cache(maxsize=1)
def expected_plr_by_voice_distance() -> dict[int, float]:
    """Conditional mean PLR distance, grouped by voice-leading distance.

    The reference distribution is UNIFORM over all 276 unordered distinct
    triad pairs, NOT over observed transitions in a musical corpus. Excluding
    identical pairs is intentional. No emotion labels enter this baseline.
    """
    total: Counter[int] = Counter()
    count: Counter[int] = Counter()
    for a, b in theoretical_pairs():
        v = voice_leading_distance(a, b)
        total[v] += plr_distance(a, b)
        count[v] += 1
    return {v: total[v] / count[v] for v in sorted(count)}


def graph_voice_discordance(source: Chord, target: Chord) -> float:
    """PLR distance residual after conditioning on pitch-class VL distance.

    Zero denotes an ordinary graph distance within this theoretical matching
    class; positive is graph-far relative to equal VL distance. This is not an
    experimentally validated measure of affect, tension or surprise. Identical
    chord pairs return 0 by convention and are not in the reference baseline.
    """
    source = _validate_chord(source)
    target = _validate_chord(target)
    if source == target:
        return 0.0
    v = voice_leading_distance(source, target)
    return plr_distance(source, target) - expected_plr_by_voice_distance()[v]


def pearson_correlation(xs: list[int], ys: list[int]) -> float:
    """Pearson r without third-party scientific packages."""
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("Expected at least two paired observations")
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    xx = sum((x - mean_x) ** 2 for x in xs)
    yy = sum((y - mean_y) ** 2 for y in ys)
    if xx == 0 or yy == 0:
        raise ValueError("Correlation undefined for a constant variable")
    return numerator / sqrt(xx * yy)


def distance_analysis() -> dict[str, object]:
    """Small exhaustive theoretical audit; does not involve dataset inference."""
    pairs = theoretical_pairs()
    gs = [plr_distance(a, b) for a, b in pairs]
    vs = [voice_leading_distance(a, b) for a, b in pairs]
    records = [
        {
            "source": a,
            "target": b,
            "plr_distance": g,
            "voice_leading_distance": v,
            "hexatonic_pole": is_hexatonic_pole(a, b),
            "discordance": graph_voice_discordance(a, b),
        }
        for (a, b), g, v in zip(pairs, gs, vs)
    ]
    return {
        "node_count": len(PLR_GRAPH),
        "edge_count": sum(len(edges) for edges in PLR_GRAPH.values()) // 2,
        "diameter": max(gs),
        "pair_count": len(pairs),
        "pearson_r": pearson_correlation(gs, vs),
        "plr_histogram": dict(sorted(Counter(gs).items())),
        "voice_leading_histogram": dict(sorted(Counter(vs).items())),
        "mean_plr_by_voice": expected_plr_by_voice_distance().copy(),
        "records": records,
    }
