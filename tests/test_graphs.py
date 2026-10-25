"""Reference properties of PLR and voice-leading models, independent of MIDI."""

import csv
import math

import pytest

from src.research.graph_analysis import write_csv, write_distance_plot
from src.research.graphs import (
    CHORDS, OPERATIONS, PLR_GRAPH, build_plr_graph,
    chord_pitch_classes, distance_analysis, expected_plr_by_voice_distance,
    graph_voice_discordance, is_hexatonic_pole, plr_distance,
    plr_transform, shortest_plr_path, theoretical_pairs,
    voice_leading_distance,
)

C = (0, "major")
CM = (0, "minor")
AM = (9, "minor")
ABM = (8, "minor")
FM = (5, "minor")


def test_graph_24_nodes_36_edges_and_undirected_reciprocity():
    assert len(CHORDS) == len(PLR_GRAPH) == 24
    assert sum(map(len, PLR_GRAPH.values())) // 2 == 36
    assert build_plr_graph() == PLR_GRAPH
    for chord, neighbors in PLR_GRAPH.items():
        assert set(neighbors) == set(OPERATIONS)
        assert len(set(neighbors.values())) == 3
        for operation, destination in neighbors.items():
            assert destination in PLR_GRAPH
            assert PLR_GRAPH[destination][operation] == chord
            assert plr_transform(destination, operation) == chord


def test_correct_plr_transforms():
    assert plr_transform(C, "P") == CM
    assert plr_transform(C, "R") == AM
    assert plr_transform(C, "L") == (4, "minor")
    assert plr_transform(AM, "R") == C


def test_graph_bfs_and_diameter():
    assert plr_distance(C, C) == 0
    assert plr_distance(C, CM) == 1
    assert plr_distance(C, AM) == 1
    assert plr_distance(C, ABM) == 3
    assert plr_distance(C, FM) == 3
    assert plr_distance(C, (11, "major")) == 4
    assert plr_distance(C, (10, "minor")) == 5
    for a in CHORDS:
        for b in CHORDS:
            path = shortest_plr_path(a, b)
            assert path[0] == a and path[-1] == b
            assert len(path) - 1 == plr_distance(a, b)
            assert plr_distance(a, b) == plr_distance(b, a)
            for start, end in zip(path, path[1:]):
                assert end in PLR_GRAPH[start].values()
    assert distance_analysis()["diameter"] == 5


def test_pitch_class_sets_and_pitch_class_voice_leading():
    assert chord_pitch_classes(C) == (0, 4, 7)
    assert chord_pitch_classes(AM) == (0, 4, 9)
    assert voice_leading_distance(C, C) == 0
    assert voice_leading_distance(C, CM) == 1
    assert voice_leading_distance(C, AM) == 2
    assert voice_leading_distance(C, FM) == 2
    assert voice_leading_distance(C, ABM) == 3
    assert voice_leading_distance(C, (11, "major")) == 3
    assert voice_leading_distance(C, (2, "minor")) == 5
    for a in CHORDS:
        for b in CHORDS:
            assert voice_leading_distance(a, b) == voice_leading_distance(b, a)


def test_hexatonic_poles_symmetry_and_count():
    assert is_hexatonic_pole(C, ABM)
    assert is_hexatonic_pole(ABM, C)
    assert not is_hexatonic_pole(C, AM)
    assert not is_hexatonic_pole(C, C)
    assert sum(is_hexatonic_pole(a, b) for a, b in theoretical_pairs()) == 12


def test_theoretical_discordance_groups_have_zero_mean():
    pairs = theoretical_pairs()
    assert len(pairs) == 276
    assert len(set(pairs)) == 276
    expected = expected_plr_by_voice_distance()
    assert all(0 <= mean <= 5 for mean in expected.values())
    for v in expected:
        residuals = [graph_voice_discordance(a, b) for a, b in pairs
                     if voice_leading_distance(a, b) == v]
        assert math.isclose(sum(residuals), 0.0, abs_tol=1e-11)
    assert graph_voice_discordance(C, C) == 0
    assert graph_voice_discordance(C, FM) == graph_voice_discordance(FM, C)


def test_analysis_integrity_and_correlation():
    report = distance_analysis()
    assert report["node_count"] == 24
    assert report["edge_count"] == 36
    assert report["pair_count"] == 276
    assert sum(report["plr_histogram"].values()) == 276
    assert sum(report["voice_leading_histogram"].values()) == 276
    assert -1 <= report["pearson_r"] <= 1
    assert len(report["records"]) == 276


def test_analysis_csv_export(tmp_path):
    output = tmp_path / "results" / "pairs.csv"
    write_csv(output, distance_analysis()["records"])
    with output.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 276
    assert set(rows[0]) == {
        "source", "target", "plr_distance", "voice_leading_distance",
        "hexatonic_pole", "discordance",
    }


def test_analysis_plot_export(tmp_path):
    output = tmp_path / "results" / "distance_plot.png"
    write_distance_plot(output, distance_analysis()["records"])
    assert output.is_file() and output.stat().st_size > 1_000


@pytest.mark.parametrize("bad", [(-1, "major"), (12, "minor"), (0, "augmented"),
                                      (0, "diminished"), (0, "Major"), (True, "major")])
def test_invalid_chords_raise_clear_error(bad):
    with pytest.raises(ValueError):
        plr_distance(C, bad)
    with pytest.raises(ValueError):
        voice_leading_distance(bad, C)
    with pytest.raises(ValueError):
        is_hexatonic_pole(bad, C)


def test_unknown_transform_rejected():
    with pytest.raises(ValueError):
        plr_transform(C, "X")
