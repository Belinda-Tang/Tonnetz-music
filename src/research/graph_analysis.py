"""Reproducible theoretical distance audit for 24 major/minor triads.

Usage:
    python -m research.graph_analysis
    python -m research.graph_analysis --csv output/triad_distances.csv --top 10
"""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from research.chords import chord_name
from research.graphs import distance_analysis


def write_csv(path: Path, records: list[dict[str, object]]) -> None:
    """Export every unique chord pair and its computed graph properties."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=(
            "source", "target", "plr_distance", "voice_leading_distance",
            "hexatonic_pole", "discordance",
        ))
        writer.writeheader()
        for record in records:
            writer.writerow({
                **record,
                "source": chord_name(*record["source"]),
                "target": chord_name(*record["target"]),
            })


def write_distance_plot(path: Path, records: list[dict[str, object]]) -> None:
    """Bubble plot of all 276 theoretical pairs; bubble labels show counts."""
    import matplotlib.pyplot as plt

    counts = Counter((row["plr_distance"], row["voice_leading_distance"])
                     for row in records)
    points = sorted(counts)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter([p[0] for p in points], [p[1] for p in points],
               s=[25 + 35 * counts[p] for p in points], alpha=0.6)
    for x, y in points:
        ax.annotate(str(counts[x, y]), (x, y), ha="center", va="center", fontsize=8)
    ax.set_xlabel("PLR distance (number of transformations)")
    ax.set_ylabel("Pitch-class voice-leading distance (semitones)")
    ax.set_title("All 276 distinct pairs of major/minor triads")
    ax.set_xticks(range(1, 6))
    ax.set_yticks(sorted({v for _, v in points}))
    ax.grid(alpha=0.2)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, help="Optional CSV export path")
    parser.add_argument("--plot", type=Path, help="Optional PNG/PDF scatter plot path")
    parser.add_argument("--top", type=int, default=8,
                        help="Number of positive/negative discordance examples")
    args = parser.parse_args()
    if args.top < 0:
        parser.error("--top must be nonnegative")

    stats = distance_analysis()
    records = stats["records"]
    print("Exhaustive PLR graph and pitch-class voice-leading analysis")
    print(f"Nodes: {stats['node_count']}; edges: {stats['edge_count']}; "
          f"diameter: {stats['diameter']}; unordered pairs: {stats['pair_count']}")
    print(f"Pearson r (PLR vs pitch-class VL): {stats['pearson_r']:.4f}")
    print(f"PLR distance distribution: {stats['plr_histogram']}")
    print(f"Mean PLR distance given VL: {stats['mean_plr_by_voice']}")
    for direction, selected in (
        ("Most graph-far (conditional on VL)",
         sorted(records, key=lambda row: (-row["discordance"], row["source"], row["target"]))[:args.top]),
        ("Most graph-near (conditional on VL)",
         sorted(records, key=lambda row: (row["discordance"], row["source"], row["target"]))[:args.top]),
    ):
        print(f"\n{direction}:")
        for row in selected:
            a = chord_name(*row["source"])
            b = chord_name(*row["target"])
            print(f"  {a:5s} -> {b:5s} | PLR={row['plr_distance']} "
                  f"VL={row['voice_leading_distance']} "
                  f"discordance={row['discordance']:+.3f}")

    if args.csv:
        write_csv(args.csv, records)
        print(f"\nExported {len(records)} pairs to {args.csv}")
    if args.plot:
        write_distance_plot(args.plot, records)
        print(f"Exported scatter plot to {args.plot}")


if __name__ == "__main__":
    main()
