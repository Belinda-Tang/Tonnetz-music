# Graph-Theoretic Model of Triad Space

This project compares two ways of measuring distance between major and minor triads in 12-tone equal temperament: shortest-path distance on the PLR graph and pitch-class voice-leading (VL) distance.

The analysis covers all 276 unordered pairs of distinct triads. It also defines graph–voice-leading discordance (GVLD), a conditional residual that describes how a pair's PLR distance differs from the average among pairs with the same VL distance.

## Installation

```bash
python -m pip install -e .
python -m pip install pytest
```

## Usage

Run the tests and analysis from the project root:

```bash
python -m pytest -q
python -m research.graph_analysis --csv output/triad_distances.csv --plot output/graph_vs_voice.png --top 10
```

The analysis generates a CSV distance table, a scatter plot, conditional counts, graph statistics, the Pearson correlation, and the largest conditional residuals. The `--top` argument controls how many residuals are reported.

## Mathematical Model

Triads are represented as `(root, quality)` tuples in `research.graphs`.

### PLR Graph Distance

The graph contains 24 vertices, representing the 12 major and 12 minor triads. Two vertices are connected by an undirected, unit-weight edge if they are related by a P (Parallel), L (Leading-tone exchange), or R (Relative) transformation.

The graph is 3-regular, with 36 edges and diameter 5.

`plr_distance(a, b)` returns the minimum number of P/L/R transformations needed to connect two triads.

### Voice-Leading Distance

VL distance is the minimum total circular semitone displacement between two triads. The implementation considers all 3! possible matchings between their pitch classes and selects the one with the smallest total displacement.

The calculation ignores octave placement, register, voice identity, and note multiplicity. It is a pitch-class simplification of voice leading rather than an implementation of Tymoczko's generalized chord geometry.

### Hexatonic Poles

A major triad with root `r` and a minor triad with root `(r + 8) mod 12` form a hexatonic-pole pair.

The model identifies these 12 unordered pairs. It does not classify the broader chromatic PL/LP relations discussed by Forrest (2017).

### Graph–Voice-Leading Discordance (GVLD)

GVLD measures the deviation of a pair's PLR distance from the conditional mean at its VL distance:

```text
D(a, b) = PLR(a, b) - E[PLR | VL = VL(a, b)]
```

The expectation is calculated over the uniform distribution on all 276 unordered pairs of distinct triads.

- **Positive GVLD:** The pair's PLR distance is above the conditional mean.
- **Negative GVLD:** The pair's PLR distance is below the conditional mean.
- **Zero GVLD:** The pair's PLR distance equals the conditional mean.

For identical triads, `D(a, a) = 0` by convention.

PLR distance, VL distance, and GVLD are symmetric and invariant under transposition.

## Results

The table shows the number of unordered triad pairs for each combination of VL and PLR distance.

| VL distance (semitones) | PLR distance: number of pairs |
| ---: | --- |
| 1 | 1: 24 |
| 2 | 1: 12; 2: 24; 3: 24 |
| 3 | 2: 48; 3: 12; 4: 24 |
| 4 | 3: 36 |
| 5 | 3: 24; 5: 12 |
| 6 | 4: 36 |

The Pearson correlation between PLR and VL distance across all 276 pairs is **0.73806177**.

Although the distances are positively correlated, equal VL distances do not always imply equal PLR distances. For example, a VL distance of 2 semitones can correspond to 1, 2, or 3 PLR steps.

For VL distances of 1, 4, and 6, the PLR distance is constant, so GVLD is zero for every pair in those classes.

These are descriptive results from a complete enumeration of the finite triad space, not estimates from a sample of musical transitions.

## Sequence Features

The `research.sequence_features` module computes distance-based features and coverage statistics for ordered sequences of pre-labelled major/minor chords.

Unknown chords are represented by `None` and interrupt the transition sequence.

The module currently expects chord labels as input. MIDI chord extraction, duration modelling, and EMOPIA dataset processing are not implemented.

## Limitations

- **Previous work.** PLR transformations, Tonnetz relations, parsimonious voice leading, and generalized chord geometries are established in music theory. This project implements and compares existing distance measures rather than proposing a new theory of harmonic space. See [LITERATURE_REVIEW.md](LITERATURE_REVIEW.md) for further discussion.

- **GVLD.** GVLD is derived from PLR and VL distances and contains no additional information beyond them. Any predictive benefit would need to be evaluated against models using both original distances, including their interaction. A zero residual indicates agreement with the conditional mean, not that a transition is common or expected in actual music.

- **Chord quality.** Every P/L/R transformation changes chord quality. Consequently, PLR distances are odd between triads of different qualities and even between triads of the same quality. Downstream analyses must account for this dependence.

- **Musical context.** The model does not account for key, harmonic function, phrase position, harmonic direction, or performed voicing. Neither GVLD nor hexatonic-pole membership has been validated as a measure of tension, surprise, or uncanniness.

## Future Work

- Evaluate chord-extraction accuracy and PLR coverage on sampled clips, including unsupported chords and sensitivity to segmentation.
- Compare PLR, VL, and GVLD-based features using song-disjoint training, validation, and test sets.
- Examine associations with EMOPIA's four categorical emotion quadrants, without treating the labels as continuous measures of musical tension.

## References

- Cohn, R. (1997). Neo-Riemannian operations, parsimonious trichords, and their "Tonnetz" representations. *Journal of Music Theory*, 41(1), 1–66. https://doi.org/10.2307/843761
- Tymoczko, D. (2011). *A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice*. Oxford University Press.
- Forrest, D. (2017). PL voice leading and the uncanny in pop music. *Music Theory Online*, 23(4). https://mtosmt.org/issues/mto.17.23.4/mto.17.23.4.forrest.html
