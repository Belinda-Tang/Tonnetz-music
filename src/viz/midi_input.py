import mido
from research.tonnetz import NOTE_NAMES, print_grid
from research.chords import identify_triad, chord_name


def note_name(n: int) -> str:
    return f"{NOTE_NAMES[n % 12]}{n // 12 - 1}"

held = set()   # MIDI note numbers currently held down

with mido.open_input() as inport:
    print("Listening... press the stop button to quit")
    for msg in inport:
        if msg.type == 'note_on' and msg.velocity > 0:
            held.add(msg.note)
        elif msg.type in ('note_off', 'note_on'):
            # Some keyboards send note_on with velocity 0 instead of note_off
            held.discard(msg.note)
        else:
            continue  # Ignore other messages (control change, clock, etc.)

        pitch_classes = {n % 12 for n in held}
        bass = min(held) % 12 if held else None
        chord = identify_triad(pitch_classes, bass=bass)
        label = chord_name(*chord) if chord else "-"
        print("-" * 45)
        print([note_name(n) for n in sorted(held)], "->", label)
        print_grid(highlight=pitch_classes)
