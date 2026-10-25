"""Research safeguards for partial coverage, segment boundaries and repeats."""

import math

import pytest

from research.graphs import graph_voice_discordance, voice_leading_distance
from research.sequence_features import extract_progression_features

C = (0, "major")
AM = (9, "minor")
ABM = (8, "minor")
FM = (5, "minor")


def test_unknown_events_break_transitions_without_teleporting():
    result = extract_progression_features([C, C, AM, None, FM, FM, C])
    assert result["n_events"] == 7
    assert result["n_recognized_events"] == 6
    assert result["n_distinct_recognized_chords"] == 3
    assert result["recognized_event_fraction"] == pytest.approx(6 / 7)
    assert result["n_adjacent_pairs"] == 6
    assert result["n_valid_adjacent_pairs"] == 4
    assert result["valid_adjacent_fraction"] == pytest.approx(4 / 6)
    assert result["n_repeated_adjacent_pairs"] == 2
    assert result["n_changed_transitions"] == 2  # C->Am, Fm->C only
    assert result["n_hexatonic_poles"] == 0
    assert result["mean_plr_distance"] == pytest.approx(2)
    assert result["mean_voice_leading_distance"] == pytest.approx(2)
    assert result["mean_discordance"] == pytest.approx(
        (graph_voice_discordance(C, AM) + graph_voice_discordance(FM, C)) / 2
    )


def test_missing_chord_does_not_invent_pole_transition():
    result = extract_progression_features([C, None, ABM])
    assert result["n_changed_transitions"] == 0
    assert result["n_hexatonic_poles"] == 0
    assert result["mean_plr_distance"] is None
    assert result["hexatonic_pole_fraction"] is None
    assert result["valid_adjacent_fraction"] == 0


def test_actual_hexatonic_poles_and_symmetric_direction():
    forward = extract_progression_features([C, ABM])
    reverse = extract_progression_features([ABM, C])
    assert forward["n_hexatonic_poles"] == 1
    assert forward["hexatonic_pole_fraction"] == 1
    assert forward["mean_plr_distance"] == 3
    assert forward["mean_voice_leading_distance"] == 3
    assert forward["mean_discordance"] == reverse["mean_discordance"]


def test_no_observed_change_is_not_zero_effect():
    for sequence in ([], [None], [C], [C, C, C], [None, None]):
        result = extract_progression_features(sequence)
        assert result["n_changed_transitions"] == 0
        assert result["mean_plr_distance"] is None
        assert result["mean_discordance"] is None
        assert result["positive_discordance_fraction"] is None
    assert extract_progression_features([])["recognized_event_fraction"] is None
    assert extract_progression_features([C, C])["valid_adjacent_fraction"] == 1


def test_repeated_chords_do_not_dilute_change_distance():
    direct = extract_progression_features([C, AM])
    repeated = extract_progression_features([C, C, C, AM, AM])
    for key in (
        "mean_plr_distance", "mean_voice_leading_distance",
        "mean_discordance", "hexatonic_pole_fraction",
    ):
        assert repeated[key] == direct[key]
    assert repeated["n_repeated_adjacent_pairs"] == 3


def test_accepts_single_pass_generator_and_is_transposition_invariant():
    events = [C, AM, None, FM, C]
    original = extract_progression_features(iter(events))
    for semitones in range(12):
        shifted = [((c[0] + semitones) % 12, c[1]) if c else None for c in events]
        translated = extract_progression_features(shifted)
        for key, value in original.items():
            if isinstance(value, float):
                assert translated[key] == pytest.approx(value)
            else:
                assert translated[key] == value


@pytest.mark.parametrize("bad", [(-1, "major"), (0, "diminished"),
                                 (0, "augmented"), (True, "major"),
                                 (0, "Major"), "C", (0, 1)])
def test_unsupported_input_is_rejected_not_silently_skipped(bad):
    with pytest.raises(ValueError, match="Invalid chord at index 1"):
        extract_progression_features([C, bad, AM])
