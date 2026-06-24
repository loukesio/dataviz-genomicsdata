"""Build day3.ipynb from inline cell sources.

Run from the day3/ directory:
    python _build_ipynb.py

Produces day3.ipynb — a standalone Colab-ready notebook with one polished
"final version" per package. The slides walk students through the build
step by step; this notebook hands them the finished tool to play with.
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
# Genomics Data Visualization · Day 3

**Production-grade tools** — the runnable companion to the Day-3 deck. One
polished final example per package. Days 1-2 built every chart from
matplotlib primitives so you'd understand the mechanics; this notebook is
the destination: how the same plot looks when you let the right package
do the heavy lifting.

**How to use:**

1. Run the install cell once (~2 minutes on Colab — it pulls a lot).
2. Run the setup cell to import the theme + the bundled loaders.
3. Each cell below is **self-contained** — re-run any cell in any order.

The tools covered:

| # | Tool | What it does |
|---|---|---|
| 1a | seaborn heatmap | Simple z-scored heatmap, no clustering |
| 1b | PyComplexHeatmap | Clustered heatmap + row/col annotations |
| 2 | Toytree | Phylogenetic tree drawing |
| 3 | pyMSAviz | Multiple sequence alignment viewer |
| 4 | DashBio | Interactive Plotly bio widgets |
| 5 | pyGenomeTracks | Genome-browser tracks (CLI-driven) |
| 6 | dna_features_viewer | Gene maps + plasmid features |
| 7 | Synteny dot plot | matplotlib version of the JCVI / MCscan view |
| 8a | UpSetPlot | Set intersections (many sets) |
| 8b | matplotlib_venn | Venn diagram (2–3 sets) |
| 9 | PyWaffle | Waffle composition charts |
| 10 | gget | Gene / pathway lookups (network) |
| 11a | Bio.Phylo | matplotlib-native phylogenetic tree |
| 11b | Bio.Graphics | SVG plasmid diagram |

Every line has an inline comment. **Read the comments — they're the lesson.**
"""

INSTALL = """\
# One-line install: pulls every package today needs + their dependencies
# directly from the course GitHub branch. Run this once per Colab session.
# Coffee-break install — ~2 minutes on a fresh Colab kernel.
!pip install -q "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026" matplotlib-venn
"""

SETUP = """\
# === Setup — run once after the install above ===
# Single source of truth for palette, fonts, and rcParams.
from genomics_course.theme import *

from genomics_course.data import (
    load_deseq2, load_admixture, load_gwas, load_variants, load_lineages,
    load_timecourse, load_coexpression, load_expression, load_expression_meta,
    load_microbiome, load_peaks, load_peak_genes, load_qc, load_variant_classes,
    load_enrichment,
)

import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
import matplotlib.patches as mpatches
import warnings; warnings.filterwarnings("ignore")

rng = np.random.default_rng(23)             # day-3 seed
print("setup OK — palette:", [GREEN, BLUE, AMBER, RED, PURPLE])
"""

HEATMAP_SIMPLE_MD = """\
## 1a · Heatmap — Simple (seaborn)

Start with the bare-bones version: z-score by row, render with
`sns.heatmap`. No clustering, no annotation — just the matrix.
"""

HEATMAP_SIMPLE = """\
expr = load_expression()                                   # 40 genes x 24 samples
expr_z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(8, 5))                     # CREATE
sns.heatmap(                                               # CALL
    expr_z,                                                # row-z-scored matrix
    cmap="RdBu_r", center=0,                               # diverging palette centred at 0
    cbar_kws={"label": "z-score"},
    xticklabels=True, yticklabels=False,                   # too many genes to label
    linewidths=0, ax=ax)
ax.set_title("Expression z-score (40 genes × 24 samples)")
ax.set_xlabel("sample"); ax.set_ylabel("gene")
plt.tight_layout(); plt.show()
"""

HEATMAP_COMPLEX_MD = """\
## 1b · Heatmap — Complex (PyComplexHeatmap)

Now layer the things PyComplexHeatmap does in one call: row + column
dendrograms, a three-row sample annotation bar (condition / batch /
QC), and the diverging colour scale. Same data, paper-ready output.
"""

HEATMAP_COMPLEX = """\
import PyComplexHeatmap as pch

expr = load_expression()                                   # 40 genes x 24 samples
meta = load_expression_meta().set_index("sample").loc[expr.columns]
expr_z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1), axis=0)

# Three-row column annotation bar above the heatmap
col_ann = pch.HeatmapAnnotation(
    condition=pch.anno_simple(meta["condition"],
                              colors={"Control": BLUE, "Drought": RED}),
    batch=pch.anno_simple(meta["batch"],
                          colors={"A": AMBER, "B": GREEN, "C": PURPLE}),
    qc=pch.anno_simple(meta["qc"], cmap=econ_cmap("chicago")),
    axis=1, verbose=0)

# CREATE — ClusterMapPlotter draws into the *current* matplotlib figure;
# size it before calling, then plt.show() to flush it inline.
plt.figure(figsize=(9, 6))
pch.ClusterMapPlotter(                                     # CALL — clustering + annot + legend
    data=expr_z,
    top_annotation=col_ann,
    row_cluster=True, col_cluster=True,
    cmap="RdBu_r",
    show_rownames=False, show_colnames=True,
    label="z-score", verbose=0)
plt.show()
"""

TOYTREE_MD = """\
## 3 · Toytree — Phylogenetic Tree with Highlighted Clade

A balanced 9-leaf Newick tree, one clade spotlighted in red.
"""

TOYTREE = """\
import toytree

newick = ("((((A:1.2,B:1.5):2.1,(C:0.9,D:1.7):1.8):3.0,"
          "(E:2.3,F:1.6):2.7):1.5,((G:1.9,H:2.0):2.3,I:3.5):1.4);")
tre = toytree.tree(newick)

# spotlight the (A,B,C,D) clade
try:
    mrca = tre.get_mrca_node("A", "B", "C", "D")
    clade_idx = {n.idx for n in mrca.get_descendants()} | {mrca.idx}
except AttributeError:                                     # older toytree
    mrca_idx = tre.get_mrca_idx_from_tip_labels(names=["A","B","C","D"])
    mrca = tre.idx_dict[mrca_idx]
    clade_idx = {n.idx for n in mrca.get_descendants()} | {mrca.idx}

edge_colors = [RED if n.idx in clade_idx else GREY         # one colour per node
               for n in tre.treenode.traverse()]

canvas, axes, mark = tre.draw(                             # CREATE+CALL (Toyplot, not matplotlib)
    width=520, height=420,
    tip_labels_align=True,
    edge_colors=edge_colors,
    edge_widths=2.2,
    node_sizes=0)
canvas
"""

PYMSAVIZ_MD = """\
## 4 · pyMSAviz — Production MSA Viewer

Synthetic 8 × 60 alignment, colored with the Clustal scheme, with
consensus + count tracks and one highlighted region.
"""

PYMSAVIZ = """\
import tempfile, os
from pymsaviz import MsaViz

# 1. build a synthetic alignment (FASTA on disk)
ALPHABET = np.array(list("ACGT"))
N_SEQ, N_COL = 8, 60
base = rng.choice(ALPHABET, N_COL)
aln  = np.tile(base, (N_SEQ, 1)).astype("<U1")
for i in range(1, N_SEQ):
    mask = rng.random(N_COL) < 0.05                        # 5% mutation rate
    aln[i, mask] = rng.choice(ALPHABET, mask.sum())
aln[4, 22:27] = "-"                                        # insert one gap region

fa_path = os.path.join(tempfile.gettempdir(), "demo_msa.fasta")
with open(fa_path, "w") as fh:                              # write to /tmp
    for i, row in enumerate(aln, start=1):
        fh.write(f">seq{i}\\n{''.join(row)}\\n")

# 2. render via pyMSAviz
mv = MsaViz(fa_path,
            color_scheme="Nucleotide",                     # built-in base colour scheme
            wrap_length=60,                                # one row, full width
            show_consensus=True,                           # consensus letter row at top
            show_count=True)                               # column count on the right
mv.set_highlight_pos([(23, 27)])                           # box the gap region (1-indexed)
mv.plotfig()                                               # CALL — returns matplotlib Figure
plt.show()
"""

DASHBIO_MD = """\
## 5 · DashBio — Interactive Manhattan & Volcano

One-line widgets. Returned object is a Plotly Figure; hover for SNP/gene IDs.
"""

DASHBIO = """\
import dash_bio as dashbio
import numpy as np

gwas = load_gwas("height")                                 # tidy GWAS table
fig = dashbio.ManhattanPlot(
    dataframe=gwas,
    chrm="chrom", bp="pos", p="pval", snp="snp", gene=None,
    genomewideline_value=-np.log10(5e-8),
    suggestiveline_value=-np.log10(1e-5),
    highlight_color=RED,
    point_size=6,
    title="Height GWAS — interactive")
fig.update_layout(                                          # match deck theme
    paper_bgcolor=CREAM, plot_bgcolor=CREAM,
    font=dict(family="IBM Plex Mono", color=INK, size=11),
    height=420, margin=dict(l=10, r=10, t=40, b=10))
fig
"""

PYGENOMETRACKS_MD = """\
## 6 · pyGenomeTracks — Multi-track Genome-Browser Figure

This package is CLI-first; the cell below shows a pure-Python equivalent
multi-track plot, plus the canonical INI workflow for when you have real
BED/BigWig/BedGraph files.
"""

PYGENOMETRACKS = """\
# pyGenomeTracks CLI workflow (commented — needs files + the CLI on PATH):
#
#   $ cat > /tmp/tracks.ini <<'INI'
#   [peaks]
#   file = peaks.bedgraph
#   title = H3K27ac
#   color = #B4405F
#   [genes]
#   file = genes.bed
#   title = genes
#   INI
#   $ pyGenomeTracks --tracks /tmp/tracks.ini --region "chr1:0-20000" \\
#                     --outFileName fig.png
#
# Below: an equivalent matplotlib-native multi-track figure built from the
# bundled load_peaks() + load_peak_genes(). Same shape, no CLI needed.

peaks = load_peaks(); genes = load_peak_genes()
fig, axes = plt.subplots(4, 1, figsize=(10, 6.5), sharex=True,
                         gridspec_kw=dict(height_ratios=[3, 3, 3, 1]))
ax_h3k27, ax_h3k4, ax_atac, ax_gene = axes
for ax, col, hue in [(ax_h3k27, "H3K27ac", RED),
                     (ax_h3k4, "H3K4me3", BLUE),
                     (ax_atac, "ATAC",    GREEN)]:
    ax.fill_between(peaks["position"], peaks[col], color=hue, alpha=0.7, linewidth=0)
    ax.set_ylabel(col, color=hue, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
ax_gene.set_ylim(-0.5, 0.5); ax_gene.set_yticks([])
for _, g in genes.iterrows():
    ax_gene.add_patch(mpatches.Rectangle(
        (g["start"], -0.2), g["end"] - g["start"], 0.4,
        facecolor=PURPLE, edgecolor=INK, linewidth=0.6))
    ax_gene.text((g["start"] + g["end"]) / 2, 0.6, g["name"],
                 ha="center", fontsize=9, color=INK)
ax_gene.set_xlabel("position (bp)")
ax_gene.spines[["top", "right", "left"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

DNAVIEWER_MD = """\
## 7 · dna_features_viewer — Gene Map of a 5 kb Plasmid

Linear gene map with strand arrows. Trivial to read, paper-ready.
"""

DNAVIEWER = """\
from dna_features_viewer import GraphicFeature, GraphicRecord

features = [
    GraphicFeature(start=  50, end= 900, strand=+1, color=GREEN,  label="geneA"),
    GraphicFeature(start=1100, end=1900, strand=+1, color=BLUE,   label="geneB"),
    GraphicFeature(start=2200, end=3000, strand=-1, color=AMBER,  label="geneC"),
    GraphicFeature(start=3200, end=3900, strand=+1, color=RED,    label="geneD"),
    GraphicFeature(start=4100, end=4900, strand=-1, color=PURPLE, label="geneE"),
]

record = GraphicRecord(sequence_length=5000, features=features)
ax, _ = record.plot(figure_width=11)                       # CREATE+CALL in one
ax.set_title("Demo plasmid (5 kb) — 5 genes")
plt.show()
"""

JCVI_MD = """\
## 8 · Synteny Dot Plot (matplotlib)

A dot plot is the canonical way to look at synteny between two genomes:
x = gene index in genome A, y = gene index in genome B. Anchors fall on
the diagonal when order is conserved, flip onto the antidiagonal under
an inversion, and scatter off the line for translocations or duplications.

The full **JCVI / MCscan** pipeline (FASTA → LAST → `.anchors` →
`jcvi.graphics.dotplot`) renders the same picture from real anchor files
— pip-install `jcvi` and call `jcvi.graphics.dotplot.dotplot(anchorfile,
qbed, sbed, fig, root, ax)` once you have one. Here we draw the same
plot from primitives so the cell runs without the LAST binary.
"""

JCVI = """\
# === Synteny dot plot (pure matplotlib) ===
# Three block types, one per colour:
#   collinear (grey) — same gene index in both genomes
#   inversion (red)  — genome B index runs backwards over a window
#   duplication (blue) — one A gene maps to two B positions

N = 50
collinear = [(i, i) for i in range(N) if not (20 <= i < 30)]   # most of the genome
inversion = [(i, 49 - i) for i in range(20, 30)]               # window 20-30 flips
duplicate = [(i, i + 30) for i in range(5, 10)]                # 5 extra hits, off-diagonal

fig, ax = plt.subplots(figsize=(6, 6))                          # CREATE
xs, ys = zip(*collinear); ax.scatter(xs, ys, color=GREY, s=22, label="syntenic")
xs, ys = zip(*inversion); ax.scatter(xs, ys, color=RED, s=36, label="inversion")
xs, ys = zip(*duplicate); ax.scatter(xs, ys, color=BLUE, s=36, label="duplication")

ax.set_xlim(-1, N); ax.set_ylim(-1, N)
ax.set_xlabel("gene index — Genome A")
ax.set_ylabel("gene index — Genome B")
ax.set_title("Synteny dot plot — collinear + 1 inversion + 1 duplication")
ax.legend(frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.set_aspect("equal")
plt.tight_layout(); plt.show()
"""

UPSET_MD = """\
## 9 · UpSetPlot — Five-Set Gene Membership

The matrix below the bar chart replaces a 5-way Venn that no one can read.
"""

UPSET = """\
from upsetplot import UpSet, from_indicators

# build five overlapping gene sets — 200 genes, ~40% inclusion per set
genes = [f"G{i:03d}" for i in range(200)]
sets  = ["DE", "Leaf", "Root", "Photo", "Stress"]
df    = pd.DataFrame(
    {s: rng.random(200) < 0.4 for s in sets},              # boolean membership
    index=genes)

mat = from_indicators(sets, data=df)                       # transform for UpSet
up  = UpSet(mat,
            sort_by="cardinality",                         # biggest intersection first
            show_counts=True,                              # label every bar
            facecolor=GREEN)                               # primary colour
up.plot()                                                  # CALL — UpSetPlot draws several axes
plt.show()
"""

VENN_MD = """\
## 9b · Venn Diagram — 3-Set Overlap

UpSet scales to many sets; **Venn** is the canonical view for 2 or 3.
Past 3 sets the regions become unreadable, so use it sparingly — but
for the classic "what's shared between three groups" question, nothing
beats it for instant pattern recognition. Uses `matplotlib_venn`.
"""

VENN = """\
# install once per Colab session if matplotlib_venn isn't already there:
#   !pip install -q matplotlib-venn
from matplotlib_venn import venn3, venn3_circles

# build three gene sets from the same indicator frame as the UpSet cell
genes = [f"G{i:03d}" for i in range(200)]
sets  = ["DE", "Photo", "Stress"]                              # three sets only
df    = pd.DataFrame({s: rng.random(200) < 0.4 for s in sets}, index=genes)
gene_sets = {s: set(df.index[df[s]]) for s in sets}            # name -> set of genes

fig, ax = plt.subplots(figsize=(6.5, 5))                       # CREATE
v = venn3(                                                     # CALL — fills regions
    [gene_sets["DE"], gene_sets["Photo"], gene_sets["Stress"]],
    set_labels=("DE", "Photo", "Stress"),
    set_colors=(GREEN, BLUE, AMBER),
    alpha=0.55, ax=ax)
venn3_circles(                                                 # outline pass for crisp edges
    [gene_sets["DE"], gene_sets["Photo"], gene_sets["Stress"]],
    color=INK, linewidth=0.8, ax=ax)

# bump the count labels into INK so they read on the cream canvas
for label in (v.subset_labels or []):
    if label is not None:
        label.set_color(INK); label.set_fontsize(11)
for label in v.set_labels:
    label.set_color(INK); label.set_fontsize(12); label.set_fontweight("bold")

ax.set_title("Gene overlap across three pathway categories")
plt.tight_layout(); plt.show()
"""

PYWAFFLE_MD = """\
## 10 · PyWaffle — One Waffle per Population

5 populations, 100 squares each (= percentage). Eye counts the K
components without doing maths.
"""

PYWAFFLE = """\
from pywaffle import Waffle

adm = load_admixture()
K_cols = ["K1", "K2", "K3", "K4", "K5"]
pops = ["EUR", "AFR", "EAS", "SAS", "AMR"]
pop_mean = adm.groupby("population")[K_cols].mean().loc[pops]
pop_pct  = (pop_mean * 100).round().astype(int)

panels = {                                                 # one sub-waffle per population
    150 + i + 1: {                                         # integer subplot code (1 row, 5 cols, slot i+1)
        "values": pop_pct.loc[p].to_dict(),
        "title":  {"label": p, "loc": "left", "fontsize": 12},
    }
    for i, p in enumerate(pops)
}

fig = plt.figure(                                          # CREATE — pywaffle draws
    FigureClass=Waffle,
    plots=panels,
    rows=5, columns=10,                                    # 50 squares per panel
    colors=[GREEN, BLUE, AMBER, RED, PURPLE],
    figsize=(11, 3),
    legend={"loc": "lower center", "bbox_to_anchor": (0.5, -0.4),
            "ncol": 5, "frameon": False})
plt.show()
"""

GGET_MD = """\
## 11 · gget — Pathway Enrichment Bar Chart (offline-safe)

The pathway-enrichment result is **cached as a literal** below so this cell
runs offline. To refresh from Enrichr, uncomment the `gget.enrichr(...)` line.
"""

GGET = """\
# import gget                       # uncomment + run live for fresh data
# enr = gget.enrichr(["BRCA1","TP53","EGFR","MYC","KRAS"], "KEGG_2021_Human")

# cached top-10 KEGG hits (so the cell renders without network)
enr = pd.DataFrame({
    "pathway":   ["Pathways in cancer", "Endocrine resistance",
                  "PI3K-Akt signaling", "Cell cycle",
                  "p53 signaling", "MicroRNAs in cancer",
                  "FoxO signaling", "Glioma",
                  "Breast cancer", "ErbB signaling"],
    "adj_pval":  [1.2e-9, 3.4e-7, 2.1e-6, 5.8e-6,
                  7.9e-6, 1.1e-5, 2.0e-5, 3.3e-5, 4.2e-5, 6.1e-5],
    "overlap":   ["5/520", "4/98", "5/354", "4/124",
                  "3/72", "4/299", "3/132", "3/75", "3/147", "3/85"],
})
enr["mlog10"] = -np.log10(enr["adj_pval"])
enr = enr.sort_values("mlog10")                            # bars ascending = top at the right

fig, ax = plt.subplots(figsize=(8, 4.5))                   # CREATE
ax.barh(enr["pathway"], enr["mlog10"],                     # CALL — horizontal bars
        color=GREEN, edgecolor="white", linewidth=0.5)
for i, (path, m, ov) in enumerate(zip(enr["pathway"], enr["mlog10"], enr["overlap"])):
    ax.text(m + 0.15, i, ov, va="center", fontsize=9, color=MUTED)
ax.set_xlabel(r"$-\\log_{10}(\\mathrm{adj.}\\ p)$")
ax.set_title("KEGG enrichment — 5 cancer driver genes (cached)")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.show()
"""

BIOPY_TREE_MD = """\
## 12a · Biopython — Bio.Phylo Tree (matplotlib)

Read a Newick tree and draw it onto matplotlib axes.  Compact, no
extra dependencies beyond biopython itself.
"""

BIOPY_TREE = """\
from io import StringIO
from Bio import Phylo

# tiny synthesised tree with 9 leaves and 4 internal clades
newick = ("((((A:1.2,B:1.5):2.1,(C:0.9,D:1.7):1.8):3.0,"
          "(E:2.3,F:1.6):2.7):1.5,((G:1.9,H:2.0):2.3,I:3.5):1.4);")
tree = Phylo.read(StringIO(newick), "newick")

fig, ax = plt.subplots(figsize=(7, 4.2))                   # CREATE
Phylo.draw(tree, axes=ax, do_show=False)                   # CALL — draws onto ax
ax.set_title("Bio.Phylo — matplotlib tree")
plt.show()
"""

BIOPY_PLASMID_MD = """\
## 12b · Biopython — Bio.Graphics Plasmid (SVG)

`Bio.Graphics.GenomeDiagram` builds publication-quality plasmid maps.
The PNG backend requires `rlPyCairo` (which itself needs a Cairo system
library), so we write **SVG** instead — universal, scalable, no compile
step.  Same diagram, no install pain.
"""

BIOPY_PLASMID = """\
from pathlib import Path
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, SimpleLocation
from Bio.Graphics import GenomeDiagram
from IPython.display import SVG

# 5-kb pseudo-plasmid with five labelled genes (mixed strands)
record = SeqRecord(Seq("N" * 5000), id="plasmid")
gene_spans = [(  50,  900, +1, "geneA", GREEN),
              (1100, 1900, +1, "geneB", BLUE),
              (2200, 3000, -1, "geneC", AMBER),
              (3200, 3900, +1, "geneD", RED),
              (4100, 4900, -1, "geneE", PURPLE)]
for s, e, strand, name, _ in gene_spans:
    record.features.append(SeqFeature(
        SimpleLocation(s, e, strand=strand),
        type="gene", qualifiers={"label": [name]}))

gd  = GenomeDiagram.Diagram("toy plasmid")                 # CREATE
trk = gd.new_track(1, name="genes", greytrack=False,
                   scale_largetick_interval=1000)
fs  = trk.new_set()
for (s, e, strand, name, hue), feat in zip(gene_spans, record.features):
    fs.add_feature(feat, color=hue, label=True,
                   sigil="ARROW", label_size=10, label_angle=0)

out = Path("biopy_plasmid.svg")
gd.draw(format="circular", circular=True,
        pagesize=(800, 800), start=0, end=5000, circle_core=0.6)
gd.write(str(out), "SVG")                                  # SVG bypasses the PNG backend
SVG(filename=str(out))
"""

CLOSER_MD = """\
## Done

That's the full Day-3 set. Each package wraps the matplotlib primitives
you learned in days 1-2 into a one-call API. Reach for the package when
the chart is canonical for the field; reach for matplotlib when you need
the control.

Read the slide deck (`day3.html`) for the full step-by-step builds and
the "compare with" notes at each takeaway.
"""

cells = [
    md(HEADER_MD),
    code(INSTALL),
    code(SETUP),
    md(HEATMAP_SIMPLE_MD),   code(HEATMAP_SIMPLE),
    md(HEATMAP_COMPLEX_MD),  code(HEATMAP_COMPLEX),
    md(TOYTREE_MD),          code(TOYTREE),
    md(PYMSAVIZ_MD),         code(PYMSAVIZ),
    md(DASHBIO_MD),          code(DASHBIO),
    md(PYGENOMETRACKS_MD),   code(PYGENOMETRACKS),
    md(DNAVIEWER_MD),        code(DNAVIEWER),
    md(JCVI_MD),             code(JCVI),
    md(UPSET_MD),            code(UPSET),
    md(VENN_MD),             code(VENN),
    md(PYWAFFLE_MD),         code(PYWAFFLE),
    md(GGET_MD),             code(GGET),
    md(BIOPY_TREE_MD),       code(BIOPY_TREE),
    md(BIOPY_PLASMID_MD),    code(BIOPY_PLASMID),
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

out = Path(__file__).parent / "day3.ipynb"
out.write_text(json.dumps(notebook, indent=2))
print(f"wrote {out}  ({out.stat().st_size:,} bytes, {len(cells)} cells)")
