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


def test_datasets_match_catalog_schemas() -> None:
    """Every dataset generator must produce the columns its strict template reads."""
    expected = {
        "expression":            {"gene", "time", "tpm", "sem"},
        "coexpression":          {"sample", "tissue", "gene_x", "gene_y"},
        "tissue_expression":     {"tissue", "tpm"},
        "expression_groups":     {"group", "value"},
        "pseudotime":            {"id", "stage", "value"},
        "deseq2":                {"gene", "log2FoldChange", "pvalue", "padj"},
        "admixture_components":  {"A", "B", "C"},
        "variant_classes":       {"classification", "n"},
        "tmb_cohort":            {"patient", "value", "subtype", "msi"},
        "admixture_kinship":     {"individual", "population", "K1", "K2", "K3", "K4", "K5"},
        "microbiome_timeseries": {"day", "phase", "taxon", "abundance"},
        "gwas":                  {"chrom", "pos", "pval", "snp"},
        "microbiome_abundance":  {"taxon", "abundance"},
        "gene_sets":             {"DE", "Leaf", "Root", "Photo", "Stress"},
    }
    for name, cols in expected.items():
        df = getattr(plotpy.datasets, name)()
        assert cols.issubset(df.columns), f"{name}: missing {cols - set(df.columns)}"
        assert len(df) > 0, f"{name}: empty DataFrame"


def test_datasets_are_deterministic() -> None:
    """Same seed → identical DataFrame, two calls."""
    a = plotpy.datasets.expression()
    b = plotpy.datasets.expression()
    pd.testing.assert_frame_equal(a, b)


def test_expression_matrix_returns_pair() -> None:
    expr, meta = plotpy.datasets.expression_matrix()
    assert expr.shape[1] == len(meta)
    assert set(meta.columns) == {"sample", "condition"}
    assert set(meta["condition"].unique()) == {"Control", "Drought"}


def test_list_datasets_covers_every_generator() -> None:
    table = plotpy.datasets.list_datasets()
    listed = set(table["dataset"])
    exposed = {n for n in plotpy.datasets.__all__ if n != "list_datasets"}
    assert listed == exposed


# ===================================================================
# agent-level regression tests for the fixes shipped 2026-06-24
# ===================================================================
class _MockChat:
    """Duck-typed stand-in for providers.Chat — scripted, offline."""

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []  # list of (messages, json_mode)

    def complete(self, messages, temperature=None, json_mode=False):
        self.calls.append((messages, json_mode))
        return self._responses.pop(0)


def test_generation_prompt_contains_chosen_name() -> None:
    """Fix A — the LLM must be told which catalog entry it's generating for."""
    mock = _MockChat(["```python\nfig, ax = plt.subplots(); p = fig\n```"])
    df = plotpy.datasets.coexpression()
    agent = plotpy.PlotAgent(chat=mock).inspect(df)
    agent.ask("show", mode="loose", plot_type="scatter_coexpression")
    user_prompt = mock.calls[0][0][1]["content"]  # first call, user message
    assert "scatter_coexpression" in user_prompt


def test_last_raw_split() -> None:
    """Fix B — selection and generation raw responses are separately readable."""
    mock = _MockChat([
        '{"chosen": "scatter_coexpression", "alternatives": []}',   # selection
        "```python\nfig, ax = plt.subplots(); p = fig\n```",        # generation
    ])
    df = plotpy.datasets.coexpression()
    agent = plotpy.PlotAgent(chat=mock).inspect(df)
    agent.ask("scatter please", mode="loose")
    assert "scatter_coexpression" in agent.last_raw_select
    assert "```python" in agent.last_raw_generate
    # backwards-compatible alias points at the most recent one
    assert agent.last_raw == agent.last_raw_generate


def test_extract_python_raises_on_garbage() -> None:
    """Fix C — a non-code refusal must surface as a clear error, not SyntaxError."""
    import pytest

    from plotpy.agent import _extract_python

    with pytest.raises(RuntimeError, match="no fenced"):
        _extract_python("Sorry, I cannot help with that.")


def test_extract_python_accepts_unfenced_valid_code() -> None:
    """Fix C — models that drop the fence but emit valid Python still work."""
    from plotpy.agent import _extract_python
    assert _extract_python("p = 1 + 1") == "p = 1 + 1"


def test_extract_json_finds_first_balanced_object() -> None:
    """Fix D — brace counting beats greedy regex when prose has stray braces."""
    from plotpy.agent import _extract_json

    raw = (
        'Sure! Here is my pick:\n'
        '{"chosen": "scatter_coexpression", "alternatives": ["scatter", "bar"]}\n'
        'I hope that helps {with your plot}.'
    )
    extracted = _extract_json(raw)
    assert extracted.startswith("{") and extracted.endswith("}")
    import json as _json
    parsed = _json.loads(extracted)
    assert parsed["chosen"] == "scatter_coexpression"


def test_data_summary_shows_categorical_levels() -> None:
    """Fix E — head(4) hides levels when rows are grouped; summary must list them."""
    df = plotpy.datasets.coexpression()   # tissue column groups Leaf/Root/Seed
    summary = plotpy.PlotAgent()._summarize_df(df)
    for level in ("Leaf", "Root", "Seed"):
        assert level in summary, f"summary missed tissue level {level!r}"
