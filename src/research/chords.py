from research.tonnetz import NOTE_NAMES

# Semitone intervals above the root for each triad quality
TRIAD_TYPES = {
    "major": {0, 4, 7},
    "minor": {0, 3, 7},
    "diminished": {0, 3, 6},
    "augmented": {0, 4, 8},
}

SUFFIXES = {
    "major": "",
    "minor": "m",
    "diminished": "dim",
    "augmented": "aug",
}


def identify_triad(pitch_classes, bass=None):
    """Identify a triad (major, minor, diminished or augmented).

    For symmetric chords (e.g. augmented), several roots match;
    prefer the bass note if given.
    Returns (root, quality), or None if no match.
    """
    pcs = set(pitch_classes)
    if len(pcs) != 3:
        return None

    # Collect every (root, quality) that fits a template
    matches = []
    for root in pcs:
        intervals = {(pc - root) % 12 for pc in pcs}
        for quality, pattern in TRIAD_TYPES.items():
            if intervals == pattern:
                matches.append((root, quality))

    if not matches:
        return None
    for root, quality in matches:
        if root == bass:
            return root, quality
    return min(matches)  # Deterministic fallback


def chord_name(root: int, quality: str) -> str:
    """Format a chord label, e.g. (9, "minor") -> 'Am'."""
    return NOTE_NAMES[root] + SUFFIXES[quality]


