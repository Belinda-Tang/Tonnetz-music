from tonnetz import NOTE_NAMES

# Semitone intervals above the root for each triad quality
TRIAD_TYPES = {
    "major": {0, 4, 7},
    "minor": {0, 3, 7},
}


def identify_triad(pitch_classes):
    """Identify a major or minor triad.

    Returns (root, quality) such as (9, "minor"), or None if no match.
    """
    pcs = set(pitch_classes)
    if len(pcs) != 3:
        return None

    # Try every note as the root
    for root in pcs:
        intervals = {(pc - root) % 12 for pc in pcs}
        for quality, pattern in TRIAD_TYPES.items():
            if intervals == pattern:
                return root, quality
    return None


def chord_name(root: int, quality: str) -> str:
    """Format a chord label, e.g. (9, "minor") -> 'Am'."""
    suffix = "m" if quality == "minor" else ""
    return NOTE_NAMES[root] + suffix


if __name__ == "__main__":
    # Sanity checks, including inversions and non-triads
    assert identify_triad({0, 4, 7}) == (0, "major")    # C
    assert identify_triad({0, 3, 7}) == (0, "minor")    # Cm
    assert identify_triad({0, 4, 9}) == (9, "minor")    # Am (root is not the smallest number)
    assert identify_triad({2, 5, 9}) == (2, "minor")    # Dm
    assert identify_triad({2, 7, 11}) == (7, "major")   # G
    assert identify_triad({0, 4}) is None               # Only two notes
    assert identify_triad({0, 1, 2}) is None            # Not a triad
    print("All tests passed!")
    print(chord_name(9, "minor"))  # Am