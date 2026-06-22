"""Build day2.ipynb from inline cell sources.

Run from the day2/ directory:
    python _build_ipynb.py

Produces day2.ipynb — a standalone Colab-ready notebook with one polished
"final version" per topic. The slides walk students through the build
step by step; the notebook hands them the finished tool to play with.
"""
from __future__ import annotations
import json
from pathlib import Path

# ---------------------------------------------------------------- helpers ----
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

# ----------------------------------------------------------------- cells ----
HEADER_MD = """\
# Genomics Data Visualization · Day 2

**Genome-scale charts & comparative views** — the runnable companion to the
Day-2 deck. Each section gives you the *final, polished* version of a chart
the slides built step by step.

**How to use this notebook:**

1. Run the install cell once (it takes ~1 minute on Colab).
2. Run the setup cell to import everything.
3. Each chart cell is self-contained — you can rerun any of them in any order.

The Day-2 sections covered here:

- Stacked bar plots — admixture composition across populations
- Time series — gene expression trajectories with uncertainty
- Multiple sequence alignment (MSA) — colored conservation grid
- Manhattan plots — GWAS results genome-wide
- Genome stats — coverage QC, peak tracks, gene models
- pyCirclize — circular genome plots
- Synteny — comparing two genomes with ribbons

Every line has an inline comment. **Read the comments — they're the lesson.**
"""

INSTALL = """\
# One-line install: pulls the genomics_course package + all its dependencies
# (matplotlib, pandas, seaborn, plotly, pyCirclize, biopython, ...) directly
# from the course GitHub branch. Run this once per Colab session.
!pip install -q "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026"
"""

SETUP = """\
# === Setup ===
# Single source of truth for palette, fonts, and rcParams. Importing the
# theme registers IBM Plex Mono, defines the Economist palette (GREEN, BLUE,
# AMBER, RED, PURPLE + neutrals INK/CREAM/LINE/MUTED/GREY), and applies the
# cream-canvas matplotlib rcParams so every later figure inherits the look.
from genomics_course.theme import *

# Loaders bundled with the package — no network calls needed.
from genomics_course.data import (
    load_gwas,        # GWAS height: chrom, pos, pval, snp
    load_admixture,   # individual, population, K1..K5
    load_qc,          # sample, raw, callable, loss
    load_peaks,       # position, H3K27ac, H3K4me3, ATAC
    load_peak_genes,  # name, start, end, strand
    load_timecourse,  # gene, time, tpm, sem
)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches            # for synteny ribbons
import warnings
warnings.filterwarnings("ignore")

rng = np.random.default_rng(11)                  # day-2 seed
print("setup OK — palette:", [GREEN, BLUE, AMBER, RED, PURPLE])
"""

STACKED_BAR_MD = """\
## 1 · Stacked Bar — Admixture

Each column is one individual; the column height (always 1.0) is split into
five K components. Sort within each population, then stack to reveal who is
"pure" and who is admixed.
"""

STACKED_BAR = """\
# === Stacked bar: admixture ===
adm = load_admixture().copy()                          # one row per individual
K_cols = ["K1", "K2", "K3", "K4", "K5"]                # the five components
pop_order = ["EUR", "EAS", "AFR", "AMR", "SAS"]        # left-to-right populations

# sort individuals within each population by their dominant component, then by K1
adm["dominant"] = adm[K_cols].idxmax(axis=1)           # which K is biggest
adm = (adm.sort_values(["population", "dominant", "K1"], ascending=[True, True, False])
          .reset_index(drop=True))
adm["x"] = np.arange(len(adm))                         # bar x-position

fig, ax = plt.subplots(figsize=(11, 4.2))              # CREATE: wide canvas
bottom = np.zeros(len(adm))                            # running cumulative height

for K, color in zip(K_cols, COURSE_PAL):               # one stack layer per K
    ax.bar(adm["x"], adm[K],                           # CALL: bars at every x
           bottom=bottom,                              # start where previous stack ended
           width=1.0, color=color, label=K,
           edgecolor="none")
    bottom += adm[K].to_numpy()                        # update for next layer

# population separators + labels
for pop in pop_order:
    sub = adm[adm["population"] == pop]
    if sub.empty:
        continue
    ax.axvline(sub["x"].max() + 0.5, color=INK, lw=0.5)    # vertical separator
    ax.text(sub["x"].mean(), 1.04, pop, ha="center",       # population label
            color=MUTED, fontsize=10, fontweight="bold")

ax.set_xlim(-0.5, len(adm) - 0.5)                      # tight x-range
ax.set_ylim(0, 1.08)                                   # room for top labels
ax.set_ylabel("ancestry proportion")
ax.set_xticks([])                                      # no per-individual ticks
ax.set_title("Admixture across 5 populations (sorted within each)")
ax.legend(ncol=5, frameon=False, title="component",
          loc="upper center", bbox_to_anchor=(0.5, -0.05))
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()
"""

TIMESERIES_MD = """\
## 2 · Time Series — Gene Expression with Uncertainty

Six genes, five timepoints, mean ± SEM as a ribbon. Bracket access on
`g["sem"]` is mandatory — `g.sem` returns the DataFrame method, not the
column!
"""

TIMESERIES = """\
# === Time series: gene expression ± SEM ===
tc = load_timecourse()                                  # gene, time, tpm, sem
genes  = tc["gene"].unique()                            # 6 genes
colors = COURSE_PAL + ["#666666"]                       # 5 palette + 1 grey

fig, ax = plt.subplots(figsize=(8, 5))                  # CREATE

for color, gene in zip(colors, genes):
    g = tc[tc["gene"] == gene].sort_values("time")      # this gene's trajectory
    # central line + ribbon for ± SEM
    ax.plot(g["time"], g["tpm"], color=color, lw=2, marker="o",  # CALL
            markersize=5, label=gene, zorder=3)
    ax.fill_between(g["time"],                          # ribbon span
                    g["tpm"] - g["sem"],
                    g["tpm"] + g["sem"],
                    color=color, alpha=0.18, zorder=2)

ax.set_xlabel("time (h)")
ax.set_ylabel("TPM (transcripts per million)")
ax.set_title("Gene expression over time (mean ± SEM)")
ax.legend(frameon=False, title="gene",
          loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=6)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()
"""

MSA_MD = """\
## 3 · MSA — Colored Conservation Grid

A small synthetic alignment (8 sequences × 60 columns) with one inserted
gap region. Letters are colored by identity, with a conservation track
above so the eye lands on interesting columns immediately.
"""

MSA = """\
# === MSA: synthetic alignment + conservation track ===
ALPHABET = np.array(list("ACGT"))                       # bases we sample from
N_SEQ, N_COL = 8, 60                                    # alignment dimensions

# 1. build a base sequence + 7 mutants (5% mutation rate)
base = rng.choice(ALPHABET, N_COL)                      # ancestral sequence
aln  = np.tile(base, (N_SEQ, 1)).astype("<U1")          # start identical
for i in range(1, N_SEQ):                               # mutate all but row 0
    mask = rng.random(N_COL) < 0.05                     # 5% sites flip
    aln[i, mask] = rng.choice(ALPHABET, mask.sum())     # to a random base
aln[4, 22:27] = "-"                                     # insert a gap in row 4

# 2. colour map (DNA: identity-encoded; gap is grey)
PAL_BASE = {"A": GREEN, "C": BLUE, "G": AMBER, "T": RED, "-": GREY}
encode   = {b: i for i, b in enumerate("ACGT-")}
img = np.vectorize(encode.get)(aln).astype(float)       # numerical for imshow

from matplotlib.colors import ListedColormap
cmap = ListedColormap([PAL_BASE[b] for b in "ACGT-"])

# 3. conservation per column: fraction of most-common non-gap letter
def conservation(col):
    no_gap = col[col != "-"]
    if len(no_gap) == 0:
        return 0
    _, counts = np.unique(no_gap, return_counts=True)
    return counts.max() / len(no_gap)
cons = np.array([conservation(aln[:, c]) for c in range(N_COL)])

# 4. two-panel layout: conservation on top, alignment below
fig, (ax_top, ax) = plt.subplots(2, 1, figsize=(11, 4.2),
                                  gridspec_kw={"height_ratios": [1, 4]},
                                  sharex=True)
ax_top.bar(np.arange(N_COL), cons, color=PURPLE, width=1.0)   # conservation
ax_top.set_ylim(0, 1.05); ax_top.set_yticks([0, 1])
ax_top.set_ylabel("cons.", rotation=0, ha="right", va="center", fontsize=9, color=MUTED)
ax_top.spines[["top", "right"]].set_visible(False)

ax.imshow(img, aspect="auto", cmap=cmap, interpolation="nearest")  # heatmap
for r in range(N_SEQ):                                  # overlay letters in white
    for c in range(N_COL):
        ax.text(c, r, aln[r, c], ha="center", va="center",
                color="white", fontsize=8, fontweight="bold")

ax.set_yticks(range(N_SEQ))
ax.set_yticklabels([f"seq{i+1}" for i in range(N_SEQ)], fontsize=9)
ax.set_xlabel("column")
plt.tight_layout()
plt.show()
"""

MANHATTAN_MD = """\
## 4 · Manhattan — GWAS Hits Genome-Wide

22 chromosomes laid end-to-end via cumulative position, alternating
colours so the eye separates them, two threshold lines, hits painted red
on top and labelled with their rsID.
"""

MANHATTAN = """\
# === Manhattan plot: GWAS height ===
gwas = load_gwas("height").sort_values(["chrom", "pos"]).copy()
gwas["nlog10p"] = -np.log10(gwas["pval"])               # significance axis

# 1. cumulative x-position: chr2 starts where chr1 ended, ...
chrom_len = gwas.groupby("chrom")["pos"].max()
offsets   = chrom_len.cumsum().shift(fill_value=0)
gwas["cum_pos"] = gwas["pos"] + gwas["chrom"].map(offsets)

# 2. alternating colour per chromosome (parity)
palette = {True: BLUE, False: GREEN}
gwas["color"] = (gwas["chrom"] % 2 == 0).map(palette)

# 3. plot
fig, ax = plt.subplots(figsize=(11, 4.5))               # CREATE: wide canvas
ax.scatter(gwas["cum_pos"], gwas["nlog10p"],            # background cloud
           c=gwas["color"], s=6, alpha=0.55, linewidths=0)

# 4. threshold lines
ax.axhline(-np.log10(5e-8), color=RED,   lw=.9, ls="--")   # genome-wide
ax.axhline(-np.log10(1e-5), color=AMBER, lw=.9, ls="--")   # suggestive

# 5. spotlight the hits
hits = gwas[gwas["pval"] < 5e-8]
ax.scatter(hits["cum_pos"], hits["nlog10p"],
           color=RED, s=42, edgecolor="white", linewidths=0.6, zorder=5)
for _, row in hits.nsmallest(3, "pval").iterrows():     # label top 3
    ax.annotate(row["snp"], (row["cum_pos"], row["nlog10p"]),
                xytext=(5, 5), textcoords="offset points", fontsize=8)

# 6. tick at each chromosome midpoint
tick_pos = offsets + chrom_len / 2
ax.set_xticks(tick_pos); ax.set_xticklabels(chrom_len.index, fontsize=8)
ax.set_xlabel("chromosome")
ax.set_ylabel(r"$-\\log_{10}(p)$")
ax.set_title(f"Height GWAS — {len(hits)} genome-wide significant SNPs")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.show()
"""

GENOME_STATS_MD = """\
## 5 · Genome Stats — Peak Tracks + Gene Model

Three ChIP/ATAC tracks share an x-axis with a gene model below. Same
contract as a paper figure: aligned axes tell a positional story.
"""

GENOME_STATS = """\
# === Genome stats: peak tracks + gene model ===
peaks = load_peaks()             # position, H3K27ac, H3K4me3, ATAC
genes = load_peak_genes()        # name, start, end, strand

# 4 vertical panels, shared x-axis (positional alignment is the contract)
fig, axes = plt.subplots(4, 1, figsize=(10, 6.5), sharex=True,
                         gridspec_kw=dict(height_ratios=[3, 3, 3, 1]))
ax_h3k27, ax_h3k4, ax_atac, ax_gene = axes

# track 1 — H3K27ac filled area, RED
ax_h3k27.fill_between(peaks["position"], peaks["H3K27ac"],
                      color=RED, alpha=0.7, linewidth=0)
ax_h3k27.set_ylabel("H3K27ac", color=RED, fontsize=9)

# track 2 — H3K4me3 filled area, BLUE
ax_h3k4.fill_between(peaks["position"], peaks["H3K4me3"],
                     color=BLUE, alpha=0.7, linewidth=0)
ax_h3k4.set_ylabel("H3K4me3", color=BLUE, fontsize=9)

# track 3 — ATAC filled area, GREEN
ax_atac.fill_between(peaks["position"], peaks["ATAC"],
                     color=GREEN, alpha=0.7, linewidth=0)
ax_atac.set_ylabel("ATAC", color=GREEN, fontsize=9)

# track 4 — gene model: a rectangle per gene + strand arrowhead
ax_gene.set_ylim(-0.5, 0.5)
ax_gene.set_yticks([])
for _, g in genes.iterrows():
    body = mpatches.Rectangle((g["start"], -0.2), g["end"] - g["start"], 0.4,
                              facecolor=PURPLE, edgecolor=INK, linewidth=0.6)
    ax_gene.add_patch(body)
    # arrowhead in strand direction
    if g["strand"] == "+":
        head = [(g["end"], -0.2), (g["end"] + 200, 0), (g["end"], 0.2)]
    else:
        head = [(g["start"], -0.2), (g["start"] - 200, 0), (g["start"], 0.2)]
    ax_gene.add_patch(mpatches.Polygon(head, facecolor=PURPLE,
                                        edgecolor=INK, linewidth=0.6))
    ax_gene.text((g["start"] + g["end"]) / 2, 0.6, g["name"],
                 ha="center", fontsize=9, color=INK)

ax_gene.set_xlabel("position (bp)")
ax_gene.set_ylabel("genes", color=MUTED, fontsize=9)

for ax in axes[:-1]:
    ax.spines[["top", "right"]].set_visible(False)
ax_gene.spines[["top", "right", "left"]].set_visible(False)

plt.suptitle("ChIP-seq + ATAC + gene model", y=0.995, fontsize=12)
plt.tight_layout()
plt.show()
"""

CIRCOS_MD = """\
## 6 · pyCirclize — Manhattan on a Ring with Chord Links

Same GWAS data, bent into a circle. SNP density on the outer track, hits
in red, and chords connecting the top hits across chromosomes.
"""

CIRCOS = """\
# === Circular plot: pyCirclize ===
from pycirclize import Circos                          # circular genome library

gwas = load_gwas("height").copy()                      # same table as Manhattan
gwas["nlog10p"] = -np.log10(gwas["pval"])
chrom_len = gwas.groupby("chrom")["pos"].max().to_dict()
sectors = {f"chr{c}": chrom_len[c] for c in sorted(chrom_len)}
gw_thresh = -np.log10(5e-8)

# CREATE the ring with 2deg gaps between sectors
circos = Circos(sectors, space=2)

for sector in circos.sectors:                          # iterate as list
    name = sector.name
    sector.text(name, r=108, size=8, color=INK)        # chromosome label (outside)
    sector.axis(fc=CREAM, ec=INK, lw=0.6)              # outer rim line

    # data track between radii 60-90 — the SNP cloud
    track = sector.add_track((60, 90))
    chrom_num = int(name.replace("chr", ""))
    df = gwas[gwas["chrom"] == chrom_num]
    track.scatter(df["pos"].to_numpy(), df["nlog10p"].to_numpy(),
                  s=1.5, color=GREY, alpha=0.6)        # background cloud

    # red hits — only draw if non-empty (most chroms have none)
    hits = df[df["pval"] < 5e-8]
    if not hits.empty:
        track.scatter(hits["pos"].to_numpy(), hits["nlog10p"].to_numpy(),
                      s=10, color=RED, alpha=0.95)

    # threshold ring at -log10(5e-8)
    track.line([0, chrom_len[chrom_num]], [gw_thresh, gw_thresh],
               color=RED, lw=0.6, ls="--")

# chord links between consecutive top-5 hits (different chromosomes)
top5 = gwas.nsmallest(5, "pval").reset_index(drop=True)
for i in range(len(top5) - 1):
    a, b = top5.iloc[i], top5.iloc[i + 1]
    if a["chrom"] == b["chrom"]:
        continue                                       # skip intra-chrom
    circos.link((f"chr{a['chrom']}", int(a['pos']) - 1, int(a['pos']) + 1),
                (f"chr{b['chrom']}", int(b['pos']) - 1, int(b['pos']) + 1),
                color=PURPLE, alpha=0.55)

fig = circos.plotfig(figsize=(7, 7))                   # CALL: returns matplotlib Figure
plt.show()
"""

SYNTENY_MD = """\
## 7 · Synteny — Ribbons Between Two Genomes

Two chromosomes drawn as horizontal tracks. Coloured polygons connect
homologous regions: grey = conserved (SYN), amber = inversion (INV),
blue = translocation (TRANS).
"""

SYNTENY = """\
# === Synteny ribbons between two genomes ===
# Synthetic comparison: chr_A and chr_B, each 100 Mb. Hand-crafted blocks
# show every type a real comparison surfaces.
blocks = pd.DataFrame([
    # SYN — same order, same strand
    dict(chrA_start= 5, chrA_end=20, chrB_start= 7, chrB_end=22, type="SYN"),
    dict(chrA_start=22, chrA_end=35, chrB_start=24, chrB_end=37, type="SYN"),
    dict(chrA_start=60, chrA_end=78, chrB_start=64, chrB_end=82, type="SYN"),
    dict(chrA_start=83, chrA_end=95, chrB_start=85, chrB_end=97, type="SYN"),
    # INV — same range, flipped strand (chrB_start > chrB_end)
    dict(chrA_start=38, chrA_end=52, chrB_start=55, chrB_end=40, type="INV"),
    # TRANS — block at different positions in chrA vs chrB
    dict(chrA_start=53, chrA_end=58, chrB_start= 1, chrB_end= 6, type="TRANS"),
])

COLOUR = {"SYN": GREY, "INV": AMBER, "TRANS": BLUE}
TOP_Y, BOT_Y, H = 1.0, 0.0, 0.06                       # chromosome lane y/heights

fig, ax = plt.subplots(figsize=(11, 4))                # CREATE

# 1. chromosome lanes — two grey rectangles
for y, name in [(TOP_Y, "Genome A"), (BOT_Y, "Genome B")]:
    ax.add_patch(mpatches.Rectangle((0, y), 100, H,    # 100 Mb wide bar
                                     facecolor=LINE, edgecolor=INK, lw=0.5))
    ax.text(-2, y + H/2, name, ha="right", va="center",
            fontsize=10, fontweight="bold", color=INK)

# 2. synteny ribbons — one Polygon per block
for _, row in blocks.iterrows():
    # vertex order (clockwise): top-left, top-right, bottom-right, bottom-left
    verts = [
        (row["chrA_start"], TOP_Y),                    # top-left
        (row["chrA_end"],   TOP_Y),                    # top-right
        (row["chrB_end"],   BOT_Y + H),                # bottom-right (note: H lifts ribbon to top of lower lane)
        (row["chrB_start"], BOT_Y + H),                # bottom-left
    ]
    ax.add_patch(mpatches.Polygon(verts, closed=True,
                                   facecolor=COLOUR[row["type"]],
                                   edgecolor="none", alpha=0.55))

# 3. legend + frame polish
ax.legend(handles=[mpatches.Patch(color=COLOUR[t], label=t) for t in COLOUR],
          loc="upper center", bbox_to_anchor=(0.5, -0.05),
          frameon=False, ncol=3, title="block type")
ax.set_xlim(-8, 105); ax.set_ylim(-0.15, 1.25)
ax.set_xticks(range(0, 101, 20))
ax.set_xticklabels([f"{x} Mb" for x in range(0, 101, 20)], fontsize=9)
ax.set_yticks([])
ax.set_title("Synteny: Genome A vs Genome B")
ax.spines[["top", "right", "left"]].set_visible(False)
plt.tight_layout()
plt.show()
"""

CLOSER_MD = """\
## Done

That's the full set of Day-2 plots. Every chart pulls from the bundled
`genomics_course` datasets, every line is annotated, every figure follows
the Economist palette + IBM Plex Mono via `from genomics_course.theme import *`.

Read the slide deck (`day2.html`) for the step-by-step builds; this notebook
is the polished destination they walk you to.
"""

# --------------------------------------------------------------- assemble ----
cells = [
    md(HEADER_MD),
    code(INSTALL),
    code(SETUP),
    md(STACKED_BAR_MD),    code(STACKED_BAR),
    md(TIMESERIES_MD),     code(TIMESERIES),
    md(MSA_MD),            code(MSA),
    md(MANHATTAN_MD),      code(MANHATTAN),
    md(GENOME_STATS_MD),   code(GENOME_STATS),
    md(CIRCOS_MD),         code(CIRCOS),
    md(SYNTENY_MD),        code(SYNTENY),
    md(CLOSER_MD),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = Path(__file__).parent / "day2.ipynb"
out.write_text(json.dumps(notebook, indent=2))
print(f"wrote {out}  ({out.stat().st_size:,} bytes, {len(cells)} cells)")
