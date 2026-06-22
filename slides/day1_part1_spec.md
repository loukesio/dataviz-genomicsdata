# day1_part1.qmd — spec

> For Claude Code. **CLAUDE.md is authoritative.** Where anything here conflicts
> with CLAUDE.md, follow CLAUDE.md and flag the conflict. This deck is **new and
> self-contained**; it must **not** touch `day1_python_gendataviz26.qmd`.

## What it is

One Quarto reveal.js file: YAML + a setup chunk (Economist palette, IBM Plex
Mono, `ECON` ramps, `econ_cmap`/`econ_diverging`/`econ_spectrum`, the
`pipeline_flowchart` helper), then teaching slides. Every figure runs on **real
`genomics_course` data** (no in-chunk simulation), and every chart is taught as a
two-column, code-visible build.

## Style contract (reconciled with CLAUDE.md)

- **Palette (CLAUDE.md rule 1):** Economist only. GREEN `#379A8B` carries the
  story; BLUE/AMBER secondary; RED/PURPLE highlight one thing; GREY de-emphasises.
  `ECON` ramps + `ECON_QUAL` + `econ_cmap` + `econ_diverging` + `econ_spectrum`.
- **Fonts (rule 2):** IBM Plex Mono for all matplotlib, registered from
  `../fonts/IBM_Plex_Mono/` with a DejaVu Sans Mono fallback. UI fonts stay in SCSS.
- **Classes (rule 3):** `.eyebrow`, `.takeaway`, `.divider`, `.columns`/`.column`.
- **Eyebrow-above-title (rule 4):** `## Title {.smaller}` → `[eyebrow]{.eyebrow}` →
  `### subtitle`. (Filled `##`, the Anscombe pattern the deck already uses.)
- **Code+plot / step-build (rule 5, UPDATED):** **two-column, code always
  visible.** Left (~46%): the **full, commented build code** (never a stub),
  growing one step per slide; `# CREATE` marks `plt.subplots(...)`, `# CALL` marks
  the plotting method. Right (~54%): the rendered plot. **Every line is
  commented.** No `panel-tabset`.
- **Figures (rule 6):** reuse setup constants + rcParams; perceptually-uniform
  maps only; no rainbow/jet except to teach against it.
- **Size (rule 7):** 1280×720 (in YAML).
- **Markers (rule 8):** every slide has `<!-- slide N -->` above its heading;
  flat sequential from the **YAML title slide = 1**; dotted sub-numbers for
  step-builds (`9.1`, `9.2`, …); decimal-insert, never renumber.
- **Data shown:** a `df.head()` table appears before the first plot of each dataset.
- **No em-dashes** in titles/prose; footers at 0.58em, sized to fit (no clipping).

## Contents (current file)

Built and validated (every figure executes against real data):

| Slides | Section |
|---|---|
| 1 | Title (YAML) |
| 2–4 | Why we visualise: Anscombe, Datasaurus |
| 5–6 | Logistics: course structure |
| 7–9.4 | Matplotlib from scratch: figure anatomy + build-a-plot (canvas → data → uncertainty → message) |

Remaining sections are appended to this same file (same patterns, same validation):
**Fundamentals** (15 principles + palette build + theme build) · **Distributions**
(box when/anatomy/build, violin when/anatomy/build, ridgeline build) ·
**Proportions** (bars-not-pies, stacked bar on admixture, stacked area on lineages) ·
**Scatter+fit** (coexpression) · **Volcano** (concept, pipeline, build) ·
**Exercises** (5 with expected-result thumbnails + recap).

## Dependencies (must be in place first)

1. **Package data layer** — apply `package-data-layer.md` and run
   `python -m genomics_course.data._build`. The setup chunk imports **nine**
   loaders: `load_deseq2, load_admixture, load_gwas, load_variants, load_lineages,
   load_timecourse, load_coexpression, load_anscombe, load_datasaurus`. The import
   fails if the parquets aren't built. (`load_anscombe` + `load_datasaurus` are the
   two newest; the data-layer spec includes their build functions and loaders.)
2. **Fonts** — `fonts/IBM_Plex_Mono/*.ttf` at the repo root (sibling of `slides/`).
3. **`style.scss`** — referenced in the YAML `theme:`.

## Install & render

```bash
python -m genomics_course.data._build      # build all datasets first
cp day1_part1.qmd slides/
quarto render slides/day1_part1.qmd        # or: quarto preview slides/day1_part1.qmd
```

## Verify

- Renders with no errors.
- Every plot slide is **two-column with the full commented code visible on the
  left** and the plot on the right (no hidden code, no stubs).
- `df.head()` table shown before each dataset's first plot.
- Figures in IBM Plex Mono on the cream Economist canvas.
- Slide markers present and sequential from the title slide = 1.
- No em-dashes in titles/prose; footers do not clip.
- Real-data spot checks: Anscombe 4 panels with identical fit lines; Datasaurus 13
  shapes; BRCA1 time course peaks then settles.
