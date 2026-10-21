import matplotlib.pyplot as plt
import mido

from chords import chord_name, identify_triad
from tonnetz_view import draw


def main() -> None:
    plt.ion()  # Interactive mode: the window updates without blocking
    fig, ax = plt.subplots(figsize=(10, 6))
    draw(ax, set())

    held = set()
    with mido.open_input() as inport:
        # Keep running until the plot window is closed
        while plt.fignum_exists(fig.number):
            changed = False

            # Read all MIDI messages that arrived since the last frame
            for msg in inport.iter_pending():
                if msg.type == "note_on" and msg.velocity > 0:
                    held.add(msg.note)
                    changed = True
                elif msg.type in ("note_off", "note_on"):
                    held.discard(msg.note)
                    changed = True

            if changed:
                pcs = {n % 12 for n in held}
                bass = min(held) % 12 if held else None
                chord = identify_triad(pcs, bass=bass)
                label = chord_name(*chord) if chord else ""
                draw(ax, pcs, chord, label)
                fig.canvas.draw_idle()

            plt.pause(0.02)  # Let the window refresh (~50 frames per second)


if __name__ == "__main__":
    main()