"""Plot CATALOG + per-library BASE_THEME helpers.

Mirror of PlotR's ``R/specs.R``.  Each catalog entry has both a **strict** spec
(near-verbatim code from the course, with column names as the deck uses them)
and a **loose** spec (prose conventions the LLM can adapt to a new dataset).

Why both?  Strict mode is a fast path for the exact teaching example — the
LLM essentially fills in the dataset name and returns.  Loose mode unlocks
the LLM to apply the chart *idea* to a different DataFrame, which is what
students reach for once they leave the course examples behind.

Every entry also carries:

- ``library`` — one of matplotlib / seaborn / plotnine / plotly
- ``interactive`` — True only for plotly variants meant to be hovered/zoomed
- ``day`` — 1, 2, or 3 (matches the course deck the plot was extracted from)
- ``summary`` — a single sentence shown to the LLM during plot selection

The four ``apply_base_theme_*`` helpers below are what makes a figure look
"on-deck" regardless of which library produced it: cream canvas, IBM Plex
Mono, no top/right spines, dashed grid where it earns its keep.

Source of truth for palette + rcParams: the course's
``genomics_course/theme.py`` (Economist colour system).  The constants below
duplicate the hex values so PlotPy stays runnable without the course package
installed.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

# --------------------------------------------------------------------- palette
# Mirror of genomics_course.theme — kept in sync by hand so PlotPy installs
# standalone.  Update both when the course palette changes.

GREEN = "#379A8B"   # primary story colour
BLUE = "#006BA2"    # secondary
AMBER = "#EBB434"   # secondary
RED = "#B4405F"     # highlight (up / pathogenic)
PURPLE = "#9A607F"  # highlight

GREY = "#B3B3B3"    # de-emphasis
INK = "#0D0D0D"     # near-black text/axis
CREAM = "#FAF9F7"   # warm canvas
LINE = "#D9D9D9"    # hairlines
MUTED = "#666666"   # secondary text

COURSE_PAL = [GREEN, BLUE, AMBER, RED, PURPLE]

# Fonts: try IBM Plex Mono, fall back to a monospace already on most systems.
FONT_FAMILY = "IBM Plex Mono, DejaVu Sans Mono, monospace"


# --------------------------------------------------------------- theme appliers
def apply_base_theme_mpl(ax: Any) -> Any:
    """Apply BASE_THEME to a matplotlib Axes.

    Centred bold title, cream canvas, no top/right spines, dashed minor grid.
    Mutates ``ax`` and returns it for chaining.
    """
    import matplotlib.pyplot as plt

    fig = ax.figure
    fig.patch.set_facecolor(CREAM)
    ax.set_facecolor(CREAM)

    # title weight + font (only if a title was set already)
    title = ax.get_title()
    if title:
        ax.set_title(title, fontweight="bold", color=INK, loc="center")

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(LINE)

    ax.tick_params(colors=MUTED)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)

    ax.grid(True, which="major", color=LINE, linestyle="--", linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)

    plt.rcParams["font.family"] = FONT_FAMILY
    return ax


def apply_base_theme_sns(g: Any) -> Any:
    """Apply BASE_THEME to a seaborn figure-level grid (FacetGrid, ClusterGrid, …).

    Walks every Axes the grid exposes and runs :func:`apply_base_theme_mpl`.
    Returns the grid object for chaining.
    """
    # ClusterGrid: heatmap axis is .ax_heatmap; FacetGrid: .axes is a 2D ndarray.
    axes = []
    if hasattr(g, "ax_heatmap"):
        axes.append(g.ax_heatmap)
    elif hasattr(g, "axes"):
        flat = getattr(g.axes, "flat", None)
        axes.extend(list(flat) if flat is not None else [g.axes])
    elif hasattr(g, "ax"):
        axes.append(g.ax)

    for ax in axes:
        apply_base_theme_mpl(ax)
    return g


def apply_base_theme_p9(p: Any) -> Any:
    """Apply BASE_THEME to a plotnine ggplot.

    Returns a new ``p + theme(...)`` (plotnine plots are immutable — the
    addition operator produces a new instance).
    """
    from plotnine import element_blank, element_line, element_rect, element_text, theme

    return p + theme(
        figure_size=(6, 4),
        plot_background=element_rect(fill=CREAM, color=CREAM),
        panel_background=element_rect(fill=CREAM, color=CREAM),
        panel_grid_major=element_line(color=LINE, linetype="dashed", size=0.4),
        panel_grid_minor=element_blank(),
        axis_line=element_line(color=LINE, size=0.5),
        axis_text=element_text(color=MUTED, family=FONT_FAMILY.split(",")[0].strip()),
        axis_title=element_text(color=MUTED, family=FONT_FAMILY.split(",")[0].strip()),
        plot_title=element_text(
            face="bold",
            color=INK,
            family=FONT_FAMILY.split(",")[0].strip(),
            ha="center",
        ),
        legend_position="none",
    )


def apply_base_theme_plotly(fig: Any) -> Any:
    """Apply BASE_THEME to a plotly Figure.  Returns ``fig`` for chaining."""
    fig.update_layout(
        template="simple_white",
        paper_bgcolor=CREAM,
        plot_bgcolor=CREAM,
        font=dict(family=FONT_FAMILY, color=INK, size=12),
        title=dict(x=0.5, xanchor="center", font=dict(color=INK, size=14)),
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    fig.update_xaxes(gridcolor=LINE, gridwidth=0.5, griddash="dash", zerolinecolor=LINE)
    fig.update_yaxes(gridcolor=LINE, gridwidth=0.5, griddash="dash", zerolinecolor=LINE)
    return fig


# -------------------------------------------------------------- catalog entry
class CatalogEntry(TypedDict):
    """One plot in :data:`CATALOG`."""

    library: Literal["matplotlib", "seaborn", "plotnine", "plotly"]
    interactive: bool
    day: int
    summary: str
    strict: str
    loose: str


# Every strict template assumes:
#   - ``df`` is a pandas DataFrame already in the exec namespace
#   - ``np``, ``pd``, ``plt``, ``sns``, ``px``, ``go`` are imported as needed
#     by the agent based on ``library``.
#   - The palette constants (GREEN, BLUE, AMBER, RED, PURPLE, GREY, INK, CREAM,
#     LINE, MUTED, COURSE_PAL) are pre-injected from this module.
#
# Loose templates speak in conventions, not code — they tell the LLM what
# the chart *means* and which aesthetics to keep, then trust it to adapt
# the column names to whatever ``df`` actually carries.

CATALOG: dict[str, CatalogEntry] = {
    # ============================================================ DAY 1 ====
    "timecourse_line": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Gene expression over time — one line per gene, markers at timepoints, error bars or ribbon for SEM.",
        strict="""
# df: gene, time, tpm, sem
fig, ax = plt.subplots(figsize=(7.4, 4.6))
genes  = df["gene"].unique()
colors = COURSE_PAL + [GREY]
for color, gene in zip(colors, genes):
    g = df[df["gene"] == gene].sort_values("time")
    ax.errorbar(g["time"], g["tpm"], yerr=g["sem"],
                marker="o", capsize=3, lw=2, color=color, label=gene)
ax.set_xlabel("time (h)")
ax.set_ylabel("TPM")
ax.set_title("Gene expression over time (mean ± SEM)")
ax.legend(frameon=False, title="gene", loc="upper center",
          bbox_to_anchor=(0.5, -0.12), ncol=6)
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Line plot of a numeric trajectory across a continuous predictor.
- x = time-like column (continuous, increasing)
- y = response measurement (continuous)
- one line per categorical grouping column, in COURSE_PAL order
- if there is an uncertainty column (sem / sd / ci), show it as error bars or fill_between
- legend below the axes when more than 4 groups
Use ax.errorbar with markers; suppress top/right spines.
""",
    ),
    "timecourse_line_interactive": dict(
        library="plotly",
        interactive=True,
        day=1,
        summary="Interactive time course — hover for gene, sample, value; click legend to toggle traces.",
        strict="""
# df: gene, time, tpm, sem
import plotly.express as px
fig = px.line(df, x="time", y="tpm", color="gene", markers=True,
              color_discrete_sequence=COURSE_PAL + [GREY],
              error_y="sem",
              hover_data={"sem": ":.2f"},
              labels={"time": "time (h)", "tpm": "TPM"},
              title="Gene expression over time")
fig.update_layout(template="simple_white", paper_bgcolor=CREAM, plot_bgcolor=CREAM)
p = fig
""",
        loose="""
Same idea as the static version, but hovers reveal exact y at each x.
- color discrete by group; one trace per group
- error_y supplied when an SEM/SD column exists
- markers=True so individual timepoints are tappable
Default to plotly express; finish with template='simple_white'.
""",
    ),
    "bar_simple": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Sorted horizontal bar — one bar per category, highlight one bar in RED.",
        strict="""
# df: tissue, tpm
te = df.sort_values("tpm")
colors = [RED if t == "Heart" else GREY for t in te["tissue"]]
fig, ax = plt.subplots(figsize=(6.2, 4.4))
ax.barh(te["tissue"], te["tpm"], color=colors)
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
ax.tick_params(left=False)
ax.grid(axis="x", alpha=.3, lw=.6); ax.set_axisbelow(True)
ax.bar_label(ax.containers[0], padding=6, color=INK, fontsize=10)
ax.set_xlim(0, max(100, te["tpm"].max() * 1.1))
fig.suptitle("BRCA1 is highest in heart tissue", fontsize=13, fontweight="bold",
             color=INK, x=.04, ha="left", y=.98)
fig.text(.04, .90, "Expression across five tissues (TPM)", fontsize=10, color=MUTED)
plt.tight_layout(rect=[0, 0, 1, .88])
p = fig
""",
        loose="""
Editorial horizontal bar chart that names one finding.
- sort by the value column ascending so the headline bar lands at the top
- colour the headline bar RED; everything else GREY
- bold left-aligned figure title that *states* the finding
- value labels at the end of each bar
- drop left/right/top spines; light vertical grid only
""",
    ),
    "scatter_coexpression": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Two-gene scatter coloured by tissue, with a linear fit and an outlier annotation.",
        strict="""
# df: sample, tissue, gene_x, gene_y
pal = {"Leaf": GREEN, "Root": BLUE, "Seed": AMBER}
fig, ax = plt.subplots(figsize=(5.6, 4.8))
ax.set_xlabel("gene X expression (TPM)")
ax.set_ylabel("gene Y expression (TPM)")
for tissue, c in pal.items():
    g = df[df["tissue"] == tissue]
    ax.scatter(g["gene_x"], g["gene_y"], color=c, s=50, alpha=.4,
               edgecolors=CREAM, label=tissue, zorder=3)
m, b = np.polyfit(df["gene_x"], df["gene_y"], 1)
xs = np.array([df["gene_x"].min(), df["gene_x"].max()])
ax.plot(xs, m * xs + b, color=RED, lw=2.2, zorder=1)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="lower right")
ax.set_title("Two genes, one trend")
p = fig
""",
        loose="""
Scatter of two continuous variables, coloured by a categorical column.
- mark every point with low alpha so density reads
- overlay a single linear fit across ALL groups (np.polyfit then ax.plot)
- title states the finding ("X and Y co-vary" etc.)
- legend in the empty corner, no frame
""",
    ),
    "scatter_coexpression_interactive": dict(
        library="plotly",
        interactive=True,
        day=1,
        summary="Interactive co-expression — hover for sample id; toggle tissues via legend.",
        strict="""
import plotly.express as px
fig = px.scatter(df, x="gene_x", y="gene_y", color="tissue",
                 color_discrete_map={"Leaf": GREEN, "Root": BLUE, "Seed": AMBER},
                 hover_data=["sample"], trendline="ols",
                 labels={"gene_x": "gene X (TPM)", "gene_y": "gene Y (TPM)"})
fig.update_traces(marker=dict(size=8, opacity=0.6, line=dict(color=CREAM, width=0.6)))
fig.update_layout(template="simple_white", paper_bgcolor=CREAM, plot_bgcolor=CREAM)
p = fig
""",
        loose="""
Same as the static scatter but interactive.
- trendline='ols' overlays a fit per group; pass trendline_scope='overall' for a single fit
- hover_data carries the sample id
""",
    ),
    "boxplot_distributions": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Boxplot across groups with jittered raw points underneath; medians and IQR.",
        strict="""
# df: group, value  (or wide; we melt on the fly)
groups = df["group"].unique()
data = [df.loc[df["group"] == g, "value"].values for g in groups]
rj = np.random.default_rng(2)
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_ylabel("value")
ax.set_xticks(range(1, len(groups) + 1)); ax.set_xticklabels(groups)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=18, alpha=0.3, edgecolors="none")
bp = ax.boxplot(data, positions=range(1, len(groups) + 1),
                widths=0.5, patch_artist=True, showfliers=False)
for box in bp["boxes"]:
    box.set_facecolor(LINE); box.set_edgecolor(GREEN); box.set_alpha(0.75)
for med in bp["medians"]: med.set_color(INK); med.set_linewidth(2)
for w in bp["whiskers"] + bp["caps"]: w.set_color(GREEN)
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Box-and-whiskers across N groups, with raw points jittered behind.
- box face = LINE (or pale tint); edge = GREEN; median = INK bold
- show every observation as a low-alpha GREEN point at jittered x
- hide outlier diamonds (we already show every point)
- emphasise the comparison the title makes
""",
    ),
    "violin_shape": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Violin plot for shape comparison across groups — wider where the density is.",
        strict="""
groups = df["group"].unique()
data = [df.loc[df["group"] == g, "value"].values for g in groups]
fig, ax = plt.subplots(figsize=(6.4, 4.7))
ax.set_xticks(range(1, len(groups) + 1)); ax.set_xticklabels(groups)
ax.set_ylabel("value")
rj = np.random.default_rng(4)
for i, d in enumerate(data, start=1):
    ax.scatter(rj.normal(i, 0.06, len(d)), d, color=GREEN, s=14, alpha=0.25, edgecolors="none")
vp = ax.violinplot(data, positions=range(1, len(groups) + 1), showextrema=False)
for body in vp["bodies"]:
    body.set_facecolor(LINE); body.set_edgecolor(GREEN); body.set_alpha(0.6); body.set_linewidth(1.4)
for i, d in enumerate(data, start=1):
    bx = ax.boxplot(d, positions=[i], widths=0.1, patch_artist=True, showfliers=False)
    for box in bx["boxes"]: box.set_facecolor(INK)
    for m in bx["medians"]: m.set_color(CREAM); m.set_linewidth(1.4)
    for w in bx["whiskers"] + bx["caps"]: w.set_color(INK)
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Violin for shape comparison; nest a thin INK boxplot inside each violin.
- jittered raw points behind everything (same as boxplot pattern)
- violin body alpha 0.6 so shape doesn't dominate
- use when you suspect bimodality or skew that a boxplot would hide
""",
    ),
    "ridgeline_pseudotime": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Stacked KDE distributions along an ordered axis (pseudotime, stage) — one ridge per level.",
        strict="""
# df: <id>, stage (ordered), value
from scipy.stats import gaussian_kde
stages = sorted(df["stage"].unique())
xs = np.linspace(df["value"].min(), df["value"].max(), 300)
n = len(stages); overlap = 1.8
fig, ax = plt.subplots(figsize=(6.4, 5.2))
for i, s in enumerate(stages):
    vals = df.loc[df["stage"] == s, "value"].values
    k = gaussian_kde(vals)(xs); k = k / k.max() * overlap
    col = COURSE_PAL[i % len(COURSE_PAL)]
    ax.fill_between(xs, i + k, i, color=col, alpha=.8, lw=1, edgecolor=CREAM, zorder=n - i)
    ax.plot(xs, i + k, color=CREAM, lw=.8, zorder=n - i)
ax.set_yticks(range(n)); ax.set_yticklabels([f"stage {s}" for s in stages])
ax.set_xlabel("value"); ax.set_ylabel("ordering →")
for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
p = fig
""",
        loose="""
Ridgelines (also called joy plot) — one KDE per ordered category.
- ridges overlap by ~1.8 units; later ridges paint OVER earlier ones (zorder)
- colour walks through COURSE_PAL or econ_spectrum
- drop top, right AND left spines; the y-axis is just labels
""",
    ),
    "volcano_deseq2": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Differential expression volcano — log2FC vs -log10(p); red up, green down, grey background.",
        strict="""
# df: gene, log2FoldChange, pvalue, padj
de = df.copy()
de["neg_log10_p"] = -np.log10(de["pvalue"])
de["reg"] = np.where((de["log2FoldChange"] >  1) & (de["padj"] < 0.05), "up",
            np.where((de["log2FoldChange"] < -1) & (de["padj"] < 0.05), "down", "ns"))
cm = {"up": RED, "down": GREEN, "ns": GREY}
fig, ax = plt.subplots(figsize=(5.8, 4.8))
for st, grp in de.groupby("reg"):
    ax.scatter(grp["log2FoldChange"], grp["neg_log10_p"],
               c=cm[st], s=26 if st != "ns" else 7,
               alpha=.75 if st != "ns" else .3,
               linewidths=0, zorder=3 if st != "ns" else 1)
ax.axhline(-np.log10(0.05), color=INK, lw=.8, ls="--")
ax.axvline( 1, color=INK, lw=.8, ls="--")
ax.axvline(-1, color=INK, lw=.8, ls="--")
try:
    from adjustText import adjust_text
    top = de[de["reg"] != "ns"].nsmallest(8, "pvalue")
    texts = [ax.text(r["log2FoldChange"], r["neg_log10_p"], r["gene"],
                     fontsize=7, fontweight="bold")
             for _, r in top.iterrows()]
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="->", color=GREY, lw=.6))
except ImportError:
    pass  # adjustText is an optional dep
ax.set_xlabel("log2 fold change"); ax.set_ylabel("-log10(p)")
ax.set_title(f"DE: {(de['reg']=='up').sum()} up, {(de['reg']=='down').sum()} down")
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Volcano: x = log2FC, y = -log10(p).
- thresholds at |log2FC| > 1 and p_adj < 0.05; classify as up / down / ns
- up = RED, down = GREEN, ns = GREY (small + transparent)
- draw three dashed cutoff lines (vertical ±1, horizontal p=0.05)
- label the most significant hits with adjustText if available
""",
    ),
    "volcano_interactive": dict(
        library="plotly",
        interactive=True,
        day=1,
        summary="Interactive volcano — hover for gene + raw p; click legend to isolate up/down.",
        strict="""
import plotly.express as px
de = df.copy()
de["neg_log10_p"] = -np.log10(de["pvalue"])
de["reg"] = np.where((de["log2FoldChange"] >  1) & (de["padj"] < 0.05), "up",
            np.where((de["log2FoldChange"] < -1) & (de["padj"] < 0.05), "down", "ns"))
fig = px.scatter(de, x="log2FoldChange", y="neg_log10_p", color="reg",
                 color_discrete_map={"up": RED, "down": GREEN, "ns": GREY},
                 category_orders={"reg": ["up", "down", "ns"]},
                 hover_name="gene", hover_data={"pvalue": ":.1e", "reg": False},
                 labels={"log2FoldChange": "log2 fold change", "neg_log10_p": "-log10(p)"})
fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color=INK)
fig.add_vline(x=1,  line_dash="dash", line_color=INK)
fig.add_vline(x=-1, line_dash="dash", line_color=INK)
fig.update_traces(marker=dict(size=5, opacity=0.6, line=dict(width=0)))
fig.update_layout(template="simple_white", paper_bgcolor=CREAM, plot_bgcolor=CREAM)
p = fig
""",
        loose="""
Same volcano logic as the matplotlib version.  Build with plotly.express, use
color_discrete_map for red/green/grey, add hlines/vlines for thresholds.
hover_name=<gene-column> makes every dot identifiable.
""",
    ),
    "pca_population": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Population structure via PCA — PC1 vs PC2 coloured by population label, variance on the axis.",
        strict="""
# df: feature matrix + a categorical label column 'population'
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
feature_cols = [c for c in df.columns if c not in ("population", "individual")]
X = df[feature_cols].values
Xs = StandardScaler().fit_transform(X)
pca = PCA(n_components=2, random_state=42).fit(Xs)
coords = pca.transform(Xs)
var = pca.explained_variance_ratio_ * 100
pal = {"EUR": GREEN, "AFR": BLUE, "EAS": AMBER, "SAS": RED, "AMR": PURPLE}
fig, ax = plt.subplots(figsize=(5.4, 4.6))
for pop, c in pal.items():
    if pop not in df["population"].values:
        continue
    m = df["population"].values == pop
    ax.scatter(coords[m, 0], coords[m, 1], color=c, s=24, alpha=.8,
               edgecolors=CREAM, linewidths=.3, label=pop)
ax.set_xlabel(f"PC1 ({var[0]:.0f}%)"); ax.set_ylabel(f"PC2 ({var[1]:.0f}%)")
ax.legend(frameon=False, fontsize=9, title="population")
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
2-component PCA over a feature matrix.
- StandardScaler before PCA — features were on different scales
- colour by the categorical label column
- axes report variance explained as a percentage
- legend without frame, small font
""",
    ),
    "heatmap_expression": dict(
        library="seaborn",
        interactive=False,
        day=1,
        summary="Clustered heatmap — gene×sample matrix, z-scored, with a sample annotation strip on top.",
        strict="""
# df is the expression matrix (genes rows, samples cols)
# A separate meta DataFrame with sample, condition lives in ``meta`` if supplied;
# otherwise the agent will pass df verbatim.
expr = df
z = expr.sub(expr.mean(1), axis=0).div(expr.std(1), axis=0)
col_colors = None
if 'meta' in globals() and meta is not None and 'condition' in meta.columns:
    cond_pal = {"Control": BLUE, "Drought": AMBER}
    col_colors = meta.set_index("sample")["condition"].map(cond_pal)
cg = sns.clustermap(z, cmap="RdBu_r", center=0, figsize=(6.0, 5.5),
                    col_colors=col_colors,
                    xticklabels=False, yticklabels=False,
                    cbar_kws={"label": "z-score"},
                    dendrogram_ratio=(.12, .12),
                    tree_kws={"colors": MUTED, "linewidths": .6})
cg.fig.suptitle("Clustered expression heatmap", fontweight="bold", color=INK, y=1.02)
p = cg.fig
""",
        loose="""
seaborn.clustermap on a z-scored row-wise matrix.
- cmap='RdBu_r' centred at 0 (negative blue, positive red)
- col_colors carries a sample annotation bar if metadata is provided
- hide row/column tick labels when the matrix is large
- thin dendrogram trees in MUTED
""",
    ),
    "heatmap_expression_interactive": dict(
        library="plotly",
        interactive=True,
        day=1,
        summary="Interactive heatmap — hover for gene/sample/value, no dendrograms (use clustermap for those).",
        strict="""
import plotly.express as px
expr = df
z = expr.sub(expr.mean(1), axis=0).div(expr.std(1), axis=0)
fig = px.imshow(z, color_continuous_scale="RdBu_r", zmin=-3, zmax=3,
                aspect="auto", labels=dict(color="z-score"))
fig.update_layout(template="simple_white", paper_bgcolor=CREAM, plot_bgcolor=CREAM,
                  title="Expression z-score (hover to inspect)")
p = fig
""",
        loose="""
plotly.express.imshow on a z-scored matrix.  No dendrograms (px.imshow
can't cluster).  Use this when interactivity matters more than ordering;
otherwise use the seaborn version.
""",
    ),
    "ternary_admixture": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Three-component composition on a ternary triangle — each point sums to 1; dominant component coloured.",
        strict="""
# df: columns = [A, B, C] (proportions summing to ~1) OR raw 'population' column
from ternary_diagram import TernaryDiagram
cols = [c for c in df.columns if c in ("A", "B", "C")] or df.columns[:3].tolist()
comp = df[cols].to_numpy()
cols_arr = np.array([GREEN, BLUE, AMBER])[comp.argmax(1)]
fig, ax = plt.subplots(figsize=(5.4, 4.6))
td = TernaryDiagram(cols, ax=ax)
td.scatter(vector=comp, c=cols_arr, s=28, edgecolors=CREAM, linewidths=0.4, zorder=3)
p = fig
""",
        loose="""
Three-component composition where each row sums to 1.
- TernaryDiagram from the ternary_diagram package
- colour each point by its dominant component
- white edges on the markers so they don't merge
""",
    ),
    "waffle_variant_classes": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Waffle composition — 10×10 grid, each square one observation, coloured by category.",
        strict="""
# df: classification, n
from pywaffle import Waffle
pal = [RED, AMBER, GREY, BLUE, GREEN][: len(df)]
values = dict(zip(df["classification"], df["n"]))
fig = plt.figure(FigureClass=Waffle, rows=10, values=values, colors=pal,
                 figsize=(6.6, 3.6), block_aspect_ratio=1,
                 legend={"loc": "upper left", "bbox_to_anchor": (1, 1),
                         "fontsize": 8, "frameon": False},
                 title={"label": "Variant composition", "fontsize": 12, "fontweight": "bold"})
p = fig
""",
        loose="""
Composition as discrete squares (100 squares = 100%).
- use the pywaffle package, pass values as a dict of {category: count}
- legend outside on the right
- title states the finding, not just the chart type
""",
    ),
    "waterfall_tmb": dict(
        library="matplotlib",
        interactive=False,
        day=1,
        summary="Cohort waterfall — patients ranked descending by a numeric value, coloured by subtype.",
        strict="""
# df: patient, value (e.g., tmb), subtype, msi
from matplotlib.patches import Patch
co = df.sort_values("value", ascending=False).reset_index(drop=True)
sub_pal = {"Luminal A": GREEN, "Luminal B": BLUE, "HER2+": AMBER, "TNBC": RED}
fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.bar(range(len(co)), co["value"], width=1.0, linewidth=0,
       color=co["subtype"].map(sub_pal).fillna(GREY))
ax.set_xticks([])
ax.set_xlabel("patients (ranked by value)"); ax.set_ylabel("value")
if "msi" in co.columns:
    mask = co["msi"].astype(str).str.contains("MSI-H", na=False)
    ax.scatter(co.index[mask], co["value"][mask] + co["value"].max() * .03,
               marker="*", color=INK, s=55, zorder=5)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
handles = [Patch(color=c, label=k) for k, c in sub_pal.items()]
ax.legend(handles=handles, frameon=False, fontsize=8, ncol=2)
p = fig
""",
        loose="""
Waterfall = bars sorted descending by the headline metric.
- one bar per individual, width=1 so they touch
- colour by subtype using a palette dict
- mark exceptional individuals with a star above their bar
""",
    ),
    # ============================================================ DAY 2 ====
    "stacked_bar_admixture": dict(
        library="matplotlib",
        interactive=False,
        day=2,
        summary="Admixture stacked bar — one bar per individual summing to 1, sorted within each population.",
        strict="""
# df: individual, population, K1, K2, K3, K4, K5
adm = df.copy()
Kc = ["K1", "K2", "K3", "K4", "K5"]
pal = [GREEN, BLUE, AMBER, RED, PURPLE]
pops = list(dict.fromkeys(adm["population"].values))   # preserve order seen
adm["dominant"] = adm[Kc].idxmax(axis=1)
adm = (adm.sort_values(["population", "dominant", "K1"], ascending=[True, True, False])
          .reset_index(drop=True))
x = np.arange(len(adm)); bottom = np.zeros(len(adm))
fig, ax = plt.subplots(figsize=(11, 4.2))
for k, col in enumerate(Kc):
    ax.bar(x, adm[col], bottom=bottom, color=pal[k], width=1.0, linewidth=0, label=col)
    bottom += adm[col].values
for pop in pops:
    sub = adm[adm["population"] == pop]
    if sub.empty: continue
    ax.axvline(sub.index.max() + 0.5, color=INK, lw=0.5)
    ax.text(sub.index.to_numpy().mean(), 1.04, pop, ha="center", color=MUTED,
            fontsize=10, fontweight="bold")
ax.set_xlim(-0.5, len(adm) - 0.5); ax.set_ylim(0, 1.08)
ax.set_xticks([]); ax.set_ylabel("ancestry proportion")
ax.legend(title="K", ncol=5, frameon=False, loc="upper center",
          bbox_to_anchor=(0.5, -0.05))
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Each column = one individual, height = 1, K1..K5 stacked.
- sort within each population by dominant component
- thin separator line between populations
- legend below for K components
- height bar always exactly 1.0
""",
    ),
    "stacked_bar_microbiome": dict(
        library="matplotlib",
        interactive=False,
        day=2,
        summary="Microbiome composition over time — stacked bars per day, taxa ordered by mean abundance.",
        strict="""
# df: day, phase, taxon, abundance
import matplotlib.ticker as mtick
wide = df.pivot(index="day", columns="taxon", values="abundance")
taxa = (df.groupby("taxon")["abundance"].mean()
          .sort_values(ascending=False).index.tolist())
tax_pal = dict(zip(taxa, (COURSE_PAL * 3)[:len(taxa)]))
days = wide.index.values
fig, ax = plt.subplots(figsize=(6.8, 4.4))
bottom = np.zeros(len(wide))
for t in taxa:
    ax.bar(days, wide[t], bottom=bottom, color=tax_pal[t],
           width=1.0, linewidth=0, label=t)
    bottom += wide[t].values
ax.set_xlim(days.min() - 0.5, days.max() + 0.5)
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, decimals=0))
ax.set_xlabel("day"); ax.set_ylabel("relative abundance")
ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", frameon=False, fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Composition over an ordered (time-like) axis.
- pivot to (time × taxon) wide form first
- order taxa by mean abundance descending; tallest at the bottom
- y-axis 0..1 with percent formatter
- legend on the right outside the axes
""",
    ),
    "manhattan_gwas": dict(
        library="matplotlib",
        interactive=False,
        day=2,
        summary="Genome-wide Manhattan — cumulative bp position vs -log10(p), alternating chromosome colours, hits highlighted.",
        strict="""
# df: chrom, pos, pval, snp
gwas = df.sort_values(["chrom", "pos"]).copy()
gwas["nlog10p"] = -np.log10(gwas["pval"])
chrom_len = gwas.groupby("chrom")["pos"].max()
offsets = chrom_len.cumsum().shift(fill_value=0)
gwas["cum_pos"] = gwas["pos"] + gwas["chrom"].map(offsets)
gwas["color"] = (gwas["chrom"] % 2 == 0).map({True: BLUE, False: GREEN})
fig, ax = plt.subplots(figsize=(9.5, 4.5))
ax.scatter(gwas["cum_pos"], gwas["nlog10p"], c=gwas["color"], s=6, alpha=0.55, linewidths=0)
ax.axhline(-np.log10(5e-8), color=RED,   lw=.9, ls="--")
ax.axhline(-np.log10(1e-5), color=AMBER, lw=.9, ls="--")
tick_pos = offsets + chrom_len / 2
ax.set_xticks(tick_pos); ax.set_xticklabels(chrom_len.index, fontsize=8)
hits = gwas[gwas["pval"] < 5e-8]
ax.scatter(hits["cum_pos"], hits["nlog10p"], color=RED, s=42,
           edgecolor="white", linewidths=0.6, zorder=5)
for _, row in hits.nsmallest(3, "pval").iterrows():
    ax.annotate(row["snp"], (row["cum_pos"], row["nlog10p"]),
                xytext=(5, 5), textcoords="offset points", fontsize=8)
ax.set_xlabel("chromosome"); ax.set_ylabel(r"$-\\log_{10}(p)$")
ax.set_title(f"GWAS — {len(hits)} genome-wide significant SNPs")
ax.spines[["top", "right"]].set_visible(False)
p = fig
""",
        loose="""
Manhattan plot — every variant in the genome, ordered.
- build a cumulative x by stacking chromosome lengths
- alternate two colours by chromosome parity (BLUE / GREEN)
- two dashed horizontals: genome-wide (5e-8) RED, suggestive (1e-5) AMBER
- top hits as larger RED dots with rsID labels
""",
    ),
    "manhattan_interactive": dict(
        library="plotly",
        interactive=True,
        day=2,
        summary="Interactive Manhattan — hover for rsID, chromosome, position, p-value.",
        strict="""
import plotly.express as px
gwas = df.sort_values(["chrom", "pos"]).copy()
gwas["nlog10p"] = -np.log10(gwas["pval"])
chrom_len = gwas.groupby("chrom")["pos"].max()
offsets = chrom_len.cumsum().shift(fill_value=0)
gwas["cum_pos"] = gwas["pos"] + gwas["chrom"].map(offsets)
gwas["chrom_parity"] = (gwas["chrom"] % 2 == 0).astype(str)
fig = px.scatter(gwas, x="cum_pos", y="nlog10p", color="chrom_parity",
                 color_discrete_map={"True": BLUE, "False": GREEN},
                 hover_data=["chrom", "pos", "snp", "pval"],
                 labels={"cum_pos": "genomic position", "nlog10p": "-log10(p)"})
fig.add_hline(y=-np.log10(5e-8), line_dash="dash", line_color=RED)
fig.add_hline(y=-np.log10(1e-5), line_dash="dash", line_color=AMBER)
fig.update_traces(marker=dict(size=4, opacity=0.6))
fig.update_layout(showlegend=False, template="simple_white",
                  paper_bgcolor=CREAM, plot_bgcolor=CREAM)
p = fig
""",
        loose="""
Same Manhattan logic, but interactive (hover the dots, zoom into a region).
- px.scatter with color by chromosome parity
- add_hline for both threshold lines
- hide the parity legend
""",
    ),
    "treemap_microbiome": dict(
        library="matplotlib",
        interactive=False,
        day=2,
        summary="Treemap of community composition — tile area proportional to abundance, one tile per taxon.",
        strict="""
# df: taxon, abundance
import squarify
comm = (df.groupby("taxon")["abundance"].mean()
          .sort_values(ascending=False).reset_index())
comm["pct"] = comm["abundance"] * 100
labels = [f"{t}\\n{p:.0f}%" for t, p in zip(comm["taxon"], comm["pct"])]
colors = [COURSE_PAL[i % len(COURSE_PAL)] for i in range(len(comm))]
fig, ax = plt.subplots(figsize=(6.2, 5.0)); ax.set_axis_off()
squarify.plot(sizes=comm["abundance"], label=labels, color=colors, pad=True,
              text_kwargs={"color": "white", "fontsize": 10}, ax=ax)
p = fig
""",
        loose="""
Treemap: each rectangle's area encodes the value.
- aggregate to one row per category first
- sort descending so the largest tile is in the corner
- white labels (the deck convention) over coloured tiles
- ax.set_axis_off — there are no axes to read
""",
    ),
    # ============================================================ DAY 3 ====
    # Production packages. These import their own library inside the template
    # (upsetplot / PyComplexHeatmap are optional deps); the agent injects only
    # plt/np/pd/palette, and raises a clean install hint if the package is absent.
    "upset_gene_sets": dict(
        library="matplotlib",
        interactive=False,
        day=3,
        summary="UpSet plot of set intersections — for 4+ overlapping sets where a Venn breaks down (variant/GO/DE-gene overlaps).",
        strict="""
# df: gene index + one boolean column per set (e.g. DE, Leaf, Root, Photo, Stress)
from upsetplot import UpSet, from_indicators
sets = [c for c in df.columns if df[c].dtype == bool]
mat = from_indicators(sets, data=df)
fig = plt.figure(figsize=(7.4, 4.6))
up = UpSet(mat, sort_by="cardinality", show_counts=True)
up.plot(fig=fig)
fig.suptitle("Set intersections")
p = fig
""",
        loose="""
UpSet plot — the scalable replacement for a 4+ circle Venn diagram.
- input is one boolean column per set (membership indicators)
- build with upsetplot.from_indicators(sets, data=df), then UpSet(mat).plot(fig=fig)
- sort_by="cardinality" so the biggest intersections read left-to-right
- show_counts=True to label each bar
- assign the matplotlib Figure to p
""",
    ),
    "heatmap_annotated": dict(
        library="matplotlib",
        interactive=False,
        day=3,
        summary="Clustered heatmap with annotation tracks (PyComplexHeatmap) — a matrix plus per-sample metadata strips, richer than a plain clustermap.",
        strict="""
# df: numeric matrix, rows = features, columns = samples (log2 TPM or similar)
import PyComplexHeatmap as pch
fig = plt.figure(figsize=(8, 5))
hm = pch.ClusterMapPlotter(
    data=df,
    row_cluster=True, col_cluster=True,
    cmap="RdBu_r",
    show_rownames=False, show_colnames=True,
    label="value",
)
p = fig
""",
        loose="""
Annotated clustered heatmap (PyComplexHeatmap.ClusterMapPlotter).
- input is a numeric matrix DataFrame (features × samples)
- row_cluster=True + col_cluster=True for dendrograms on both axes
- a diverging cmap ("RdBu_r") when the matrix is centred/z-scored
- if per-column metadata is available, build a pch.HeatmapAnnotation and pass
  it as top_annotation to paint condition/batch strips above the heatmap
- assign the matplotlib Figure to p
""",
    ),
}


def list_plots(
    library: str | None = None,
    interactive: bool | None = None,
    day: int | None = None,
) -> dict[str, CatalogEntry]:
    """Return a filtered view of :data:`CATALOG`.

    Filters are AND'd.  ``None`` means "don't filter on this field."
    Useful for browsing the catalog interactively in a notebook.
    """
    out = {}
    for name, entry in CATALOG.items():
        if library is not None and entry["library"] != library:
            continue
        if interactive is not None and entry["interactive"] != interactive:
            continue
        if day is not None and entry["day"] != day:
            continue
        out[name] = entry
    return out


def get_strict_spec(name: str) -> str:
    """Return the strict template for ``name`` or raise KeyError."""
    return CATALOG[name]["strict"]


def get_loose_spec(name: str) -> str:
    """Return the loose prose spec for ``name`` or raise KeyError."""
    return CATALOG[name]["loose"]
