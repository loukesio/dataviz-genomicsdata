# Genomics Course — Project Instructions

All plots follow a strict visual identity: **The Economist meets Nature Reviews Genetics** —
editorial, clean, no chartjunk. See @plotting-style-guide.md for full spec.
Slide theme lives in `slides.scss` (Quarto Reveal.js) — separate system, do NOT mix.

## Two Visual Systems — Do NOT Mix

| Layer      | Font            | Background | Colors                         |
|------------|-----------------|------------|--------------------------------|
| **Plots**  | Geist Sans      | `#FAF9F7`  | Crimson / blue / amber / green |
| **Slides** | Asap + Literata | `#F8F8F8`  | Teal `#28A87D` brand system    |

Never apply teal to plots. Never apply crimson/Geist to slide UI.

## Dataset Packaging

Pre-built datasets ship with the course package. Students load, not simulate:

```python
from genomics_course.data import load_admixture, load_gwas_summary, load_variants
df = load_admixture(K=5)
```

Simulation code lives in package source for reference but is NOT used in class.

## Exercise & Solution Pattern

Every exercise MUST include a hidden solution. Two patterns:

### In slides — collapsible details:

```markdown
::: {.exercise}
Load the GWAS summary stats and create a Manhattan plot.
Highlight SNPs crossing genome-wide significance.

<details>
<summary>Show solution</summary>

`python
from genomics_course.data import load_gwas_summary
from genomics_course.plots import plot_manhattan

df = load_gwas_summary("height")
plot_manhattan(df, threshold=5e-8, highlight_genes=True)
`

</details>
:::
```

### In notebooks — code-fold:

````markdown
```{python}
#| code-fold: true
#| code-summary: "Show solution"
df = load_gwas_summary("height")
plot_manhattan(df, threshold=5e-8)
```
````

### Exercise rules:

1. State the **goal** in 1–2 sentences
2. Name the **dataset** and **function** to use
3. Solution must be **complete and runnable** — no pseudocode
4. Show FULL modified code, not diffs
5. Add `# why:` comments on non-obvious lines

## Slide Content Rules

- Use `{.smaller}` or `{.smallest}` class on dense slides to prevent text overflow
- Use `{.scrollable}` on unavoidably long content
- Use `{.plot-slide}` on plot-focused slides to maximize image area
- Use `{.sandbox}` div for live-coding / try-it blocks
- Use `{.exercise}` div for student exercises (always with `<details>` solution)

## Plotting Quick Reference

- Font: Geist → IBM Plex Sans fallback
- Canvas: `#FAF9F7` (warm off-white, never pure white)
- Palette: `#C23B22` crimson, `#2B6CB0` blue, `#E6A817` amber, `#5A8F29` green, `#7B5EA7` purple
- Titles: ALL CAPS, bold. Footnotes: italic, `text_light`
- Export: PNG 300dpi + SVG, always `facecolor=COLORS["canvas"]`
- Full spec: @plotting-style-guide.md
