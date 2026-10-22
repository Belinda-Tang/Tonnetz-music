from collections import deque

import matplotlib.pyplot as plt
import mido

from chords import chord_name, identify_triad
from tonnetz_view import draw


def main() -> None:
    plt.ion()
    fig, ax = plt.subplots(figsize=(10, 6))
    draw(ax, set())

    held = set()
    history = deque(maxlen=4)  # The 4 most recent chords, oldest first

    with mido.open_input() as inport:
        while plt.fignum_exists(fig.number):
            changed = False
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

                # Record a chord only when it is new
                if chord and (not history or history[-1] != chord):
                    history.append(chord)

                label = chord_name(*chord) if chord else ""
                draw(ax, pcs, history, label)
                fig.canvas.draw_idle()

            plt.pause(0.02)


if __name__ == "__main__":
    main()