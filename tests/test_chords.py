from research.chords import chord_name, identify_triad
from research.tonnetz import pitch_class_at


def test_grid_intervals():
    assert pitch_class_at(0, 0) == 0    # Origin is C
    assert pitch_class_at(1, 0) == 7    # Right: perfect fifth
    assert pitch_class_at(0, 1) == 4    # Up-right: major third


def test_triads_and_inversions():
    assert identify_triad({0, 4, 7}) == (0, "major")    # C
    assert identify_triad({0, 3, 7}) == (0, "minor")    # Cm
    assert identify_triad({0, 4, 9}) == (9, "minor")    # Am
    assert identify_triad({11, 2, 5}) == (11, "diminished")


def test_augmented_prefers_bass():
    assert identify_triad({0, 4, 8}, bass=4) == (4, "augmented")


def test_non_triads():
    assert identify_triad({0, 4}) is None
    assert identify_triad({0, 1, 2}) is None


def test_chord_name():
    assert chord_name(9, "minor") == "Am"