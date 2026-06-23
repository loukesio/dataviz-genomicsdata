# CLAUDE.md — Day 3: Production-Grade Genomics Tools

> Day-3 inherits **every** convention from `../day1/CLAUDE.md`. This is the short delta.

A Quarto **reveal.js** Day-3 deck. One section per production-grade package: how to
install, the minimum data it needs, and a 3-5 step build per chart type. Every plot
runs end-to-end on the cream canvas, IBM Plex Mono, Economist palette via
`from genomics_course.theme import *`.

## Sections

```
_00_intro.qmd
_01_pycomplexheatmap.qmd      # clustered heatmap + annotations
_02_pycirclize_xref.qmd       # short cross-ref to day-2 _06
_03_toytree.qmd               # phylogenetic tree drawing
_04_pymsaviz.qmd              # production MSA viewer
_05_dashbio.qmd               # Plotly DashBio widgets
_06_pygenometracks.qmd        # genome-browser tracks
_07_dna_features_viewer.qmd   # gene maps / plasmid features
_08_jcvi_mcscan.qmd           # synteny via jcvi.graphics
_09_upsetplot.qmd             # set intersections
_10_pywaffle.qmd              # waffle composition charts
_11_gget.qmd                  # gene + pathway queries
_12_biopython_phylo.qmd       # Bio.Phylo / Bio.Graphics
```

## Day-1 rules that still apply (no exceptions)

1. **Economist palette + IBM Plex Mono** via `from genomics_course.theme import *`.
2. **Two-column code+plot** — code LEFT, rendered plot RIGHT.
3. **Show `df.head()`** when a real dataset first appears (per-section, not deck-wide).
4. **Comment every meaningful line** — `# CREATE` on `plt.subplots()`, `# CALL` on the plotting method.
5. **Spotlight what changed** with `code-line-numbers="..."`.
6. **Each section opens with a divider** (`# Title {.divider}`).
7. **Each section closes with `::: {.takeaway}`** — one-paragraph summary.

## Day-3 additions

- **Installation slide first** for each package — Colab one-liner, then import.
- **Compare-with** lines in every takeaway — when to reach for this package vs the
  matplotlib-from-primitives equivalent in day-2.
- **Network warning** in `gget` section — it queries Ensembl; mention offline failure mode.

## Don't

- Don't repeat full pyCirclize coverage from day-2 _06; the day-3 section is just a cross-ref.
- Don't add packages outside the requested 12 to scope creep.
- Don't run network-dependent calls without a fallback or clear marker.
