"""Build day1.ipynb from inline cell sources.

Run from the day1/ directory:
    python _build_ipynb.py

Produces day1.ipynb — a standalone Colab-ready notebook with one polished
"final version" per Day-1 topic. The slides walk students through the
build step by step; this notebook is the destination they walk to.
"""
from __future__ import annotations
import json
from pathlib import Path


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(src: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


HEADER_MD = """\
# Genomics Data Visualization · Day 1

**Foundations & differential expression** — the runnable companion to the
Day-1 deck. Every cell is the *final, polished* version of a chart the
slides built one annotated step at a time.

**How to use this notebook:**

1. Run the install cell once (~1-2 minutes on Colab).
2. Run the setup cell to import the theme + every loader.
3. Each chart cell below is **self-contained** — rerun any cell in any order.

**Topics covered (the Day-1 deck):**

- Why we visualise — Anscombe's quartet, Datasaurus
- Time-course expression (multi-gene line plot)
- Distributions — boxplot, violin
- Scatter + linear fit (`load_coexpression`)
- Volcano plot (`load_deseq2`)
- Dimensionality reduction — PCA on `load_expression`
- Admixture stacked bar (`load_admixture`)
- Clustered heatmap (`sns.clustermap`)
- Waffle / Waterfall composition
- Peak tracks + gene model (`load_peaks` + `load_peak_genes`)
- Pathway enrichment lollipop (`load_enrichment`)

Every line carries an inline comment. **Read the comments — they're the lesson.**
"""

INSTALL = """\
# One-line install: the genomics_course package + every dependency, straight
# from the course GitHub branch. Run this once per Colab session.
!pip install -q "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026"
"""

SETUP = """\
# === Setup ===
# Single source of truth for palette, fonts, and rcParams. Importing the theme
# registers IBM Plex Mono, defines the Economist palette (GREEN, BLUE, AMBER,
# RED, PURPLE + neutrals INK/CREAM/LINE/MUTED/GREY), and applies the cream-
# canvas matplotlib rcParams so every later figure inherits the look.
from genomics_course.theme import *

# Every loader we'll touch today.
from genomics_course.data import (
    load_anscombe, load_datasaurus,         # Why we visualise
    load_timecourse,                        # time-series
    load_coexpression,                      # scatter + fit
    load_deseq2,                            # volcano
    load_expression, load_expression_meta,  # PCA + clustermap
    load_admixture,                         # stacked bar
    load_peaks, load_peak_genes,            # peaks + gene model
    load_enrichment,                        # pathway enrichment
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches
import warnings; warnings.filterwarnings("ignore")

rng = np.random.default_rng(7)              # Day-1 seed
print("setup OK — palette:", [GREEN, BLUE, AMBER, RED, PURPLE])
"""

ANSCOMBE_MD = """\
## 1 · Anscombe's Quartet — Why We Visualise

Four datasets with identical mean, variance, correlation (0.816), and
regression line. Summary statistics alone hide the shape — plot first.
"""

ANSCOMBE = """\
# === Anscombe's Quartet ===
RED_LINE = "#D73A2B"                                    # regression line (off-theme, on purpose)
GOLD_PT  = "#DB9716"                                    # data points

ans = load_anscombe()                                   # dataset, x, y; 4 quartets

# 2x2 panel, shared axes so the *shape* is the only difference
fig, axes = plt.subplots(2, 2, figsize=(7, 4.6),
                         sharex=True, sharey=True, constrained_layout=True)

for ax, (dataset, g) in zip(axes.flat, ans.groupby("dataset")):
    m, b = np.polyfit(g["x"], g["y"], 1)                # linear fit slope + intercept
    xs = np.linspace(2, 20, 50)                         # smooth line domain
    ax.plot(xs, m * xs + b, color=RED_LINE, lw=1.8, zorder=2)
    ax.scatter(g["x"], g["y"], color=GOLD_PT, s=55, alpha=0.9,
               edgecolors="white", linewidths=0.6, zorder=3)
    ax.set_title(f"Dataset {dataset}", loc="left", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)

fig.supxlabel("x"); fig.supylabel("y")
plt.show()
"""

DATASAURUS_MD = """\
## 2 · Datasaurus Dozen — The Lesson, Extended

12 (well, 13) datasets with identical summary statistics, dramatically
different shapes. The dinosaur is the most famous.
"""

DATASAURUS = """\
# === Datasaurus ===
saurus = load_datasaurus()                              # dataset, x, y

# Twelve panels; iterate over the named groups
names = saurus["dataset"].unique()
fig, axes = plt.subplots(3, 5, figsize=(11, 6),
                         sharex=True, sharey=True, constrained_layout=True)
for ax, name in zip(axes.flat, names):
    g = saurus[saurus["dataset"] == name]
    ax.scatter(g["x"], g["y"], s=8, color=BLUE, alpha=0.7, linewidths=0)
    ax.set_title(name, loc="left", fontsize=9, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)

# hide unused axes if more cells than datasets
for ax in axes.flat[len(names):]:
    ax.set_visible(False)

fig.suptitle("Datasaurus dozen — same stats, different shapes", y=1.02)
plt.show()
"""

TIMECOURSE_MD = """\
## 3 · Time Course — Multi-Gene Line Plot with Error Bars

6 genes, 5 timepoints, mean ± SEM. Use `g["sem"]` (bracket access) — the
attribute `g.sem` returns the `DataFrame.sem()` method, not the column.
"""

TIMECOURSE = """\
# === Multi-gene time course ===
tc = load_timecourse()                                  # gene, time, tpm, sem
genes  = tc["gene"].unique()                            # 6 genes
colors = COURSE_PAL + ["#666666"]                       # 5 palette + 1 grey

fig, ax = plt.subplots(figsize=(8, 5))                  # CREATE

for color, gene in zip(colors, genes):
    g = tc[tc["gene"] == gene].sort_values("time")      # this gene's trajectory
    ax.errorbar(g["time"], g["tpm"],                    # CALL: line + error bars
                yerr=g["sem"],                          # ± SEM (bracket access!)
                marker="o", capsize=3, lw=2,
                color=color, label=gene)

ax.set_xlabel("time (h)")
ax.set_ylabel("TPM (transcripts per million)")
ax.set_title("Gene expression over time (mean ± SEM)")
ax.legend(frameon=False, title="gene",
          loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=6)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()
"""

DISTRIBUTIONS_MD = """\
## 4 · Distributions — Boxplot vs Violin

Synthetic teaching data (per the deck convention for pure illustration).
Boxplots show 5-number summary; violins add the density shape.
"""

DISTRIBUTIONS = """\
# === Distributions ===
# Three synthetic conditions — clean teaching example
groups = ["Control", "Drought", "Heat"]
data = [rng.normal(loc=10, scale=2.0, size=120),
        rng.normal(loc= 7, scale=2.5, size=120),
        rng.normal(loc= 8, scale=3.5, size=120)]
colors = [GREEN, BLUE, AMBER]

fig, (ax_box, ax_vio) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

# --- boxplot (left) ---
bp = ax_box.boxplot(data, patch_artist=True, widths=0.5)
for patch, c in zip(bp["boxes"], colors):
    patch.set_facecolor(c); patch.set_alpha(0.75); patch.set_edgecolor(INK)
for median in bp["medians"]: median.set_color(INK)
ax_box.set_xticks([1, 2, 3]); ax_box.set_xticklabels(groups)
ax_box.set_title("Boxplot"); ax_box.set_ylabel("expression (TPM)")
ax_box.spines[["top", "right"]].set_visible(False)

# --- violin (right) ---
parts = ax_vio.violinplot(data, showmedians=True, widths=0.7)
for body, c in zip(parts["bodies"], colors):
    body.set_facecolor(c); body.set_alpha(0.75); body.set_edgecolor(INK)
for k in ("cmedians", "cmins", "cmaxes", "cbars"):
    if k in parts: parts[k].set_color(INK)
ax_vio.set_xticks([1, 2, 3]); ax_vio.set_xticklabels(groups)
ax_vio.set_title("Violin")
ax_vio.spines[["top", "right"]].set_visible(False)

plt.tight_layout(); plt.show()
"""

SCATTER_FIT_MD = """\
## 5 · Scatter + Linear Fit (Co-expression)

`load_coexpression()` — 180 samples across 3 tissues, two correlated
genes. Scatter + linear fit + Pearson r in the title.
"""

SCATTER_FIT = """\
# === Scatter + linear fit ===
co = load_coexpression()                                # sample, tissue, gene_x, gene_y

fig, ax = plt.subplots(figsize=(6, 5))                  # CREATE

# 1. scatter every sample, colour by tissue
tissues = co["tissue"].unique()
for color, tissue in zip([GREEN, BLUE, AMBER], tissues):
    sub = co[co["tissue"] == tissue]                    # one tissue's samples
    ax.scatter(sub["gene_x"], sub["gene_y"], color=color,
               s=32, alpha=0.7, edgecolors="white",
               linewidths=0.5, label=tissue)

# 2. linear fit across all samples
m, b = np.polyfit(co["gene_x"], co["gene_y"], 1)        # slope + intercept
xs = np.linspace(co["gene_x"].min(), co["gene_x"].max(), 50)
ax.plot(xs, m * xs + b, color=RED, lw=1.8, ls="--", zorder=4)

# 3. Pearson r — annotate the headline
r = co[["gene_x", "gene_y"]].corr().iloc[0, 1]
ax.set_title(f"Gene X vs Gene Y — Pearson r = {r:.2f}")

ax.set_xlabel("Gene X (log2 TPM)")
ax.set_ylabel("Gene Y (log2 TPM)")
ax.legend(frameon=False, title="tissue")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

VOLCANO_MD = """\
## 6 · Volcano Plot (Differential Expression)

`load_deseq2()` — one row per gene, with `log2FoldChange`, `pvalue`,
`padj`. Top-right = significantly up, top-left = significantly down.
"""

VOLCANO = """\
# === Volcano plot ===
from adjustText import adjust_text                      # nudges labels apart

de = load_deseq2("drought").copy()                      # one row per gene
de["nlog10p"] = -np.log10(de["pvalue"])                 # significance axis

# Classify each gene by direction + significance
de["reg"] = np.where(
    (de["log2FoldChange"] >  1) & (de["padj"] < 0.05), "up",
    np.where((de["log2FoldChange"] < -1) & (de["padj"] < 0.05), "down", "ns"))

cm = {"up": RED, "down": GREEN, "ns": GREY}             # red up, green down, grey background

fig, ax = plt.subplots(figsize=(6.5, 5.5))              # CREATE
for state, grp in de.groupby("reg"):                    # plot each class
    ax.scatter(grp["log2FoldChange"], grp["nlog10p"],
               c=cm[state], s=28 if state != "ns" else 7,
               alpha=0.75 if state != "ns" else 0.3,
               linewidths=0, zorder=3 if state != "ns" else 1,
               label=state)

# threshold lines
ax.axhline(-np.log10(0.05), color=INK, lw=0.8, ls="--")
ax.axvline( 1, color=INK, lw=0.8, ls="--")
ax.axvline(-1, color=INK, lw=0.8, ls="--")

# label the top 6 hits — adjustText prevents overlap
hits = de[de["reg"] != "ns"].nsmallest(6, "padj")
texts = [ax.text(r["log2FoldChange"], r["nlog10p"], r["gene"],
                 fontsize=9, color=INK)
         for _, r in hits.iterrows()]
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5))

ax.set_xlabel("log2 fold change")
ax.set_ylabel(r"$-\\log_{10}(p)$")
ax.set_title(f"Drought vs Control — {len(de[de['reg']!='ns'])} significant genes")
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

PCA_MD = """\
## 7 · Dim Reduction — PCA on Expression

`load_expression()` is 40 genes × 24 samples. Transpose so samples are
rows, run PCA, plot PC1 vs PC2 coloured by condition.
"""

PCA = """\
# === PCA on expression ===
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

expr = load_expression()                                # 40 genes x 24 samples
meta = load_expression_meta().set_index("sample").loc[expr.columns]
X = expr.T.values                                       # samples become rows

# z-score per feature, then 2-component PCA
Xz = StandardScaler().fit_transform(X)
pcs = PCA(n_components=2).fit(Xz)
coords = pcs.transform(Xz)                              # (24, 2)

fig, ax = plt.subplots(figsize=(6.5, 5))                # CREATE
for color, condition in zip([BLUE, RED], ["Control", "Drought"]):
    mask = meta["condition"].values == condition
    ax.scatter(coords[mask, 0], coords[mask, 1],
               color=color, s=70, alpha=0.85,
               edgecolors="white", linewidths=0.7, label=condition)

# variance explained on axis labels
v1, v2 = pcs.explained_variance_ratio_
ax.set_xlabel(f"PC1 ({v1:.0%})")
ax.set_ylabel(f"PC2 ({v2:.0%})")
ax.set_title("PCA — control vs drought separates on PC1")
ax.axhline(0, color=LINE, lw=0.5); ax.axvline(0, color=LINE, lw=0.5)
ax.legend(frameon=False, title="condition")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

ADMIXTURE_MD = """\
## 8 · Admixture — Stacked Bar by Population

`load_admixture()` — 120 individuals × 5 K-components. Each column = one
individual (height always sums to 1); columns grouped by population.
"""

ADMIXTURE = """\
# === Admixture stacked bar ===
adm = load_admixture().copy()
K_cols = ["K1", "K2", "K3", "K4", "K5"]
pop_order = ["EUR", "EAS", "AFR", "AMR", "SAS"]

# sort within each population by dominant component, then by K1
adm["dominant"] = adm[K_cols].idxmax(axis=1)
adm = (adm.sort_values(["population", "dominant", "K1"], ascending=[True, True, False])
          .reset_index(drop=True))
adm["x"] = np.arange(len(adm))                          # bar x-position

fig, ax = plt.subplots(figsize=(11, 4.2))               # CREATE
bottom = np.zeros(len(adm))                             # running cumulative height
for K, color in zip(K_cols, COURSE_PAL):
    ax.bar(adm["x"], adm[K], bottom=bottom,             # CALL
           width=1.0, color=color, label=K, edgecolor="none")
    bottom += adm[K].to_numpy()

# population separators + labels
for pop in pop_order:
    sub = adm[adm["population"] == pop]
    if sub.empty: continue
    ax.axvline(sub["x"].max() + 0.5, color=INK, lw=0.5)
    ax.text(sub["x"].mean(), 1.04, pop, ha="center",
            color=MUTED, fontsize=10, fontweight="bold")

ax.set_xlim(-0.5, len(adm) - 0.5)
ax.set_ylim(0, 1.08)
ax.set_ylabel("ancestry proportion")
ax.set_xticks([])
ax.set_title("Admixture across 5 populations (sorted within each)")
ax.legend(ncol=5, frameon=False, title="component",
          loc="upper center", bbox_to_anchor=(0.5, -0.05))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

CLUSTERMAP_MD = """\
## 9 · Clustered Heatmap with Annotation

seaborn's `clustermap` gives row + column dendrograms and a coloured
sample annotation bar in 6 lines.
"""

CLUSTERMAP = """\
# === Clustered heatmap ===
expr = load_expression()                                # 40 genes x 24 samples
meta = load_expression_meta().set_index("sample").loc[expr.columns]
expr_z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1), axis=0)  # row z-score

# colour bar for the condition (column annotation)
col_colors = meta["condition"].map({"Control": BLUE, "Drought": RED})

g = sns.clustermap(
    expr_z,                                             # data: rows=gene, cols=sample
    cmap="RdBu_r", center=0,                            # diverging palette, centred at 0
    col_colors=col_colors,                              # sample condition bar
    row_cluster=True, col_cluster=True,                 # both dendrograms
    yticklabels=False,                                  # 40 row labels = too many
    figsize=(8, 6),
    cbar_kws={"label": "z-score"})
g.fig.suptitle("Drought vs Control — z-scored expression", y=1.02)
plt.show()
"""

WAFFLE_MD = """\
## 10 · Waffle / Waterfall — Composition with Discrete Squares

A 10x10 waffle = each square is 1%. Reach for it when the audience
should *count*, not estimate from angle.
"""

WAFFLE = """\
# === Waffle: ancestry composition for one population ===
from pywaffle import Waffle

adm = load_admixture()
K_cols = ["K1", "K2", "K3", "K4", "K5"]
eur_pct = (adm[adm["population"] == "EUR"][K_cols].mean() * 100).round().astype(int).to_dict()

fig = plt.figure(                                       # CREATE — pywaffle takes over
    FigureClass=Waffle,                                 # special incantation
    rows=10, columns=10,                                # 100 squares = exactly 1%/square
    values=eur_pct,                                     # K1..K5 percentages
    colors=[GREEN, BLUE, AMBER, RED, PURPLE],
    title={"label": "EUR — average ancestry composition",
           "loc": "left", "fontdict": {"fontsize": 12}},
    legend={"loc": "lower center", "bbox_to_anchor": (0.5, -0.1),
            "ncol": 5, "frameon": False},
    figsize=(8, 5))
plt.show()
"""

PEAKS_MD = """\
## 11 · Peak Tracks + Gene Model

`load_peaks()` (1000 positions, 3 ChIP/ATAC signals) +
`load_peak_genes()` (3 gene bodies + strand). Same x-axis = the contract.
"""

PEAKS = """\
# === Peak tracks + gene model ===
peaks = load_peaks(); genes = load_peak_genes()

fig, axes = plt.subplots(4, 1, figsize=(10, 6.5), sharex=True,
                         gridspec_kw=dict(height_ratios=[3, 3, 3, 1]))
ax_h3k27, ax_h3k4, ax_atac, ax_gene = axes

# three signal tracks
for ax, col, hue in [(ax_h3k27, "H3K27ac", RED),
                     (ax_h3k4,  "H3K4me3", BLUE),
                     (ax_atac,  "ATAC",    GREEN)]:
    ax.fill_between(peaks["position"], peaks[col],
                    color=hue, alpha=0.7, linewidth=0)
    ax.set_ylabel(col, color=hue, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)

# gene model — rectangle per gene + strand arrow
ax_gene.set_ylim(-0.5, 0.5); ax_gene.set_yticks([])
for _, g in genes.iterrows():
    ax_gene.add_patch(mpatches.Rectangle(
        (g["start"], -0.2), g["end"] - g["start"], 0.4,
        facecolor=PURPLE, edgecolor=INK, linewidth=0.6))
    if g["strand"] == "+":
        head = [(g["end"], -0.2), (g["end"] + 200, 0), (g["end"], 0.2)]
    else:
        head = [(g["start"], -0.2), (g["start"] - 200, 0), (g["start"], 0.2)]
    ax_gene.add_patch(mpatches.Polygon(head, facecolor=PURPLE,
                                       edgecolor=INK, linewidth=0.6))
    ax_gene.text((g["start"] + g["end"]) / 2, 0.6, g["name"],
                 ha="center", fontsize=9, color=INK)
ax_gene.set_xlabel("position (bp)")
ax_gene.spines[["top", "right", "left"]].set_visible(False)

plt.suptitle("ChIP-seq + ATAC + gene model", y=0.995)
plt.tight_layout(); plt.show()
"""

PATHWAY_MD = """\
## 12 · Pathway Enrichment — Lollipop Chart

`load_enrichment()` — 16 pathways with adjusted p-values + direction.
Lollipop = a horizontal bar's leaner cousin; dot at the tip carries
both significance (x) and gene count (size).
"""

PATHWAY = """\
# === Pathway enrichment lollipop ===
enr = load_enrichment().copy()
enr["mlog10p"] = -np.log10(enr["p_adj"])
enr = enr.sort_values("mlog10p")                        # bars ascending = strongest at top

fig, ax = plt.subplots(figsize=(8.5, 5.5))              # CREATE
colors = enr["direction"].map({"up": RED, "down": GREEN})

# lollipop = horizontal line + dot at the tip
ax.hlines(y=enr["pathway"], xmin=0, xmax=enr["mlog10p"],
          color=LINE, lw=1)                             # thin stem
ax.scatter(enr["mlog10p"], enr["pathway"],
           s=enr["gene_count"] * 4,                     # dot size = gene count
           c=colors, edgecolors=INK, linewidths=0.5, zorder=3)

# legend handles — direction colour + size scale
from matplotlib.lines import Line2D
handles = [Line2D([0], [0], marker="o", linestyle="", color=RED,   label="up"),
           Line2D([0], [0], marker="o", linestyle="", color=GREEN, label="down")]
ax.legend(handles=handles, frameon=False, title="direction",
          loc="lower right")

ax.set_xlabel(r"$-\\log_{10}(\\mathrm{adj.}\\ p)$")
ax.set_title("Pathway enrichment — drought response")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

CLOSER_MD = """\
## Done

That's the full set of Day-1 plots — every chart pulls from the bundled
`genomics_course` datasets, every figure uses the Economist palette + IBM
Plex Mono via `from genomics_course.theme import *`.

Read the slide deck (`day1.html`) for the **step-by-step builds**; this
notebook is the polished destination they walk you to.

**Up next:** `day2.ipynb` (genome-scale charts), `day3.ipynb` (production
packages).
"""

cells = [
    md(HEADER_MD),
    code(INSTALL),
    code(SETUP),
    md(ANSCOMBE_MD),       code(ANSCOMBE),
    md(DATASAURUS_MD),     code(DATASAURUS),
    md(TIMECOURSE_MD),     code(TIMECOURSE),
    md(DISTRIBUTIONS_MD),  code(DISTRIBUTIONS),
    md(SCATTER_FIT_MD),    code(SCATTER_FIT),
    md(VOLCANO_MD),        code(VOLCANO),
    md(PCA_MD),            code(PCA),
    md(ADMIXTURE_MD),      code(ADMIXTURE),
    md(CLUSTERMAP_MD),     code(CLUSTERMAP),
    md(WAFFLE_MD),         code(WAFFLE),
    md(PEAKS_MD),          code(PEAKS),
    md(PATHWAY_MD),        code(PATHWAY),
    md(CLOSER_MD),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path(__file__).parent / "day1.ipynb"
out.write_text(json.dumps(notebook, indent=2))
print(f"wrote {out}  ({out.stat().st_size:,} bytes, {len(cells)} cells)")
