# 🧬 Genomics Data Visualization with Python — 2026

A hands-on 3-day workshop on creating publication-quality visualizations for genomics and biological data using Python.

## 📚 Course Overview

This course teaches researchers and bioinformaticians how to build compelling, reproducible figures using Python's scientific visualization ecosystem. Each day builds on the previous, moving from core plotting fundamentals to specialized genomics visualizations.

| Day | Theme | Key Topics |
|-----|-------|-----------|
| 1 | Foundations | matplotlib anatomy, seaborn, volcano plots, PCA/t-SNE/UMAP, heatmaps |
| 2 | Genomics Plots | stacked bars, time series, MSA visualization, Manhattan plots, genome statistics |
| 3 | Specialized | phylogenetic trees, Circos plots, Venn/UpSet, synteny, ideograms |

---

## 🚀 Quick Start

### 1 — Install the course package

```bash
pip install genomicsviz
```

This installs every library used across all three days in a single command.

### 2 — Verify your setup

```python
import genomicsviz as gv

gv.apply_course_theme()   # set publication-ready matplotlib defaults
print(gv.COURSE_PAL)      # 10-colour palette used throughout the slides
```

### 3 — Recommended: use a dedicated environment

```bash
# conda
conda create -n genomicsviz python=3.11
conda activate genomicsviz
pip install genomicsviz

# or venv
python -m venv genomicsviz_env
source genomicsviz_env/bin/activate   # Windows: genomicsviz_env\Scripts\activate
pip install genomicsviz
```

---

## 📦 What Gets Installed

`genomicsviz` is a thin meta-package: installing it pulls in the full dependency stack so students never have to track individual packages manually.

| Category | Packages |
|----------|----------|
| Core numerics & data | `numpy`, `pandas`, `scipy`, `scikit-learn` |
| Plotting foundations | `matplotlib`, `seaborn`, `plotly` |
| Genomics-specific | `biopython`, `scanpy`, `toytree`, `pycirclize`, `pymsaviz`, `gget` |
| Enrichment & annotation | `gget`, `PyComplexHeatmap` |
| Specialized charts | `matplotlib-venn`, `upsetplot`, `pywaffle`, `adjustText` |
| Dimensionality reduction | `umap-learn` |

---

## 🗓 Curriculum

### Day 1 — Visualization Foundations

- Why visualization matters: Anscombe's Quartet & the Datasaurus Dozen
- Python's genomics visualization ecosystem
- Anatomy of a matplotlib figure — canvas, axes, artists
- Building plots step by step: scatter → color → polish → publication style
- Common plot types: scatter, bar, box, violin
- **Volcano plots** — theory, data preparation, gene labeling with `adjustText`
- **Dimensionality reduction** — PCA scree plots, t-SNE, UMAP
- **Heatmaps** — `seaborn` clustermap, `PyComplexHeatmap` rich annotations

### Day 2 — Genomics-Relevant Plots

- **Stacked bar charts** — microbiome composition, 100% normalized
- **Time series** — replicated gene-expression time courses, mean ± SEM ribbons
- **MSA visualization** — multiple sequence alignments with `pyMSAviz`
- **Manhattan plots** — GWAS results, chromosome alternation, Q-Q plots
- **Genome statistics** — GC content, read depth, coverage windows

### Day 3 — Specialized Visualizations

- **Phylogenetic trees** — `toytree`, `Bio.Phylo`, custom matplotlib rendering
- **Circos / chord diagrams** — `pycirclize`, structural variant links
- **Venn & UpSet plots** — `matplotlib-venn`, `upsetplot` for complex overlaps
- **Synteny plots** — ribbon diagrams, dot plots for comparative genomics
- **Ideograms** — chromosome-level overview with simulated cytobands

---

## 🎓 Learning Outcomes

By the end of the workshop you will be able to:

- Build publication-ready figures entirely in Python
- Choose the right visualization for each data type
- Customize every element of a matplotlib figure
- Visualize single-cell, GWAS, phylogenetic, and comparative-genomics data
- Apply colorblind-friendly, consistent color schemes across a project
- Reproduce and adapt all course examples on your own data

---

## 🗂 Repository Structure

```
dataviz-genomicsdata/
├── day1/  day2/  day3/          # one folder per course day
│   ├── dayN.qmd                 #   Quarto reveal.js source
│   ├── sections/*.qmd           #   the deck split into slide sections
│   ├── dayN.html                #   rendered deck (students view this)
│   ├── dayN.ipynb               #   companion Colab notebook
│   └── dayN.pdf                 #   landscape PDF export (kept local, git-ignored)
├── genomics_course/             # the pip-installable course package
│   └── genomics_course/         #   datasets + publication theme (theme.py)
├── plotpy/                      # LLM plotting agent — "describe a chart, get the code"
│   ├── plotpy/                  #   providers (multi-LLM) · agent · catalog · datasets
│   ├── tests/                   #   offline tests (no API key needed)
│   └── README.md                #   ← full usage guide for the agent
├── fonts/                       # deck fonts (IBM Plex Mono, …)
├── pyproject.toml               # course package metadata + dependency stack
└── README.md
```

Each deck is authored in Quarto (`dayN.qmd` + `sections/`), rendered to
`dayN.html` for viewing, and also shipped as a Colab notebook and a landscape
PDF. The PDFs live on disk but are git-ignored to keep the repo light — see
each day folder to regenerate.

---

## 🤖 PlotPy — the plotting agent

`plotpy/` is a small LLM agent built from the course material: hand it a
`pandas.DataFrame` and a sentence ("make an interactive GWAS Manhattan"), and it
picks the right chart, writes the code in the course house style, runs it, and
fixes its own mistakes. It suggests plots for data you haven't seen, works with
any LLM provider (Groq / OpenAI / Anthropic / Ollama …), and returns the source
so students can learn from it.

```python
import plotpy
plotpy.use(plotpy.chat_groq(api_key="gsk_..."))
plotpy.suggest(df)                     # a ranked menu of plot ideas
plotpy.ask(df, "volcano plot").plot    # the figure + .code that made it
```

Full instructions live in [`plotpy/README.md`](plotpy/README.md).

---

## 🔗 Related Branches

| Branch | Language | Year |
|--------|----------|------|
| `R_2024` | R / ggplot2 | 2024 |
| `R_2025` | R / ggplot2 | 2025 |
| `Python_2026` | Python / matplotlib | **2026 ← you are here** |

---

## 👨‍🏫 Instructor

**Dr. Loukas Theodosiou**
Senior Data Scientist · Population Genomics & AI/ML
[GitHub](https://github.com/loukesio)

---

**License**: Materials provided for educational purposes.
