# Literature Review

Last updated: 2026-10-25

## Research Question

Do features derived from harmonic transformation graphs improve emotion prediction for symbolic piano music beyond simpler musical features?

## Status

The graph model (major/minor triads, PLR graph distance, pitch-class voice-leading distance, and the conditional residual GVLD) is implemented. The emotion experiments are not. This document records related work and the limits it places on what the project can claim.

## 1. Music-Theoretic Background

| Reference | Contribution | Implication for this project |
| --- | --- | --- |
| [Hyer (1995), *Reimag(in)ing Riemann*](https://www.jstor.org/stable/843900) | Describes the Tonnetz as a space of triad relationships and transformations rather than tonal functions. | A visual path on the Tonnetz is not the same object as a PLR path. |
| [Cohn (1996), *Maximally Smooth Cycles*](https://www.jstor.org/stable/854168) | Studies parsimonious triadic cycles and hexatonic systems in late-Romantic music. | Hexatonic relations are established; enumerating them is not a new result. |
| [Cohn (1997), *Neo-Riemannian Operations*](https://doi.org/10.2307/843761) | Develops the P, L and R operations and extends them beyond consonant triads. | Basis for the 24-vertex PLR graph and the transformation tests. |
| [Cohn (1998), *Introduction to Neo-Riemannian Theory*](https://www.jstor.org/stable/843871) | Surveys the motivation for transformational approaches to chromatic music. | PLR distance omits tonal function and listening context. |
| [Douthett & Steinbach (1998), *Parsimonious Graphs*](https://www.jstor.org/stable/843877) | Constructs parsimonious graphs, including Cube Dance, for several chord relations. | Graph models of chords are not new. Cube Dance is a candidate later comparison and would need its own definition. |
| [Gollin (1998), *Three-Dimensional Tonnetze*](https://doi.org/10.2307/843873) | Uses three-dimensional Tonnetze to represent tetrachords and contextual transformations. | A 3D viewer is not by itself a research contribution. |
| [Tymoczko (2006), *The Geometry of Musical Chords*](https://doi.org/10.1126/science.1126287) | Models chords as points in geometric spaces and studies efficient voice leading. | The VL distance here is an octave-independent, three-pitch-class matching cost. It does not model performed voices or the orbifold geometry. |
| [Forrest (2017), *PL Voice Leading and the Uncanny in Pop Music*](https://doi.org/10.30535/mto.23.4.6) | Analyzes PL/LP relations, hexatonic poles and their possible uncanny associations in individual songs. | These are contextual interpretations, not emotion labels. The pole predicate in this repository does not cover all of Forrest's examples. |
| [Hutchinson (2020), *From a Certain Point of View*](https://www.jstor.org/stable/27121055) | Shows that chromatic harmony can be heard differently depending on tonal context. | The distance between an isolated chord pair cannot account for the full listening experience. |

## 2. Closest Machine-Learning Work

[Xia et al. (2026), *Let the Model Learn to Feel: Mode-Guided Tonality Injection for Symbolic Music Emotion Recognition*](https://doi.org/10.1609/aaai.v40i3.37201) (AAAI 2026).

The authors classify symbolic music by emotion with MIDIBERT. Major/minor mode is estimated with a Krumhansl–Kessler method, pitch-transposition augmentation is applied, and mode information is injected through a FiLM module. They report 75.2% accuracy / 75.1% F1 on EMOPIA and 59.1% accuracy / 58.7% F1 on VGMIDI. In their ablation on EMOPIA, removing mode knowledge lowers accuracy from 75.2% to 71.6%. Clips from the same song are kept in the same split.

Consequences for this project:

- Music-theory features, mode information, transposition augmentation and song-disjoint splits are not novel in themselves.
- Mode must be included as a control. Otherwise any gain from PLR features may reflect major/minor information already available to the model.
- Their method uses global mode; this project uses chord-to-chord transformations. This is a possible distinction, not evidence of novelty.
- Their model is a relevant published benchmark, but scores obtained under different splits and training setups are not directly comparable to results here.
- Their Table 2 appears to pair some emotion names with the wrong valence–arousal quadrants. Quadrant names should follow the [original EMOPIA Q1–Q4 definitions](https://annahung31.github.io/EMOPIA/).
- Their augmentation experiment and layer probes support the proposed method. A gain in accuracy alone does not show that the model represents mode as a listener would.

## 3. Other Related Work to Check

- [Zhang et al. (2025), *Moderating effects of chord progressions on the emotional experience of major and minor chords*](https://doi.org/10.1016/j.actpsy.2025.104690). Listener experiments show that chord context changes emotional judgments, so a link between progressions and emotion is already documented.
- [*Deep Learning Model for Quantification of Harmonic Tension and Its Application in Emotional Composition* (2026)](https://doi.org/10.1016/j.sasc.2026.200606). Studies harmonic-tension features and emotion-related tasks, including on EMOPIA+. Its methods should be read before any claim of a new tension/emotion framework.
- [*Symbolic music structure analysis with graph representations and changepoint detection methods* (2026)](https://doi.org/10.1016/j.neucom.2025.132208). Graph representations are already used for symbolic music structure analysis, although the prediction task differs.

## 4. Positioning

The question under study is whether the order and structure of chord changes carry information beyond which chords occur in a piece. The planned comparison is between conventional symbolic features (mode, rhythm, velocity, chord counts) and PLR distance, VL distance, GVLD and six-dimensional tonal-centroid features.

At the level of a single transition, GVLD is a deterministic function of the pair (PLR, VL) and adds no information. A clip-level mean GVLD can still differ from what mean PLR and mean VL capture, since averaging discards information. The appropriate baselines are therefore richer joint-distance summaries or models with interaction terms, not only the two means.

## 5. Planned First Experiment

1. **Chord extraction.** Measure the accuracy of major/minor chord sequences extracted from EMOPIA and the fraction of events that cannot be assigned.
2. **Prediction.** Test whether transition-based features improve song-disjoint valence/arousal or four-quadrant prediction over mode-aware symbolic and tonal baselines.
3. **Order ablation.** Shuffle chord order within clips while keeping chord counts fixed, and compare results. This tests the contribution of sequence order, with the caveat that shuffling produces artificial progressions.
