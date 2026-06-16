"""
genomics_course.plots
─────────────────────
Style-guaranteed plotting functions. The course theme is applied on import,
so every figure these produce is consistent — no improvisation.

    from genomics_course.data import load_admixture
    from genomics_course.plots import plot_admixture
    fig = plot_admixture(load_admixture(K=5))
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from ..theme import COLORS, ANCESTRY, save  # noqa: F401  (applies theme on import)


# ════════════════════════════════════════════════════════════════
# ADMIXTURE
# ════════════════════════════════════════════════════════════════

def plot_admixture(df, k_cols=None, title="ADMIXTURE  ANALYSIS"):
    """Stacked ancestry-proportion bar plot.

    df: columns = individual, population, K1..Kn
    """
    if k_cols is None:
        k_cols = [c for c in df.columns if c.startswith("K")]
    K = len(k_cols)
    pops = df["population"].tolist()
    props = df[k_cols].to_numpy()
    n = len(df)

    fig, ax = plt.subplots(figsize=(12, 3.8))
    x = np.arange(n)
    bottom = np.zeros(n)
    for k in range(K):
        ax.bar(x, props[:, k], bottom=bottom, width=1.0,
               color=ANCESTRY[k % len(ANCESTRY)], edgecolor="none")
        bottom += props[:, k]

    # population separators + labels
    boundaries, labels, start = [], [], 0
    order = list(dict.fromkeys(pops))
    for p in order:
        size = pops.count(p)
        if start > 0:
            ax.axvline(start - 0.5, color="white", linewidth=1.5, zorder=3)
        ax.text(start + size / 2, -0.07, p, ha="center", va="top",
                fontsize=11, fontweight="bold", color=COLORS["text_dark"],
                transform=ax.get_xaxis_transform())
        start += size

    fig.suptitle(f"{title}  ( K = {K} )", fontsize=14, fontweight="bold",
                 color=COLORS["text_dark"], y=0.98)
    legend = [Patch(facecolor=ANCESTRY[k % len(ANCESTRY)], label=k_cols[k])
              for k in range(K)]
    leg = ax.legend(handles=legend, loc="upper right", frameon=False,
                    fontsize=8.5, ncol=K, bbox_to_anchor=(1.0, 1.16),
                    handlelength=1.2, handletextpad=0.4, columnspacing=1.0)
    for t in leg.get_texts():
        t.set_color(COLORS["text_mid"])

    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.5, 1.0])
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.set_ylabel("Ancestry\nproportion", fontsize=9.5, color=COLORS["text_mid"])
    ax.spines["bottom"].set_visible(False)
    plt.subplots_adjust(top=0.82, bottom=0.10)
    return fig


# ════════════════════════════════════════════════════════════════
# VOLCANO (DESeq2)
# ════════════════════════════════════════════════════════════════

def plot_volcano(df, lfc_thresh=1.0, padj_thresh=0.05, title="DIFFERENTIAL  EXPRESSION"):
    """Volcano plot. df: log2FoldChange, padj columns."""
    lfc = df["log2FoldChange"].to_numpy()
    padj = df["padj"].to_numpy().clip(1e-300)
    neglog = -np.log10(padj)

    sig_p = padj < padj_thresh
    sig_fc = np.abs(lfc) > lfc_thresh
    color = np.full(len(df), COLORS["text_light"], dtype=object)
    color[sig_fc & ~sig_p] = COLORS["secondary"]
    color[sig_p & ~sig_fc] = COLORS["tertiary"]
    color[sig_fc & sig_p] = COLORS["primary"]

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.scatter(lfc, neglog, c=color, s=14, alpha=0.7, edgecolors="none")
    ax.axhline(-np.log10(padj_thresh), color=COLORS["zero_line"], lw=0.8, ls="--")
    ax.axvline(lfc_thresh, color=COLORS["zero_line"], lw=0.8, ls="--")
    ax.axvline(-lfc_thresh, color=COLORS["zero_line"], lw=0.8, ls="--")

    fig.suptitle(title, fontsize=14, fontweight="bold", color=COLORS["text_dark"])
    ax.set_xlabel("log\u2082 fold change", fontsize=11, color=COLORS["text_mid"])
    ax.set_ylabel("\u2212log\u2081\u2080 adjusted p", fontsize=11, color=COLORS["text_mid"])
    legend = [Patch(facecolor=COLORS["primary"], label="significant"),
              Patch(facecolor=COLORS["secondary"], label="FC only"),
              Patch(facecolor=COLORS["tertiary"], label="p only"),
              Patch(facecolor=COLORS["text_light"], label="NS")]
    leg = ax.legend(handles=legend, loc="upper center", frameon=False,
                    fontsize=8.5, ncol=4, bbox_to_anchor=(0.5, 1.06))
    for t in leg.get_texts():
        t.set_color(COLORS["text_mid"])
    plt.subplots_adjust(top=0.88)
    return fig


# ════════════════════════════════════════════════════════════════
# MANHATTAN (GWAS)
# ════════════════════════════════════════════════════════════════

def plot_manhattan(df, threshold=5e-8, title="GWAS  —  GENOME-WIDE  ASSOCIATION"):
    """Manhattan plot. df: chrom, pos, pval columns."""
    df = df.sort_values(["chrom", "pos"]).reset_index(drop=True)
    df["neglog"] = -np.log10(df["pval"].clip(1e-300))

    x, ticks, labels, offset = [], [], [], 0
    colors = []
    for c in sorted(df["chrom"].unique()):
        sub = df[df["chrom"] == c]
        xs = np.arange(len(sub)) + offset
        x.extend(xs)
        colors.extend([COLORS["secondary"] if c % 2 == 0 else COLORS["text_light"]] * len(sub))
        ticks.append(offset + len(sub) / 2)
        labels.append(str(c))
        offset += len(sub) + 200

    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.scatter(x, df["neglog"], c=colors, s=6, edgecolors="none")
    ax.axhline(-np.log10(threshold), color=COLORS["primary"], lw=1.0, ls="--")
    ax.text(offset, -np.log10(threshold), "  genome-wide significance",
            color=COLORS["primary"], fontsize=8, va="center")

    fig.suptitle(title, fontsize=14, fontweight="bold", color=COLORS["text_dark"])
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, fontsize=7, color=COLORS["text_light"])
    ax.set_xlabel("chromosome", fontsize=10, color=COLORS["text_mid"])
    ax.set_ylabel("\u2212log\u2081\u2080 p", fontsize=11, color=COLORS["text_mid"])
    ax.set_xlim(-200, offset)
    plt.subplots_adjust(top=0.9)
    return fig


# ════════════════════════════════════════════════════════════════
# LLD BAR (variant effects)
# ════════════════════════════════════════════════════════════════

def plot_lld(df, title="LOG-LIKELIHOOD  DIFFERENCE"):
    """Horizontal LLD bar chart. df: gene, variant, lld, classification."""
    labels = [f"{r.gene} {r.variant}" for r in df.itertuples()]
    vals = df["lld"].to_numpy()
    cls = df["classification"].tolist()
    y = np.arange(len(df))[::-1]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(y, vals, height=0.52, color=[COLORS[c] for c in cls], edgecolor="none")
    ax.axvline(0, color=COLORS["zero_line"], lw=0.8)

    for i, v in enumerate(vals):
        if v < -80:
            ax.text(v + 5, y[i], f"{v:.2f}", ha="left", va="center",
                    fontsize=10.5, fontweight="bold", color="white")
        elif v < 0:
            ax.text(v + 5, y[i], f"{v:.2f}", ha="left", va="center",
                    fontsize=9.5, color=COLORS["text_mid"])
        else:
            ax.plot(v, y[i], "o", color=COLORS[cls[i]], markersize=8)
            ax.text(v + 6, y[i], f"+{v:.2f}", ha="left", va="center",
                    fontsize=9.5, color=COLORS["text_mid"])

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10.5, color=COLORS["text_dark"])
    for i, c in enumerate(cls):
        ax.annotate(c, xy=(0, y[i]), xycoords=("axes fraction", "data"),
                    xytext=(-10, -13), textcoords="offset points",
                    fontsize=8.5, color=COLORS[c], ha="right", va="top",
                    annotation_clip=False)
    fig.suptitle(title, fontsize=14, fontweight="bold", color=COLORS["text_dark"], y=0.97)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-360, 360)
    plt.subplots_adjust(left=0.22, top=0.88)
    return fig


__all__ = ["plot_admixture", "plot_volcano", "plot_manhattan", "plot_lld", "save"]
