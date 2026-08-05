"""LLM-driven plotting agent — selection, suggestion, generation, self-repair.

Redesigned from the two-call mirror of PlotR into a small agent that:

1. **Suggests** — :meth:`PlotAgent.suggest` reasons over the data (grounded in
   the course catalog) and returns a *ranked menu* of plot ideas with a reason
   each, before writing any code.  This is the "just suggest me plots" path.
2. **Selects** — for ``mode="strict"`` / ``"loose"`` it still picks one catalog
   entry, exactly like before.
3. **Generates + self-repairs** — the generated code is ``exec``'d in a fresh
   namespace; if it raises, the traceback is fed back to the model and the code
   is regenerated, up to ``max_repairs`` times.  This loop is why weak/free
   models become usable: first-try failures get fixed instead of surfacing.
4. **Free mode** — ``mode="free"`` skips the catalog entirely and lets the model
   write open-ended plotting code (any of matplotlib/seaborn/plotly/plotnine),
   grounded in the course theme.  Unlocks Day-3 and novel charts on any data.

The model behind all of this is a :class:`plotpy.providers.Chat`, so you can
swap providers (Groq / OpenAI / Anthropic / Ollama …) at any time.
"""

from __future__ import annotations

import json
import re
import sys
import traceback
from dataclasses import dataclass, field
from textwrap import dedent
from typing import Any

import pandas as pd

from . import specs
from .providers import Chat, get_active

# What the model is allowed to lean on, stated once and injected into every
# generation/repair/free prompt. This IS the "trained on the course" grounding:
# the palette, theme appliers, and house rules that make output look on-deck.
COURSE_KNOWLEDGE = dedent(
    """
    You are PlotPy, a plotting assistant for the "Genomics Viz with Python"
    course. You write clean, publication-quality Python that matches the course
    house style:

    - Colours: use the named constants GREEN, BLUE, AMBER, RED, PURPLE, GREY
      (plus INK, CREAM, LINE, MUTED) or the COURSE_PAL list. There is NO
      variable called `palette`. RED = highlight / up / significant.
    - Theme: after building a matplotlib/seaborn axes you may call
      apply_base_theme_mpl(ax) / apply_base_theme_sns(grid); for plotly
      apply_base_theme_plotly(fig); for plotnine apply_base_theme_p9(p).
    - Hide the top and right spines on matplotlib axes; keep titles that state
      the finding, not the mechanism.
    - The DataFrame is already in scope as `df` — never redefine it, never read
      a file. Adapt to the ACTUAL column names shown in the data summary.
    - Assign the final figure to a variable named `p`
      (matplotlib Figure / seaborn grid / plotly Figure / plotnine ggplot).
    - Do NOT call plt.show(), fig.show(), or save anything to disk.
    - Respond with EXACTLY ONE fenced ```python``` code block and nothing else.
    """
).strip()


# ----------------------------------------------------------- public result types
@dataclass
class Suggestion:
    """One entry in :meth:`PlotAgent.suggest`'s ranked menu."""

    name: str            # catalog entry name, or a short slug for a custom idea
    reason: str          # one line: why this plot fits THIS data
    library: str = ""    # matplotlib / seaborn / plotly / plotnine
    interactive: bool = False
    in_catalog: bool = False

    def _repr_html_(self) -> str:
        tag = "" if self.in_catalog else " <i>(custom)</i>"
        star = " ⚡" if self.interactive else ""
        return f"<li><code>{self.name}</code>{tag}{star} — {self.reason}</li>"


@dataclass
class PlotResult:
    """What :meth:`PlotAgent.ask` returns.

    Attributes
    ----------
    plot
        The rendered object (matplotlib Figure / seaborn grid / plotly Figure /
        plotnine ggplot).
    chosen
        The catalog entry the agent picked, or ``"free"`` in free mode.
    alternatives
        Up to two other catalog entries considered — the "next best" hints.
    code
        The exact source that produced ``plot`` (post-repair, if any).
    repairs
        How many repair attempts it took (0 = worked first try).
    """

    plot: Any
    chosen: str
    alternatives: list[str] = field(default_factory=list)
    code: str = ""
    repairs: int = 0

    def _repr_html_(self) -> str:
        alt = ", ".join(self.alternatives) or "—"
        rep = f" &nbsp;<b>repairs:</b> {self.repairs}" if self.repairs else ""
        return (
            f"<div><b>plot:</b> {type(self.plot).__name__} &nbsp;"
            f"<b>chosen:</b> <code>{self.chosen}</code> &nbsp;"
            f"<b>alternatives:</b> {alt}{rep}</div>"
        )


# ----------------------------------------------------------------- agent class
class PlotAgent:
    """Stateful, one-DataFrame agent.

    Call :meth:`inspect` to load a frame, then :meth:`suggest` for a menu or
    :meth:`ask` to render one plot.  All debugging state (``last_code``,
    ``last_raw_*``, ``last_repairs``) is per-instance.
    """

    last_code: str = ""
    last_prompt: str = ""
    last_raw_select: str = ""
    last_raw_generate: str = ""
    last_raw_suggest: str = ""

    def __init__(
        self,
        chat: Chat | None = None,
        catalog: dict[str, specs.CatalogEntry] | None = None,
        temperature_select: float = 0.0,
        temperature_generate: float = 0.2,
        max_repairs: int = 3,
    ) -> None:
        self._chat_obj = chat  # None → resolved lazily from the active model
        self._catalog: dict[str, specs.CatalogEntry] = catalog or specs.CATALOG
        self._df: pd.DataFrame | None = None
        self._data_summary: str = ""
        self._temperature_select = temperature_select
        self._temperature_generate = temperature_generate
        self._max_repairs = max_repairs
        self.last_repairs: list[dict[str, str]] = []
        self.last_suggestions: list[Suggestion] = []

    @property
    def chat(self) -> Chat:
        """The active model (explicit ``chat=`` or the global default)."""
        return self._chat_obj if self._chat_obj is not None else get_active()

    @property
    def last_raw(self) -> str:
        """Most recent raw LLM response (generation, else selection)."""
        return self.last_raw_generate or self.last_raw_select

    # ---- chainable setup ------------------------------------------------
    def load_catalog(self, catalog: dict[str, specs.CatalogEntry]) -> PlotAgent:
        self._catalog = catalog
        return self

    def inspect(self, df: pd.DataFrame) -> PlotAgent:
        """Attach a DataFrame and pre-compute its text summary."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"inspect() expects a pandas DataFrame, got {type(df).__name__}")
        self._df = df
        self._data_summary = self._summarize_df(df)
        return self

    # =====================================================================
    # suggest — the ranked menu, no code
    # =====================================================================
    def suggest(self, n: int = 6, interactive: bool | None = None) -> list[Suggestion]:
        """Return up to ``n`` plot ideas ranked for the attached DataFrame.

        Grounded in the course catalog but free to propose custom charts the
        catalog doesn't cover.  Produces *no* code — pick one and pass its
        ``name`` to :meth:`ask` (``plot_type=`` for catalog names, or just
        describe it in a prompt).
        """
        if self._df is None:
            raise RuntimeError("Call .inspect(df) before .suggest()")

        catalog_text = "\n".join(
            f"- {name}: {e['summary']} (library={e['library']}, interactive={e['interactive']})"
            for name, e in self._catalog.items()
            if interactive is None or e["interactive"] == interactive
        )
        system = dedent(
            f"""
            You are a data-visualisation advisor for a genomics course. Given a
            data summary and a catalog of known plot recipes, propose the best
            plots for THIS dataset, ranked best first.

            Prefer catalog entries when one fits (set "in_catalog": true and use
            its exact name). When nothing in the catalog fits well, propose a
            custom plot (set "in_catalog": false, give a short slug name).

            Reply with JSON only, no prose:
              {{"suggestions": [
                 {{"name": "...", "reason": "...", "library": "matplotlib|seaborn|plotly|plotnine",
                   "interactive": false, "in_catalog": true}}
              ]}}
            Give at most {n} suggestions. Each reason is one sentence tied to the
            actual columns.
            """
        ).strip()
        user = dedent(
            f"""
            DATA SUMMARY
            ------------
            {self._data_summary}

            CATALOG
            -------
            {catalog_text}
            """
        ).strip()

        raw = self._complete(system, user, temperature=self._temperature_select, json_mode=True)
        self.last_raw_suggest = raw
        try:
            obj = json.loads(_extract_json(raw))
            items = obj.get("suggestions", obj if isinstance(obj, list) else [])
        except Exception as e:
            raise RuntimeError(
                f"Could not parse suggestions JSON: {e}\n\nRaw response:\n{raw}"
            ) from e

        out: list[Suggestion] = []
        for it in items[:n]:
            if not isinstance(it, dict) or "name" not in it:
                continue
            name = str(it["name"])
            in_cat = bool(it.get("in_catalog", name in self._catalog)) or name in self._catalog
            entry = self._catalog.get(name)
            out.append(Suggestion(
                name=name,
                reason=str(it.get("reason", "")).strip(),
                library=str(it.get("library", entry["library"] if entry else "")),
                interactive=bool(it.get("interactive", entry["interactive"] if entry else False)),
                in_catalog=in_cat,
            ))
        self.last_suggestions = out
        return out

    # =====================================================================
    # ask — select (or free) → generate → execute-with-repair
    # =====================================================================
    def ask(
        self,
        prompt: str,
        mode: str = "strict",
        interactive: bool | None = None,
        plot_type: str | None = None,
        max_repairs: int | None = None,
    ) -> PlotResult:
        """Generate one plot from a natural-language prompt.

        Parameters
        ----------
        mode
            ``"strict"`` — verbatim catalog template, only column names change.
            ``"loose"`` — adapt the catalog recipe's aesthetics to your data.
            ``"free"``  — no catalog; open-ended chart grounded in the theme.
        interactive
            ``True``/``False`` to force/forbid plotly; ``None`` lets the model choose.
        plot_type
            Force a specific catalog entry, skipping selection.
        max_repairs
            Override the agent's repair-attempt budget for this call.
        """
        if mode not in ("strict", "loose", "free"):
            raise ValueError("mode must be 'strict', 'loose', or 'free'")
        if self._df is None:
            raise RuntimeError("Call .inspect(df) before .ask(...)")

        self.last_prompt = prompt
        budget = self._max_repairs if max_repairs is None else max_repairs

        if mode == "free":
            code = self._generate_free(prompt, interactive)
            plot, code, n = self._execute_with_repair(code, None, prompt, mode, budget)
            return PlotResult(plot=plot, chosen="free", alternatives=[], code=code, repairs=n)

        # strict / loose — catalog path
        if plot_type is not None:
            if plot_type not in self._catalog:
                raise KeyError(f"plot_type={plot_type!r} not in catalog")
            chosen, alternatives = plot_type, []
        else:
            chosen, alternatives = self._select_plot(prompt, interactive)

        entry = self._catalog[chosen]
        spec_text = entry["strict"] if mode == "strict" else entry["loose"]
        code = self._generate_code(prompt, chosen, entry, spec_text, mode)
        plot, code, n = self._execute_with_repair(code, entry, prompt, mode, budget)
        return PlotResult(plot=plot, chosen=chosen, alternatives=alternatives, code=code, repairs=n)

    # =====================================================================
    # internal: selection
    # =====================================================================
    def _select_plot(self, prompt: str, interactive: bool | None) -> tuple[str, list[str]]:
        candidates = {
            name: e["summary"]
            for name, e in self._catalog.items()
            if interactive is None or e["interactive"] == interactive
        }
        if not candidates:
            raise RuntimeError(f"No catalog entries match interactive={interactive!r}")
        catalog_text = "\n".join(f"- {n}: {s}" for n, s in candidates.items())

        system = dedent(
            """
            You are a plot-chooser. Given a data summary, a user request, and a
            catalog of plot recipes (name + one-line description), pick the single
            best plot and two runners-up.

            Reply with JSON only, no prose:
              {"chosen": "<name>", "alternatives": ["<name>", "<name>"]}
            All three names must come from the catalog. Do not invent names.
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

        raw = self._complete(system, user, temperature=self._temperature_select, json_mode=True)
        self.last_raw_select = raw
        self.last_raw_generate = ""  # a new ask() invalidates the old generation

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
                f"LLM picked unknown plot {chosen!r}. Raw response on .last_raw_select."
            )
        alts = [a for a in alts if a in self._catalog and a != chosen]
        return chosen, alts

    # =====================================================================
    # internal: generation (catalog + free)
    # =====================================================================
    def _generate_code(
        self, prompt: str, chosen_name: str, entry: specs.CatalogEntry,
        spec_text: str, mode: str,
    ) -> str:
        if mode == "strict":
            instruction = (
                "Use the STRICT TEMPLATE below as your starting point. Adapt only the"
                " column names to match the DataFrame. Keep aesthetics (palette,"
                " spines, labels) exactly as written."
            )
        else:
            instruction = (
                "Apply the LOOSE CONVENTIONS below to the DataFrame. You may rename"
                " variables and restructure, but keep the palette + spine rules."
            )
        available = ", ".join(self._injected_names(entry))
        system = (
            COURSE_KNOWLEDGE
            + "\n\n- These names are ALREADY in scope; do not import or redefine "
            f"them, and do not reference any name outside this list:\n    {available}\n"
            f"- {instruction}"
        )
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
            name: {chosen_name}  (library={entry["library"]}, interactive={entry["interactive"]})
            summary: {entry["summary"]}

            {"STRICT TEMPLATE" if mode == "strict" else "LOOSE CONVENTIONS"}
            ----------------
            {spec_text}
            """
        ).strip()

        raw = self._complete(system, user, temperature=self._temperature_generate)
        self.last_raw_generate = raw
        return _extract_python(raw)

    def _generate_free(self, prompt: str, interactive: bool | None) -> str:
        """Open-ended generation — no catalog template, any library."""
        available = ", ".join(self._injected_names(None))
        if interactive is True:
            lib_hint = "Use plotly (px / go) so the chart is interactive (hover/zoom)."
        elif interactive is False:
            lib_hint = "Use matplotlib or seaborn (static figure)."
        else:
            lib_hint = ("Choose the library that best fits the request: matplotlib/seaborn "
                        "for static, plotly for interactive.")
        system = (
            COURSE_KNOWLEDGE
            + "\n\n- These names are ALREADY in scope; do not import or redefine "
            f"them:\n    {available}\n- {lib_hint}\n- Pick the single best chart "
            "for the request and the data; label axes and give an informative title."
        )
        user = dedent(
            f"""
            DATA SUMMARY
            ------------
            {self._data_summary}

            USER REQUEST
            ------------
            {prompt}
            """
        ).strip()
        raw = self._complete(system, user, temperature=self._temperature_generate)
        self.last_raw_generate = raw
        return _extract_python(raw)

    def _repair_code(self, prompt: str, entry: specs.CatalogEntry | None,
                     mode: str, broken_code: str, tb: str) -> str:
        """Ask the model to fix code that just raised, given the traceback."""
        available = ", ".join(self._injected_names(entry))
        system = (
            COURSE_KNOWLEDGE
            + "\n\n- These names are ALREADY in scope; do not import or redefine "
            f"them:\n    {available}\n- Return the FULL corrected script, not a diff."
        )
        # Re-state the spec on repair. Without it a strict-mode fix is generated
        # blind to the template it was supposed to follow, so the repaired plot
        # silently drifts off the course house style.
        spec_block = ""
        if entry is not None and mode in ("strict", "loose"):
            spec_text = entry["strict"] if mode == "strict" else entry["loose"]
            label = "STRICT TEMPLATE" if mode == "strict" else "LOOSE CONVENTIONS"
            spec_block = f"\n{label}\n{'-' * len(label)}\n{spec_text}\n"
        user = dedent(
            f"""
            The Python below was meant to satisfy this request:
                {prompt}

            It raised an error when executed. Fix the cause and return the full
            corrected code. Common causes: a column name that isn't in the data,
            a wrong library API call, or referencing an undefined name.

            DATA SUMMARY
            ------------
            {self._data_summary}
            {spec_block}

            CODE THAT FAILED
            ----------------
            ```python
            {broken_code}
            ```

            ERROR / TRACEBACK
            -----------------
            {tb[-1600:]}
            """
        ).strip()
        raw = self._complete(system, user, temperature=self._temperature_generate)
        self.last_raw_generate = raw
        return _extract_python(raw)

    # =====================================================================
    # internal: execution with self-repair
    # =====================================================================
    def _execute_with_repair(
        self, code: str, entry: specs.CatalogEntry | None,
        prompt: str, mode: str, max_repairs: int,
    ) -> tuple[Any, str, int]:
        """exec ``code``; on failure feed the traceback back and regenerate.

        Returns ``(plot, final_code, n_repairs)``.  Raises only after the repair
        budget is exhausted, with the full attempt history on ``last_repairs``.
        """
        self.last_repairs = []
        attempt = 0
        while True:
            self.last_code = code
            try:
                plot = self._execute(code, entry)
                return plot, code, attempt
            except ModuleNotFoundError as e:
                # A missing package can't be fixed by regenerating code — don't
                # burn repair attempts on it; surface an install hint instead.
                self.last_repairs.append({"error": f"ModuleNotFoundError: {e}", "code": code})
                raise RuntimeError(
                    f"The generated plot needs a package that isn't installed: {e.name!r}. "
                    f"Install it (e.g. `pip install {e.name}`) and re-run. "
                    "Some catalog plots use optional packages — see plotpy[extras]."
                ) from e
            except Exception as e:
                tb = traceback.format_exc()
                self.last_repairs.append({"error": f"{type(e).__name__}: {e}", "code": code})
                if attempt >= max_repairs:
                    raise RuntimeError(
                        f"Generated code still failing after {attempt} repair "
                        f"attempt(s). Last error: {type(e).__name__}: {e}\n\n"
                        f"Last code (also on .last_code):\n{code}"
                    ) from e
                attempt += 1
                code = self._repair_code(prompt, entry, mode, code, tb)

    def _execute(self, code: str, entry: specs.CatalogEntry | None) -> Any:
        ns = self._build_namespace(entry)
        before = _open_figure_ids()
        try:
            exec(code, ns)  # noqa: S102
            return _resolve_figure(ns)
        except BaseException:
            # A failed attempt usually leaves a half-built figure open. Without
            # this the repair loop leaks one figure per try — matplotlib warns
            # past 20, and a long-lived server (BiMA) grows without bound.
            _close_figures_since(before)
            raise

    _PALETTE_NAMES = (
        "GREEN BLUE AMBER RED PURPLE GREY INK CREAM LINE MUTED "
        "COURSE_PAL FONT_FAMILY"
    ).split()
    _THEME_HELPERS = [
        "apply_base_theme_mpl", "apply_base_theme_sns",
        "apply_base_theme_p9", "apply_base_theme_plotly",
    ]
    _PLOTNINE_NAMES = ["p9", "ggplot", "aes", "geom_point", "geom_line",
                       "geom_bar", "geom_boxplot", "geom_smooth", "labs", "theme"]
    _LIB_NAMES: dict[str, list[str]] = {
        "matplotlib": ["plt"],
        "seaborn":    ["plt", "sns"],
        "plotly":     ["px", "go"],
        "plotnine":   _PLOTNINE_NAMES,
    }
    _ALL_LIB_NAMES = ["plt", "sns", "px", "go", *_PLOTNINE_NAMES]

    @classmethod
    def _injected_names(cls, entry: specs.CatalogEntry | None) -> list[str]:
        """Names bound in the exec namespace. ``entry=None`` (free) → everything.

        An entry whose ``library`` isn't one of the four known keys also gets
        everything: external catalogs label recipes freely ("Plotly Express",
        "SciPy + Plotly", "scikit-learn"), and injecting too much is harmless
        where guessing wrong is a guaranteed NameError.
        """
        if entry is None:
            libs = cls._ALL_LIB_NAMES
        else:
            libs = cls._LIB_NAMES.get(entry["library"], cls._ALL_LIB_NAMES)
        return ["df", "np", "pd", *libs, *cls._PALETTE_NAMES, *cls._THEME_HELPERS]

    def _build_namespace(self, entry: specs.CatalogEntry | None) -> dict[str, Any]:
        """Pre-import what the code expects. Free mode gets every library."""
        import numpy as np

        ns: dict[str, Any] = {"df": self._df, "np": np, "pd": pd}
        for name in self._PALETTE_NAMES:
            ns[name] = getattr(specs, name)
        for name in self._THEME_HELPERS:
            ns[name] = getattr(specs, name)

        # Derive from _injected_names so what we *promise* the model is in scope
        # and what we actually bind can never drift apart.
        wanted = set(self._injected_names(entry))
        want_mpl = "plt" in wanted
        want_sns = "sns" in wanted
        want_plotly = "px" in wanted
        want_p9 = "p9" in wanted

        if want_mpl:
            import matplotlib.pyplot as plt
            ns["plt"] = plt
        if want_sns:
            try:
                import seaborn as sns
                ns["sns"] = sns
            except ImportError:
                pass
        if want_plotly:
            try:
                import plotly.express as px
                import plotly.graph_objects as go
                ns["px"], ns["go"] = px, go
            except ImportError:
                pass
        if want_p9:
            try:
                import plotnine as p9
                ns["p9"] = p9
                for n in self._PLOTNINE_NAMES[1:]:
                    if hasattr(p9, n):
                        ns[n] = getattr(p9, n)
            except ImportError:
                pass
        return ns

    # =====================================================================
    # internal: LLM plumbing
    # =====================================================================
    def _complete(self, system: str, user: str, temperature: float,
                  json_mode: bool = False) -> str:
        return self.chat.complete(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            json_mode=json_mode,
        )

    # =====================================================================
    # internal: data summary
    # =====================================================================
    _MAX_SUMMARY_COLS = 40

    @classmethod
    def _summarize_df(cls, df: pd.DataFrame) -> str:
        """Compact text summary the LLM sees — columns, dtypes, levels, head.

        Categorical levels matter: head(4) on a grouped frame hides other
        levels and lets the model hard-code only what it saw.

        Wide frames are truncated to :attr:`_MAX_SUMMARY_COLS` columns. A
        2000-gene expression matrix would otherwise emit a ~40k-character
        summary into *every* prompt (select, generate, and each repair) — an
        easy way to blow the context window and the bill on a user upload.
        """
        col_lines: list[str] = []
        for c in df.columns[: cls._MAX_SUMMARY_COLS]:
            t = df[c].dtype
            line = f"  {c}: {t}"
            if not pd.api.types.is_numeric_dtype(t):
                uniques = df[c].dropna().unique()
                shown = list(uniques[:8])
                more = f" (+{len(uniques) - 8} more)" if len(uniques) > 8 else ""
                line += f"  levels={shown}{more}"
            col_lines.append(line)
        hidden = df.shape[1] - cls._MAX_SUMMARY_COLS
        if hidden > 0:
            col_lines.append(
                f"  … +{hidden} more columns not listed (last is {df.columns[-1]!r}); "
                "select columns programmatically rather than by name"
            )
        head = df.head(4).to_string(max_cols=12)
        return dedent(
            f"""
            shape: {df.shape[0]} rows × {df.shape[1]} columns
            columns:
            {chr(10).join(col_lines)}

            head:
            {head}
            """
        ).strip()


# ------------------------------------------------------------- figure hygiene
def _pyplot() -> Any:
    """``matplotlib.pyplot`` if it has already been imported, else ``None``.

    Deliberately does not import it: if pyplot was never loaded, no figure can
    be open, and a plotly-only run shouldn't pay to find that out.
    """
    return sys.modules.get("matplotlib.pyplot")


def _open_figure_ids() -> set[int]:
    plt = _pyplot()
    return set(plt.get_fignums()) if plt is not None else set()


def _close_figures_since(before: set[int]) -> None:
    """Close figures opened since ``before`` — never ones the caller already had."""
    plt = _pyplot()
    if plt is None:
        return
    for num in set(plt.get_fignums()) - before:
        plt.close(num)


# --------------------------------------------------------- result validation
_FIGURE_MODULES = {"matplotlib", "seaborn", "plotly", "plotnine"}
# Escape hatch for figure-like objects from elsewhere (pyCirclize, pyMSAviz …).
_FIGURE_DUCK_ATTRS = ("savefig", "to_plotly_json", "plotfig", "draw")


def _looks_like_figure(obj: Any) -> bool:
    if obj is None:
        return False
    if type(obj).__module__.split(".")[0] in _FIGURE_MODULES:
        return True
    return any(hasattr(obj, a) for a in _FIGURE_DUCK_ATTRS)


def _resolve_figure(ns: dict[str, Any]) -> Any:
    """Pull the figure out of an executed namespace, or raise so repair can fix it.

    Anything raised here lands in the traceback the repair loop feeds back, so
    the message is written for the model as much as for the user.
    """
    if _looks_like_figure(ns.get("p")):
        return ns["p"]
    # Models bind the figure to `fig` constantly. Accepting it beats spending a
    # whole repair round-trip on a one-line rename.
    for alt in ("fig", "figure"):
        if _looks_like_figure(ns.get(alt)):
            return ns[alt]
    if "p" not in ns:
        raise RuntimeError(
            "Generated code did not assign `p`. Assign the final figure to `p`."
        )
    got = ns["p"]
    shown = repr(got)
    if len(shown) > 120:
        shown = shown[:120] + "…"
    raise RuntimeError(
        f"Generated code assigned p = {shown} (type {type(got).__name__}), which is "
        "not a figure. Assign the matplotlib / seaborn / plotly / plotnine figure "
        "object to `p`."
    )


# ---------------------------------------------------------------- regex parsers
_PY_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def _extract_python(text: str) -> str:
    """Pull the first fenced ```python``` block; fall back to raw if it compiles."""
    m = _PY_FENCE.search(text)
    if m:
        return m.group(1).strip()
    candidate = text.strip()
    try:
        compile(candidate, "<llm-response>", "exec")
    except SyntaxError as e:
        raise RuntimeError(
            "LLM response contained no fenced ```python``` block and the raw text "
            f"does not parse as Python ({e.msg}). See .last_raw_generate."
        ) from None
    return candidate


def _extract_json(text: str) -> str:
    """Pull the first balanced ``{...}`` (or ``[...]``) object out of a response."""
    starts = [i for i in (text.find("{"), text.find("[")) if i != -1]
    if not starts:
        raise ValueError("no JSON object found in LLM response")
    start = min(starts)
    open_ch = text[start]
    close_ch = "}" if open_ch == "{" else "]"
    depth = 0
    in_str = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\" and in_str:
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    raise ValueError("unbalanced JSON object in LLM response")
