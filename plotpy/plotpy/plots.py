"""Public plotting entry points.

Mirror of PlotR's ``R/plots.R``.  Three layers of API, by directness:

1. :func:`ask` — the LLM picks the plot from the catalog (loosest)
2. per-plot wrappers (:func:`scatter`, :func:`volcano`, …) — student already
   knows the plot type; skip the selection step (tightest)
3. :func:`list_plots` — browse the catalog without making any LLM call

All wrappers return a :class:`~plotpy.agent.PlotResult` so the calling
notebook can still inspect ``.code`` / ``.alternatives`` / ``.chosen``.
"""

from __future__ import annotations

import pandas as pd

from .agent import PlotAgent, PlotResult, Suggestion
from .providers import Chat
from .specs import CATALOG
from .specs import list_plots as _list_plots


def ask(
    df: pd.DataFrame,
    prompt: str,
    mode: str = "strict",
    interactive: bool | None = None,
    llm: Chat | None = None,
    max_repairs: int | None = None,
) -> PlotResult:
    """Primary entry point — let the agent pick and render.

    Parameters
    ----------
    df
        The DataFrame to plot.  The agent's text summary of this is what
        the LLM uses to choose the right chart.
    prompt
        What you want the plot to show, in plain English.
    mode
        ``"strict"`` (default) — verbatim catalog template, only column names
        change.  ``"loose"`` — adapt the recipe to your data.  ``"free"`` —
        open-ended chart, no catalog, grounded in the course theme (best for
        data or plot types the catalog never saw).
    interactive
        ``True`` to force a plotly variant, ``False`` for static only,
        ``None`` (default) to let the LLM choose.
    llm
        A :class:`plotpy.providers.Chat` to use for this call only (e.g.
        ``plotpy.chat_openai()``).  ``None`` uses the active model — set one
        globally with ``plotpy.use(...)``.
    max_repairs
        Override the self-repair attempt budget for this call.

    Returns
    -------
    PlotResult
        ``.plot`` is the figure; ``.code`` is the source that produced it.
    """
    agent = PlotAgent(chat=llm)
    agent.inspect(df)
    return agent.ask(prompt=prompt, mode=mode, interactive=interactive, max_repairs=max_repairs)


def suggest(
    df: pd.DataFrame,
    n: int = 6,
    interactive: bool | None = None,
    llm: Chat | None = None,
) -> list[Suggestion]:
    """Ask the agent for a ranked menu of plot ideas for ``df`` — no code yet.

    Each :class:`~plotpy.agent.Suggestion` has a ``name`` (catalog entry or a
    custom slug) and a one-line ``reason``.  Pick one and render it::

        for s in plotpy.suggest(df):
            print(s.name, "—", s.reason)
        plotpy.ask(df, "make the manhattan one interactive", interactive=True)
    """
    agent = PlotAgent(chat=llm)
    agent.inspect(df)
    return agent.suggest(n=n, interactive=interactive)


def list_plots(library: str | None = None, interactive: bool | None = None, day: int | None = None):
    """Browse the catalog without invoking the LLM.

    Use this to discover what plots PlotPy ships:

        >>> from plotpy import list_plots
        >>> list_plots(day=1, interactive=False).keys()

    Returns a ``{name: CatalogEntry}`` dict.  Filters are AND'd; ``None``
    means "no filter on this field".
    """
    return _list_plots(library=library, interactive=interactive, day=day)


# ----------------------------------------------------- per-plot convenience API
# Mirror of PlotR's plotr_scatter / plotr_manhattan / plotr_volcano / plotr_heatmap.
# Each wrapper just calls ask(..., plot_type=<name>) to skip the LLM-selection step.
#
# We expose one wrapper per BASE plot (not the *_interactive variants).  Pass
# interactive=True to any wrapper to switch to the plotly cousin if one exists.

_INTERACTIVE_SIBLINGS = {
    "timecourse_line": "timecourse_line_interactive",
    "scatter_coexpression": "scatter_coexpression_interactive",
    "volcano_deseq2": "volcano_interactive",
    "manhattan_gwas": "manhattan_interactive",
    "heatmap_expression": "heatmap_expression_interactive",
}


def _pinned(df: pd.DataFrame, prompt: str, name: str, mode: str, interactive: bool) -> PlotResult:
    agent = PlotAgent()
    agent.inspect(df)
    target = _INTERACTIVE_SIBLINGS.get(name, name) if interactive else name
    if target not in CATALOG:
        target = name  # the requested plot has no interactive sibling
    return agent.ask(prompt=prompt, mode=mode, plot_type=target)


def timecourse(df, prompt="Plot expression over time, one line per gene.", *,
               mode="strict", interactive=False):
    """One line per gene across timepoints; SEM as error bars if present."""
    return _pinned(df, prompt, "timecourse_line", mode, interactive)


def bar(df, prompt="Sorted bar chart of the value column, highlight the leader.",
        *, mode="strict", interactive=False):
    """Sorted horizontal bar with one bar coloured RED for the headline."""
    return _pinned(df, prompt, "bar_simple", mode, interactive)


def scatter(df, prompt="Scatter two genes, colour by tissue, add a linear fit.",
            *, mode="strict", interactive=False):
    """Two-variable scatter coloured by category, with a linear fit."""
    return _pinned(df, prompt, "scatter_coexpression", mode, interactive)


def boxplot(df, prompt="Boxplot across groups with jittered points.",
            *, mode="strict", interactive=False):
    """Boxplot + jittered raw points."""
    return _pinned(df, prompt, "boxplot_distributions", mode, interactive)


def violin(df, prompt="Violin plot for distribution shape across groups.",
           *, mode="strict", interactive=False):
    """Violin (with an inner thin boxplot) — for shape, esp. bimodality."""
    return _pinned(df, prompt, "violin_shape", mode, interactive)


def ridgeline(df, prompt="Ridgeline plot of value distributions per stage.",
              *, mode="strict", interactive=False):
    """Stacked KDEs along an ordered axis (pseudotime, stage, …)."""
    return _pinned(df, prompt, "ridgeline_pseudotime", mode, interactive)


def volcano(df, prompt="Volcano: log2FC vs -log10(p), label top hits.",
            *, mode="strict", interactive=False):
    """Differential-expression volcano with thresholds and labels."""
    return _pinned(df, prompt, "volcano_deseq2", mode, interactive)


def pca(df, prompt="PCA of the feature matrix, colour by population.",
        *, mode="strict", interactive=False):
    """2-component PCA scatter."""
    return _pinned(df, prompt, "pca_population", mode, interactive)


def heatmap(df, prompt="Clustered heatmap of the expression matrix.",
            *, mode="strict", interactive=False):
    """Clustered z-scored heatmap with sample annotation."""
    return _pinned(df, prompt, "heatmap_expression", mode, interactive)


def ternary(df, prompt="Ternary plot of three-component composition.",
            *, mode="strict", interactive=False):
    """Three-component composition on a triangle."""
    return _pinned(df, prompt, "ternary_admixture", mode, interactive)


def waffle(df, prompt="Waffle chart of categorical composition.",
           *, mode="strict", interactive=False):
    """10×10 waffle of category counts."""
    return _pinned(df, prompt, "waffle_variant_classes", mode, interactive)


def waterfall(df, prompt="Waterfall plot of patients ranked by TMB.",
              *, mode="strict", interactive=False):
    """Cohort waterfall — sorted bars coloured by subtype."""
    return _pinned(df, prompt, "waterfall_tmb", mode, interactive)


def admixture(df, prompt="Admixture stacked bar of K1..K5 per individual.",
              *, mode="strict", interactive=False):
    """One bar per individual, K1..K5 stacked, sorted within population."""
    return _pinned(df, prompt, "stacked_bar_admixture", mode, interactive)


def microbiome(df, prompt="Stacked bar of taxa abundance over time.",
               *, mode="strict", interactive=False):
    """Composition over time as a stacked percentage bar chart."""
    return _pinned(df, prompt, "stacked_bar_microbiome", mode, interactive)


def manhattan(df, prompt="Manhattan plot of GWAS p-values with thresholds.",
              *, mode="strict", interactive=False):
    """Genome-wide Manhattan with significance lines and hit labels."""
    return _pinned(df, prompt, "manhattan_gwas", mode, interactive)


def treemap(df, prompt="Treemap of taxon abundance.",
            *, mode="strict", interactive=False):
    """Area-proportional treemap of a composition."""
    return _pinned(df, prompt, "treemap_microbiome", mode, interactive)


# ------------------------------------------------------------------ Day 3
def upset(df, prompt="UpSet plot of set intersections, sorted by size.",
          *, mode="strict", interactive=False):
    """UpSet plot from boolean membership columns (needs ``upsetplot``)."""
    return _pinned(df, prompt, "upset_gene_sets", mode, interactive)


def complexheatmap(df, prompt="Clustered heatmap with annotation tracks.",
                   *, mode="strict", interactive=False):
    """Annotated clustered heatmap from a matrix (needs ``PyComplexHeatmap``)."""
    return _pinned(df, prompt, "heatmap_annotated", mode, interactive)
