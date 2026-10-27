"""Generate a timeline with ONE stem per year.

Articles from the same year are stacked under the same label, like this:

    AUTHOR A
    AUTHOR B
    (year)
"""

import csv
from collections import defaultdict

import matplotlib.pyplot as plt

import settings


def load_by_year(path):
    """Return {year: [sorted authors]} from the CSV."""
    by_year = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_year[int(r["year"])].append(r["author"].strip())
    return {y: sorted(authors) for y, authors in sorted(by_year.items())}


def label_text(year, authors):
    lines = [a.upper() for a in authors] + [f"({year})"]
    return "\n".join(lines)


def main():
    by_year = load_by_year(settings.CSV_PATH)
    years = list(by_year)
    x_min, x_max = min(years) - 1.0, max(years) + 2.0

    fig_w, fig_h = settings.FIG_SIZE
    fig = plt.figure(figsize=settings.FIG_SIZE)
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])

    # Y-axis in points (1 unit = 1 pt), to size stems and labels
    half_h = fig_h * 72 * 0.96 / 2
    ax.set_ylim(-half_h, half_h)
    ax.set_xlim(x_min, x_max)
    ax.axis("off")

    # Axis (green arrow) + "Years" label
    ax.annotate(
        "",
        xy=(x_max, 0),
        xytext=(x_min, 0),
        arrowprops=dict(arrowstyle="-|>", color=settings.AXIS_COLOR, lw=3, mutation_scale=25),
    )
    ax.text(
        x_max - 0.05, 8, settings.AXIS_LABEL,
        color=settings.AXIS_COLOR, fontsize=settings.AXIS_LABEL_FONT_SIZE,
        fontstyle="italic", fontweight="bold", ha="right", va="bottom",
    )

    levels = settings.STEM_LEVELS_PT
    for i, (year, authors) in enumerate(by_year.items()):
        side = 1 if i % 2 == 0 else -1          # alternate above/below
        h = levels[i % len(levels)] * side      # stem height (varies)
        ax.plot([year, year], [0, h], color=settings.STEM_COLOR, lw=1.8, solid_capstyle="butt")

        # Year next to the stem; each author in a rounded box, stacked outward
        y = h + (settings.YEAR_OFFSET_PT * side)
        ax.text(
            year, y, f"({year})",
            ha="center", va="center",
            fontsize=settings.FONT_SIZE, fontweight="bold", color=settings.TEXT_COLOR,
        )
        y += settings.YEAR_TO_BOX_PT * side
        for author in authors:
            ax.text(
                year, y, author.upper(),
                ha="center", va="center",
                fontsize=settings.FONT_SIZE, fontweight="bold", color=settings.TEXT_COLOR,
                bbox=dict(
                    boxstyle=f"round,pad={settings.BOX_PAD},rounding_size={settings.BOX_ROUNDING}",
                    facecolor=settings.BOX_FACE,
                    edgecolor=settings.BOX_EDGE,
                    linewidth=1.4,
                ),
            )
            y += settings.BOX_STEP_PT * side

    for ext in ("png", "pdf"):
        fig.savefig(f"timeline.{ext}", dpi=settings.DPI, facecolor="white")
    n = sum(len(a) for a in by_year.values())
    print(f"Timeline saved in {settings.OUTPUT_PATH} ({n} articles, {len(by_year)} years)")


if __name__ == "__main__":
    main()