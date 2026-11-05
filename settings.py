"""Timeline settings."""

# Files
CSV_PATH = "articles.csv"
OUTPUT_BASENAME = "timeline"
OUTPUT_FORMATS = ["png", "pdf"]

USE_LATEX = False

# Figure size is computed automatically from the layout
DPI = 150

# Colors
AXIS_COLOR = "#007b3d"      # green "Time" arrow
TEXT_COLOR = "#000000"

STEM_COLOR = "#3678ac"      # dark blue stems and year text
PANEL_FACE = "#E8F2FF"     # very light blue year panel
DIVIDER_COLOR = "#8199ad"   # thin line between authors of the same year
DIVIDER_WIDTH = 0.8

# Text
AXIS_LABEL = "Years"
FONT_SIZE = 16
AXIS_LABEL_FONT_SIZE = 28

# Author names
BOX_STEP_PT = 38        # vertical distance between stacked boxes (pt)
YEAR_OFFSET_PT = 10     # height of the year above the stem (pt)

# Year panel: background that groups all boxes of a year and attaches to the stem
PANEL_PAD_PT = 6        # space between the panel border and the boxes (pt)
PANEL_ROUNDING = 10     # corner rounding of the panel (pt)

# Columns: a year with at least this many articles is split into two columns
TWO_COLUMNS_FROM = 4
COLUMN_GAP_PT = 10      # horizontal gap between the two columns (pt)

# Vertical layout (pt). Spacing is proportional to time.
# PT_PER_YEAR = None -> the smallest value that avoids overlaps is chosen automatically.
# Set a number (e.g. 80) to force a scale; larger = more spread out.
PT_PER_YEAR = None
MIN_YEAR_STEP_PT = 60     # minimum distance between two consecutive years
BLOCK_GAP_PT = 12         # minimum gap between box blocks on the same side
MARGIN_PT = 60            # space above the first and below the last block
SIDE_MARGIN_PT = 20       # space left of / right of the widest block
AXIS_LABEL_ROOM_PT = 150  # minimum room to the right of the axis for the label

# Stem lengths (pt); they repeat in a cycle, alternating right/left,
# to create the effect of stems with varying lengths.
STEM_LEVELS_PT = [60, 110, 160]
