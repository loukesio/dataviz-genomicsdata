# CLAUDE.md — Day 2: Genomics Viz with Python

> Auto-loaded by Claude Code. Day-2 inherits **every** convention from
> `../day1/CLAUDE.md` (palette, fonts, two-column layout, head-in-code,
> step-by-step build, flat slide markers). This file is the short delta.

## What this is

A Quarto **reveal.js** Day-2 deck for the course "Genomics Viz with Python,"
assembled from ordered section files under `sections/`. Visual system =
**Economist palette on warm cream**, figures in **IBM Plex Mono**. Every
figure runs on real `genomics_course` data; every chart is a **two-column,
code-visible, step-by-step build** (rules 5, 10, 11 of day-1).

## Folder layout

```
day2/
  day2.qmd              # YAML + setup + {{< include >}} sections in order
  CLAUDE.md             # this file (delta from day-1)
  style.scss            # symlink → ../day1/style.scss (one theme source)
  day2.ipynb            # standalone Colab notebook — one plot per cell
  sections/             # ordered section files (one topic each)
    _00_intro.qmd
    _01_stacked_bar.qmd       # load_admixture()
    _02_timeseries.qmd        # load_timecourse()
    _03_msa.qmd               # synthesised alignment (biopython)
    _04_manhattan.qmd         # load_gwas("height")
    _05_genome_stats.qmd      # load_qc(), load_peaks(), load_peak_genes()
    _06_pycirclize.qmd        # circular genome plot
    _07_synteny.qmd           # synteny ribbons
```

## Build / preview

```bash
quarto preview day2.qmd        # live reload while authoring
quarto render  day2.qmd        # -> day2.html
```

Datasets are bundled in the `genomics_course` wheel (no `_build` step
needed by students); refer to `../day1/CLAUDE.md` for the install one-liner.

## Day-1 rules that still apply (no exceptions)

1. **Economist palette + IBM Plex Mono** via `from genomics_course.theme import *`.
2. Eyebrow-above-title pattern; `[label]{.eyebrow}` · `::: {.takeaway}` ·
   `# Title {.divider}` · `.keybox` · `.fragment`.
3. **Two-column code+plot** — code LEFT, rendered plot RIGHT, never full-width.
4. **Slide size 1280×720** (inherits from `style.scss`).
5. **`<!-- slide N -->` marker** above every heading; numbering is flat 1…N
   across this deck.
6. **Show `df.head()` inside the chunk** when a real dataset first appears.
7. **Comment every meaningful line** — students should read code like prose.
   Mark `# CREATE` (the `plt.subplots(...)`) and `# CALL` (the plotting method).
8. **Spotlight what changed** with `code-line-numbers="..."` in step-builds.

## Day-2 additions

- **`pyCirclize`** — circular genome plots (`_06_pycirclize.qmd`).
- **Synteny ribbons** — matplotlib `Polygon` between two genome tracks
  (`_07_synteny.qmd`); reference `plotsr` for the CLI alternative.
- **plotly variant** of the Manhattan plot — hover tooltips for SNP IDs.
- **seaborn variant** of the stacked bar — shows ergonomic vs control trade-off.

## Don't

- Don't edit `style.scss` (it's a symlink — changes affect day-1 too).
- Don't duplicate data; everything comes from `genomics_course.data`.
- Don't ship a notebook with hidden cells or "Run all" magic — students must
  see every line they're learning.
