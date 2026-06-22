# Refactor day1 into a shell + sections (content-neutral)

> For Claude Code. This is a **structural** change only: no slide content is added,
> removed, or edited. The deck must render **identically** after it. Work from the
> **original day1** (revert the old 29-slide insert first; we are NOT building on
> HEAD bb25938). Tag the original as a backup before starting.
>
> The idea: `day1_python_gendataviz26.qmd` becomes a thin shell (YAML + setup chunk
> + a list of `{{< include >}}` lines). Each existing section moves verbatim into
> `sections/_NN_*.qmd`. Quarto splices them at render into one deck sharing one
> Python session, so every section still sees the setup-chunk constants.

---

## STEP A — Make the shell

In `slides/day1_python_gendataviz26.qmd`, **keep everything from the top through the
end of the `setup` chunk** (the YAML header, then the chunk ending with the
`pipeline_flowchart` function). **Delete everything from `<!-- slide 1 -->` to the
end of the file.** Then append exactly this include list:

```markdown
{{< include sections/_00_motivation.qmd >}}
{{< include sections/_01_why_python.qmd >}}
{{< include sections/_02_ecosystem.qmd >}}
{{< include sections/_03_matplotlib_basics.qmd >}}
{{< include sections/_04_fundamentals.qmd >}}
{{< include sections/_05_logistics.qmd >}}
{{< include sections/_06_scatter.qmd >}}
{{< include sections/_07_volcano.qmd >}}
{{< include sections/_08_distributions.qmd >}}
{{< include sections/_09_dimreduction.qmd >}}
{{< include sections/_10_admixture.qmd >}}
{{< include sections/_11_heatmaps.qmd >}}
{{< include sections/_12_waffle_waterfall.qmd >}}
{{< include sections/_13_peaks.qmd >}}
{{< include sections/_14_pathways.qmd >}}
{{< include sections/_15_recap.qmd >}}
```

## STEP B — Carve the existing slides into section files

Create `slides/sections/`. Move each slide range **verbatim** (the `<!-- slide N -->`
markers, headings, chunks, footers — everything, unchanged) into the file below.
Each range runs from its first marker up to **but not including** the next range's
first marker. Leave the slide numbers exactly as they are for now (we renumber
across files in a later, separate step).

| File | Slides (by marker) | Content |
|---|---|---|
| `_00_motivation.qmd` | 1 → before 4 | Why visualise, Anscombe, Datasaurus |
| `_01_why_python.qmd` | 4 → before 9 | Big data in biology, data explosion, why Python, ggplot2→Python |
| `_02_ecosystem.qmd` | 9 → before 13 | Viz ecosystem, publication-ready, libraries, setup |
| `_03_matplotlib_basics.qmd` | 13 → before 21 | Intro mpl/seaborn, anatomy, building-a-plot 1–5, common types |
| `_05_logistics.qmd` | 21 → before 23 | How we work, Course Structure |
| `_07_volcano.qmd` | 23 → before 30 | Volcano: what / data prep / building / labelling / exercise |
| `_09_dimreduction.qmd` | 30 → before 40 | PCA, t-SNE, UMAP |
| `_10_admixture.qmd` | 40 → before 45 | Admixture: theory / pipeline / code / exercise |
| `_11_heatmaps.qmd` | 45 → before 51 | Heatmaps, clustermap, exercise |
| `_12_waffle_waterfall.qmd` | 51 → before 59 | Waffle & waterfall |
| `_13_peaks.qmd` | 59 → before 65 | Peak visualisation, pyGenomeTracks |
| `_14_pathways.qmd` | 65 → before 71 | GO / pathway enrichment, bubble |
| `_15_recap.qmd` | 71 → end | Recap, what we covered, resources |

## STEP C — Create three empty placeholder sections

These are where new content lands later. For now each is just a one-line comment so
the include resolves and renders nothing:

`_04_fundamentals.qmd`:
```markdown
<!-- Fundamentals of data visualization — principles + build-your-own palette. To be filled. -->
```

`_06_scatter.qmd`:
```markdown
<!-- Scatter + fitted line (coexpression dataset). To be filled. -->
```

`_08_distributions.qmd`:
```markdown
<!-- Distributions: boxplot / violin / ridgeline builds. To be filled. -->
```

## Rules for the section files (important)

- **No YAML in any section file.** Only the shell has YAML + the setup chunk.
- Filenames **must** start with `_` (Quarto won't treat `_`-prefixed files as
  standalone render targets).
- Don't touch the setup chunk or the palette in this step — that's a later edit.
- Don't renumber markers in this step — they stay as-is; a later script renumbers
  flat across the include order.

## Verify it rendered identically

```bash
quarto render slides/day1_python_gendataviz26.qmd
```

- The rendered deck has the **same number of slides** and the **same order** as the
  pre-refactor original (the three empty placeholders add nothing).
- Spot-check a few slides from different sections — content, plots, and styling
  unchanged.
- `git diff --stat` should show the monolith shrinking to the shell and the new
  `sections/*.qmd` files appearing — and **no change in rendered output**.

## Commit

One commit: "refactor: split day1 into shell + sections (no content change)".
