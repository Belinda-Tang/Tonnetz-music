# Tonnetz-music

**See harmony as shapes.** Play chords on a MIDI keyboard and watch them light up on a live Tonnetz, a geometric map of musical harmony.

<!-- Replace with your demo video or GIF (see "Adding the demo" in the reply) -->
![Demo](assets/demo.gif)

---

## What is the Tonnetz?

The Tonnetz ("tone network") is a grid where every node is a note and neighbors are related by simple intervals:

| Direction | Interval | Example |
|---|---|---|
| → right | Perfect fifth (+7 semitones) | C → G |
| ↗ up-right | Major third (+4 semitones) | C → E |
| ↘ down-right | Minor third (+3 semitones) | C → E♭ |

On this grid, every **major triad is an upward triangle** and every **minor triad is a downward triangle**. Chords that sound smooth together sit right next to each other.

## Features

- 🎹 **Live MIDI input** from any USB MIDI keyboard
- 🔺 **Chord recognition** for major, minor, diminished and augmented triads, in any inversion or octave
- 🎨 **Real-time visualization**: held notes light up, major triads glow pink, minor triads glow mint green

## How it works

**1. Notes → pitch classes.** Octaves are ignored, so C4 and C5 are both `0`. This matches the Tonnetz, where each node is a note name rather than a specific pitch.

**2. Pitch class at any grid point.**

```
pitch_class(x, y) = (7x + 4y) mod 12
```

`x` counts steps of a fifth, `y` counts steps of a major third. Instead of searching for a note's position, the program computes the note at every grid point and highlights every match.

**3. Chord recognition.** Each note is tried as the root, and the intervals above it are compared with templates:

| Quality | Intervals above root |
|---|---|
| Major | {0, 4, 7} |
| Minor | {0, 3, 7} |
| Diminished | {0, 3, 6} |
| Augmented | {0, 4, 8} |

The augmented triad is **symmetric**: it splits the octave into three equal parts, so every note fits as the root. C+, E+ and G♯+ contain exactly the same notes. The program resolves this by preferring the lowest note being played.

## Observations

Playing **C → Am → F → G**, one of the most common progressions in pop music:

- **C → Am** and **Am → F** are neighboring triangles that share an edge. Only one note moves, which is why these changes sound smooth.
- **F → G** shares no notes, so the chord *jumps* across the grid. That jump creates tension, which **G → C** resolves.

Flipping a triangle across one edge corresponds to the three operations of Neo-Riemannian theory:

- **P** (Parallel): C ↔ Cm
- **R** (Relative): C ↔ Am
- **L** (Leading-tone): Am ↔ F

### Demo progression

The demo uses a progression that covers all four triad types:

**C → Caug → F → Fm → C → G → G♯dim → Am**

The inner voices move by single semitones (G → G♯ → A, and A → A♭), so each step changes just one node on the grid.

## Getting started

### Requirements

- Python 3.10+
- A USB MIDI keyboard (developed with a Roland JUNO-DS)

### Installation

```bash
git clone https://github.com/<your-username>/tonnetz-music.git
cd tonnetz-music
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python src/live_view.py      # Graphical Tonnetz (close the window to quit)
python src/midi_input.py     # Text version in the terminal
```

> **Keyboard not detected?** Check Audio MIDI Setup → MIDI Studio (⌘2) on macOS. Some Roland keyboards need **[SYSTEM] → USB Driver** set to **GENERIC** to work without a vendor driver.

## Project structure

```
tonnetz-music/
├── src/
│   ├── tonnetz.py        # Grid math: pitch class at (x, y)
│   ├── chords.py         # Triad recognition
│   ├── tonnetz_view.py   # Matplotlib drawing
│   ├── live_view.py      # Live MIDI → graphical Tonnetz
│   └── midi_input.py     # Live MIDI → terminal output
├── data/
├── notebooks/
└── requirements.txt
```

## Roadmap

- [x] Live MIDI input
- [x] Triad recognition
- [x] Graphical Tonnetz with live highlighting
- [ ] Chord trails: show the path a progression takes across the grid
- [ ] Read MIDI files and draw the trajectory of a whole song
- [ ] 3D torus view
- [ ] Analyze how harmonic complexity in popular music has changed over the decades

## License

MIT