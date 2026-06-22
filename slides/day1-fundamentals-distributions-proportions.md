# Task: Add Fundamentals + Distributions + Proportions to Day 1

> Hand this whole file to Claude Code. It is the authoritative spec for one
> piece of work on `slides/day1_python_gendataviz26.qmd` (+ a small `CLAUDE.md`
> rule update). Follow `CLAUDE.md` rules throughout. **Do not delete or rephrase
> any existing slide content.** This work has four steps, in order:
> (0) update `CLAUDE.md` so its rules match the expanded palette + font,
> (1) patch the `setup` chunk, (2) insert 42 new slides after slide 3,
> (3) renumber every marker in the whole file.

---

## Summary of what changes

0. **CLAUDE.md** — update rules 1 (colour) and 2 (font) so the rulebook documents
   the full Economist palette (`ECON` ramps + helpers) and global IBM Plex Mono.
1. **Setup chunk** — switch the matplotlib palette to the **Economist** system
   (the five story colours from `CLAUDE.md` + the full named base ramps), and
   register **IBM Plex Mono** from `../fonts/IBM_Plex_Mono/` as the figure font.
   All existing constant **names and dict keys are preserved** — only values are
   repointed — so every existing slide still runs.
2. **42 new slides** inserted **after current slide 3** (Datasaurus Dozen) and
   **before current slide 4** (Big data in biology):
   - **Act I–III — Fundamentals of Data Visualization** (18 slides)
   - **Showing Distributions** (14 slides: when/why + box & violin step-builds + ridgeline)
   - **Showing Proportions** (9 slides: bars-not-pies + stacked-bar & stacked-area step-builds)
3. **Full renumber** — flat consecutive integers `1 … 130` in document order.

## Global style rules (from CLAUDE.md — obey on every new slide)

- **Slide pattern (unified — match the existing "Anscombe" slide):**
  `## Title {.smaller}` → blank line → `[Section · subsection]{.eyebrow}` →
  blank line → `### Visible subtitle` → content. Dividers are `# Title {.divider}`
  with an eyebrow under them.
- **Colours:** use only the setup-chunk constants. `GREEN` (`#379A8B`) carries the
  story; `RED`/`PURPLE` highlight **one thing at a time**; `GREY` de-emphasises;
  `BLUE`/`AMBER` are secondary categoricals. Many-category → `ECON_QUAL`.
  Continuous/stacked → `econ_cmap("…")`. **No off-system colours, no rainbow/jet**
  except where a slide explicitly teaches *against* jet.
- **Font:** figures inherit IBM Plex Mono from the patched rcParams. Do not set
  slide fonts (Asap/Space Grotesk) inside matplotlib.
- **Figures:** reuse `rng`, the rcParams, and the palette constants. `plt.show()`
  ends every chunk. Canvas is `CREAM`.
- **Code/Plot toggle:** every slide whose figure is the focus wraps it in a
  `panel-tabset` with a **Plot** tab (executed, `#| echo: false`) and a **Code**
  tab (a non-executed ```python block showing the plotting logic).
- **Takeaway:** only the punchline slides use `::: {.takeaway}` (`.alt` = purple
  variant). Not every slide.
- **Fenced-div colon nesting (use exactly this so Quarto parses correctly):**
  tabset `::::: {.panel-tabset}` (5) › columns `:::: {.columns}` (4) ›
  column `::: {.column width="X%"}` (3). Standalone `::: {.takeaway}` / `::: {.footer}` use 3.

---

---

# STEP 0 — Update CLAUDE.md (keep the rulebook in sync)

Two rules in `CLAUDE.md` are about to be out of date: rule 1 lists only five
colours (we now also use the full Economist base ramps), and rule 2 scopes
IBM Plex Mono to "pipeline/flow diagrams" (we now use it for *all* figures).
Make these two replacements so a future session doesn't flag the `ECON` dict or
the global font as violations.

**Replace rule 1** — find this block:

```
1. **No new colors.** The chromatic palette is the **Economist categorical
   palette**, exposed via the SCSS tokens / CSS vars:
   `--gv-green` `#379A8B` (Econ green-teal, primary "story" colour) ·
   `--gv-blue` `#006BA2` (Econ deep blue) ·
   `--gv-amber` `#EBB434` (Econ yellow) ·
   `--gv-red` `#B4405F` (Econ red-magenta) ·
   `--gv-purple` `#9A607F` (Econ mauve) ·
   plus the neutrals `--gv-ink` / `--gv-cream` / `--gv-muted` and the
   DNA bases `--base-a/c/g/t`. Same constants live in the Day-1 `setup`
   chunk as `GREEN BLUE AMBER RED PURPLE` (and the `COURSE_PAL` list).
   Green-teal carries the story; red/purple highlight one thing at a time.
```

with:

```
1. **No off-system colours.** The palette is the **Economist colour system** —
   the five categorical "story" colours plus the named base ramps. Nothing from
   outside this system; no ad-hoc hexes outside the Day-1 `setup` chunk.
   - **Primary five** (SCSS vars / `setup` constants):
     `--gv-green`/`GREEN` `#379A8B` (green-teal — carries the story) ·
     `--gv-blue`/`BLUE` `#006BA2` · `--gv-amber`/`AMBER` `#EBB434` ·
     `--gv-red`/`RED` `#B4405F` · `--gv-purple`/`PURPLE` `#9A607F`.
     Green-teal carries the story; red/purple highlight one thing at a time.
   - **Neutrals:** `--gv-ink`/`INK` · `--gv-cream`/`CREAM` · `--gv-muted`/`MUTED`
     · `GREY` `#B3B3B3`; plus the DNA bases `--base-a/c/g/t`.
   - **Economist base ramps** for many-category & continuous needs — the `ECON`
     dict in `setup`: Chicago (blue), Hong Kong (teal), New York (amber),
     Shanghai (green), Singapore (orange), Tokyo (magenta), Econ Red, London
     (greyscale), Canvas. Source: the marber.economist.com colour system.
   - **Helpers in `setup`:** `COURSE_PAL` (the five) · `ECON_QUAL` (~6
     maximally-distinct hues, one strong tint per ramp, for qualitative
     categories) · `econ_cmap("ramp")` (continuous sequential from one ramp —
     use for stacked areas/heatmaps, **never** a rainbow) · `econ_diverging`
     (blue–cream–red for signed values, e.g. log2 fold-change).
```

**Replace rule 2** — find this block:

```
2. **No new fonts.** JetBrains Mono (labels/code) · Space Grotesk (titles) ·
   Asap (body), all imported in `style.scss`. **IBM Plex Mono** is also
   registered in the Day-1 `setup` chunk via `matplotlib.font_manager` and is
   the font for **all matplotlib pipeline/flow diagrams** — do not use the
   slide fonts inside matplotlib figures.
```

with:

```
2. **No new fonts.** Slide UI: JetBrains Mono (labels/code) · Space Grotesk
   (titles) · Asap (body), imported in `style.scss`. Matplotlib figures:
   **IBM Plex Mono**, registered in the Day-1 `setup` chunk via
   `matplotlib.font_manager` and set as `rcParams["font.family"]`, so it is the
   font for **all** matplotlib figures (not just pipeline/flow diagrams).
   - The `.ttf` files live in **`fonts/IBM_Plex_Mono/`** at the repo root
     (sibling of `slides/`). The `setup` chunk resolves them with path fallbacks
     (`../fonts/IBM_Plex_Mono`, then `fonts/IBM_Plex_Mono`, …) and falls back to
     `DejaVu Sans Mono` if the folder ever moves — a render never hard-fails on a
     missing font.
   - Never set the slide UI fonts (Asap / Space Grotesk / JetBrains) inside a
     matplotlib figure, and never set IBM Plex Mono in the SCSS.
```

---

# STEP 1 — Replace the `setup` chunk

Find the existing chunk labelled `#| label: setup` (near the top, right after the
YAML, beginning `# Course-wide matplotlib defaults — the "Carbon-cream" look.`).
Replace **everything from that `# Course-wide…` comment down to the end of the
`pipeline_flowchart` function** with the block below.

**Preservation guarantees (verify after pasting):** the names `GREEN BLUE AMBER
RED PURPLE GREY CREAM INK LINE COLORS COURSE_PAL BRAND BRAND_LIGHT BRAND_BG
ACCENT_YLW ACCENT_PURP GRAY_DARK rng pipeline_flowchart` all still exist, and every
key that was in `COLORS` is still present. Existing slides reference these — none
may disappear. Only values are repointed to Economist equivalents.

> Note: this intentionally recolours and re-fonts **all** existing Day-1 figures
> (the agreed Option A). After Step 1, run `quarto render` and eyeball a few older
> plot slides to confirm nothing broke.

```{python}
#| label: setup
#| echo: false
# ════════════════════════════════════════════════════════════════════════
# Course-wide matplotlib defaults — Economist editorial system.
#   Palette : Economist categorical five + named base ramps
#             (marber.economist.com colour system).
#   Font    : IBM Plex Mono, registered from ../fonts/IBM_Plex_Mono/.
# Two visual systems do NOT mix: slide UI uses Asap/Space Grotesk (SCSS);
# matplotlib figures use IBM Plex Mono (here).
# ════════════════════════════════════════════════════════════════════════
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── Register IBM Plex Mono from the repo's fonts/ folder ─────────────────────
# slides/ and fonts/ are siblings under the repo root, so ../fonts/ is the
# normal path; a couple of fallbacks keep preview AND render working.
_font_dir = None
for _cand in (Path("../fonts/IBM_Plex_Mono"),
              Path("fonts/IBM_Plex_Mono"),
              Path("../../fonts/IBM_Plex_Mono")):
    if _cand.exists():
        _font_dir = _cand
        break
if _font_dir is not None:
    for _ttf in _font_dir.glob("*.ttf"):
        fm.fontManager.addfont(str(_ttf))
    _MONO = "IBM Plex Mono"
else:
    _MONO = "DejaVu Sans Mono"   # graceful fallback if the folder moves

# ── Economist categorical palette — the canonical "story" colours ───────────
# green-teal carries the story; red / purple highlight one thing at a time.
GREEN  = "#379A8B"   # Econ green-teal — PRIMARY story colour
BLUE   = "#006BA2"   # Econ deep blue
AMBER  = "#EBB434"   # Econ yellow
RED    = "#B4405F"   # Econ red-magenta — highlight
PURPLE = "#9A607F"   # Econ mauve — highlight
GREY   = "#B3B3B3"   # London grey — neutral / de-emphasis

# ── Neutrals ─────────────────────────────────────────────────────────────────
INK   = "#0D0D0D"    # near-black ink (London 5)
CREAM = "#FAF9F7"    # warm canvas — never pure white
LINE  = "#D9D9D9"    # hairlines / spines (London 85)
MUTED = "#666666"    # axis labels / secondary text (London 40)

# ── Full Economist base ramps (dark → light) ────────────────────────────────
# Distinct ramps → qualitative palette; one ramp interpolated → sequential.
ECON = {
    "chicago":   ["#141F52", "#1F2E7A", "#2E45B8", "#475ED1", "#D6DBF5", "#EBEDFA"],  # blue
    "hongkong":  ["#169C7F", "#1DC9A4", "#36E2BD", "#D2F9F0", "#E9FCF8"],             # teal
    "newyork":   ["#F9C31F", "#FBD051", "#FCDE83", "#FEF2CD", "#FEF8E6"],             # amber
    "shanghai":  ["#4C9C16", "#62C91D", "#7BE236", "#E2F9D2", "#F0FCE9"],             # green
    "singapore": ["#F97A1F", "#FB9851", "#FCB583", "#FEE1CD", "#FEF0E6"],             # orange
    "tokyo":     ["#9C1633", "#C91D42", "#E2365B", "#F9D2DB", "#FCE9ED"],             # magenta
    "red":       ["#CC100A", "#E3120B", "#F6423C", "#FEE7E7"],                         # Econ red
    "london":    ["#0D0D0D", "#1A1A1A", "#333333", "#595959", "#666666",
                  "#B3B3B3", "#D9D9D9", "#F2F2F2", "#FFFFFF"],                          # greyscale
    "canvas":    ["#D0D3E1", "#E0E2EB", "#EFF0F5"],                                     # near-white
}

# Qualitative palettes for distinct categories.
COURSE_PAL = [GREEN, BLUE, AMBER, RED, PURPLE]                       # the five
ECON_QUAL  = [ECON["chicago"][2], ECON["hongkong"][0], ECON["newyork"][0],
              ECON["shanghai"][1], ECON["tokyo"][1], ECON["singapore"][0]]  # ~6 hues

def econ_cmap(ramp="chicago", reverse=False):
    """Continuous Economist colormap from one named ramp (perceptual, no rainbow)."""
    cols = ECON[ramp][::-1] if reverse else ECON[ramp]
    return LinearSegmentedColormap.from_list(f"econ_{ramp}", cols)

# Diverging blue–cream–red (for fold-change etc.) — on-palette, not rainbow.
econ_diverging = LinearSegmentedColormap.from_list("econ_div", [BLUE, CREAM, RED])

# Full-spectrum ramp for many-component stacks (blue→teal→green→amber→red).
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1],
     ECON["newyork"][0], ECON["red"][1]])

# ── Matplotlib rcParams — IBM Plex Mono on the warm Economist canvas ─────────
mpl.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "font.family": _MONO,
    "axes.edgecolor": LINE, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 12,
})
rng = np.random.default_rng(7)

# ── Backwards-compat aliases (existing slides rely on these KEYS) ────────────
# Values repointed to Economist equivalents; every key preserved.
COLORS = {
    "pathogenic": RED, "risk": AMBER, "benign": GREEN, "uncertain": GREY,
    "primary": GREEN, "secondary": BLUE, "tertiary": AMBER,
    "quaternary": PURPLE, "quinary": ECON["tokyo"][1],
    "text_dark": INK, "text_mid": MUTED, "text_light": GREY,
    "grid": LINE, "zero_line": LINE, "canvas": CREAM,
    "highlight_bg": ECON["hongkong"][4],
}
BRAND, BRAND_LIGHT, BRAND_BG = GREEN, ECON["hongkong"][3], ECON["hongkong"][4]
ACCENT_YLW, ACCENT_PURP, GRAY_DARK = AMBER, PURPLE, MUTED

# ── Pipeline flowchart helper (unchanged API; inherits IBM Plex Mono) ────────
def pipeline_flowchart(steps, figsize=None):
    """Render a horizontal pipeline. Accepts bare strings or (label, desc) tuples."""
    norm = [(s if isinstance(s, str) else s[0]) for s in steps]
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
```

---

# STEP 2 — Insert 42 new slides

Find this exact text (end of current slide 3 + start of current slide 4):

```
::: {.footer style="font-size: 0.7em; color: #606060;"}
Source: Matejka & Fitzmaurice (2017). [Same Stats, Different Graphs](https://www.research.autodesk.com/publications/same-stats-different-graphs/). ACM CHI 2017.
:::

<!-- slide 4 -->
# Big data in biology {.divider}
```

Insert the entire block below **between the closing `:::` and `<!-- slide 4 -->`**.
(The markers below are provisional `4 … 45`; Step 3 will renumber the whole file.)

````markdown

<!-- ═══════════════════════════════════════════════════════════════════ -->
<!-- ACT I–III · FUNDAMENTALS OF DATA VISUALIZATION                       -->
<!-- ═══════════════════════════════════════════════════════════════════ -->

<!-- slide 4 -->
# Fundamentals of Data Visualization {.divider}

[Chart design principles · Day 01]{.eyebrow}


<!-- slide 5 -->
## The Lie Factor {.smaller}

[Honest charts · baselines]{.eyebrow}

### Truncating the y-axis exaggerates differences

:::: {.columns}
::: {.column width="44%"}
Bars encode by **length**, so the axis must start at zero. Cutting the bottom makes a tiny difference look dramatic, like a thermometer starting at 35 °C where 37 °C looks like a fever.

```python
ax[0].bar(genes, expr, color=RED)
ax[0].set_ylim(43, 54)   # the lie
ax[1].bar(genes, expr, color=GREEN)
ax[1].set_ylim(0, 60)    # honest
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS"]; expr = [48, 52, 45, 50, 47]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 4.7))
ax[0].bar(genes, expr, color=RED, edgecolor=CREAM); ax[0].set_ylim(43, 54)
ax[0].set_title("MISLEADING", fontsize=11, fontweight="bold", color=RED, pad=8)
ax[0].tick_params(axis="x", rotation=45, labelsize=8)
ax[1].bar(genes, expr, color=GREEN, edgecolor=CREAM); ax[1].set_ylim(0, 60)
ax[1].set_title("HONEST", fontsize=11, fontweight="bold", color=GREEN, pad=8)
ax[1].tick_params(axis="x", rotation=45, labelsize=8)
ax[0].set_ylabel("Expression (TPM)")
fig.subplots_adjust(wspace=0.45, bottom=0.2)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Tufte (2001); Schwabish (2021).
:::


<!-- slide 6 -->
## Data-to-Ink Ratio {.smaller}

[Honest charts · simplicity]{.eyebrow}

### Remove what doesn't help, but keep what does

:::: {.columns}
::: {.column width="44%"}
Every drop of ink should encode data. Strip the gridlines, hatching, and boxed labels, keep the bars and the numbers. Like seasoning: too much overwhelms, too little is bland.

```python
# chartjunk -> clean
ax.barh(samples, vals, color=GREEN)
for i, v in enumerate(vals):
    ax.text(v + 1, i, v, va="center")
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
samples = ["Liver", "Brain", "Heart", "Kidney", "Lung"]; vals = [72, 58, 85, 63, 91]
fig, ax = plt.subplots(1, 2, figsize=(6.4, 4.7))
a = ax[0]; a.set_facecolor(ECON["canvas"][1])
a.bar(samples, vals, color=PURPLE, edgecolor=INK, linewidth=1.5, hatch="//")
a.grid(True, color=GREY); a.spines["top"].set_visible(True); a.spines["right"].set_visible(True)
a.set_title("TOO MUCH INK", fontsize=11, fontweight="bold", color=RED, pad=8)
a.tick_params(axis="x", rotation=45, labelsize=7)
a = ax[1]; a.barh(samples[::-1], vals[::-1], color=GREEN, height=0.62)
for i, v in enumerate(vals[::-1]): a.text(v + 1, i, str(v), va="center", fontsize=9, color=MUTED)
a.set_title("JUST RIGHT", fontsize=11, fontweight="bold", color=GREEN, pad=8); a.set_xlim(0, 105)
for s in ["top", "right", "bottom"]: a.spines[s].set_visible(False)
a.xaxis.set_visible(False)
fig.subplots_adjust(wspace=0.5, bottom=0.18)
plt.show()
```
:::
::::

::: {.takeaway}
Maximise the share of ink that encodes real data. The right amount lets the data shine.
:::


<!-- slide 7 -->
## The 3D Trap & Proportional Ink {.smaller}

[Honest charts · geometric accuracy]{.eyebrow}

### 3D distorts, and area must match the value

:::: {.columns}
::: {.column width="44%"}
A 3D pie is a plate seen at an angle: the near slice looks bigger. With bubbles, **area** must encode the value, not the radius, since doubling the radius quadruples the area.

```python
ax[0].pie(sizes, autopct="%1.0f%%")  # hard
ax[1].barh(labels, sizes)            # easy
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
fig, ax = plt.subplots(1, 2, figsize=(6.4, 4.7))
labels = ["Gene A", "Gene B", "Gene C"]; sizes = [50, 30, 20]
ax[0].pie(sizes, labels=labels, colors=[RED, BLUE, GREY], autopct="%1.0f%%", startangle=90, textprops={"fontsize": 8})
ax[0].set_title("PIE: HARD", fontsize=11, fontweight="bold", color=RED, pad=8)
ax[1].barh(labels[::-1], sizes[::-1], color=[GREY, BLUE, RED], height=0.55)
for i, v in enumerate(sizes[::-1]): ax[1].text(v + 1, i, f"{v}%", va="center", fontsize=9, color=MUTED)
ax[1].set_title("BAR: EASY", fontsize=11, fontweight="bold", color=GREEN, pad=8); ax[1].set_xlim(0, 62)
for s in ["top", "right", "bottom"]: ax[1].spines[s].set_visible(False)
ax[1].xaxis.set_visible(False)
fig.subplots_adjust(wspace=0.5)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Tufte (2001), proportional ink.
:::


<!-- slide 8 -->
## How We See: Perceptual Ranking {.smaller}

[Honest charts · perception]{.eyebrow}

### Some visual channels are decoded far more accurately than others

:::: {.columns}
::: {.column width="42%"}
The same four values, four ways. Position is read most accurately, then length, then area, and colour least of all.

Encode your **main message** with position or length, reserve area and colour for secondary variables.
:::
::: {.column width="58%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 5
fig, ax = plt.subplots(2, 2, figsize=(6.6, 5))
labels = ["A", "B", "C", "D"]; vals = [75, 50, 90, 30]
ax[0, 0].scatter(vals, range(4), color=GREEN, s=90, zorder=3)
ax[0, 0].set_yticks(range(4)); ax[0, 0].set_yticklabels(labels, fontsize=8); ax[0, 0].set_xlim(0, 100)
ax[0, 0].set_title("1. POSITION", fontsize=10, fontweight="bold", color=GREEN)
ax[0, 1].barh(labels, vals, color=BLUE, height=0.55); ax[0, 1].set_xlim(0, 100)
ax[0, 1].set_title("2. LENGTH", fontsize=10, fontweight="bold", color=BLUE)
for i, v in enumerate(vals):
    ax[1, 0].scatter(i, 0.5, s=v * 8, color=PURPLE, alpha=0.75, edgecolors=CREAM)
    ax[1, 0].text(i, -0.15, labels[i], ha="center", fontsize=8, color=MUTED)
ax[1, 0].set_ylim(-0.5, 1.2); ax[1, 0].set_xlim(-0.8, 3.8); ax[1, 0].axis("off")
ax[1, 0].set_title("3. AREA", fontsize=10, fontweight="bold", color=PURPLE)
cmap = econ_cmap("hongkong", reverse=True); norm = plt.Normalize(0, 100)
for i, v in enumerate(vals):
    ax[1, 1].barh(labels[i], 1, color=cmap(norm(v)), height=0.6)
    ax[1, 1].text(0.5, i, str(v), ha="center", va="center", fontsize=9, fontweight="bold", color=CREAM if v > 55 else INK)
ax[1, 1].set_xlim(0, 1); ax[1, 1].xaxis.set_visible(False)
for s in ax[1, 1].spines.values(): s.set_visible(False)
ax[1, 1].set_title("4. COLOUR", fontsize=10, fontweight="bold", color=GREEN)
fig.subplots_adjust(wspace=0.35, hspace=0.45)
plt.show()
```
:::
::::

::: {.takeaway}
Give your audience the easiest channel. Position and length for the headline, colour and area for the rest.
:::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Cleveland & McGill (1984), *JASA* 79(387).
:::


<!-- slide 9 -->
## Pre-attentive Cues & Gestalt {.smaller}

[Honest charts · perception]{.eyebrow}

### The brain groups and spots things before conscious thought

:::: {.columns}
::: {.column width="44%"}
Your eye finds the red dots before you decide to look, so one highlight colour works. The brain also auto-groups by **proximity**, so put related things close and let the clusters speak.

```python
cols = [GREY]*n
for i in highlight: cols[i] = RED
ax.scatter(x, y, c=cols)
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6
#| fig-height: 5
fig, ax = plt.subplots(2, 1, figsize=(6, 5))
n = 90; x = rng.uniform(0, 10, n); y = rng.uniform(0, 5, n)
cols = [GREY] * n
for idx in rng.choice(n, 3, replace=False): cols[idx] = RED
ax[0].scatter(x, y, c=cols, s=70, edgecolors=CREAM, lw=0.5)
ax[0].set_title("PRE-ATTENTIVE: POP-OUT", fontsize=11, fontweight="bold", color=INK, pad=6); ax[0].axis("off")
for cx, col in [(2, GREEN), (5, BLUE), (8, PURPLE)]:
    ax[1].scatter(rng.normal(cx, 0.35, 14), rng.normal(2.5, 0.35, 14), c=col, s=60, edgecolors=CREAM, lw=0.5, alpha=0.85)
ax[1].set_title("GESTALT: PROXIMITY GROUPS", fontsize=11, fontweight="bold", color=INK, pad=6)
ax[1].set_xlim(0, 10); ax[1].set_ylim(0, 5); ax[1].axis("off")
fig.subplots_adjust(hspace=0.3)
plt.show()
```
:::
::::


<!-- slide 10 -->
# Colour in Data Visualization {.divider}

[Colour theory for charts · Day 01]{.eyebrow}


<!-- slide 11 -->
## Three Palette Types {.smaller}

[Colour · palette types]{.eyebrow}

### Match the palette to your data's structure

:::: {.columns}
::: {.column width="42%"}
**Qualitative** for unordered categories, **sequential** for magnitude (one hue, light to dark), **diverging** for signed values around zero (two hues, neutral midpoint).

```python
ax0.barh(cats, cv, color=ECON_QUAL)
ax1.barh(r, sv, color=cmap(norm(sv)))
ax2.barh(g, fc, color=econ_diverging(...))
```
:::
::: {.column width="58%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 5
fig, ax = plt.subplots(3, 1, figsize=(6.6, 5))
cats = ["Liver", "Brain", "Heart", "Kidney", "Lung"]; cv = [72, 58, 85, 63, 91]
ax[0].barh(cats[::-1], cv[::-1], color=ECON_QUAL[:5][::-1], height=0.65); ax[0].set_xlim(0, 105)
ax[0].set_title("QUALITATIVE", fontsize=10, fontweight="bold", color=INK)
ax[0].tick_params(labelsize=7)
for s in ["top", "right", "bottom"]: ax[0].spines[s].set_visible(False)
ax[0].xaxis.set_visible(False)
sv = np.linspace(10, 90, 8); cmap = econ_cmap("hongkong", reverse=True); norm = plt.Normalize(0, 100)
ax[1].barh(range(8), sv, color=[cmap(norm(v)) for v in sv], height=0.7); ax[1].set_yticks([])
ax[1].set_title("SEQUENTIAL", fontsize=10, fontweight="bold", color=INK)
for s in ["top", "right", "bottom"]: ax[1].spines[s].set_visible(False)
ax[1].xaxis.set_visible(False)
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]; fc = [-2.1, -1.2, -0.3, 0.6, 1.4, 2.3]
norm = plt.Normalize(-3, 3)
ax[2].barh(genes, fc, color=[econ_diverging(norm(v)) for v in fc], height=0.65); ax[2].axvline(0, color=LINE, lw=1)
ax[2].set_title("DIVERGING", fontsize=10, fontweight="bold", color=INK); ax[2].tick_params(labelsize=7)
for s in ["top", "right"]: ax[2].spines[s].set_visible(False)
fig.subplots_adjust(hspace=0.55)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Qualitative = `ECON_QUAL` · sequential = `econ_cmap()` · diverging = `econ_diverging`.
:::


<!-- slide 12 -->
## The Rainbow Trap & Accessibility {.smaller}

[Colour · accessibility]{.eyebrow}

### Rainbow scales mislead, and about 5% of your audience is colour-blind

:::: {.columns}
::: {.column width="44%"}
Hue has no natural order, so the brain cannot turn a rainbow back into magnitude. Prefer perceptually-uniform maps, avoid red-green pairs, and use the squint test.

```python
ax[0].imshow(data, cmap="jet")      # bad
ax[1].imshow(data, cmap="viridis")  # good
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6
#| fig-height: 5
fig, ax = plt.subplots(2, 1, figsize=(6, 5))
data = rng.normal(size=(12, 12))
ax[0].imshow(data, cmap="jet", aspect="auto")
ax[0].set_title("JET (RAINBOW): MISLEADING", fontsize=11, fontweight="bold", color=RED, pad=6)
ax[0].set_xticks([]); ax[0].set_yticks([])
ax[1].imshow(data, cmap="viridis", aspect="auto")
ax[1].set_title("VIRIDIS: UNIFORM", fontsize=11, fontweight="bold", color=GREEN, pad=6)
ax[1].set_xticks([]); ax[1].set_yticks([])
fig.subplots_adjust(hspace=0.3)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Crameri, Shephard & Heron (2020), *Nat. Commun.*
:::


<!-- slide 13 -->
## Grey Is Your Best Friend {.smaller}

[Colour · strategic use]{.eyebrow}

### Highlight by de-emphasising everything else

:::: {.columns}
::: {.column width="44%"}
Grey the 95% that is context, colour the 5% that matters. Like silence in music, it makes the melody stand out.

```python
ax.scatter(fc[~sig], p[~sig], c=GREY,
           alpha=0.25)
ax.scatter(fc[sig], p[sig], c=RED)
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 4.6
fig, ax = plt.subplots(1, 2, figsize=(6.6, 4.6))
n = 700; fc = rng.normal(0, 1.5, n); p = rng.exponential(1.5, n)
noisy = [RED if f > 1 and q > 2 else BLUE if f < -1 and q > 2 else GREEN if abs(f) < 0.5 else PURPLE for f, q in zip(fc, p)]
ax[0].scatter(fc, p, c=noisy, s=10, alpha=0.6, edgecolors="none")
ax[0].set_title("ALL COLOURED", fontsize=10, fontweight="bold", color=RED, pad=6)
ax[0].set_xlabel("log2 FC", fontsize=8); ax[0].set_ylabel("-log10 p", fontsize=8)
sig = (np.abs(fc) > 1) & (p > 2)
ax[1].scatter(fc[~sig], p[~sig], c=GREY, s=10, alpha=0.25, edgecolors="none")
ax[1].scatter(fc[sig], p[sig], c=RED, s=16, alpha=0.85, edgecolors=CREAM, lw=0.3)
ax[1].set_title("GREY + ONE HIGHLIGHT", fontsize=10, fontweight="bold", color=GREEN, pad=6)
ax[1].set_xlabel("log2 FC", fontsize=8)
fig.subplots_adjust(wspace=0.3, bottom=0.16)
plt.show()
```
:::
::::

::: {.takeaway}
Colour the 5% that matters, grey the 95% that is context.
:::


<!-- slide 14 -->
# From Chart to Story {.divider}

[Narrative data visualization · Day 01]{.eyebrow}


<!-- slide 15 -->
## Editorial Thinking: Angle, Frame, Focus {.smaller}

[Storytelling · editorial]{.eyebrow}

### Before you code, answer three questions

:::: {.columns}
::: {.column width="44%"}
"Expression varies across tissues" is a topic. "Heart shows the highest BRCA1" is an **angle**, so put it in the title. Frame by showing the top 10, not all 20,000. Focus with one highlight colour.

```python
bc = [GREEN if t=="Heart" else GREY
      for t in tissues]
ax.barh(tissues, e, color=bc)
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
fig, ax = plt.subplots(2, 1, figsize=(6.4, 4.7))
tissues = ["Heart", "Liver", "Brain", "Kidney", "Lung"]; e = [91, 72, 58, 63, 85]
ax[0].barh(tissues[::-1], e[::-1], color=GREY, height=0.5)
ax[0].set_title("EXPRESSION ACROSS TISSUES", fontsize=10, fontweight="bold", color=GREY, pad=6); ax[0].set_xlim(0, 105)
for s in ["top", "right", "bottom"]: ax[0].spines[s].set_visible(False)
ax[0].xaxis.set_visible(False); ax[0].tick_params(labelsize=8)
bc = [GREEN if t == "Heart" else GREY for t in tissues[::-1]]
ax[1].barh(tissues[::-1], e[::-1], color=bc, height=0.5)
ax[1].set_title("HEART SHOWS HIGHEST BRCA1", fontsize=10, fontweight="bold", color=GREEN, pad=6); ax[1].set_xlim(0, 105)
for s in ["top", "right", "bottom"]: ax[1].spines[s].set_visible(False)
ax[1].xaxis.set_visible(False); ax[1].tick_params(labelsize=8)
fig.subplots_adjust(hspace=0.5)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Kirk (2019), *Data Visualisation*, 2nd ed.
:::


<!-- slide 16 -->
## The Story Arc {.smaller}

[Storytelling · arc]{.eyebrow}

### Every data presentation needs tension and resolution

:::: {.columns}
::: {.column width="44%"}
A single figure rarely tells the whole story. Open with context, raise a challenge (which loci?), show the action (fine-mapping), then resolve it with the causal variant. Chapters, not one slide.
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
fig, ax = plt.subplots(figsize=(6.4, 4.7))
x = np.linspace(0, 10, 200); y = 0.5 + 4 * np.exp(-0.5 * ((x - 5.5) / 2.2) ** 2)
ax.fill_between(x, 0, y, color=GREEN, alpha=0.15); ax.plot(x, y, color=GREEN, lw=3)
for xp, lab in [(1.2, "OPENING"), (3.5, "CHALLENGE"), (5.5, "CLIMAX"), (7.7, "RESOLUTION")]:
    yp = 0.5 + 4 * np.exp(-0.5 * ((xp - 5.5) / 2.2) ** 2)
    ax.plot(xp, yp, "o", color=GREEN, markersize=10, zorder=5)
    ax.annotate(lab, (xp, yp), textcoords="offset points", xytext=(0, 14), ha="center", fontsize=8, fontweight="bold", color=INK)
ax.set_xlabel("presentation flow"); ax.set_ylabel("engagement")
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("THE STORY ARC", fontsize=12, fontweight="bold", color=INK, pad=8)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 29.
:::


<!-- slide 17 -->
## Make a Figure for the Generals {.smaller}

[Storytelling · simplicity]{.eyebrow}

### If a busy reader can't get the point in ten seconds, simplify

:::: {.columns}
::: {.column width="44%"}
The generals aren't slow, they're busy. If five data dimensions are tangential to your point, strip them down to the one comparison that answers the question. *(after Claus Wilke)*
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 4.7
fig, ax = plt.subplots(1, 2, figsize=(6.6, 4.7))
n = 130; tis = rng.choice(["Brain", "Liver", "Heart", "Kidney", "Lung"], n)
x = rng.normal(50, 15, n); y = 0.3 * x + rng.normal(0, 8, n); s = rng.uniform(20, 200, n)
tc = dict(zip(["Brain", "Liver", "Heart", "Kidney", "Lung"], ECON_QUAL[:5]))
ax[0].scatter(x, y, c=[tc[t] for t in tis], s=s, alpha=0.5, edgecolors=CREAM, lw=0.3)
ax[0].set_title("TOO COMPLEX", fontsize=10, fontweight="bold", color=RED, pad=6)
ax[0].set_xlabel("feature A", fontsize=8); ax[0].set_ylabel("feature B", fontsize=8)
me = {"Heart": 85, "Lung": 78, "Liver": 72, "Kidney": 63, "Brain": 58}
it = sorted(me.items(), key=lambda kv: kv[1], reverse=True)
names = [k for k, _ in it]; vals = [v for _, v in it]
ax[1].barh(names[::-1], vals[::-1], color=[GREEN if n == "Heart" else GREY for n in names][::-1], height=0.6)
ax[1].set_title("ONE CLEAR MESSAGE", fontsize=10, fontweight="bold", color=GREEN, pad=6); ax[1].set_xlim(0, 100)
for sp in ["top", "right", "bottom"]: ax[1].spines[sp].set_visible(False)
ax[1].xaxis.set_visible(False); ax[1].tick_params(labelsize=8)
fig.subplots_adjust(wspace=0.45, bottom=0.16)
plt.show()
```
:::
::::

::: {.takeaway .alt}
If five dimensions are tangential to your point, remove them.
:::


<!-- slide 18 -->
## Build Up Towards Complexity {.smaller}

[Storytelling · progressive disclosure]{.eyebrow}

### Show a simple version first, then reveal the full picture

:::: {.columns}
::: {.column width="44%"}
Teach the reader to read **one** panel first, then show the full grid with shared scales. Like playing one bar on the piano before handing over the orchestral score.

```python
fig, ax = plt.subplots(2, 3,
    sharex=True, sharey=True)
for a, g in zip(ax.flat, genes):
    a.plot(xc, expr[g], "-o", color=GREEN)
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
cond = ["0h", "2h", "6h", "12h", "24h"]; xc = range(5)
fig, ax = plt.subplots(2, 3, figsize=(6.4, 4.7), sharex=True, sharey=True)
for a, g in zip(ax.flat, ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]):
    eg = rng.integers(5, 20) + np.cumsum(rng.integers(-2, 8, 5)); sg = rng.uniform(1, 4, 5)
    a.plot(xc, eg, "-o", color=GREEN, lw=1.8, markersize=4)
    a.fill_between(xc, eg - sg, eg + sg, color=GREEN, alpha=0.12)
    a.set_title(g, fontsize=9, fontweight="bold", color=INK)
    a.set_xticks(xc); a.set_xticklabels(cond, fontsize=6); a.tick_params(axis="y", labelsize=6)
fig.suptitle("ONE GENE, THEN THE GRID", fontsize=11, fontweight="bold", color=INK)
fig.subplots_adjust(hspace=0.4, wspace=0.2, top=0.86)
plt.show()
```
:::
::::


<!-- slide 19 -->
## Memorability vs Minimalism {.smaller}

[Storytelling · memorability]{.eyebrow}

### Simple is clear, distinctive is remembered

:::: {.columns}
::: {.column width="44%"}
Tufte says strip everything, research says distinctive figures stick. Both are right: add elements that **carry meaning**, one consistent colour per assay and the key number, never decoration.

```python
ax.barh(methods, counts, color=cols)
for i, v in enumerate(counts):
    ax.text(v+5, i, f"{v} datasets")
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
fig, ax = plt.subplots(2, 1, figsize=(6.4, 4.7))
m = ["RNA-seq", "ATAC-seq", "ChIP-seq", "WGS"]; c = [342, 187, 156, 98]
ax[0].barh(m[::-1], c[::-1], color=GREY, height=0.55)
for i, v in enumerate(c[::-1]): ax[0].text(v + 5, i, str(v), va="center", fontsize=9, color=MUTED)
ax[0].set_title("PLAIN: FORGETTABLE", fontsize=10, fontweight="bold", color=GREY, pad=6); ax[0].set_xlim(0, 400)
for s in ["top", "right", "bottom"]: ax[0].spines[s].set_visible(False)
ax[0].xaxis.set_visible(False); ax[0].tick_params(labelsize=8)
cols = [GREEN, BLUE, PURPLE, RED]
ax[1].barh(m[::-1], c[::-1], color=cols[::-1], height=0.55)
for i, (v, col) in enumerate(zip(c[::-1], cols[::-1])): ax[1].text(v + 5, i, f"{v} datasets", va="center", fontsize=9, fontweight="bold", color=col)
ax[1].set_title("SEMANTIC: MEMORABLE", fontsize=10, fontweight="bold", color=GREEN, pad=6); ax[1].set_xlim(0, 440)
for s in ["top", "right", "bottom"]: ax[1].spines[s].set_visible(False)
ax[1].xaxis.set_visible(False); ax[1].tick_params(labelsize=8)
fig.subplots_adjust(hspace=0.5)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Bateman et al. (2010), *ACM CHI*.
:::


<!-- slide 20 -->
## Don't Repeat Yourself: Vary Chart Types {.smaller}

[Storytelling · variety]{.eyebrow}

### Use a different visualization for each distinct analysis

:::: {.columns}
::: {.column width="44%"}
Two bar charts blur together. Use a **bar** for the discrete comparison and a **line** for the time course, and each panel reads as its own idea.

```python
ax[0].barh(cond, ev)        # comparison
ax[1].plot(tm, tv, "-o")    # time course
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 4.6
cond = ["Control", "Drug A", "Drug B"]; ev = [45, 68, 72]
tm = ["0h", "6h", "12h", "24h"]; tv = [45, 55, 68, 72]
fig, ax = plt.subplots(1, 2, figsize=(6.6, 4.6))
ax[0].barh(cond[::-1], ev[::-1], color=[BLUE, BLUE, GREY][::-1], height=0.55)
for i, v in enumerate(ev[::-1]): ax[0].text(v + 1, i, str(v), va="center", fontsize=9, color=MUTED)
ax[0].set_title("COMPARISON (BAR)", fontsize=10, fontweight="bold", color=INK, pad=6); ax[0].set_xlim(0, 85)
for s in ["top", "right", "bottom"]: ax[0].spines[s].set_visible(False)
ax[0].xaxis.set_visible(False); ax[0].tick_params(labelsize=8)
ax[1].plot(tm, tv, "-o", color=GREEN, lw=2.5, markersize=8)
ax[1].fill_between(range(4), [v - 4 for v in tv], [v + 4 for v in tv], color=GREEN, alpha=0.12)
ax[1].set_title("TIME COURSE (LINE)", fontsize=10, fontweight="bold", color=INK, pad=6); ax[1].tick_params(labelsize=8)
fig.subplots_adjust(wspace=0.35)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Aim for 3 to 6 figures per story. Wilke (2019), Ch. 29.
:::


<!-- slide 21 -->
## Small Multiples · Step 1: the spaghetti problem {.smaller}

[Storytelling · faceting]{.eyebrow}

### Six genes on one axis overlap into an unreadable tangle

:::: {.columns}
::: {.column width="44%"}
Plotting many series on a single axis quickly becomes spaghetti: the lines cross, the legend grows, and no one trend is followable.

```python
for g, c in zip(genes, ECON_QUAL[:6]):
    ax.plot(tp, gd[g], "-o", color=c,
            label=g)
ax.legend()
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]; pal = ECON_QUAL[:6]
tp = np.arange(5); tl = ["0h", "2h", "6h", "12h", "24h"]
gd = {g: rng.integers(10, 40) + np.cumsum(rng.integers(-3, 8, 5)) for g in genes}
fig, ax = plt.subplots(figsize=(6.4, 4.7))
for g, c in zip(genes, pal):
    ax.plot(tp, gd[g], "-o", color=c, lw=2.2, markersize=5, label=g, alpha=0.8)
ax.set_xticks(tp); ax.set_xticklabels(tl); ax.set_ylabel("Expression (TPM)")
ax.set_title("SPAGHETTI: HARD TO FOLLOW", fontsize=11, fontweight="bold", color=RED, pad=8)
ax.legend(fontsize=8, frameon=False, ncol=3, loc="upper left")
plt.show()
```
:::
::::


<!-- slide 22 -->
## Small Multiples · Step 2: the faceted fix {.smaller}

[Storytelling · faceting]{.eyebrow}

### One small panel per gene, with shared scales, scans at a glance

:::: {.columns}
::: {.column width="44%"}
Give each series its own panel and **share the axes** so the panels are comparable. The eye scans a grid far faster than it untangles overlapping lines.

```python
fig, ax = plt.subplots(2, 3,
    sharex=True, sharey=True)
for a, (g, c) in zip(ax.flat,
                     zip(genes, pal)):
    a.plot(tp, gd[g], "-o", color=c)
```
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 4.7
genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]; pal = ECON_QUAL[:6]
tp = np.arange(5); tl = ["0h", "2h", "6h", "12h", "24h"]
gd = {g: rng.integers(10, 40) + np.cumsum(rng.integers(-3, 8, 5)) for g in genes}
fig, ax = plt.subplots(2, 3, figsize=(6.6, 4.7), sharex=True, sharey=True)
for a, (g, c) in zip(ax.flat, zip(genes, pal)):
    a.plot(tp, gd[g], "-o", color=c, lw=2.2, markersize=5)
    a.fill_between(tp, gd[g] - rng.uniform(1, 3, 5), gd[g] + rng.uniform(1, 3, 5), color=c, alpha=0.13)
    a.set_title(g, fontsize=9, fontweight="bold", color=c)
    a.set_xticks(tp); a.set_xticklabels(tl, fontsize=6); a.tick_params(axis="y", labelsize=6)
fig.suptitle("SMALL MULTIPLES: EASY TO SCAN", fontsize=11, fontweight="bold", color=INK)
fig.subplots_adjust(hspace=0.4, wspace=0.2, top=0.86)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Tufte (1983); `facet_wrap()` / `sns.FacetGrid`.
:::


<!-- ═══════════════════════════════════════════════════════════════════ -->
<!-- SHOWING DISTRIBUTIONS                                                -->
<!-- ═══════════════════════════════════════════════════════════════════ -->

<!-- slide 23 -->
# Showing Distributions {.divider}

[Boxplots, violins & ridgelines · Day 01]{.eyebrow}


<!-- slide 24 -->
## When & Why a Boxplot {.smaller}

[Distributions · when to use]{.eyebrow}

### A boxplot summarises spread, pick the chart that fits your question

:::: {.columns}
::: {.column width="44%"}
Use a boxplot to compare the **distribution** of a continuous value across a few groups, its centre, spread, and outliers, without plotting every point.

**Spread is not precision.** Standard deviation describes how the data scatter; standard error describes how precise the mean estimate is. A boxplot answers the first, error bars the second.
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 5
r = np.random.default_rng(1)
groups = ["WT", "Mut A", "Mut B"]
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 5))
bp = ax.boxplot(data, widths=0.55, patch_artist=True, labels=groups)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
for fl in bp["fliers"]: fl.set(marker="o", markerfacecolor=CREAM, markeredgecolor=RED, markersize=5)
ax.set_ylabel("Expression (TPM)")
ax.set_title("DISTRIBUTION ACROSS THREE GENOTYPES", fontsize=11, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::

::: {.takeaway}
SD vs SE: the spread of the data vs the precision of the estimate. Same numbers, different questions, different charts.
:::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 9.
:::


<!-- slide 25 -->
## Building a Boxplot · Step 1: the canvas {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Set up the figure, labels, and scale before any data

:::: {.columns}
::: {.column width="46%"}
Start with an empty, labelled canvas: the axes, the group positions, the y-scale. Decide the frame first, then fill it.

```python
groups = ["WT", "Mut A", "Mut B"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)")
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5)
ax.set_ylim(30, 85)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)")
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
ax.set_title("STEP 1: THE CANVAS", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide 26 -->
## Building a Boxplot · Step 2: the raw points {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Always look at the data first, with a little horizontal jitter

:::: {.columns}
::: {.column width="46%"}
Plot every observation, jittering the x-position so points don't stack on one line. This shows the sample size and shape that a summary will later hide.

```python
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70),
        r.normal(62, 10, 70),
        r.normal(58, 4, 70)]
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d,
               color=GREEN, s=18, alpha=0.5,
               edgecolors="none")
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.5, edgecolors="none")
ax.set_title("STEP 2: RAW POINTS", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide 27 -->
## Building a Boxplot · Step 3: add the box {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Overlay the five-number summary on top of the points

:::: {.columns}
::: {.column width="46%"}
The box draws Q1 to Q3, the median line, and whiskers to the most extreme points within 1.5× IQR. Matplotlib computes all of it.

```python
bp = ax.boxplot(
    data,
    positions=[1, 2, 3],
    widths=0.5,
    patch_artist=True,   # so we can colour it
)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.35, edgecolors="none")
ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True)
ax.set_title("STEP 3: ADD THE BOX (DEFAULT)", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 28 -->
## Building a Boxplot · Step 4: style on-palette {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Economist green box, ink median, fade the points behind

:::: {.columns}
::: {.column width="46%"}
Style every element: a soft teal fill, a green edge, a bold ink median, green whiskers. Drop the points' alpha so the box reads on top.

```python
for p in bp["boxes"]:
    p.set_facecolor(ECON["hongkong"][3])
    p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]:
    m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]:
    w.set_color(GREEN)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.3, edgecolors="none")
bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
ax.set_title("STEP 4: STYLED ON-PALETTE", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 29 -->
## Building a Boxplot · Step 5: the message {.smaller}

[Distributions · boxplot build]{.eyebrow}

### Hide duplicate outliers, add a title that states the finding

:::: {.columns}
::: {.column width="46%"}
The points already show every value, so turn off the default flier markers. Finish with a title that says what to take away.

```python
bp = ax.boxplot(data, showfliers=False, ...)
ax.set_title(
    "MUT A SHOWS THE WIDEST SPREAD")
```

The whole recipe: **canvas → points → box → style → message.**
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(1)
data = [r.normal(50, 6, 70), r.normal(62, 10, 70), r.normal(58, 4, 70)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("Expression (TPM)"); ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups)
ax.set_xlim(0.5, 3.5); ax.set_ylim(30, 85)
rj = np.random.default_rng(2)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.3, edgecolors="none")
bp = ax.boxplot(data, positions=[1, 2, 3], widths=0.5, patch_artist=True, showfliers=False)
for p in bp["boxes"]: p.set_facecolor(ECON["hongkong"][3]); p.set_edgecolor(GREEN); p.set_alpha(0.75)
for m in bp["medians"]: m.set_color(INK); m.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
ax.set_title("MUT A SHOWS THE WIDEST SPREAD", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide 30 -->
## When & Why a Violin {.smaller}

[Distributions · when to use]{.eyebrow}

### Reach for a violin when the shape matters, not just the summary

:::: {.columns}
::: {.column width="44%"}
A boxplot hides shape: two very different distributions can share one five-number summary. A violin draws a **mirrored density**, so a second hump or a skew is visible at a glance.

Use it when the data might be **bimodal** or strongly skewed.
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 5
r = np.random.default_rng(3)
bimodal = np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)])
fig, ax = plt.subplots(figsize=(6.4, 5))
vp = ax.violinplot([bimodal], positions=[1], widths=0.7, showextrema=False)
for b in vp["bodies"]: b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.85)
bx = ax.boxplot([bimodal], positions=[1], widths=0.12, patch_artist=True, showfliers=False)
for p in bx["boxes"]: p.set_facecolor(INK)
for m in bx["medians"]: m.set_color(CREAM)
ax.set_xticks([1]); ax.set_xticklabels(["one sample"]); ax.set_ylabel("Expression (TPM)")
ax.set_title("THE BOX MISSES THE TWO PEAKS", fontsize=11, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 7.
:::


<!-- slide 31 -->
## Building a Violin · Step 1: the canvas {.smaller}

[Distributions · violin build]{.eyebrow}

### Same canvas as the boxplot, with one bimodal group

:::: {.columns}
::: {.column width="46%"}
The recipe starts identically: an empty, labelled frame. One group is deliberately **bimodal** so the violin has something a box would hide.

```python
r = np.random.default_rng(3)
groups = ["WT", "Mut A", "Mut B"]
data = [np.concatenate([r.normal(45,5,45),
                        r.normal(62,5,35)]),
        r.normal(62, 10, 80),
        r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylim(25, 85)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
ax.set_title("STEP 1: THE CANVAS", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide 32 -->
## Building a Violin · Step 2: the raw points {.smaller}

[Distributions · violin build]{.eyebrow}

### The WT group already shows two clouds, not one

:::: {.columns}
::: {.column width="46%"}
Jittered points hint at the structure: WT sits in two clusters. The violin will make that explicit.

```python
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d,
               color=GREEN, s=16, alpha=0.5,
               edgecolors="none")
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]), r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=16, alpha=0.5, edgecolors="none")
ax.set_title("STEP 2: RAW POINTS", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide 33 -->
## Building a Violin · Step 3: add the density {.smaller}

[Distributions · violin build]{.eyebrow}

### violinplot draws a kernel density and mirrors it about each axis

:::: {.columns}
::: {.column width="46%"}
The body width at any height is the point density there. The WT violin now shows two bulges, the bimodality a box would flatten.

```python
vp = ax.violinplot(
    data,
    positions=[1, 2, 3],
    showextrema=False,
)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]), r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=14, alpha=0.3, edgecolors="none")
ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
ax.set_title("STEP 3: ADD THE DENSITY (DEFAULT)", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 34 -->
## Building a Violin · Step 4: style on-palette {.smaller}

[Distributions · violin build]{.eyebrow}

### Teal body, green edge, fade the points behind

:::: {.columns}
::: {.column width="46%"}
Loop over the violin bodies and colour them on-brand, then drop the points' alpha so the density reads on top.

```python
vp = ax.violinplot(data, positions=[1,2,3],
                   showextrema=False)
for b in vp["bodies"]:
    b.set_facecolor(ECON["hongkong"][3])
    b.set_edgecolor(GREEN)
    b.set_alpha(0.75)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]), r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=14, alpha=0.25, edgecolors="none")
vp = ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
for b in vp["bodies"]: b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.75); b.set_linewidth(1.4)
ax.set_title("STEP 4: STYLED ON-PALETTE", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 35 -->
## Building a Violin · Step 5: the message {.smaller}

[Distributions · violin build]{.eyebrow}

### Add a slim inner boxplot, then a title that states the finding

:::: {.columns}
::: {.column width="46%"}
A thin boxplot inside each violin gives the summary and the shape together. Finish with the takeaway in the title.

```python
for i, d in enumerate(data, start=1):
    bx = ax.boxplot(d, positions=[i],
        widths=0.1, patch_artist=True,
        showfliers=False)
    bx["boxes"][0].set_facecolor(INK)
ax.set_title("WT IS BIMODAL")
```

Same recipe: **canvas → points → density → style → message.**
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
groups = ["WT", "Mut A", "Mut B"]
r = np.random.default_rng(3)
data = [np.concatenate([r.normal(45, 5, 45), r.normal(62, 5, 35)]), r.normal(62, 10, 80), r.normal(58, 4, 80)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks([1, 2, 3]); ax.set_xticklabels(groups); ax.set_xlim(0.5, 3.5)
ax.set_ylim(25, 85); ax.set_ylabel("Expression (TPM)")
vp = ax.violinplot(data, positions=[1, 2, 3], showextrema=False)
for b in vp["bodies"]: b.set_facecolor(ECON["hongkong"][3]); b.set_edgecolor(GREEN); b.set_alpha(0.6); b.set_linewidth(1.4)
for i, d in enumerate(data, start=1):
    bx = ax.boxplot(d, positions=[i], widths=0.1, patch_artist=True, showfliers=False)
    for p in bx["boxes"]: p.set_facecolor(INK)
    for m in bx["medians"]: m.set_color(CREAM); m.set_linewidth(1.4)
    for w in bx["whiskers"] + bx["caps"]: w.set_color(INK)
ax.set_title("WT IS BIMODAL", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::

::: {.takeaway}
Box vs violin: the box gives the summary, the violin reveals the shape. Show the violin when bimodality or skew is the story.
:::


<!-- slide 36 -->
## Distributions Over Time: Ridgelines {.smaller}

[Distributions · ridgeline]{.eyebrow}

### Stack many distributions into one panel, two groups in two colours

:::: {.columns}
::: {.column width="42%"}
A stress gene across the year in two genotypes. The tolerant line stays low, the sensitive line spikes in summer. One row per month with a slight overlap packs a dozen distributions into one panel, and blue vs Economist red keeps the groups colour-blind safe.
:::
::: {.column width="58%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.6
#| fig-height: 5.2
from scipy.stats import gaussian_kde
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
TOLERANT, SENSITIVE = BLUE, ECON["red"][1]
fig, ax = plt.subplots(figsize=(6.6, 5.2))
xgrid = np.linspace(0, 100, 300); overlap = 1.9
season = np.array([0, 0, 1, 2, 4, 7, 9, 8, 5, 2, 1, 0])
for i, m in enumerate(months[::-1]):
    mi = len(months) - 1 - i
    tol = rng.normal(28 + season[mi] * 0.8, 6, 200); sen = rng.normal(30 + season[mi] * 6.5, 9, 200)
    for d, col in [(tol, TOLERANT), (sen, SENSITIVE)]:
        k = gaussian_kde(d)(xgrid); k = k / k.max() * overlap
        ax.fill_between(xgrid, i + k, i, color=col, alpha=0.5, lw=1, edgecolor=CREAM, zorder=i)
ax.set_yticks(range(len(months))); ax.set_yticklabels(months[::-1], fontsize=8)
ax.set_xlabel("Expression (TPM)")
ax.scatter([], [], color=TOLERANT, label="tolerant"); ax.scatter([], [], color=SENSITIVE, label="sensitive")
ax.legend(loc="upper right", frameon=False, fontsize=9)
ax.set_title("STRESS-GENE EXPRESSION ACROSS THE YEAR", fontsize=10, fontweight="bold", color=INK, pad=8)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Ridgeline (joyplot): Wilke (2019), Ch. 9.4.
:::


<!-- ═══════════════════════════════════════════════════════════════════ -->
<!-- SHOWING PROPORTIONS                                                  -->
<!-- ═══════════════════════════════════════════════════════════════════ -->

<!-- slide 37 -->
# Showing Proportions {.divider}

[Parts of a whole · Day 01]{.eyebrow}


<!-- slide 38 -->
## Proportions: Bars, Not Pies {.smaller}

[Proportions · why bars]{.eyebrow}

### The same parts-of-a-whole, read far more accurately

:::: {.columns}
::: {.column width="42%"}
Humans judge **length on a common scale** far better than **angle or area**. So for parts-of-a-whole, reach for a stacked bar, not a pie: every segment is read along one axis.
:::
::: {.column width="58%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.8
#| fig-height: 4.8
labels = ["Taxon A", "Taxon B", "Taxon C", "Taxon D"]; vals = [243, 214, 100, 39]
cols = [GREY, RED, AMBER, BLUE]
fig, ax = plt.subplots(2, 1, figsize=(6.8, 4.8))
ax[0].pie(vals, labels=labels, colors=cols, autopct="%1.0f%%", startangle=90, textprops={"fontsize": 8})
ax[0].set_title("PIE: NO-GO", fontsize=10, fontweight="bold", color=RED)
tot = sum(vals); left = 0
for v, l, c in zip(vals, labels, cols):
    ax[1].barh(0, v, left=left, color=c, edgecolor=CREAM)
    ax[1].text(left + v / 2, 0, f"{v}", ha="center", va="center", fontsize=9,
               color=CREAM if c in (GREY, RED, BLUE) else INK, fontweight="bold")
    left += v
ax[1].set_xlim(0, tot); ax[1].set_ylim(-0.5, 0.5); ax[1].set_yticks([]); ax[1].set_xlabel("count")
ax[1].set_title("STACKED BAR: YES", fontsize=10, fontweight="bold", color=GREEN)
for s in ["top", "right", "left"]: ax[1].spines[s].set_visible(False)
fig.subplots_adjust(hspace=0.55)
plt.show()
```
:::
::::

::: {.takeaway}
Length on a common scale beats angle or area, so for proportions reach for bars, not pies.
:::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Wilke (2019), Ch. 10; Cleveland & McGill (1984).
:::


<!-- slide 39 -->
## Building a Stacked Bar · Step 1: the canvas {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Timepoints on x, abundance on y, a distinct colour per taxon

:::: {.columns}
::: {.column width="46%"}
Track six taxa across six timepoints. Choose **distinct Economist hues**, one per taxon, with grey reserved for the catch-all "Other".

```python
taxa = ["Firmicutes","Bacteroidetes",
        "Proteobacteria","Actinobacteria",
        "Verrucomicrobia","Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0],
        ECON["hongkong"][0], ECON["tokyo"][1],
        ECON["newyork"][0], GREY]
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks(range(len(tps))); ax.set_xticklabels(tps)
ax.set_ylabel("Read count"); ax.set_xlabel("Timepoint")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cols]
ax.legend(handles, taxa, loc="upper right", fontsize=7, frameon=False)
ax.set_title("STEP 1: CANVAS + PALETTE", fontsize=12, fontweight="bold", color=MUTED, pad=10)
plt.show()
```
:::
::::


<!-- slide 40 -->
## Building a Stacked Bar · Step 2: stack the counts {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Stack each taxon by carrying a running bottom

:::: {.columns}
::: {.column width="46%"}
Draw each taxon as a bar, then add its height to a running `bottom` so the next taxon sits on top. Raw counts let sample totals differ.

```python
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, counts[i], bottom=bottom,
           color=c, label=t, edgecolor=CREAM)
    bottom += counts[i]
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
fig, ax = plt.subplots(figsize=(6.4, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, counts[i], bottom=bottom, color=c, label=t, edgecolor=CREAM, width=0.8); bottom += counts[i]
ax.set_ylabel("Read count"); ax.set_xlabel("Timepoint")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("STEP 2: ABSOLUTE COUNTS", fontsize=12, fontweight="bold", color=INK, pad=10)
plt.show()
```
:::
::::


<!-- slide 41 -->
## Building a Stacked Bar · Step 3: normalise to 100% {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Divide each column by its total so composition is comparable

:::: {.columns}
::: {.column width="46%"}
Absolute counts confound depth with composition. Divide every column by its sum so each bar reaches 100%, and only the **proportions** vary.

```python
comp = counts / counts.sum(axis=0,
                           keepdims=True) * 100
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom,
           color=c, edgecolor=CREAM)
    bottom += comp[i]
ax.set_ylim(0, 100)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
comp = counts / counts.sum(axis=0, keepdims=True) * 100
fig, ax = plt.subplots(figsize=(6.4, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom, color=c, edgecolor=CREAM, width=0.8); bottom += comp[i]
ax.set_ylim(0, 100); ax.set_ylabel("Relative abundance (%)"); ax.set_xlabel("Timepoint")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("STEP 3: NORMALISED TO 100%", fontsize=12, fontweight="bold", color=GREEN, pad=10)
plt.show()
```
:::
::::


<!-- slide 42 -->
## Building a Stacked Bar · Step 4: legend & message {.smaller}

[Proportions · stacked-bar build]{.eyebrow}

### Move the legend outside, title the trend

:::: {.columns}
::: {.column width="44%"}
Put the legend to the right so it never covers a bar, and write the finding into the title.

```python
ax.legend(loc="upper left",
          bbox_to_anchor=(1.01, 1.0),
          frameon=False)
ax.set_title("MICROBIOME SHIFTS OVER TIME")
```

Recipe: **canvas → stack → normalise → label.**
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.8
#| fig-height: 4.7
taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria", "Actinobacteria", "Verrucomicrobia", "Other"]
cols = [ECON["chicago"][2], ECON["singapore"][0], ECON["hongkong"][0], ECON["tokyo"][1], ECON["newyork"][0], GREY]
tps = ["D0", "D3", "D7", "D14", "D21", "D28"]
rr = np.random.default_rng(5)
raw = rr.dirichlet(np.array([6, 5, 2, 2, 1, 1.0]), size=len(tps))
counts = (raw.T * rr.integers(8000, 12000, len(tps)))
comp = counts / counts.sum(axis=0, keepdims=True) * 100
fig, ax = plt.subplots(figsize=(6.8, 4.7))
bottom = np.zeros(len(tps))
for i, (t, c) in enumerate(zip(taxa, cols)):
    ax.bar(tps, comp[i], bottom=bottom, color=c, label=t, edgecolor=CREAM, width=0.8); bottom += comp[i]
ax.set_ylim(0, 100); ax.set_ylabel("Relative abundance (%)"); ax.set_xlabel("Timepoint")
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.set_title("MICROBIOME COMPOSITION OVER TIME", fontsize=10, fontweight="bold", color=INK, pad=10)
fig.subplots_adjust(right=0.72)
plt.show()
```
:::
::::

::: {.footer style="font-size: 0.58em; color: #808080;"}
Cap categories (top taxa + "Other") so the palette stays distinct.
:::


<!-- slide 43 -->
## Building a Stacked Area · Step 1: a few lineages {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Start with the handful of dominant lineages as stacked bands

:::: {.columns}
::: {.column width="46%"}
A stacked area is a stacked bar with a continuous x-axis. Begin with the top few lineages: each band is one lineage, and frequencies sum to 1 each day.

```python
econ_spectrum  # blue→teal→green→amber→red
top = freq[:6]
cols = [econ_spectrum(i/5) for i in range(6)]
ax.stackplot(days, top, colors=cols)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
top = freq[:6]
cols = [econ_spectrum(i / 5) for i in range(6)]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.stackplot(days, top, colors=cols, edgecolor=CREAM, lw=0.4)
ax.set_xlim(0, n_t - 1); ax.set_xlabel("Time (days)"); ax.set_ylabel("Frequency")
ax.set_title("STEP 1: TOP 6 LINEAGES", fontsize=12, fontweight="bold", color=INK, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::


<!-- slide 44 -->
## Building a Stacked Area · Step 2: all of them, full spectrum {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Colour every band by its vertical position so the whole ramp shows

:::: {.columns}
::: {.column width="46%"}
Add all 150 lineages. The trick: colour each band by **where it sits in the stack** (its cumulative height), not its rank. That spreads the full blue to red ramp across the whole height, so every band gets its own colour.

```python
mean_ab = freq.mean(axis=1)
cum = np.cumsum(mean_ab)
centre = (cum - mean_ab/2) / cum[-1]
colors = [econ_spectrum(c) for c in centre]
ax.stackplot(days, freq, colors=colors)
```
:::
::: {.column width="54%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.4
#| fig-height: 4.7
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
mean_ab = freq.mean(axis=1); cum = np.cumsum(mean_ab)
centre = (cum - mean_ab / 2) / cum[-1]
colors = [econ_spectrum(c) for c in centre]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.stackplot(days, freq, colors=colors, edgecolor="none")
ax.set_xlim(0, n_t - 1); ax.set_ylim(0, 1); ax.set_xlabel("Time (days)"); ax.set_ylabel("Frequency")
ax.set_title("STEP 2: ALL 150, FULL SPECTRUM", fontsize=12, fontweight="bold", color=GREEN, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::


<!-- slide 45 -->
## Building a Stacked Area · Step 3: the message {.smaller}

[Proportions · stacked-area build]{.eyebrow}

### Label the axes and title the dynamic

:::: {.columns}
::: {.column width="44%"}
The finished plot reads as a smooth blue-to-red gradient where each lineage keeps its own band, and you can follow any band as it widens or fades over time.

```python
ax.set_xlabel("Time (days)")
ax.set_ylabel("Barcode frequency")
ax.set_title(
    "A FEW LINEAGES SWEEP TO FIXATION")
```

Recipe: **few bands → all by height → label.**
:::
::: {.column width="56%"}
```{python}
#| echo: false
#| out-width: "100%"
#| fig-width: 6.8
#| fig-height: 4.8
econ_spectrum = LinearSegmentedColormap.from_list("econ_spectrum",
    [ECON["chicago"][2], ECON["hongkong"][0], ECON["shanghai"][1], ECON["newyork"][0], ECON["red"][1]])
n_lin, n_t = 150, 21
days = np.arange(n_t)
traj = np.abs(rng.normal(1, 0.07, (n_lin, n_t)).cumprod(axis=1))
traj *= rng.dirichlet(np.ones(n_lin) * 0.5)[:, None] * 50
freq = traj / traj.sum(axis=0, keepdims=True)
freq = freq[np.argsort(freq.sum(axis=1))[::-1]]
mean_ab = freq.mean(axis=1); cum = np.cumsum(mean_ab)
centre = (cum - mean_ab / 2) / cum[-1]
colors = [econ_spectrum(c) for c in centre]
fig, ax = plt.subplots(figsize=(6.8, 4.8))
ax.stackplot(days, freq, colors=colors, edgecolor="none")
ax.set_xlim(0, n_t - 1); ax.set_ylim(0, 1)
ax.set_xlabel("Time (days)"); ax.set_ylabel("Barcode frequency")
ax.set_title("BARCODE LINEAGE FREQUENCIES, REPLICATE 2", fontsize=10, fontweight="bold", color=INK, pad=10)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.show()
```
:::
::::

::: {.takeaway}
Many components, one continuous ramp keyed to vertical position, so every band is its own colour and the eye can still track a lineage over time.
:::
````

---

# STEP 3 — Renumber every marker

This is the explicit "clean up the markers" renumber that `CLAUDE.md` allows as its
own action. After inserting Step 2, walk **all** `<!-- slide X -->` comments in
document order and assign **flat consecutive integers** `1, 2, 3, …`. This collapses
the existing decimal sub-numbers (e.g. `14.1`, `14.2` → consecutive integers) into a
clean sequence. One marker per slide; never reuse a number.

**Algorithm:** scan top-to-bottom; maintain a counter starting at 1; for each
`<!-- slide ... -->` line, replace its number with the counter, then increment.
Match the regex `<!-- slide [0-9]+(\.[0-9]+)? -->` and rewrite to `<!-- slide N -->`.

> **This renumbers the EXISTING slides too — not only the new ones.** The former
> slide 4 ("Big data in biology") becomes 46, the former last marker (74) becomes
> 130, and every existing decimal (14.1, 33.1, 43.2, 69.2, …) collapses into a
> plain integer. That is the whole point of the renumber: after inserting 29
> slides between 3 and 4, every downstream number must shift so the sequence stays
> gapless. Do this as a **separate commit** from Steps 1–2 (CLAUDE.md rule 8:
> "renumbering is its own commit").

**Anchors to verify after renumbering:**

| Slide | Heading |
|-------|---------|
| 1 | Why do we need data visualisations? *(divider)* |
| 2 | Anscombe's Quartet |
| 3 | The Datasaurus Dozen |
| 4 | Fundamentals of Data Visualization *(new divider)* |
| 10 | Colour in Data Visualization *(new divider)* |
| 14 | From Chart to Story *(new divider)* |
| 23 | Showing Distributions *(new divider)* |
| 37 | Showing Proportions *(new divider)* |
| 45 | Building a Stacked Area · Step 3 *(last new slide)* |
| 46 | Big data in biology *(former slide 4)* |
| 130 | the original final slide |

**Final count:** the file had **88** physical slide markers; **+42** new ⇒ **130**.
Confirm the last marker is `<!-- slide 130 -->`.

---

# Verification checklist

- [ ] `CLAUDE.md` rules 1 and 2 replaced; the file still parses as Markdown and no
      other rule text changed.
- [ ] `setup` chunk: `GREEN BLUE AMBER RED PURPLE GREY CREAM INK LINE COLORS
      COURSE_PAL BRAND BRAND_LIGHT BRAND_BG ACCENT_YLW ACCENT_PURP GRAY_DARK rng
      pipeline_flowchart ECON ECON_QUAL econ_cmap econ_diverging` all defined; no
      `COLORS` key removed.
- [ ] `../fonts/IBM_Plex_Mono/` resolves; figures render in IBM Plex Mono (check a
      tick label). If the folder isn't found, the fallback keeps rendering.
- [ ] New slides use only palette constants — grep the inserted block for stray
      hex codes; the only literals should be inside the `setup` chunk and `ECON`.
- [ ] Every new figure slide has a working **Plot** / **Code** tabset.
- [ ] `scipy` is importable (used by the violin-anatomy and ridgeline slides:
      `from scipy.stats import gaussian_kde`). It ships with the course env; if not,
      add `scipy` to the environment.
- [ ] Slide 3 = Datasaurus, 4 = Fundamentals divider, 23 = Distributions divider,
      37 = Proportions divider, 45 = last new slide, 46 = Big data in biology, last = 130.
- [ ] `quarto render slides/day1_python_gendataviz26.qmd` completes with no errors;
      spot-check a few **existing** plot slides to confirm the recolour/refont
      didn't break them.
- [ ] No existing slide text, code, data, or topic order changed (this was an
      insert + restyle, not a rewrite).

## Notes / decisions baked in
- Palette = Economist (five story colours + named base ramps). Green-teal carries
  the story; red/purple highlight one thing; grey de-emphasises.
- Font = IBM Plex Mono for all matplotlib figures (Option A: patched globally).
- Unified slide pattern (the "Anscombe" pattern) across all new slides.
- `::: {.takeaway}` used only on punchline slides.
- Code/Plot tabset on every figure-focused slide.
- Pie shown only as an explicit anti-pattern (slides 7 and 30); never as a real
  recommendation.
