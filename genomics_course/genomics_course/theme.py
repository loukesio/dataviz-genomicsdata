"""
genomics_course.theme
─────────────────────
Single source of truth for the course plotting identity.

Importing this module:
  1. Registers IBM Plex Mono from ../fonts/IBM_Plex_Mono (with fallbacks; falls
     back to DejaVu Sans Mono if the folder ever moves so a render never crashes).
  2. Defines the Economist palette + named base ramps + helpers
     (ECON_QUAL, econ_cmap, econ_diverging, econ_spectrum).
  3. Applies the cream-canvas matplotlib rcParams.
  4. Exposes back-compat aliases (COLORS, BRAND, ACCENT_*, etc.) the existing
     section files still reference. New code should use the canonical names.

  >>> from genomics_course.theme import *
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
import matplotlib.pyplot as plt

# ════════════════════════════════════════════════════════════════════════
# 1) Register IBM Plex Mono so every figure inherits it via rcParams.
#    Path candidates cover: running from a deck folder (../fonts/…), running
#    from repo root (fonts/…), and the installed-package case where we walk
#    up to the repo root.
# ════════════════════════════════════════════════════════════════════════

_PKG_ROOT = Path(__file__).resolve().parent.parent   # …/genomics_course
_REPO_ROOT = _PKG_ROOT.parent                        # …/dataviz-genomicsdata

_FONT_CANDIDATES = (
    _REPO_ROOT / "fonts" / "IBM_Plex_Mono",
    Path.cwd() / "fonts" / "IBM_Plex_Mono",
    Path.cwd().parent / "fonts" / "IBM_Plex_Mono",
    Path.cwd().parent.parent / "fonts" / "IBM_Plex_Mono",
)

_font_dir: Path | None = next((p for p in _FONT_CANDIDATES if p.exists()), None)

if _font_dir is not None:
    for _ttf in _font_dir.glob("*.ttf"):
        fm.fontManager.addfont(str(_ttf))
    _MONO = "IBM Plex Mono"
else:
    _MONO = "DejaVu Sans Mono"   # graceful fallback; render never hard-fails

IBM_MONO = _MONO   # back-compat alias

# ════════════════════════════════════════════════════════════════════════
# 2) Economist categorical palette — the five "story" colours.
# ════════════════════════════════════════════════════════════════════════

GREEN  = "#379A8B"   # Econ green-teal — PRIMARY story colour
BLUE   = "#006BA2"   # Econ deep blue
AMBER  = "#EBB434"   # Econ yellow
RED    = "#B4405F"   # Econ red-magenta — highlight
PURPLE = "#9A607F"   # Econ mauve — highlight
GREY   = "#B3B3B3"   # London grey — neutral / de-emphasis

# Neutrals
INK   = "#0D0D0D"    # near-black ink (London 5)
CREAM = "#FAF9F7"    # warm canvas — never pure white
LINE  = "#D9D9D9"    # hairlines / spines (London 85)
MUTED = "#666666"    # axis labels / secondary text (London 40)

# Full Economist base ramps (dark → light).
ECON: dict[str, list[str]] = {
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

# Qualitative palettes for distinct categories.
COURSE_PAL = [GREEN, BLUE, AMBER, RED, PURPLE]                       # the five
ECON_QUAL  = [ECON["chicago"][2], ECON["hongkong"][0], ECON["newyork"][0],
              ECON["shanghai"][1], ECON["tokyo"][1], ECON["singapore"][0]]


def econ_cmap(ramp: str = "chicago", reverse: bool = False) -> LinearSegmentedColormap:
    """Continuous Economist colormap from one named ramp (perceptual, no rainbow)."""
    cols = ECON[ramp][::-1] if reverse else ECON[ramp]
    return LinearSegmentedColormap.from_list(f"econ_{ramp}", cols)


# Diverging blue–cream–red (e.g. for log2 fold-change).
econ_diverging = LinearSegmentedColormap.from_list("econ_div", [BLUE, CREAM, RED])

# Full-spectrum ramp for many-component stacks (blue→teal→green→amber→red).
econ_spectrum = LinearSegmentedColormap.from_list(
    "econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1],
     ECON["newyork"][0], ECON["red"][1]],
)

# ════════════════════════════════════════════════════════════════════════
# 3) Matplotlib rcParams — IBM Plex Mono on the warm Economist canvas.
# ════════════════════════════════════════════════════════════════════════

mpl.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "font.family": _MONO,
    "axes.edgecolor": LINE, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 12,
})

# ════════════════════════════════════════════════════════════════════════
# 4) Back-compat aliases — the existing section files still reference these
#    names (COLORS dict, BRAND*, ACCENT_*, GRAY_DARK). Values are repointed
#    to Economist equivalents; every key preserved so nothing breaks.
# ════════════════════════════════════════════════════════════════════════

COLORS = {
    "pathogenic":   RED,    "risk":      AMBER, "benign":  GREEN, "uncertain":    GREY,
    "primary":      GREEN,  "secondary": BLUE,  "tertiary": AMBER,
    "quaternary":   PURPLE, "quinary":   ECON["tokyo"][1],
    "text_dark":    INK,    "text_mid":  MUTED, "text_light": GREY,
    "grid":         LINE,   "zero_line": LINE,  "canvas":   CREAM,
    "highlight_bg": ECON["hongkong"][4],
}
BRAND, BRAND_LIGHT, BRAND_BG = GREEN, ECON["hongkong"][3], ECON["hongkong"][4]
ACCENT_YLW, ACCENT_PURP, GRAY_DARK = AMBER, PURPLE, MUTED

# Ancestry bars (K1..K5) — five Economist hues, distinct against each other.
ANCESTRY = list(COURSE_PAL)


def save(fig, path, *, dpi: int = 200, **kwargs):
    """Save a figure with the course defaults (high DPI, tight bbox, cream bg)."""
    kwargs.setdefault("bbox_inches", "tight")
    kwargs.setdefault("facecolor", CREAM)
    fig.savefig(path, dpi=dpi, **kwargs)
    return path


# ════════════════════════════════════════════════════════════════════════
# 5) Pipeline flowchart helper (used by ~8 sections; carried over verbatim).
# ════════════════════════════════════════════════════════════════════════

def pipeline_flowchart(steps, figsize=None):
    """Horizontal pipeline diagram. ``steps`` is a list of bare strings or
    (label, description) tuples; the last box is filled GREEN (the destination)."""
    norm = [s if isinstance(s, str) else s[0] for s in steps]
    n = len(norm)
    if figsize is None:
        figsize = (max(11, n * 1.9), 2.0)
    fig, ax = plt.subplots(figsize=figsize, facecolor=CREAM)
    ax.set_xlim(0, n); ax.set_ylim(0, 1); ax.axis("off")
    highlight, light_fill = GREEN, ECON["hongkong"][3]
    for i, label in enumerate(norm):
        last = (i == n - 1)
        bg, fg = (highlight, "white") if last else (light_fill, INK)
        ax.add_patch(FancyBboxPatch(
            (i + 0.07, 0.22), 0.86, 0.56,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=bg, edgecolor=highlight, linewidth=1.4))
        ax.text(i + 0.5, 0.5, label, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color=fg, wrap=True)
        if not last:
            ax.annotate("", xy=(i + 1.07, 0.5), xytext=(i + 0.93, 0.5),
                        arrowprops=dict(arrowstyle="-|>", color=LINE,
                                        lw=1.4, mutation_scale=18))
    plt.tight_layout()
    return fig


# ════════════════════════════════════════════════════════════════════════
# 6) __all__ — what `from genomics_course.theme import *` brings in.
# ════════════════════════════════════════════════════════════════════════

__all__ = [
    # Economist palette
    "GREEN", "BLUE", "AMBER", "RED", "PURPLE", "GREY",
    "INK", "CREAM", "LINE", "MUTED",
    # ramps + helpers
    "ECON", "ECON_QUAL", "econ_cmap", "econ_diverging", "econ_spectrum",
    # categorical convenience
    "COURSE_PAL",
    # back-compat aliases (existing sections + plots/ depend on these)
    "COLORS", "BRAND", "BRAND_LIGHT", "BRAND_BG",
    "ACCENT_YLW", "ACCENT_PURP", "GRAY_DARK", "IBM_MONO",
    "ANCESTRY", "save",
    # helper
    "pipeline_flowchart",
]
