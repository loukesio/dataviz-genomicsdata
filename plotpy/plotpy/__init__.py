"""PlotPy — an LLM-driven plotting agent (Python sibling of PlotR).

Quickstart::

    import pandas as pd, plotpy
    plotpy.set_key("sk-...")           # or put it in .env
    df = pd.read_csv("expression.csv")
    res = plotpy.ask(df, "I want a clustered heatmap with condition labels.")
    res.plot                            # the matplotlib / plotly figure
    res.code                            # the source the LLM produced

The four modules mirror PlotR one-for-one:

- :mod:`plotpy.api_key`  — provider-agnostic LLM client (OpenAI-compatible)
- :mod:`plotpy.agent`    — the :class:`PlotAgent` (selection + generation + exec)
- :mod:`plotpy.specs`    — :data:`CATALOG` of strict/loose plot specs + BASE_THEME helpers
- :mod:`plotpy.plots`    — :func:`ask`, :func:`list_plots`, per-plot wrappers
"""

from __future__ import annotations

from .agent import PlotAgent, PlotResult
from .api_key import get_client, get_config, get_key, set_key
from .plots import (
    admixture,
    ask,
    bar,
    boxplot,
    heatmap,
    list_plots,
    manhattan,
    microbiome,
    pca,
    ridgeline,
    scatter,
    ternary,
    timecourse,
    treemap,
    violin,
    volcano,
    waffle,
    waterfall,
)
from .specs import CATALOG

__version__ = "0.1.0"

__all__ = [
    # primary
    "ask",
    "list_plots",
    "CATALOG",
    # agent + result
    "PlotAgent",
    "PlotResult",
    # client config
    "set_key",
    "get_key",
    "get_client",
    "get_config",
    # per-plot wrappers
    "admixture",
    "bar",
    "boxplot",
    "heatmap",
    "manhattan",
    "microbiome",
    "pca",
    "ridgeline",
    "scatter",
    "ternary",
    "timecourse",
    "treemap",
    "violin",
    "volcano",
    "waffle",
    "waterfall",
    "__version__",
]
