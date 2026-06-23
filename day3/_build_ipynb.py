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

The 12 packages covered:

| # | Package | What it does |
|---|---|---|
| 1 | PyComplexHeatmap | Clustered heatmaps with row/col annotations |
| 2 | pyCirclize | Circular genome plots (also day-2 _06) |
| 3 | Toytree | Phylogenetic tree drawing |
| 4 | pyMSAviz | Multiple sequence alignment viewer |
| 5 | DashBio | Interactive Plotly bio widgets |
| 6 | pyGenomeTracks | Genome-browser tracks (CLI-driven) |
| 7 | dna_features_viewer | Gene maps + plasmid features |
| 8 | JCVI / MCscan | Synteny + comparative graphics |
| 9 | UpSetPlot | Set intersections |
| 10 | PyWaffle | Waffle composition charts |
| 11 | gget | Gene / pathway lookups (network) |
| 12 | Biopython (Phylo + Graphics) | Tree IO + feature diagrams |

Every line has an inline comment. **Read the comments — they're the lesson.**
"""

INSTALL = """\
# One-line install: pulls every package today needs + their dependencies
# directly from the course GitHub branch. Run this once per Colab session.
# Coffee-break install — ~2 minutes on a fresh Colab kernel.
!pip install -q "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026"
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

PYCOMPLEXHEATMAP_MD = """\
## 1 · PyComplexHeatmap — Clustered Heatmap with Annotations

40 genes × 24 samples. Annotation bars for condition, batch, and QC.
One call replaces a 50-line manual sns.clustermap + annotation rig.
"""

PYCOMPLEXHEATMAP = """\
import PyComplexHeatmap as pch

expr = load_expression()                                   # 40 genes x 24 samples
meta = load_expression_meta().set_index("sample").loc[expr.columns]
expr_z = expr.sub(expr.mean(axis=1), axis=0).div(expr.std(axis=1), axis=0)  # row z-score

# Column annotation: three rows stacked above the heatmap
col_ann = pch.HeatmapAnnotation(
    condition=pch.anno_simple(meta["condition"],
                              colors={"Control": BLUE, "Drought": RED}),
    batch=pch.anno_simple(meta["batch"],
                          colors={"A": AMBER, "B": GREEN, "C": PURPLE}),
    qc=pch.anno_simple(meta["qc"], cmap=econ_cmap("chicago")),
    axis=1, verbose=0)

fig = plt.figure(figsize=(9, 6))                           # CREATE the canvas
pch.ClusterMapPlotter(                                     # CALL — clustering + annot + legend in one
    data=expr_z,                                           # z-scored matrix
    top_annotation=col_ann,                                # the 3-row annotation
    row_cluster=True, col_cluster=True,                    # both dendrograms on
    cmap="RdBu_r",                                         # diverging palette
    show_rownames=False, show_colnames=True,               # 40 row names = too many
    label="z-score",                                       # colorbar title
    verbose=0)
plt.show()
"""

CIRCOS_MD = """\
## 2 · pyCirclize — Manhattan on a Ring (compact recap of day-2 _06)

Same GWAS data, bent into a circle.
"""

CIRCOS = """\
from pycirclize import Circos

gwas = load_gwas("height").copy()
gwas["nlog10p"] = -np.log10(gwas["pval"])
chrom_len = gwas.groupby("chrom")["pos"].max().to_dict()
sectors = {f"chr{c}": chrom_len[c] for c in sorted(chrom_len)}
gw_thresh = -np.log10(5e-8)

circos = Circos(sectors, space=2)                          # CREATE
for sector in circos.sectors:                              # circos.sectors is a list
    name = sector.name
    sector.text(name, r=108, size=8, color=INK)
    sector.axis(fc=CREAM, ec=INK, lw=0.6)
    track = sector.add_track((60, 90))                     # data band radii 60-90
    chrom_num = int(name.replace("chr", ""))
    df = gwas[gwas["chrom"] == chrom_num]
    track.scatter(df["pos"].to_numpy(), df["nlog10p"].to_numpy(),
                  s=1.5, color=GREY, alpha=0.6)
    hits = df[df["pval"] < 5e-8]
    if not hits.empty:                                     # most chroms have no hits
        track.scatter(hits["pos"].to_numpy(), hits["nlog10p"].to_numpy(),
                      s=10, color=RED, alpha=0.95)
    track.line([0, chrom_len[chrom_num]], [gw_thresh, gw_thresh],
               color=RED, lw=0.6, ls="--")

# top-5 hits → chord links across chromosomes
top5 = gwas.nsmallest(5, "pval").reset_index(drop=True)
for i in range(len(top5) - 1):
    a, b = top5.iloc[i], top5.iloc[i + 1]
    if a["chrom"] == b["chrom"]:
        continue
    circos.link((f"chr{a['chrom']}", int(a['pos']) - 1, int(a['pos']) + 1),
                (f"chr{b['chrom']}", int(b['pos']) - 1, int(b['pos']) + 1),
                color=PURPLE, alpha=0.55)

fig = circos.plotfig(figsize=(7, 7))                       # CALL
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
## 8 · JCVI / MCscan — Synteny Dot Plot

Synthesised anchor file with one inversion + one duplication. JCVI's
graphics module renders the canonical dot plot.
"""

JCVI = """\
import tempfile, os
from jcvi.graphics.dotplot import dotplot

tmp = tempfile.mkdtemp()
bed1 = os.path.join(tmp, "a.bed")
bed2 = os.path.join(tmp, "b.bed")
anchors = os.path.join(tmp, "ab.anchors")

# tiny synthetic genomes — 50 genes each, single chromosome
with open(bed1, "w") as f:
    for i in range(50):
        f.write(f"chrA\\t{i*100}\\t{i*100+90}\\tg{i:03d}\\t0\\t+\\n")
with open(bed2, "w") as f:
    for i in range(50):
        f.write(f"chrB\\t{i*100}\\t{i*100+90}\\tg{i:03d}\\t0\\t+\\n")

# anchors: collinear, inversion (20-30 reversed), duplication
with open(anchors, "w") as f:
    f.write("###\\n")
    for i in range(50):
        if 20 <= i < 30:
            f.write(f"g{i:03d}\\tg{49-i:03d}\\t100\\n")     # inversion
        else:
            f.write(f"g{i:03d}\\tg{i:03d}\\t100\\n")
    for i in range(5, 10):
        f.write(f"g{i:03d}\\tg{i+30:03d}\\t100\\n")        # duplication

dotplot(anchors, bed1, bed2,                               # CALL
        image_name=os.path.join(tmp, "dot.png"), iopts=None)
from IPython.display import Image
Image(filename=os.path.join(tmp, "dot.png"))
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

BIOPY_MD = """\
## 12 · Biopython — Phylo tree + GenomeDiagram plasmid (SVG)

Two demos in one cell: a matplotlib phylogenetic tree, then a circular
plasmid diagram written to SVG (since the PNG backend requires rlPyCairo
which isn't always available).
"""

BIOPY = """\
from io import StringIO
from pathlib import Path
from Bio import Phylo
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, SimpleLocation
from Bio.Graphics import GenomeDiagram
from IPython.display import SVG

# --- Phylo: matplotlib-native tree ---
newick = "((((A:1.2,B:1.5):2.1,(C:0.9,D:1.7):1.8):3.0," \\
         "(E:2.3,F:1.6):2.7):1.5,((G:1.9,H:2.0):2.3,I:3.5):1.4);"
tree = Phylo.read(StringIO(newick), "newick")

fig, ax = plt.subplots(figsize=(7, 4))                     # CREATE on matplotlib
Phylo.draw(tree, axes=ax, do_show=False)                   # CALL — draws onto ax
ax.set_title("Bio.Phylo — matplotlib tree")
plt.show()

# --- Bio.Graphics: plasmid diagram (SVG) ---
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
gd.write(str(out), "SVG")                                  # SVG — no rlPyCairo needed
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
    md(PYCOMPLEXHEATMAP_MD), code(PYCOMPLEXHEATMAP),
    md(CIRCOS_MD),           code(CIRCOS),
    md(TOYTREE_MD),          code(TOYTREE),
    md(PYMSAVIZ_MD),         code(PYMSAVIZ),
    md(DASHBIO_MD),          code(DASHBIO),
    md(PYGENOMETRACKS_MD),   code(PYGENOMETRACKS),
    md(DNAVIEWER_MD),        code(DNAVIEWER),
    md(JCVI_MD),             code(JCVI),
    md(UPSET_MD),            code(UPSET),
    md(PYWAFFLE_MD),         code(PYWAFFLE),
    md(GGET_MD),             code(GGET),
    md(BIOPY_MD),            code(BIOPY),
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
