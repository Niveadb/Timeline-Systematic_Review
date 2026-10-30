"""Timeline settings."""

# Files
CSV_PATH = "articles.csv"
OUTPUT_PATH = "timeline.png and timeline.pdf"
    
# Figure (width, height) in inches
FIG_SIZE = (24, 10)
DPI = 150

# Colors
AXIS_COLOR = "#2C7CBA"      # blue "Time" arrow
STEM_COLOR = "#083C7D"      # dark blue stems
TEXT_COLOR = "#000000"

# Text
AXIS_LABEL = "Years"
FONT_SIZE = 16
AXIS_LABEL_FONT_SIZE = 28

# Rounded boxes (one per author/article)
BOX_FACE = "#A6CEE4"  # light blue
BOX_EDGE = "#2C7CBA"  # blue
BOX_PAD = 0.45          # inner spacing, as a fraction of the font size
BOX_ROUNDING = 0.9      # corner rounding
BOX_STEP_PT = 38        # vertical distance between stacked boxes (pt)
YEAR_OFFSET_PT = 17     # distance from the stem tip to the year (pt)
YEAR_TO_BOX_PT = 36     # distance from the year to the first box (pt)

# Stem heights (in points) above/below the arrow; they repeat in a cycle
# to create the effect of stems with varying heights.
STEM_LEVELS_PT = [50, 100, 150]
