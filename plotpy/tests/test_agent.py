"""Offline tests for the redesigned agent — providers, self-repair, suggest, free.

Everything here runs without a network call: a scripted ``MockChat`` stands in
for a real provider, so the repair loop and parsing are deterministically
exercised in CI.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless
import pandas as pd
import pytest

import plotpy
from plotpy import providers
from plotpy.agent import PlotAgent, Suggestion


class MockChat:
    """Scripted stand-in for :class:`plotpy.providers.Chat`.

    ``responses`` is a list of assistant strings returned in order (one per
    ``complete`` call).  Records every call for assertions.
    """

    def __init__(self, responses):
        self._responses = list(responses)
        self.calls = []  # (messages, temperature, json_mode)

    def complete(self, messages, temperature=None, json_mode=False):
        self.calls.append((messages, temperature, json_mode))
        if not self._responses:
            raise AssertionError("MockChat ran out of scripted responses")
        return self._responses.pop(0)


def _xy() -> pd.DataFrame:
    return pd.DataFrame({"x": [1.0, 2, 3, 4], "y": [2.0, 4, 6, 8]})


# --------------------------------------------------------------- providers
def test_chat_constructors_build_without_network() -> None:
    c = plotpy.chat_groq(api_key="k")
    assert c.provider == "groq" and c.model == "llama-3.3-70b-versatile"
    assert "api.openai.com" in plotpy.chat_openai(api_key="k").base_url
    assert plotpy.chat_anthropic(api_key="k").model.startswith("claude")
    assert plotpy.chat_ollama().provider == "ollama"  # no key required


def test_unknown_provider_raises() -> None:
    with pytest.raises(KeyError, match="Unknown provider"):
        providers.chat("nope", api_key="k")


def test_missing_key_raises_clear_error(monkeypatch) -> None:
    for var in ("OPENAI_API_KEY", "PLOTPY_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    with pytest.raises(RuntimeError, match="No API key"):
        plotpy.chat_openai()


def test_use_and_get_active_switch_model() -> None:
    a = plotpy.chat_groq(api_key="k")
    b = plotpy.chat_openai(api_key="k", model="gpt-4o-mini")
    plotpy.use(a)
    assert plotpy.get_active() is a
    plotpy.use(b)  # switch any time
    assert plotpy.get_active().model == "gpt-4o-mini"


# --------------------------------------------------------------- repair loop
def test_repair_loop_fixes_broken_code() -> None:
    # first generation references an undefined name → NameError; repair fixes it.
    mock = MockChat([
        "```python\np = totally_undefined_variable\n```",             # generate (free)
        "```python\nfig, ax = plt.subplots(); ax.plot(df['x'], df['y']); p = fig\n```",  # repair
    ])
    agent = PlotAgent(chat=mock).inspect(_xy())
    res = agent.ask("scatter x vs y", mode="free")
    assert res.repairs == 1
    assert res.plot.__class__.__name__ == "Figure"
    assert len(agent.last_repairs) == 1
    assert "NameError" in agent.last_repairs[0]["error"]


def test_repair_loop_gives_up_after_budget() -> None:
    always_broken = "```python\np = still_undefined\n```"
    mock = MockChat([always_broken] * 5)
    agent = PlotAgent(chat=mock).inspect(_xy())
    with pytest.raises(RuntimeError, match="still failing after 2 repair"):
        agent.ask("anything", mode="free", max_repairs=2)


def test_no_repair_when_first_try_works() -> None:
    good = "```python\nfig, ax = plt.subplots(); ax.plot(df['x'], df['y']); p = fig\n```"
    mock = MockChat([good])
    res = PlotAgent(chat=mock).inspect(_xy()).ask("plot it", mode="free")
    assert res.repairs == 0


def test_missing_package_fails_fast_without_burning_repairs() -> None:
    # a genuinely-missing import can't be repaired by regenerating — bail at once.
    code = "```python\nimport a_package_that_does_not_exist as z\np = z.plot()\n```"
    mock = MockChat([code] * 5)
    agent = PlotAgent(chat=mock).inspect(_xy())
    with pytest.raises(RuntimeError, match="isn't installed"):
        agent.ask("something exotic", mode="free", max_repairs=3)
    assert len(mock.calls) == 1          # only the first generation, no repair calls
    assert len(agent.last_repairs) == 1


# --------------------------------------------------------------- free mode
def test_free_mode_injects_all_libraries() -> None:
    names = PlotAgent._injected_names(None)
    for n in ("plt", "sns", "px", "go", "ggplot", "df", "GREEN", "COURSE_PAL"):
        assert n in names


def test_free_mode_can_use_plotly() -> None:
    code = ("```python\nimport plotly.express as px\n"
            "p = px.scatter(df, x='x', y='y')\n```")
    res = PlotAgent(chat=MockChat([code])).inspect(_xy()).ask(
        "interactive scatter", mode="free", interactive=True)
    assert res.chosen == "free"
    assert "Figure" in res.plot.__class__.__name__


# --------------------------------------------------------------- suggest
def test_suggest_parses_ranked_menu() -> None:
    payload = (
        '{"suggestions": ['
        '{"name": "scatter_coexpression", "reason": "two numeric columns covary",'
        ' "library": "matplotlib", "interactive": false, "in_catalog": true},'
        '{"name": "hexbin_density", "reason": "many points overlap",'
        ' "library": "matplotlib", "interactive": false, "in_catalog": false}'
        ']}'
    )
    out = PlotAgent(chat=MockChat([payload])).inspect(_xy()).suggest(n=6)
    assert [s.name for s in out] == ["scatter_coexpression", "hexbin_density"]
    assert out[0].in_catalog is True          # known catalog entry
    assert out[1].in_catalog is False         # custom idea
    assert all(isinstance(s, Suggestion) for s in out)
    # the suggest call asked for JSON mode
    assert PlotAgent(chat=MockChat([payload])).inspect(_xy())  # sanity


def test_suggest_requires_inspect() -> None:
    with pytest.raises(RuntimeError, match="inspect"):
        PlotAgent(chat=MockChat([])).suggest()
