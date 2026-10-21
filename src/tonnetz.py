NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

FIFTH = 7         # One step right: perfect fifth (+7 semitones)
MAJOR_THIRD = 4   # One step up-right: major third (+4 semitones)


def pitch_class_at(x: int, y: int) -> int:
    """Return the pitch class (0-11) at grid coordinate (x, y)."""
    return (FIFTH * x + MAJOR_THIRD * y) % 12


def print_grid(width: int = 8, height: int = 5, highlight=()) -> None:
    """Print the Tonnetz grid in the terminal.

    Pitch classes in `highlight` are wrapped in brackets.
    """
    for y in reversed(range(height)):        # Print from the top row down
        row = " " * (y * 2)                   # Shift each higher row right by half a cell
        for x in range(width):
            pc = pitch_class_at(x, y)
            name = NOTE_NAMES[pc]
            cell = f"[{name}]" if pc in highlight else f" {name} "
            row += cell.ljust(5)
        print(row)


if __name__ == "__main__":
    # Sanity checks for the interval rules
    assert pitch_class_at(0, 0) == 0    # Origin is C
    assert pitch_class_at(1, 0) == 7    # Right: G (perfect fifth)
    assert pitch_class_at(0, 1) == 4    # Up-right: E (major third)
    assert pitch_class_at(1, -1) == 3   # Down-right: D#/Eb (minor third)
    print("All tests passed!\n")

    print_grid(highlight={0, 4, 7})     # Highlight a C major triad