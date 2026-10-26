from pathlib import Path
import pandas as pd

# Locate the data relative to this file, so the script works from any directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "data" / "raw" / "emopia"

# Find every MIDI file, skipping macOS junk files
midi_files = sorted(
    p for p in ROOT.rglob("*.mid")
    if "__MACOSX" not in p.parts and "_converted" not in p.parts
)
if not midi_files:
    raise FileNotFoundError(f'No midi files found in {ROOT}')
print("MIDI files:", len(midi_files))
print("Example names:", [p.name for p in midi_files[:3]])


def parse_name(name: str):
    """Split 'Q1_<youtube_id>_<seg>.mid' into (quadrant, song_id, segment)."""
    stem = name.removesuffix(".mid")
    quadrant, rest = stem.split("_", 1)
    song_id, segment = rest.rsplit("_", 1)
    return quadrant, song_id, int(segment)


records = pd.DataFrame(
    [parse_name(p.name) for p in midi_files],
    columns=["quadrant", "song_id", "segment"],
)

# 2. Basic counts to compare with the paper
print("\nClips per quadrant:")
print(records["quadrant"].value_counts().sort_index())
print("\nUnique songs:", records["song_id"].nunique())

# 3. Does any song appear in more than one quadrant?
quads_per_song = records.groupby("song_id")["quadrant"].nunique()
print("Songs with clips in >1 quadrant:", (quads_per_song > 1).sum())

# 4. Peek at the label file
label_files = list(ROOT.rglob("label.csv"))
if not label_files:
    raise FileNotFoundError(f"label.csv not found under {ROOT}")
labels = pd.read_csv(label_files[0])
if label_files:
    labels = pd.read_csv(label_files[0])
    print("\nlabel.csv columns:", list(labels.columns))
    print(labels.head())

# 5. Do filename quadrants agree with label.csv?
records["ID"] = [p.name.removesuffix(".mid") for p in midi_files]
merged = records.merge(labels, on="ID", how="outer", indicator=True)
print("\nRows in label.csv:", len(labels))
print(merged["_merge"].value_counts())

matched = merged[merged["_merge"] == "both"]
mismatch = matched[matched["quadrant"] != "Q" + matched["4Q"].astype(str)]
print("Quadrant mismatches:", len(mismatch))