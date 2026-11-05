"""Generate a VERTICAL timeline (years increase downward, spacing proportional to time).

One stem per year. Each author/article is shown as plain text; articles from
the same year are stacked at the end of the stem, split into two columns when
the year has many articles. All boxes of a year sit on a shared background panel
attached to the stem, so it is clear which articles belong to which year. The figure size is computed automatically.
"""

import csv
import math
from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

import settings

if settings.USE_LATEX:
    # Computer Modern Roman (requires LaTeX to be installed)
    plt.rcParams["text.usetex"] = True
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Computer Modern Roman"]
    WEIGHT, STYLE = "bold", "italic"
else:
    # Computer Modern bundled with matplotlib. It has no bold/italic, and asking
    # for them is what triggers the "findfont: Failed to find font weight bold" warning.
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["cmr10"]
    plt.rcParams["axes.formatter.use_mathtext"] = True
    WEIGHT, STYLE = "normal", "normal"


def load_by_year(path):
    """Return {year: [sorted authors]} from the CSV."""
    by_year = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_year[int(r["year"])].append(r["author"].strip())
    return {y: sorted(authors) for y, authors in sorted(by_year.items())}


def measure_box_widths(texts):
    """Width (pt) of each text, measured with the real font."""
    fig = plt.figure()
    renderer = fig.canvas.get_renderer()
    widths = {}
    for t in texts:
        artist = fig.text(0, 0, t, fontsize=settings.FONT_SIZE, fontweight=WEIGHT)
        w_px = artist.get_window_extent(renderer).width
        widths[t] = w_px * 72 / fig.dpi
    plt.close(fig)
    return widths


def build_blocks(by_year, box_w):
    """For each year: which box goes in which (column, row), plus block sizes."""
    blocks = {}
    for year, authors in by_year.items():
        n = len(authors)
        cols = 2 if n >= settings.TWO_COLUMNS_FROM else 1
        rows = math.ceil(n / cols)
        cells = []                                   # (text, col, row), column-major
        for j, a in enumerate(authors):
            cells.append((a, j // rows, j % rows))
        col_w = [max(box_w[t] for t, c, _ in cells if c == k) for k in range(cols)]
        blocks[year] = dict(cells=cells, cols=cols, rows=rows,
                            half=rows * settings.BOX_STEP_PT / 2, col_w=col_w)
    return blocks


def year_scale(blocks):
    """Smallest pt-per-year that keeps every block clear of its neighbours."""
    if settings.PT_PER_YEAR is not None:
        return settings.PT_PER_YEAR
    years = list(blocks)
    scale = 0.0
    for i in range(1, len(years)):
        scale = max(scale, settings.MIN_YEAR_STEP_PT / (years[i] - years[i - 1]))
        if i >= 2:       # stems alternate sides, so year i shares a side with i-2
            a, b = years[i - 2], years[i]
            need = blocks[a]["half"] + blocks[b]["half"] + settings.BLOCK_GAP_PT
            scale = max(scale, need / (b - a))
    return scale


def panel_width(b):
    """Total width (pt) of the year panel: columns + gap between them + inner padding."""
    return sum(b["col_w"]) + (b["cols"] - 1) * settings.COLUMN_GAP_PT + 2 * settings.PANEL_PAD_PT


def main():
    by_year = load_by_year(settings.CSV_PATH)
    texts = {a for authors in by_year.values() for a in authors}
    box_w = measure_box_widths(texts)
    blocks = build_blocks(by_year, box_w)

    scale = year_scale(blocks)
    y0 = min(by_year)
    pos = {y: (y - y0) * scale for y in by_year}

    # Stem sides/lengths, and how far each side extends horizontally
    levels = settings.STEM_LEVELS_PT
    stems, extent = {}, {1: 0.0, -1: 0.0}
    for i, year in enumerate(by_year):
        side = 1 if i % 2 == 0 else -1
        length = levels[i % len(levels)]
        extent[side] = max(extent[side], length + panel_width(blocks[year]))
        stems[year] = (side, length)

    left = extent[-1] + settings.SIDE_MARGIN_PT
    right = max(extent[1] + settings.SIDE_MARGIN_PT, settings.AXIS_LABEL_ROOM_PT)
    y_top = min(pos[y] - blocks[y]["half"] for y in pos) - settings.MARGIN_PT
    y_bottom = max(pos[y] + blocks[y]["half"] for y in pos) + settings.MARGIN_PT

    # 1 data unit = 1 point on both axes, so the figure size follows from the layout
    fig_w = (left + right) / 72 / 0.98
    fig_h = (y_bottom - y_top) / 72 / 0.96
    fig = plt.figure(figsize=(fig_w, fig_h))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_xlim(-left, right)
    ax.set_ylim(y_bottom, y_top)       # inverted: years grow downward
    ax.axis("off")

    # Axis (arrow pointing downward) + axis label
    ax.annotate(
        "",
        xy=(0, y_bottom),
        xytext=(0, y_top),
        arrowprops=dict(arrowstyle="-|>", color=settings.AXIS_COLOR, lw=5, mutation_scale=25),
    )
    ax.annotate(
        settings.AXIS_LABEL, xy=(0, y_bottom), xytext=(12, 0), textcoords="offset points",
        color=settings.AXIS_COLOR, fontsize=settings.AXIS_LABEL_FONT_SIZE,
        fontstyle=STYLE, fontweight=WEIGHT, ha="left", va="center",
    )

    for year in by_year:
        y = pos[year]
        side, length = stems[year]
        x_end = side * length
        b = blocks[year]
        w_panel = panel_width(b)

        # Year panel: starts exactly where the stem ends, same height as the block slot
        x0 = x_end if side > 0 else x_end - w_panel
        ax.add_patch(FancyBboxPatch(
            (x0, y - b["half"]), w_panel, 2 * b["half"],
            boxstyle=f"round,pad=0,rounding_size={settings.PANEL_ROUNDING}",
            facecolor=settings.PANEL_FACE, edgecolor=settings.STEM_COLOR, linewidth=1.6, zorder=1,
        ))

        # Horizontal stem
        ax.plot([0, x_end], [y, y], color=settings.STEM_COLOR, lw=1.8, solid_capstyle="butt", zorder=2)

        # Year, just above the stem
        ax.annotate(
            f"({year})", xy=(x_end / 2, y), xytext=(0, settings.YEAR_OFFSET_PT),
            textcoords="offset points", ha="center", va="center",
            fontsize=settings.FONT_SIZE, fontweight=WEIGHT, color=settings.STEM_COLOR,
        )

        # x offset (from the stem tip) where each column starts
        col_off, acc = [], settings.PANEL_PAD_PT
        for w in b["col_w"]:
            col_off.append(acc)
            acc += w + settings.COLUMN_GAP_PT

        for text, col, row in b["cells"]:
            dy = ((b["rows"] - 1) / 2 - row) * settings.BOX_STEP_PT
            ax.annotate(
                text, xy=(x_end, y),
                xytext=(side * col_off[col], dy), textcoords="offset points",
                ha="left" if side > 0 else "right", va="center",
                fontsize=settings.FONT_SIZE, fontweight=WEIGHT, color=settings.TEXT_COLOR,
                zorder=3,
            )

        # Thin dividers between authors of the same column
        for k in range(b["cols"]):
            n_k = sum(1 for _, c, _ in b["cells"] if c == k)
            xa = x_end + side * col_off[k]
            xb = xa + side * b["col_w"][k]
            for r in range(1, n_k + 1):
                if r == b["rows"]:       # the panel border already closes a full column
                    continue
                yl = y - b["half"] + r * settings.BOX_STEP_PT
                ax.plot([xa, xb], [yl, yl], color=settings.DIVIDER_COLOR,
                        lw=settings.DIVIDER_WIDTH, solid_capstyle="butt", zorder=2)

        # Vertical divider in the middle of the gap between the two columns
        if b["cols"] == 2:
            xm = x_end + side * (col_off[1] - settings.COLUMN_GAP_PT / 2)
            inset = settings.PANEL_PAD_PT
            ax.plot([xm, xm], [y - b["half"] + inset, y + b["half"] - inset],
                    color=settings.DIVIDER_COLOR, lw=settings.DIVIDER_WIDTH,
                    solid_capstyle="butt", zorder=2)

    for ext in settings.OUTPUT_FORMATS:
        fig.savefig(f"{settings.OUTPUT_BASENAME}.{ext}", dpi=settings.DPI, facecolor="white")
    n_art = sum(len(a) for a in by_year.values())
    print(f"Timeline saved ({n_art} articles, {len(by_year)} years, "
          f"{scale:.0f} pt/year, figure {fig_w:.1f} x {fig_h:.1f} in)")


if __name__ == "__main__":
    main()
