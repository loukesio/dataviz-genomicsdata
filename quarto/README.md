# Genomics Viz with Python — Quarto reveal.js theme

A warm **"Carbon-cream"** data-viz theme for teaching genomics visualization in Python.
Cream canvas · harmonized green + purple accents · monospace eyebrow labels ·
Space Grotesk titles · Asap body.

```
quarto/
├── style.scss     ← the reveal.js theme (all colors, type, components)
├── slides.qmd     ← runnable template with every slide layout
└── README.md      ← this file
```

## Quick start

```bash
quarto preview slides.qmd      # live reload while you write
quarto render  slides.qmd      # build slides.html
```

Requires Quarto ≥ 1.4 and a Python env with `numpy matplotlib seaborn`
(the template renders real figures from synthetic data).

## The system at a glance

| Role            | Font                | Notes                                   |
|-----------------|---------------------|-----------------------------------------|
| Eyebrow / code  | **JetBrains Mono**  | uppercase, letter-spaced labels         |
| Titles          | **Space Grotesk** 600 | geometric grotesk, tight tracking     |
| Body            | **Asap**            | echoes the `Asap Condensed` ggplot font |

| Token            | Hex       | Use                                  |
|------------------|-----------|--------------------------------------|
| `--gv-cream`     | `#f6f4ee` | slide background                     |
| `--gv-ink`       | `#211f1a` | body text                            |
| `--gv-green`     | `#208462` | **primary** — links, eyebrows, "down"|
| `--gv-purple`    | `#7754bf` | secondary highlight / "alt"          |
| `--gv-red`       | `#c0473a` | emphasis / "up-regulated"            |
| `--gv-blue`      | `#2b6fb0` | kwargs, tertiary                     |
| `--gv-amber`     | `#c98a1a` | quaternary                           |
| `--base-a/c/g/t` | —         | DNA-base chip colors (A·C·G·T)       |

Harmony rule: **green carries the story, everything else stays quiet.** Reach
for red/purple only to highlight one thing at a time.

## Authoring cheatsheet

**Eyebrow + title** (eyebrow sits above the slide title):
```markdown
## 5 · Volcano {.smaller}

[Differential expression]{.eyebrow}

### Volcano plots in three artists
```

**Inline highlights:**
```markdown
[up-regulated]{.up}   [down-regulated]{.down}   [interactive]{.alt}
`inline code`         ==highlighter==           [A]{.b-a} [T]{.b-t}
```

**Section divider** (dark slide) — add `{.divider}` to a level-1 heading;
use `*word*` for the mint accent:
```markdown
# Day 01 — Foundations & *differential expression* {.divider}
```

**Key-point callout:**
```markdown
::: {.keybox}
[What the switch buys you]{.keylabel}
CE first, FNS later …
:::
```

**Code ↔ Plot tabs** (and step-by-step build) — native Quarto tabset, restyled:
```markdown
::: {.panel-tabset}
### Code · matplotlib
```{python}
...
```
### Plot
```{python}
#| echo: false
...
```
:::
```

**Agenda** — wrap columns in `.agenda` to get the numbered, ruled list:
```markdown
::: {.columns .agenda}
::: {.column width="33%"}
**Monday · Foundations**
1. …
:::
:::
```

**App / browser frame:**
```markdown
::: {.browser}
::: {.bbar} localhost:8050 / **app** · running :::
… figure …
:::
```

## Matching figures to the theme

The `setup` chunk in `slides.qmd` sets matplotlib `rcParams` (cream facecolor,
muted axes, no top/right spines) and defines the palette constants
`GREEN PURPLE RED BLUE GREY`. Reuse them so every figure stays on-system:

```python
ax.scatter(x, y, c=np.where(up, RED, np.where(down, GREEN, GREY)))
```

For sequential/diverging colormaps prefer perceptually-uniform maps
(`mako`, `rocket`, `viridis`, or Crameri's `scico`) — they survive grayscale
and color-vision-deficiency checks.

## Export to PDF

```bash
quarto render slides.qmd --to revealjs
# then open slides.html and use the reveal print view:  ?print-pdf  →  Save as PDF
```

The theme guards against blank exports: fragments and content are never hidden
behind entrance animations under `prefers-reduced-motion`.

---

A live HTML preview of this exact system (10 sample slides, interactive tabs and
plots) ships alongside as **`Genomics Viz with Python.html`** — open it to see the
target look before you render.
