# CLAUDE.md — Day 1: Genomics Viz with Python

> Auto-loaded by Claude Code. **This file is authoritative for the whole Day-1
> deck.** If any other note, spec, or older instruction conflicts with it, follow
> this file and say so. The deck must render with `quarto render day1.qmd`.

## What this is

A Quarto **reveal.js** Day-1 deck for the course "Genomics Viz with Python,"
assembled from **ordered section files** under `sections/`. The visual system is
the **Economist colour system on a warm cream canvas**, figures in **IBM Plex
Mono**. Every figure runs on **real `genomics_course` data**; every chart is
taught as a **two-column, code-visible, step-by-step build**.

## Folder layout (the clean structure)

```
day1/
  day1.qmd              # YAML + the setup chunk + {{< include >}} of each section, in order
  CLAUDE.md             # this file (authoritative)
  style.scss            # the theme — all colours/type/components live here
  sections/             # the ordered section files (one topic each)
    _00_motivation.qmd        _08_distributions.qmd
    _01_why_python.qmd        _09_dimreduction.qmd
    _02_ecosystem.qmd         _10_admixture.qmd
    _03_matplotlib_basics.qmd _11_heatmaps.qmd
    _04_fundamentals.qmd      _12_waffle_waterfall.qmd
    _05_logistics.qmd         _13_peaks.qmd
    _06_scatter.qmd           _14_pathways.qmd
    _07_volcano.qmd           _15_recap.qmd
```

- **Data is NOT duplicated here.** It comes from the installed `genomics_course`
  package (`python -m genomics_course.data._build` builds the parquets once).
- **Fonts:** `fonts/IBM_Plex_Mono/*.ttf` at the repo root (sibling of `day1/`).
- **One deck only.** Do not create parallel decks (e.g. a separate
  `day1_part1.qmd`); fill the section files in place.

## Section order and status

The order is set by the filename number and must be preserved. Markers are flat
and sequential **across the whole deck** (see rule 8).

| # | Section | Status | Primary dataset |
|---|---|---|---|
| 00 | motivation (Anscombe, Datasaurus) | done | `load_anscombe`, `load_datasaurus` |
| 01 | why python | done | — |
| 02 | ecosystem | done | — |
| 03 | matplotlib basics | done | `load_timecourse` |
| 04 | **fundamentals** | **STUB — fill** | small illustrative arrays |
| 05 | logistics | done | — |
| 06 | **scatter + fit** | **STUB — fill** | `load_coexpression` |
| 07 | volcano | done | `load_deseq2` |
| 08 | **distributions** | **STUB — fill** | `load_deseq2` / grouped expression |
| 09 | dim. reduction | done | — |
| 10 | admixture (proportions) | done | `load_admixture` |
| 11 | heatmaps | done | — |
| 12 | waffle / waterfall | done | — |
| 13 | peaks | done | — |
| 14 | pathways | done | — |
| 15 | recap | done | — |

Done sections are **restyle-only** (apply rules, don't rewrite copy). The three
stubs are the build target; specs below.

## Build / preview

```bash
python -m genomics_course.data._build      # build datasets once
quarto preview day1.qmd                     # live reload while authoring
quarto render  day1.qmd                     # -> day1.html
```

## The setup chunk (imports the one style source)

Figure style lives in **`genomics_course/theme.py`** — the single source of truth
for palette, font, and rcParams. It registers **IBM Plex Mono** (DejaVu Sans Mono
fallback, never hard-fails), defines the Economist palette + ramp helpers, and
applies the cream-canvas rcParams on import. `day1.qmd` opens with one small setup
chunk that just imports it:

````
```{python}
#| label: setup
#| echo: false
from genomics_course.theme import *        # palette, ramps, helpers, rcParams applied
from genomics_course.data import (         # the nine dataset loaders
    load_deseq2, load_admixture, load_gwas, load_variants, load_lineages,
    load_timecourse, load_coexpression, load_anscombe, load_datasaurus)
import numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
rng = np.random.default_rng(7)             # only for synthetic teaching examples
```
````

Section figures use these names directly and **never** redefine colours or fonts.
`theme.py` is the same module the fundamentals section teaches (see `_04` spec).

## Hard rules — do not violate

1. **Economist palette only.** `GREEN #379A8B` (green-teal, carries the story) ·
   `BLUE #006BA2` · `AMBER #EBB434` · `RED #B4405F` · `PURPLE #9A607F`. Neutrals
   `INK #0D0D0D`, `CREAM #FAF9F7`, `LINE #D9D9D9`, `MUTED #666666`, `GREY #B3B3B3`.
   Green carries the story; red/purple highlight one thing; grey de-emphasises.
   Many-category / continuous needs use the `ECON` ramps + helpers `ECON_QUAL`,
   `econ_cmap("ramp")`, `econ_diverging` (blue–cream–red), `econ_spectrum`
   (blue→teal→green→amber→red). No off-system hexes; no rainbow/jet except to
   teach against it.
2. **IBM Plex Mono for all matplotlib figures**, registered in the setup chunk.
   UI fonts (JetBrains Mono / Space Grotesk / Asap) live in `style.scss` only.
   Never set IBM Plex Mono in SCSS; never set the UI fonts in a figure.
3. **Use the existing classes:** `[label]{.eyebrow}` · `::: {.takeaway}` (purple
   end-of-slide message) · `# Title {.divider}` · `:::: {.columns}` /
   `::: {.column}` · `.keybox` · `.fragment` for reveals. Don't reinvent them.
4. **Eyebrow-above-title:** `## Title {.smaller}` → `[eyebrow]{.eyebrow}` →
   `### subtitle` → content. (The filled-`##` pattern the deck already uses.)
5. **Every code+plot slide is two-column: code LEFT, rendered plot RIGHT — in all
   cases, no exceptions.** Left (~44–46%): the build code in full, never a stub,
   growing **one step per slide**. Right (~54–58%): the plot that code produces.
   Never full-width code, never a full-width plot, never a `panel-tabset` "Code"
   tab — the code always stays on screen beside its result. Code is **commented so
   a student can follow** — annotate the meaningful lines (what each call does, the
   new step), not trivial noise, and mark `# CREATE` (the `plt.subplots(...)`) and
   `# CALL` (the plotting method). Highlight the lines added in each step (rule 12).
6. **Figures on-system:** reuse the setup constants + `rcParams`; perceptually-
   uniform colormaps only.
7. **Slide size 1280×720** (in the YAML).
8. **Every slide has a `<!-- slide N -->` marker** above its heading. Numbering is
   flat and sequential **across the whole deck**, starting at the YAML title slide
   = 1 and running through every section in order (1, 2, 3, … N) — **this clean
   1…N numbering is essential.** Split a topic with dotted sub-numbers (`14.1`,
   `14.2`). **Insert** with a decimal between neighbours, **never renumber** mid-
   edit. After the three stubs are filled, do **one** renumber pass so the deck is
   clean consecutive integers from 1; that pass is its own commit.
9. **Show the data inside the code, never as a table above it.** When a dataset
   first appears, the first build step is a small **executed** chunk that loads it
   and shows `df.head()` as the chunk's own output:

   ````
   ```{python}
   #| echo: true
   tc = load_timecourse()      # gene, time, tpm, sem
   tc.head()                   # the preview IS the chunk output
   ```
   ````

   Do **not** hand-build a Markdown table of `head()` above the columns (it
   clutters the slide and overflows). If a clean in-code preview isn't possible,
   show **no** data preview at all. **Exemption:** pure teaching examples built
   from small synthetic arrays (e.g. the boxplot/violin distribution demos, the
   fundamentals bad-vs-good panels) have no meaningful `head()` — they show no
   data preview, and that is correct. The rule applies to real package datasets.
10. **Every dataset gets a load → build walkthrough.** Sequence: **(0) load +
    `head()` peek → (1) canvas → (2) data → (3) style on-palette → (4) message**,
    one step per slide, two-column, code growing left, plot right. The same recipe
    drives every chart type.
11. **Simple, readable, on-palette code.** Prefer vectorised pandas/numpy and
    direct matplotlib/seaborn calls over explicit `for` loops. A `for` loop is
    allowed **only** when it is genuinely the clearest option (faceting many
    panels; styling boxplot artists). No dense one-liners that trade readability
    for brevity. Beautiful, teachable code beats clever code.
12. **Spotlight what changed (the "flare").** In step-builds, highlight the lines
    added in that step with Quarto line-numbering — display blocks
    ` ```python {code-line-numbers="6-8"} `, executed chunks
    `#| code-line-numbers: "6-8"`. Students should see the new code at a glance.

## Data layer

`genomics_course` ships nine loaders (build with `python -m
genomics_course.data._build`):

`load_deseq2` · `load_admixture` · `load_gwas` · `load_variants` · `load_lineages`
· `load_timecourse` · `load_coexpression` · `load_anscombe` · `load_datasaurus`.

Columns and shapes are documented in `package-data-layer.md`. All deck figures
pull from these; no inline simulation of biology, no copy-pasted CSVs.

## Section specs (the three stubs)

### `_04_fundamentals.qmd` — principles + palette/theme builds
A `# … {.divider}` opener, then the 15 principles, each a focused slide (mostly a
two-panel **bad vs good** comparison; these are illustrations, so per rule 9 they
need no `head()` — use small illustrative arrays, vectorised, minimal loops):

- *Act I — honest charts:* lie factor / zero baseline · data-to-ink ratio · the
  3D trap & proportional ink · perceptual ranking (position > length > area >
  colour) · pre-attentive cues & Gestalt.
- *Act II — colour:* three palette types (qualitative / sequential / diverging) ·
  the rainbow trap & accessibility (jet vs viridis, colour-blindness) · grey is
  your best friend.
- *Act III — chart to story:* editorial angle/frame/focus · the story arc · a
  figure for the generals · build up towards complexity · memorability vs
  minimalism · vary chart types (DRY) · small multiples.

Then two **builds** that construct `genomics_course/theme.py` in front of the
students, so they see how the unified look is made, not just handed it:
**build-your-own palette** (define the Economist "story" colours + an `ECON` ramp
+ `econ_cmap`/`econ_diverging`/`econ_spectrum`) and **build-your-own theme**
(register IBM Plex Mono, then set the matplotlib `rcParams` once so every later
figure inherits the cream canvas and muted axes). End by showing the same
`from genomics_course.theme import *` line the whole deck uses — "this is the file
we just built." Step-by-step, two-column, code-highlighted.

### `_06_scatter.qmd` — scatter + fitted line
Dataset `load_coexpression()` (sample, tissue, gene_x, gene_y; r ≈ 0.9). Walkthrough
per rule 10: **(0)** load + `head()`; **(1)** canvas with axis labels; **(2)**
`ax.scatter(gene_x, gene_y)`; **(3)** `np.polyfit` fitted line on-palette; **(4)**
annotate Pearson r and a finding title. Vectorised, no loops.

### `_08_distributions.qmd` — boxplot, violin, ridgeline
**Reuse the validated slides in `corrected-boxplot-and-area.md`** — the 5-step
boxplot build (canvas → raw points → box → style on-palette → message) is the
locked pattern; keep its exact look. Then the violin (when/why → anatomy →
build, swap the box body for a KDE) and the ridgeline build (one ridge per
`|log2FC|` bin of `load_deseq2()`, distributions marching right).
The boxplot and violin demos stay on small **synthetic** arrays (`rng.normal`) —
they are pure teaching examples and are **exempt from the `head()` rule** (rule 9).
The ridgeline uses the real `load_deseq2()` data, so it opens with a `head()` peek
per rule 10.

## Don't

- Don't create a second deck or duplicate sections that already exist.
- Don't edit `style.scss` tokens to fix a one-off; restyle on-system.
- Don't add gradients, emoji, drop-shadows, or rounded-corner+left-border callout
  clichés beyond `.keybox`.
- Don't hand-build `head()` tables above the columns (rule 9).
- Don't reach for a `for` loop where a vectorised call reads better (rule 11).

## Decisions of record (settled)

1. **One style system: Economist + IBM Plex Mono.** `genomics_course/theme.py` is
   the single source — rewritten from the old Geist/`#C23B22` version. The deck
   imports it; `_04_fundamentals` teaches how it is built. The old palette is
   retired.
2. **Anscombe/Datasaurus live only in `_00_motivation.qmd`** — never rebuilt
   elsewhere. The scratch `day1_part1.qmd` is retired in favour of filling the
   section stubs.
3. **Boxplot/violin demos stay synthetic** and are exempt from the `head()` rule
   (rule 9); the ridgeline uses real `load_deseq2()` data.
4. **Clean 1…N slide numbering** (rule 8): decimal-insert while filling stubs,
   then one renumber pass to consecutive integers.
