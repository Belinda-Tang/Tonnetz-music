# Tonnetz-music

**See harmony as shapes — and study the mathematics of harmonic transitions.**

Tonnetz-music began as a Python MIDI keyboard visualizer and now contains an exploratory **graph-theoretic research toolkit**. Our working research question is:

> **Do graph-based harmonic features provide additional information for music emotion prediction?**

The planned study will compare discrete Neo-Riemannian transformation features with pitch-class voice leading, six-dimensional tonal-centroid (Tonnetz) features, and conventional symbolic musical features. We will investigate whether any features provide reproducible incremental predictive value for valence and arousal.

**Status (October 2026):** The live visualization, graph models, 276-pair theoretical audit, and sequence-feature summaries have code implementations. **EMOPIA loading, validated MIDI-to-chord extraction, emotion prediction, statistical evaluation, and a completed paper have not been implemented.** No findings about perceived musical emotion are claimed.

## Implemented research models

The PLR graph contains 24 vertices (12 major and 12 minor triads in 12-tone equal temperament), 36 undirected P/L/R edges, and has diameter 5. It uses BFS to compute the shortest number of transformations. In contrast, pitch-class voice-leading distance minimizes the total circular semitone movement under all three-note matchings; it does **not** measure actual fingering, specific octave/register motion, or performed voice identity.

Implemented in `src/research/graphs.py`:

- `plr_transform`, `build_plr_graph`, `shortest_plr_path`, `plr_distance`
- `chord_pitch_classes`, `voice_leading_distance`, `is_hexatonic_pole`
- `graph_voice_discordance`: a candidate **descriptive** residual, not a validated emotion/tension score
- `theoretical_pairs`, `distance_analysis`, `conditional_plr_distributions`

For distinct major/minor triads A and B, the exploratory discordance definition is:

```text
D(A, B) = PLR(A, B) - mean[PLR(X, Y) | VL(X, Y) = VL(A, B)]
```

The reference contains **all 276 unordered, distinct theoretical chord pairs**, counted uniformly. Self-transitions have discordance zero by convention. The theoretical model has variable conditional PLR distance only for voice-leading costs of 2, 3 and 5 semitones; the other groups have a constant PLR distance.

**Research limitation:** Discordance is a deterministic transformation of the two input distances. It cannot contain information absent from their joint values. Later experiments **must** include a baseline with PLR and voice-leading distances together (and suitable interaction controls), not just each distance separately. The graph analysis alone gives **no evidence about emotion, surprise or uncanniness**. See [`paper/GRAPH_MODEL.md`](paper/GRAPH_MODEL.md).

`src/research/sequence_features.py` summarizes existing sequences of identified major/minor triads: graph distances, voice-leading distances, discordance, hexatonic-pole frequency, repetitions and coverage. `None` means an unknown event and **breaks** the transition; unsupported chord qualities must be explicitly mapped upstream. The module does not parse MIDI or include durations.

## Visualization

The separate real-time viewer can recognize major, minor, diminished and augmented triads and highlight pitch classes in a finite 2D Tonnetz lattice with

```text
pitch_class(x, y) = (7*x + 4*y) mod 12
```

The fading on-screen trail is a **greedy screen-space visualization**, **not** PLR graph distance or a validated harmonic tension metric. Diminished and augmented chords are not represented as Tonnetz triangles in the current trail algorithm. Live MIDI operation requires a MIDI keyboard and a compatible local MIDI device setup.

## Installation

Python 3.10 or later is required. A MIDI keyboard is **not needed** for the research audit and unit tests.

```bash
git clone https://github.com/Belinda-Tang/Tonnetz-music.git
cd Tonnetz-music
git switch feature/graph-metrics
python -m venv .venv
# macOS / Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pytest
```

### Unit tests and reproducible theoretical audit

```bash
python -m pytest -q
python -m research.graph_analysis --top 10
python -m research.graph_analysis --csv output/triad_distances.csv --plot output/graph_vs_voice.png
```

The analysis CLI reports the number of nodes/edges, graph diameter, Pearson correlation across the 276 theoretical pairs, conditional distance distributions and transitions with extreme conditional residuals. Generated `output/` files are ignored by Git. **The theoretical correlation is descriptive, not a significance test on independently sampled music.**

### Live MIDI (optional)

```bash
python -m viz.live_view
# or
python -m viz.midi_input
```

## Repository layout

```text
src/
  research/
    chords.py             # Triad recognition
    tonnetz.py            # Tonnetz lattice arithmetic
    graphs.py             # PLR graph, voice leading, discordance
    graph_analysis.py     # Theoretical analysis, CSV/plot export
    sequence_features.py  # Features from existing chord-event sequences
  viz/
    live_view.py          # Real-time MIDI visualization
    midi_input.py         # Terminal MIDI feedback
    tonnetz_view.py       # Geometric display and fading trail
tests/                    # Graph, chord and missing-data tests
paper/
  GRAPH_MODEL.md          # Mathematical definitions and limitations
  DECISIONS.md            # Study decision log
  README.md               # Paper and literature notes
data/README.md            # Dataset instructions (raw data not committed)
pyproject.toml            # Installable src-layout package
requirements.txt          # Earlier pinned visualization environment
```

## Planned research protocol and milestones

| Work | Lead | Status          |
| --- | --- |-----------------|
| Review PLR, voice leading and related emotion work; create literature matrix | R + B | Planned         |
| Audit PLR graph, distances, invariance, conditional distributions and tests | R | Implemented     |
| Split viewer and research into Python packages | B | Implemented     |
| Inspect EMOPIA formats, permissions and license | B | Planned         |
| Validate time-aligned chord extraction and triad coverage | B + R | Not implemented |
| Compute six-dimensional tonal centroid and symbolic baselines | B + R | Not implemented |
| Song-disjoint emotion classification, ablation and uncertainty analysis | R + B | Not implemented |
| Manuscript, external critique and submission decision | R + B | Not implemented |


The emotion experiment must compare **symbolic baseline**, **tonal centroid baseline**, **PLR + voice-leading joint baseline**, and **joint baseline plus candidate discordance features**. Models and preprocessing must use **song-disjoint** train/validation/test partitions. Extraction quality, unsupported chords, time segmentation and missing-event coverage must be reported. The four EMOPIA quadrants are categorical labels, **not** continuous valence/arousal ground-truth scores.

## Dataset and scholarly context

Planned dataset: [EMOPIA](https://annahung31.github.io/EMOPIA), released separately under CC BY-NC-SA 4.0; see [`data/README.md`](data/README.md). No copyrighted dataset is committed here. The MIT license of our code **does not** change the dataset's license.

Relevant foundations include Cohn's Neo-Riemannian theory, Tymoczko's *The Geometry of Musical Chords* (2006), and the EMOPIA dataset (ISMIR 2021). Tonnetz and tonal-centroid features have already been used in musical analysis; **novelty and predictive benefits remain open empirical questions**. A research paper has not yet been submitted.

## License

MIT — see [`LICENSE`](LICENSE).
