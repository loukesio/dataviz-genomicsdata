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

from . import datasets
from .agent import PlotAgent, PlotResult, Suggestion
from .api_key import get_client, get_config, get_key, set_key
from .plots import (
    admixture,
    ask,
    bar,
    boxplot,
    complexheatmap,
    heatmap,
    list_plots,
    manhattan,
    microbiome,
    pca,
    ridgeline,
    scatter,
    suggest,
    ternary,
    timecourse,
    treemap,
    upset,
    violin,
    volcano,
    waffle,
    waterfall,
)
from .providers import (
    Chat,
    chat,
    chat_anthropic,
    chat_fireworks,
    chat_google,
    chat_groq,
    chat_ollama,
    chat_openai,
    chat_together,
    chat_vllm,
    get_active,
    use,
)
from .specs import CATALOG

__version__ = "0.1.0"

__all__ = [
    # primary
    "ask",
    "suggest",
    "list_plots",
    "CATALOG",
    "datasets",
    # agent + result
    "PlotAgent",
    "PlotResult",
    "Suggestion",
    # multi-LLM providers (ellmer-style)
    "Chat",
    "chat",
    "chat_groq",
    "chat_openai",
    "chat_anthropic",
    "chat_google",
    "chat_together",
    "chat_fireworks",
    "chat_ollama",
    "chat_vllm",
    "use",
    "get_active",
    # legacy client config
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
    "upset",
    "complexheatmap",
    "violin",
    "volcano",
    "waffle",
    "waterfall",
    "__version__",
]
