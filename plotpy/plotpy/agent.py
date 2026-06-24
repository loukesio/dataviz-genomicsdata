"""LLM-driven plotting agent.

Mirror of PlotR's ``R/plotr_agent.R``.  The :class:`PlotAgent` class is what
``plotpy.ask`` instantiates under the hood — but exposed directly so notebooks
can introspect ``last_raw`` / ``last_code`` / ``last_prompt`` after a call
that surprised them.

The flow inside :meth:`PlotAgent.ask` is two LLM calls:

1. **Selection** — the model sees the data summary + every catalog summary
   and answers with a chosen plot name + two alternatives.  Cheap, short,
   deterministic at ``temperature=0``.
2. **Generation** — the model then sees the strict-or-loose spec for the
   chosen plot and is asked to produce ONE fenced ``python`` code block
   that assigns ``p``.  Slightly warmer (``temperature=0.2``) so the LLM
   feels free to adapt column names from ``df``.

The generated code is executed in a *fresh* namespace populated with:

- ``df`` — the user's DataFrame
- ``np``, ``pd`` — always
- the chosen library's primary objects (``plt``, ``sns``, ``px``, ``go``,
  the plotnine grammar)
- every palette / colour constant exported by :mod:`plotpy.specs`

If the code does not assign ``p`` the agent raises a clean error pointing
the user at ``last_code`` and ``last_raw``.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Any

import pandas as pd

from . import specs
from .api_key import get_client, get_config


# ----------------------------------------------------------- public result type
@dataclass
class PlotResult:
    """What :meth:`PlotAgent.ask` returns.

    Attributes
    ----------
    plot
        The rendered plot object.  matplotlib Figure / seaborn Grid /
        plotly Figure / plotnine ggplot — depends on the chosen catalog
        entry's ``library``.
    chosen
        The catalog entry name the agent picked.
    alternatives
        Up to two other catalog entries the agent considered.  Useful for
        the "next-best" suggestion in a notebook.
    code
        The exact Python source that was exec()'d to produce ``plot``.
        Inspect this when the result surprises you.
    """

    plot: Any
    chosen: str
    alternatives: list[str] = field(default_factory=list)
    code: str = ""

    def _repr_html_(self) -> str:  # notebook-friendly summary
        alt = ", ".join(self.alternatives) or "—"
        return (
            f"<div><b>plot:</b> {type(self.plot).__name__} &nbsp;"
            f"<b>chosen:</b> <code>{self.chosen}</code> &nbsp;"
            f"<b>alternatives:</b> {alt}</div>"
        )


# ----------------------------------------------------------------- agent class
class PlotAgent:
    """Stateful agent — mirror of PlotR's ``.PlotR`` R6 object.

    The agent is a one-DataFrame thing: call :meth:`inspect` to load a frame,
    then :meth:`ask` to produce one plot at a time.  All debugging state
    (``last_raw``, ``last_code``, ``last_prompt``) is per-instance, exactly
    like the R version.
    """

    last_raw: str = ""
    last_code: str = ""
    last_prompt: str = ""

    def __init__(
        self,
        catalog: dict[str, specs.CatalogEntry] | None = None,
        temperature_select: float = 0.0,
        temperature_generate: float = 0.2,
    ) -> None:
        self._catalog: dict[str, specs.CatalogEntry] = catalog or specs.CATALOG
        self._df: pd.DataFrame | None = None
        self._data_summary: str = ""
        self._temperature_select = temperature_select
        self._temperature_generate = temperature_generate

    # ---- chainable setup mirrors PlotR's load_spec / inspect -----------
    def load_catalog(self, catalog: dict[str, specs.CatalogEntry]) -> PlotAgent:
        """Replace the catalog (for testing or alternative spec sets)."""
        self._catalog = catalog
        return self

    def inspect(self, df: pd.DataFrame) -> PlotAgent:
        """Attach a DataFrame and pre-compute its text summary."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"inspect() expects a pandas DataFrame, got {type(df).__name__}")
        self._df = df
        self._data_summary = self._summarize_df(df)
        return self

    # ---- the main entry point ------------------------------------------
    def ask(
        self,
        prompt: str,
        mode: str = "strict",
        interactive: bool | None = None,
        plot_type: str | None = None,
    ) -> PlotResult:
        """Generate a plot from a natural-language prompt.

        Parameters
        ----------
        prompt
            What you want the plot to show, in plain English.
        mode
            ``"strict"`` uses the catalog's verbatim template (fast, exact);
            ``"loose"`` lets the LLM adapt aesthetics to your DataFrame.
        interactive
            ``True`` to filter the catalog to interactive (plotly) entries,
            ``False`` for static only.  ``None`` lets the LLM choose.
        plot_type
            Skip the selection step and force a specific catalog entry.
            Useful for the per-plot wrappers in :mod:`plotpy.plots`.
        """
        if mode not in ("strict", "loose"):
            raise ValueError("mode must be 'strict' or 'loose'")
        if self._df is None:
            raise RuntimeError("Call .inspect(df) before .ask(...)")

        self.last_prompt = prompt

        # Step 1 — selection (or override)
        if plot_type is not None:
            if plot_type not in self._catalog:
                raise KeyError(f"plot_type={plot_type!r} not in catalog")
            chosen = plot_type
            alternatives: list[str] = []
        else:
            chosen, alternatives = self._select_plot(prompt, interactive)

        entry = self._catalog[chosen]

        # Step 2 — code generation
        spec_text = entry["strict"] if mode == "strict" else entry["loose"]
        code = self._generate_code(prompt, entry, spec_text, mode)
        self.last_code = code

        # Step 3 — execute
        plot = self._execute(code, entry)
        return PlotResult(plot=plot, chosen=chosen, alternatives=alternatives, code=code)

    # =====================================================================
    # internal: selection
    # =====================================================================
    def _select_plot(
        self, prompt: str, interactive: bool | None
    ) -> tuple[str, list[str]]:
        """First LLM call: ask the model to pick a catalog entry."""
        candidates = {
            name: e["summary"]
            for name, e in self._catalog.items()
            if interactive is None or e["interactive"] == interactive
        }
        if not candidates:
            raise RuntimeError(
                f"No catalog entries match interactive={interactive!r}"
            )
        catalog_text = "\n".join(f"- {n}: {s}" for n, s in candidates.items())

        system = dedent(
            """
            You are a plot-chooser.  Given a data summary, a user request,
            and a catalog of plot recipes (name + one-line description),
            pick the single best plot for the request and two runners-up.

            Reply with JSON only, no prose:
              {"chosen": "<name>", "alternatives": ["<name>", "<name>"]}

            All three names must come from the catalog.  Do not invent names.
            """
        ).strip()

        user = dedent(
            f"""
            DATA SUMMARY
            ------------
            {self._data_summary}

            USER REQUEST
            ------------
            {prompt}

            CATALOG
            -------
            {catalog_text}
            """
        ).strip()

        raw = self._chat(system, user, temperature=self._temperature_select)
        self.last_raw = raw

        try:
            obj = json.loads(_extract_json(raw))
            chosen = obj["chosen"]
            alts = list(obj.get("alternatives", []))[:2]
        except Exception as e:
            raise RuntimeError(
                f"Could not parse plot-selection JSON: {e}\n\nRaw response:\n{raw}"
            ) from e

        if chosen not in self._catalog:
            raise RuntimeError(
                f"LLM picked unknown plot {chosen!r}.  Raw response stored on .last_raw."
            )
        alts = [a for a in alts if a in self._catalog and a != chosen]
        return chosen, alts

    # =====================================================================
    # internal: generation
    # =====================================================================
    def _generate_code(
        self,
        prompt: str,
        entry: specs.CatalogEntry,
        spec_text: str,
        mode: str,
    ) -> str:
        """Second LLM call: produce one fenced python block that assigns ``p``."""
        if mode == "strict":
            instruction = (
                "Use the STRICT TEMPLATE below as your starting point.  Adapt only the"
                " column names to match the DataFrame.  Keep aesthetics (palette,"
                " spines, labels) exactly as written."
            )
        else:
            instruction = (
                "Apply the LOOSE CONVENTIONS below to the DataFrame.  You may rename"
                " variables and restructure, but keep the palette + spine rules."
            )

        available = ", ".join(self._injected_names(entry))

        system = dedent(
            f"""
            You write Python code that produces a single plot.

            - Respond with EXACTLY ONE fenced ```python``` code block and nothing else.
            - The pandas DataFrame is already in scope as `df` — do not redefine it.
            - The following names are ALREADY in your namespace; do not import or
              redefine them, and do NOT reference any name outside this list:
                {available}
            - For colours, use the named constants (GREEN, BLUE, AMBER, RED, PURPLE,
              GREY) or the COURSE_PAL list.  There is no variable called `palette`.
            - Assign the final plot to a variable named `p`.
            - Do NOT call plt.show(), fig.show(), or save the figure.
            - {instruction}
            """
        ).strip()

        user = dedent(
            f"""
            DATA SUMMARY
            ------------
            {self._data_summary}

            USER REQUEST
            ------------
            {prompt}

            CHOSEN PLOT
            -----------
            name: {self.last_raw and ''}  (library={entry["library"]}, interactive={entry["interactive"]})

            {"STRICT TEMPLATE" if mode == "strict" else "LOOSE CONVENTIONS"}
            ----------------
            {spec_text}
            """
        ).strip()

        raw = self._chat(system, user, temperature=self._temperature_generate)
        self.last_raw = raw  # overwrites the selection-step raw
        return _extract_python(raw)

    # =====================================================================
    # internal: execution
    # =====================================================================
    def _execute(self, code: str, entry: specs.CatalogEntry) -> Any:
        """exec() ``code`` in a fresh namespace and return ``p``."""
        ns = self._build_namespace(entry)
        try:
            exec(code, ns)  # noqa: S102
        except Exception as e:
            raise RuntimeError(
                f"Generated code failed at exec time: {e!r}\n\n"
                f"Code (also on .last_code):\n{code}"
            ) from e

        if "p" not in ns:
            raise RuntimeError(
                "Generated code did not assign `p`.  See .last_code / .last_raw."
            )
        return ns["p"]

    _PALETTE_NAMES = (
        "GREEN BLUE AMBER RED PURPLE GREY INK CREAM LINE MUTED "
        "COURSE_PAL FONT_FAMILY"
    ).split()
    _THEME_HELPERS = [
        "apply_base_theme_mpl", "apply_base_theme_sns",
        "apply_base_theme_p9", "apply_base_theme_plotly",
    ]
    _LIB_NAMES: dict[str, list[str]] = {
        "matplotlib": ["plt"],
        "seaborn":    ["plt", "sns"],
        "plotly":     ["px", "go"],
        "plotnine":   ["p9", "ggplot", "aes", "geom_point", "geom_line",
                       "geom_bar", "geom_boxplot", "geom_smooth", "labs", "theme"],
    }

    @classmethod
    def _injected_names(cls, entry: specs.CatalogEntry) -> list[str]:
        """Names the agent will bind in the exec namespace for ``entry``.

        Used both to build the namespace at exec time AND to enumerate the
        available names in the generation system prompt — keeping the LLM
        from inventing variables like ``palette`` that nothing binds.
        """
        return (
            ["df", "np", "pd"]
            + cls._LIB_NAMES[entry["library"]]
            + cls._PALETTE_NAMES
            + cls._THEME_HELPERS
        )

    def _build_namespace(self, entry: specs.CatalogEntry) -> dict[str, Any]:
        """Pre-import the libraries the chosen entry's code expects."""
        ns: dict[str, Any] = {"df": self._df}

        # always-on
        import numpy as np

        ns["np"] = np
        ns["pd"] = pd

        # palette + theme helpers (sourced from specs)
        for name in self._PALETTE_NAMES:
            ns[name] = getattr(specs, name)
        for name in self._THEME_HELPERS:
            ns[name] = getattr(specs, name)

        # library-specific imports
        lib = entry["library"]
        if lib in ("matplotlib", "seaborn"):
            import matplotlib.pyplot as plt

            ns["plt"] = plt
        if lib == "seaborn":
            import seaborn as sns

            ns["sns"] = sns
        if lib == "plotly":
            import plotly.express as px
            import plotly.graph_objects as go

            ns["px"] = px
            ns["go"] = go
        if lib == "plotnine":
            import plotnine as p9

            ns["p9"] = p9
            # also expose the most-used names so prompts read like ggplot
            for n in ("ggplot", "aes", "geom_point", "geom_line", "geom_bar",
                      "geom_boxplot", "geom_smooth", "labs", "theme"):
                if hasattr(p9, n):
                    ns[n] = getattr(p9, n)
        return ns

    # =====================================================================
    # internal: HTTP plumbing
    # =====================================================================
    def _chat(self, system: str, user: str, temperature: float) -> str:
        cfg = get_config()
        client = get_client()
        resp = client.chat.completions.create(
            model=cfg.model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content or ""

    # =====================================================================
    # internal: data summary
    # =====================================================================
    @staticmethod
    def _summarize_df(df: pd.DataFrame) -> str:
        head = df.head(4).to_string(max_cols=12)
        dtypes = "\n".join(f"  {c}: {t}" for c, t in df.dtypes.items())
        return dedent(
            f"""
            shape: {df.shape[0]} rows × {df.shape[1]} columns
            columns:
            {dtypes}

            head:
            {head}
            """
        ).strip()


# ---------------------------------------------------------------- regex parsers
_PY_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
_JSON_OBJ = re.compile(r"\{.*\}", re.DOTALL)


def _extract_python(text: str) -> str:
    """Pull the first fenced ```python``` block out of an LLM response."""
    m = _PY_FENCE.search(text)
    if m:
        return m.group(1).strip()
    # fall back: assume the whole response is code (some models drop fences)
    return text.strip()


def _extract_json(text: str) -> str:
    """Pull the first ``{...}`` object out of an LLM response."""
    m = _JSON_OBJ.search(text)
    if not m:
        raise ValueError("no JSON object found in LLM response")
    return m.group(0)
