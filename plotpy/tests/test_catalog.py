"""Smoke tests for the catalog + agent setup — no LLM call required."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless backend so pytest works in CI
import matplotlib.pyplot as plt
import pandas as pd

import plotpy
from plotpy import specs


def test_catalog_is_populated() -> None:
    assert len(plotpy.CATALOG) >= 15
    for name, entry in plotpy.CATALOG.items():
        assert entry["library"] in {"matplotlib", "seaborn", "plotnine", "plotly"}
        assert isinstance(entry["interactive"], bool)
        assert entry["day"] in {1, 2, 3}
        for field in ("strict", "loose", "summary"):
            assert entry[field].strip(), f"{name}: empty {field}"


def test_interactive_consistency() -> None:
    # only plotly entries are interactive
    for name, e in plotpy.CATALOG.items():
        if e["interactive"]:
            assert e["library"] == "plotly", f"{name}: interactive but not plotly"


def test_list_plots_filters() -> None:
    day2 = plotpy.list_plots(day=2)
    assert day2 and all(e["day"] == 2 for e in day2.values())
    plotly_only = plotpy.list_plots(library="plotly")
    assert plotly_only and all(e["library"] == "plotly" for e in plotly_only.values())


def test_palette_constants_present() -> None:
    for name in "GREEN BLUE AMBER RED PURPLE GREY INK CREAM LINE MUTED".split():
        assert getattr(specs, name).startswith("#")
    assert len(specs.COURSE_PAL) == 5


def test_apply_base_theme_mpl_runs() -> None:
    fig, ax = plt.subplots()
    ax.scatter([1, 2, 3], [4, 5, 6])
    specs.apply_base_theme_mpl(ax)
    assert not ax.spines["top"].get_visible()
    assert not ax.spines["right"].get_visible()
    assert ax.get_facecolor() == matplotlib.colors.to_rgba(specs.CREAM)


def test_apply_base_theme_plotly_runs() -> None:
    import plotly.graph_objects as go

    fig = go.Figure()
    specs.apply_base_theme_plotly(fig)
    assert fig.layout.paper_bgcolor == specs.CREAM
    assert fig.layout.plot_bgcolor == specs.CREAM


def test_agent_inspect_builds_summary() -> None:
    df = pd.DataFrame({"gene": ["A", "B"], "tpm": [1.0, 2.0]})
    agent = plotpy.PlotAgent().inspect(df)
    # private but worth pinning the contract — summary mentions shape + cols
    assert "2 rows" in agent._data_summary
    assert "gene" in agent._data_summary
    assert "tpm" in agent._data_summary


def test_agent_requires_inspect_before_ask() -> None:
    import pytest

    with pytest.raises(RuntimeError, match="inspect"):
        plotpy.PlotAgent().ask("anything")
