import math

from matplotlib.patches import Polygon

from tonnetz import NOTE_NAMES, pitch_class_at

WIDTH, HEIGHT = 9, 5             # Grid size (columns, rows)
ROW_HEIGHT = math.sqrt(3) / 2    # Height of an equilateral triangle

# Color palette
MAJOR_COLOR = "#F8B4C8"        # Soft pink for major triads
MINOR_COLOR = "#A8E6CF"        # Mint green for minor triads
NODE_ACTIVE = "#9B8EC4"        # Lavender for held notes
NODE_IDLE = "#FFFFFF"          # White for idle notes
NODE_EDGE = "#C9C3DD"          # Light lavender-gray outline
EDGE_COLOR = "#E6E1EF"         # Very light lines between notes
TEXT_DARK = "#4A4458"          # Dark plum-gray for idle labels
TEXT_LIGHT = "#FFFFFF"         # White for active labels


def to_screen(x: int, y: int):
    """Convert grid coordinates to screen coordinates."""
    return x + 0.5 * y, y * ROW_HEIGHT


def in_grid(x: int, y: int) -> bool:
    return 0 <= x < WIDTH and 0 <= y < HEIGHT


def triangle_vertices(x: int, y: int, quality: str):
    """Grid vertices of the triad whose root sits at (x, y)."""
    if quality == "major":
        return [(x, y), (x + 1, y), (x, y + 1)]       # Points up
    if quality == "minor":
        return [(x, y), (x + 1, y), (x + 1, y - 1)]   # Points down
    return []  # Diminished/augmented chords are not triangles


def draw(ax, held_pcs, chord=None, label: str = "") -> None:
    """Redraw the whole Tonnetz on the given axes."""
    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(label, fontsize=22)

    # Layer 1: fill every triangle that matches the current chord
    if chord:
        root, quality = chord
        color = MAJOR_COLOR if quality == "major" else MINOR_COLOR
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if pitch_class_at(x, y) != root:
                    continue
                verts = triangle_vertices(x, y, quality)
                if verts and all(in_grid(*v) for v in verts):
                    points = [to_screen(*v) for v in verts]
                    ax.add_patch(Polygon(points, closed=True,
                                         color=color, alpha=0.8, zorder=0))

    # Layer 2: grid edges (fifth, major third, minor third)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            x0, y0 = to_screen(x, y)
            for dx, dy in [(1, 0), (0, 1), (1, -1)]:
                if in_grid(x + dx, y + dy):
                    x1, y1 = to_screen(x + dx, y + dy)
                    ax.plot([x0, x1], [y0, y1], color=EDGE_COLOR,
                            linewidth=1.0, zorder=1)

    # Layer 3: note nodes, red if currently held
    for x in range(WIDTH):
        for y in range(HEIGHT):
            sx, sy = to_screen(x, y)
            pc = pitch_class_at(x, y)
            active = pc in held_pcs
            ax.scatter(sx, sy, s=650, zorder=2,
                       color=NODE_ACTIVE if active else NODE_IDLE,
                       edgecolors=NODE_EDGE)
            ax.text(sx, sy, NOTE_NAMES[pc], ha="center", va="center",
                    fontsize=9, zorder=3,
                    color=TEXT_LIGHT if active else TEXT_DARK)