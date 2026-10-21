import mido

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

def note_name(n: int) -> str:
    return f"{NOTE_NAMES[n % 12]}{n // 12 - 1}"

held = set()   # 当前按住的音

with mido.open_input() as inport:
    for msg in inport:
        if msg.type == 'note_on' and msg.velocity > 0:
            held.add(msg.note)
        elif msg.type in ('note_off', 'note_on'):
            held.discard(msg.note)
        else:
            continue

        names = [note_name(n) for n in sorted(held)]
        pitch_classes = sorted({n % 12 for n in held})
        print(names, pitch_classes)