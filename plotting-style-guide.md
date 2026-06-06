# Plotting Style Guide — Detailed Reference

Editorial data journalism aesthetic. Think: **The Economist** charts meet **Nature Reviews Genetics**.
Every plot should look like it belongs in a polished course slide deck — clean, confident, no chartjunk.

## Font: Geist Sans

Primary typeface: **Geist** by Vercel (geometric, modern, excellent tabular numbers).
Install: `npm pack geist && tar xzf geist-*.tgz` → copy TTFs to system fonts dir.
Fallback chain: Geist → IBM Plex Sans → Helvetica Neue → Arial.

## Background: Warm Canvas

Never use pure white. Canvas color: `#FAF9F7` — subtle warm off-white.
Always pass `facecolor=COLORS["canvas"]` to `fig.savefig()`.

## Base Theme Setup

Every plotting script must begin with:

```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Geist", "IBM Plex Sans", "Helvetica Neue", "Arial"],
    "font.size": 11, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10,
    "legend.fontsize": 10, "figure.titlesize": 15, "figure.titleweight": "bold",
    "figure.facecolor": "#FAF9F7", "axes.facecolor": "#FAF9F7",
    "axes.edgecolor": "#DDDDDD", "axes.linewidth": 0.6,
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.color": "#666666", "ytick.color": "#666666",
    "figure.dpi": 150, "savefig.dpi": 300,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.3,
})
```

## Color Palette

```python
COLORS = {
    "pathogenic": "#C23B22", "risk": "#E6A817", "benign": "#5A8F29",
    "uncertain": "#888888",
    "primary": "#C23B22", "secondary": "#2B6CB0", "tertiary": "#E6A817",
    "quaternary": "#5A8F29", "quinary": "#7B5EA7",
    "text_dark": "#1A1A1A", "text_mid": "#555555", "text_light": "#888888",
    "grid": "#E8E8E8", "highlight_bg": "#FFF5F5",
    "zero_line": "#CCCCCC", "canvas": "#FAF9F7",
}
```

Categorical cycling: primary → secondary → tertiary → quaternary → quinary, then 60% saturation variants.
Sequential: `"Reds"` or white → primary. Diverging: blue–white–red. Never rainbow/jet.

## Title & Annotation Rules

1. Main title: ALL CAPS, `fontweight="bold"`, `fontsize=13`
2. Axis directional labels: `← left` / `right →`, `text_light`, `fontsize=9`
3. Value annotations: at bar ends / next to points, `text_mid`, `fontsize=9`
4. Bottom footnote: 1–2 lines interpretation, `text_light`, `fontsize=8.5`, italic
5. Titles must add context — never restate axis labels

## Layout Rules

- Prefer horizontal bar charts. Always include zero reference line for diverging metrics.
- Default sizes: `(10,6)` standard, `(12,5)` wide, `(8,8)` square
- Multi-panel: `gridspec` with `hspace=0.4, wspace=0.3`
- Classification sub-labels in semantic color below main label, `fontsize=9`

## Plot-Type-Specific Guidance

### Manhattan: alternating `secondary`/`text_light` chromosomes, dashed significance line in `primary`
### Volcano: x=log2FC, y=-log10(p), four-color significance scheme (NS/FC/p/both)
### Heatmap: blue–white–red diverging, slim colorbar right, `text_light` dendrograms
### QQ: `secondary` points, dashed diagonal, gray confidence band, lambda annotation
### Bar (LLD): horizontal, semantic colors, values at bar ends, classification sub-labels
### PCA: categorical palette, `s=40 alpha=0.75 edgecolors="white"`, variance % in axis labels
### Admixture: stacked bars width=1, white separator lines between populations, ancestry legend

## Export

- PNG at 300 DPI + SVG for every figure
- `facecolor=COLORS["canvas"]` in `fig.savefig()` — mandatory
- Filename: `{plot_type}_{dataset}_{description}.png`

## What NOT To Do

- No gridlines (unless scatter + genuinely helpful, then `grid` color alpha=0.4)
- No legend frames (`frameon=False`), no default matplotlib blue, no rainbow/jet
- No 3D plots, no excessive ticks (`MaxNLocator(nbins=5)`), no x-labels beyond 45°
