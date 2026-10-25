# Graph-theoretic model audit

## Scope and definitions

`research.graphs` models **24 major/minor triads** in 12-tone equal temperament as `(root, quality)` pairs, where `root` is a pitch class from 0 to 11.

- **PLR graph**: one vertex per major/minor triad, with undirected unit-weight edges labeled P, L or R. Distances are **minimum transformation counts** computed with BFS, not Euclidean screen distance. Every vertex has degree 3; the graph has 36 undirected edges and diameter 5.
- **Pitch-class voice-leading distance**: minimum total circular semitone movement over all 3! bijections between chord pitch-class sets. Octaves, registral motion, performers' finger movements, sustained notes and voice identities are **not** represented.
- **Hexatonic poles**: a major triad rooted at `r` and a minor triad rooted at `(r + 8) % 12`, or the converse. There are 12 unique unordered pole pairs.
- **Graph–voice-leading discordance (exploratory)**: `PLR(a,b) - E[PLR | VL(a,b)]`, where the expectation is calculated over all **276 distinct unordered theoretical chord pairs** with the same voice-leading distance. Identical chord pairs receive discordance 0 by convention. The baseline is a uniform theoretical reference, NOT an estimate of actual musical transitions, and no emotion labels are used.

The term *discordance* is a candidate operational definition, **not a validated measure of surprise, tension, emotion or uncanny affect**. Correlation in the theoretical 276 pairs is descriptive and is NOT a hypothesis test on independent observations or evidence about emotion. The 276 unordered pairs avoid duplicate counts of symmetric chord transitions. Both PLR and pitch-class VL distance are transposition-invariant.

## Commands

From the repository root, with the package installed (`pip install -e .`) and pytest installed:

```bash
python -m pytest -q
python -m research.graph_analysis --csv output/triad_distances.csv --plot output/graph_vs_voice.png --top 10
```

The CLI prints node/edge counts, diameter, Pearson correlation between distances and largest positive/negative discordance examples. The optional CSV contains all 276 theoretical chord pairs; `--plot` saves a bubble plot labeled with pair counts. No MIDI input or large datasets are needed for this **Phase 1** module. Do not commit downloaded datasets or generated outputs.

## Research dependencies and limitations

1. Chord extraction and segmentation from EMOPIA are a separate task. These graph functions should receive a validated sequence of recognized major/minor triads, plus explicit handling of unknown/uncovered chords. Do not silently skip unmatched chords when computing progression statistics.
2. Do **not** interpret a higher PLR graph distance as greater emotion/tension; test such hypotheses against external labels and sound controls.
3. An EMOPIA experiment must fit features and models using **song-disjoint** train/validation/test splits; avoid leakage. The theoretical discordance baseline defined here is corpus-independent and may be used before data splitting.
4. Verify chord extraction quality, graph coverage, and class/track distributions before running any emotion prediction.
5. A future progression-feature module can aggregate PLR distances, pitch-class VL distances, pole rates, positive/negative discordance, and missing-chord coverage on time-aligned chord events. This module does not implement dataset features or emotion models.

## Mathematical sanity checks

Examples using C major `(0, 'major')`:

| Transition | PLR distance | Pitch-class VL semitones |
| --- | ---: | ---: |
| C -> Cm | 1 | 1 |
| C -> Am | 1 | 2 |
| C -> Fm | 3 | 2 |
| C -> Abm | 3 | 3 |
| C -> B | 4 | 3 |

For C -> Abm, all three matched pitch classes can move by a semitone while the transformation path needs three PLR operations. Comparing the raw numbers `3 steps` and `3 semitones` is not a meaningful signed difference; the conditional discordance definition addresses the scale issue.
