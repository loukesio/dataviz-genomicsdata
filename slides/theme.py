"""
genomics_course.theme
─────────────────────
The single source of truth for the course's plotting identity.

Importing this module does three things, once and idempotently:

  1. registers IBM Plex Mono (the figure font), with a safe fallback
  2. exposes the Economist colour palette + ramp helpers
  3. applies the matplotlib rcParams (cream canvas, muted axes, no top/right
     spines) so every figure looks the same without per-plot fuss

Every figure in the deck does `from genomics_course.theme import *`, so the look
is GUARANTEED, not improvised. This module is also the worked example taught in
`sections/_04_fundamentals.qmd` — "build your own palette" and "build your own
theme" walk through exactly these four sections.
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap


# ════════════════════════════════════════════════════════════════
# 1 · PALETTE — the Economist colour system (the only colours allowed)
# ════════════════════════════════════════════════════════════════

# the categorical "story" five
GREEN  = "#379A8B"   # green-teal — carries the story
BLUE   = "#006BA2"   # secondary
AMBER  = "#EBB434"   # secondary
RED    = "#B4405F"   # highlight one thing
PURPLE = "#9A607F"   # highlight one thing
GREY   = "#B3B3B3"   # de-emphasise

# neutrals
INK   = "#0D0D0D"
CREAM = "#FAF9F7"
LINE  = "#D9D9D9"
MUTED = "#666666"

# a name → hex view, for code that prefers a dict
COLORS = {
    "green": GREEN, "blue": BLUE, "amber": AMBER, "red": RED, "purple": PURPLE,
    "grey": GREY, "ink": INK, "cream": CREAM, "line": LINE, "muted": MUTED,
}

# the five, in order, for categorical cycles
COURSE_PAL = [GREEN, BLUE, AMBER, RED, PURPLE]

# full Economist base ramps — for many-category and continuous needs
ECON = {
    "chicago":   ["#141F52", "#1F2E7A", "#2E45B8", "#475ED1", "#D6DBF5", "#EBEDFA"],
    "hongkong":  ["#169C7F", "#1DC9A4", "#36E2BD", "#D2F9F0", "#E9FCF8"],
    "newyork":   ["#F9C31F", "#FBD051", "#FCDE83", "#FEF2CD", "#FEF8E6"],
    "shanghai":  ["#4C9C16", "#62C91D", "#7BE236", "#E2F9D2", "#F0FCE9"],
    "singapore": ["#F97A1F", "#FB9851", "#FCB583", "#FEE1CD", "#FEF0E6"],
    "tokyo":     ["#9C1633", "#C91D42", "#E2365B", "#F9D2DB", "#FCE9ED"],
    "red":       ["#CC100A", "#E3120B", "#F6423C", "#FEE7E7"],
    "london":    ["#0D0D0D", "#1A1A1A", "#333333", "#595959", "#666666",
                  "#B3B3B3", "#D9D9D9", "#F2F2F2", "#FFFFFF"],
    "canvas":    ["#D0D3E1", "#E0E2EB", "#EFF0F5"],
}

# ~6 maximally-distinct hues (one strong tint per ramp) for qualitative categories
ECON_QUAL = [ECON["chicago"][2], ECON["hongkong"][0], ECON["newyork"][0],
             ECON["shanghai"][1], ECON["tokyo"][1], ECON["singapore"][0]]


# ════════════════════════════════════════════════════════════════
# 2 · COLORMAP HELPERS — continuous scales, always on-system
# ════════════════════════════════════════════════════════════════

def econ_cmap(ramp="chicago", reverse=False):
    """Continuous colormap built from one named Economist ramp."""
    cols = ECON[ramp][::-1] if reverse else ECON[ramp]
    return LinearSegmentedColormap.from_list(f"econ_{ramp}", cols)


# blue → cream → red, for signed values (e.g. log2 fold-change)
econ_diverging = LinearSegmentedColormap.from_list("econ_div", [BLUE, CREAM, RED])

# blue → teal → green → amber → red, for many-component stacks (areas, ridges)
econ_spectrum = LinearSegmentedColormap.from_list(
    "econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1],
     ECON["newyork"][0], ECON["red"][1]])


# ════════════════════════════════════════════════════════════════
# 3 · FONT — register IBM Plex Mono, fall back gracefully
# ════════════════════════════════════════════════════════════════

def _register_mono():
    """Register IBM Plex Mono from the repo's fonts/ folder. Never hard-fail:
    fall back to DejaVu Sans Mono if the folder can't be found."""
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1] / "fonts" / "IBM_Plex_Mono",   # repo-root/fonts (package install)
        Path("../fonts/IBM_Plex_Mono"),                 # rendering from day1/
        Path("fonts/IBM_Plex_Mono"),                    # rendering from repo root
    ]
    for cand in candidates:
        if cand.exists():
            for ttf in cand.glob("*.ttf"):
                fm.fontManager.addfont(str(ttf))
            return "IBM Plex Mono"
    return "DejaVu Sans Mono"


MONO = _register_mono()


# ════════════════════════════════════════════════════════════════
# 4 · RCPARAMS — one unified look applied to every figure
# ════════════════════════════════════════════════════════════════

def apply_theme():
    """Apply the course matplotlib defaults. Idempotent — safe to call again."""
    mpl.rcParams.update({
        "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
        "font.family": MONO,
        "axes.edgecolor": LINE, "axes.labelcolor": MUTED,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "bold", "axes.titlecolor": INK,
        "axes.titlesize": 12, "font.size": 12,
    })


# apply on import, so a bare `import genomics_course.theme` is enough
apply_theme()


__all__ = [
    "GREEN", "BLUE", "AMBER", "RED", "PURPLE", "GREY",
    "INK", "CREAM", "LINE", "MUTED", "COLORS", "COURSE_PAL",
    "ECON", "ECON_QUAL", "econ_cmap", "econ_diverging", "econ_spectrum",
    "apply_theme", "MONO",
]
