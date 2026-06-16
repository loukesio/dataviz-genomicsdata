# Genomics Course — Project Instructions

Plots: **The Economist meets Nature Reviews Genetics**. Slides: teal Asap theme.

═══════════════════════════════════════════════════════════════
## RULE 1 — CONTENT MUST FIT THE SLIDE (HIGHEST PRIORITY)
═══════════════════════════════════════════════════════════════

THIS IS THE MOST IMPORTANT RULE. Nothing else matters if students can't read the slide.

- If content EXCEEDS one slide → SPLIT into a new slide. No exceptions.
- If a figure + text don't fit together → figure goes on its OWN `{.plot-slide}` slide
- >5 bullets → add `{.smaller}` to the heading
- >8 lines of any content → SPLIT into two slides
- WORST CASE: add `{.scrollable}` so the student can scroll
- NEVER let text or figures get cut off at the bottom
- Test mentally: heading + body + figure = too tall? Then SPLIT.
- When in doubt → SPLIT. An extra slide costs nothing. Hidden content costs everything.

═══════════════════════════════════════════════════════════════
## RULE 2 — FLOWCHART BEFORE EVERY PLOT
═══════════════════════════════════════════════════════════════

Before EVERY genomics result plot (volcano, heatmap, PCA, Manhattan, enrichment,
admixture, etc), add a slide with a Mermaid flowchart showing HOW the data is
generated / how the analysis works. The slide sequence is ALWAYS:

1. **Theory slide** — what the method does
2. **Flowchart slide** — Mermaid diagram of the pipeline
3. **Result slide** `{.plot-slide}` — the plot, on its own slide, no body text

═══════════════════════════════════════════════════════════════
## RULE 3 — MERMAID SYNTAX (AVOID THESE ERRORS)
═══════════════════════════════════════════════════════════════

Claude Code keeps generating broken Mermaid. Follow these EXACTLY:

### ALWAYS do:
```
flowchart LR
  A[Step one] --> B[Step two]
  B --> C[Step three]
  style C fill:#28A87D,color:#fff,stroke:#28A87D
```

### NEVER do (these ALL cause syntax errors):
```
WRONG: A[Run ADMIXTURE (K=2..10)]     ← parentheses inside [ ] break it
RIGHT: A[Run ADMIXTURE\nK = 2 to 10]

WRONG: A[p < 0.05]                     ← angle brackets break it
RIGHT: A[p less than 0.05]

WRONG: A[Filter & normalize]           ← ampersand breaks it
RIGHT: A[Filter and normalize]

WRONG: A(Step one)-->B(Step two)        ← no spaces around arrow
RIGHT: A(Step one) --> B(Step two)

WRONG: flowchart LR;                   ← semicolon after direction
RIGHT: flowchart LR

WRONG: A --> |yes| B                   ← space before pipe
RIGHT: A -->|yes| B

WRONG: A["quoted text"]                ← quotes inside brackets
RIGHT: A[quoted text]
```

### RULES:
- No parentheses `()` inside node text `[ ]` — use `\n` instead
- No `<`, `>`, `&`, `"` inside node text
- Always put spaces around `-->`
- Keep node text SHORT: max 3 words per line, use `\n` for breaks
- Max 6-8 nodes per diagram
- Test: if you see ANY of the wrong patterns above, fix before outputting

### Mermaid config (paste at top of every mermaid cell):
```
%%| fig-cap: "Description here"
%%| fig-width: 9

---
config:
  theme: base
  themeVariables:
    primaryColor: "#d9f6ec"
    primaryBorderColor: "#28A87D"
    primaryTextColor: "#1A1A1A"
    lineColor: "#888888"
    fontFamily: "Asap, sans-serif"
    fontSize: "15px"
---
```

Style the final node: `style F fill:#28A87D,color:#fff,stroke:#28A87D`

═══════════════════════════════════════════════════════════════
## RULE 4 — NO SIMULATION IN GENOMICS PLOTS
═══════════════════════════════════════════════════════════════

Use `genomics_course.data` loaders for genomics result plots.
Matplotlib-teaching code (Steps 1-5, Anscombe, Datasaurus) can use inline data
since the point is teaching matplotlib, not showing genomics results.

```python
from genomics_course.data import load_admixture, load_gwas, load_deseq2, load_variants
from genomics_course.plots import plot_admixture, plot_volcano, plot_manhattan, plot_lld, save
```

### RULE 5 — WHITE BACKGROUND, GEIST FONT
Background: white `#FFFFFF`. Never grey. Never `#FAF9F7`.
Setup cell must include: `fm._load_fontmanager()`
Every savefig: `facecolor="white"`

═══════════════════════════════════════════════════════════════
## PLOT STYLE RULES
═══════════════════════════════════════════════════════════════

Colors:
```
primary=#C23B22  secondary=#2B6CB0  tertiary=#E6A817  quaternary=#5A8F29  quinary=#7B5EA7
text_dark=#1A1A1A  text_mid=#555555  text_light=#888888
```
NEVER rainbow, jet, or default matplotlib blue.

- ALL CAPS bold titles with letter spacing
- Value labels at bar ends, footnotes italic, legends frameon=False
- Horizontal bars preferred, no gridlines, remove top + right spines
- Sizes: (10,6) standard, (12,5) wide, (8,8) square

## TWO VISUAL SYSTEMS — DO NOT MIX

| Layer      | Font            | Background | Colors                         |
|------------|-----------------|------------|--------------------------------|
| **Plots**  | Geist Sans      | white      | Crimson / blue / amber / green |
| **Slides** | Asap + Literata | `#F8F8F8`  | Teal `#28A87D`                 |

## QUARTO YAML
```yaml
format:
  revealjs:
    theme: [default, slides.scss]
```

## EXERCISE PATTERN
Every exercise has a `<details><summary>Show solution</summary>` block.
Solution must be complete and runnable.

## SLIDE CLASSES
`{.smaller}` `{.smallest}` `{.scrollable}` `{.plot-slide}` `:::{.exercise}`
