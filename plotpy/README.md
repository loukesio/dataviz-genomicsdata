# PlotPy

An LLM-driven plotting agent for the **Genomics Viz with Python** course —
Python sibling of [PlotR](https://github.com/loukesio/PlotR).

Give it a `pandas.DataFrame` and a sentence. PlotPy picks the right chart,
writes the matplotlib / seaborn / plotly / plotnine code in the course house
style, runs it, and hands you back both **the figure and the source that made
it**. If the code errors, it reads the traceback and fixes itself.

```python
import plotpy

plotpy.use(plotpy.chat_groq(api_key="gsk_..."))     # pick a model (free Groq here)
df = plotpy.datasets.gwas()

plotpy.suggest(df)                                   # "what should I plot?" → a ranked menu
res = plotpy.ask(df, "interactive GWAS Manhattan", mode="free", interactive=True)
res.plot                                             # the figure
res.code                                             # the exact code that drew it
```

---

## Contents

- [Install](#install)
- [Pick your LLM](#1-pick-your-llm) · [Suggest](#2-suggest-what-to-plot) · [Ask](#3-ask-for-a-plot) · [Your own data](#4-bring-your-own-data)
- [Strict vs loose vs free](#modes-strict-vs-loose-vs-free)
- [Self-repair](#self-repair)
- [Per-plot shortcuts](#per-plot-shortcuts)
- [The catalog](#the-catalog--what-plotpy-knows)
- [Debugging](#debugging-a-result) · [Theming](#theming) · [Troubleshooting](#troubleshooting)

---

## Install

PlotPy lives in the course repo under [`plotpy/`](.).

```bash
# From a notebook / Colab cell — install straight from GitHub:
pip install "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"

# Or if you cloned the repo:
pip install -e ./plotpy
```

Some catalog plots use optional packages (adjustText, pywaffle, squarify,
ternary-diagram, scikit-learn, and — for the Day-3 entries — `upsetplot` /
`PyComplexHeatmap`). Pull the common ones with the `extras` group:

```bash
pip install "plotpy[extras] @ git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"
```

If a plot needs a package you don't have, PlotPy stops with a clear
`pip install <package>` hint instead of failing cryptically.

> **In Colab:** after the first install, **Runtime → Restart session** once, or
> Python keeps the old module in memory. There's a ready-made notebook:
> [`notebooks/00_colab_quickstart.ipynb`](notebooks/00_colab_quickstart.ipynb).

---

## Usage

### 1. Pick your LLM

Like R's [`ellmer`](https://ellmer.tidyverse.org), PlotPy has one constructor
per provider. They all return the same `Chat`, and `plotpy.use(...)` sets the
active model — **switch it whenever you like**.

```python
import plotpy
from plotpy import chat_groq, chat_openai, chat_anthropic, chat_ollama

plotpy.use(chat_groq())                          # free tier, the default
plotpy.use(chat_openai(model="gpt-4o-mini"))     # stronger first-try code (paid)
plotpy.use(chat_anthropic())                     # Claude
plotpy.use(chat_ollama(model="llama3.1"))        # fully local, no key
```

| Constructor        | Provider  | Default model                       | Key env var         |
| ------------------ | --------- | ----------------------------------- | ------------------- |
| `chat_groq()`      | Groq      | `llama-3.3-70b-versatile`           | `GROQ_API_KEY`      |
| `chat_openai()`    | OpenAI    | `gpt-4o-mini`                       | `OPENAI_API_KEY`    |
| `chat_anthropic()` | Anthropic | `claude-3-5-sonnet-latest`          | `ANTHROPIC_API_KEY` |
| `chat_google()`    | Google    | `gemini-1.5-flash`                  | `GEMINI_API_KEY`    |
| `chat_together()`  | Together  | `Meta-Llama-3.1-70B-Instruct-Turbo` | `TOGETHER_API_KEY`  |
| `chat_fireworks()` | Fireworks | `llama-v3p3-70b-instruct`           | `FIREWORKS_API_KEY` |
| `chat_ollama()`    | Ollama    | `llama3.1`                          | — (local)           |
| `chat_vllm(model)` | vLLM      | (you name it)                       | — (local)           |

**Where the key comes from** (in order): the `api_key=` argument → the
provider's env var above → the generic `PLOTPY_API_KEY`. So you can also just
put `PLOTPY_API_KEY=...` (and optionally `GROQ_API_KEY=...`, etc.) in a `.env`
file next to your notebook and skip the argument.

> Get a free Groq key at [console.groq.com](https://console.groq.com) → **API
> Keys → Create** (no credit card). It looks like `gsk_...`.

**Use a specific model for one call only**, without changing the default:

```python
plotpy.ask(df, "volcano plot", llm=chat_openai())
```

**Legacy setup still works** — `plotpy.set_key("gsk_...")` (optionally with
`base_url=` / `model=`) configures the active model too.

### 2. Suggest what to plot

Don't know what to make? Ask for a ranked menu of ideas — no code yet. Each
suggestion is grounded in the course catalog, but the agent will also propose
custom charts the catalog doesn't cover.

```python
for s in plotpy.suggest(df):
    star = " ⚡" if s.interactive else ""
    print(f"{s.name}{star} — {s.reason}")
# manhattan_gwas ⚡ — genome-wide p-values across chromosomes
# volcano_deseq2    — separates up/down-regulated hits
# ...
```

Each item is a `Suggestion` with `.name`, `.reason`, `.library`,
`.interactive`, and `.in_catalog`. Pick one and render it (next section).

### 3. Ask for a plot

```python
res = plotpy.ask(df, "show which genes go up in drought")
res.plot            # the figure (auto-displays in a notebook)
res.chosen          # which catalog entry it used (or "free")
res.alternatives    # up to two runners-up
res.code            # the exact source that produced res.plot
res.repairs         # how many self-repairs it took (0 = first try)
```

Full signature:

```python
plotpy.ask(
    df,                      # your DataFrame
    prompt,                  # plain-English description
    mode="strict",           # "strict" | "loose" | "free"  (see below)
    interactive=None,        # True → plotly, False → static, None → agent decides
    llm=None,                # a chat_*() for this call only; None = active model
    max_repairs=None,        # override the self-repair budget (default 3)
)
```

### 4. Bring your own data

Any DataFrame works. Let the agent explore it:

```python
import pandas as pd
df = pd.read_csv("my_data.csv")

plotpy.suggest(df)                                   # what fits this data?
plotpy.ask(df, "compare the groups", mode="free")    # free mode adapts to any columns
```

If your columns happen to match a course schema (see
`plotpy.datasets.list_datasets()`), the [per-plot shortcuts](#per-plot-shortcuts)
and `mode="strict"` work directly; otherwise use `mode="loose"` or `mode="free"`
and the agent adapts to your actual column names.

---

## Modes: strict vs loose vs free

| Mode       | What the model gets                              | Reach for it when…                                        |
| ---------- | ------------------------------------------------ | --------------------------------------------------------- |
| `"strict"` | The catalog's **verbatim code**, swap col names  | Your columns match the course; you want the exact deck look |
| `"loose"`  | The catalog recipe's **prose conventions**       | Same chart *idea*, but your columns are named differently  |
| `"free"`   | **No template** — open-ended, themed by the course | Data or a chart the catalog never covered (Day-3, novel plots) |

```python
plotpy.ask(df, "two genes, colour by tissue", mode="strict")   # exact template
plotpy.ask(df, "two proteins, colour by cell type", mode="loose")  # adapts columns
plotpy.ask(df, "interactive UpSet of my marker sets", mode="free")  # anything
```

**Rule of thumb:** start `strict` if your data looks like the course; fall
through to `loose`, then `free`, as your data diverges.

---

## Self-repair

Every generated snippet is executed. If it raises — a wrong column name, a bad
API call, an undefined variable — PlotPy sends the traceback back to the model,
gets corrected code, and retries, up to `max_repairs` times (default 3). This is
what makes even the free Groq model reliable: first-try mistakes get fixed
instead of landing in your lap.

```python
res = plotpy.ask(df, "…", mode="free")
res.repairs                     # 0 if it worked first try, else the number of fixes

agent = plotpy.PlotAgent().inspect(df)
agent.ask("…")
agent.last_repairs              # [{"error": "...", "code": "..."}] for each failed try
```

A genuinely missing package is **not** retried — you get an immediate
`pip install <package>` hint instead of three wasted attempts.

---

## Per-plot shortcuts

Already know the chart you want? Skip the selection step. Each returns the same
`PlotResult` as `ask()`.

```python
plotpy.timecourse(df)     plotpy.scatter(df)      plotpy.bar(df)
plotpy.boxplot(df)        plotpy.violin(df)       plotpy.ridgeline(df)
plotpy.volcano(df)        plotpy.pca(df)          plotpy.heatmap(df)
plotpy.ternary(df)        plotpy.waffle(df)       plotpy.waterfall(df)
plotpy.admixture(df)      plotpy.microbiome(df)   plotpy.manhattan(df)
plotpy.treemap(df)        plotpy.upset(df)        plotpy.complexheatmap(df)
```

Pass `interactive=True` to any wrapper that has a plotly sibling (`scatter`,
`timecourse`, `volcano`, `manhattan`, `heatmap`) to get the hoverable version:

```python
plotpy.manhattan(plotpy.datasets.gwas(), interactive=True)
```

Every wrapper ships with synthetic data so you can try it with zero setup:

```python
plotpy.datasets.list_datasets()          # table: dataset → plot → schema
plotpy.volcano(plotpy.datasets.deseq2())
plotpy.upset(plotpy.datasets.gene_sets())
expr, meta = plotpy.datasets.expression_matrix()
plotpy.heatmap(expr)
```

---

## The catalog — what PlotPy knows

23 recipes spanning all three course days. Browse without any LLM call:

```python
plotpy.list_plots()             # every entry
plotpy.list_plots(day=2)        # by course day
plotpy.list_plots(library="plotly")     # by library
plotpy.list_plots(interactive=True)     # only the hoverable ones
```

- **Day 1 — foundations:** time-course, bar, scatter, boxplot, violin,
  ridgeline, volcano, PCA, heatmap, ternary, waffle, waterfall (+ interactive
  siblings for several).
- **Day 2 — genome-scale:** stacked-bar admixture, microbiome composition,
  Manhattan (static + interactive), treemap.
- **Day 3 — production packages:** `upset_gene_sets` (UpSetPlot),
  `heatmap_annotated` (PyComplexHeatmap).

Day-3 tools that take non-DataFrame input (trees, alignments, feature records —
Toytree, pyMSAviz, pyCirclize, …) aren't catalog entries; use `mode="free"` or
the Day-3 course notebooks for those.

---

## Debugging a result

The agent keeps everything from the last call, so you can see exactly what
happened:

```python
agent = plotpy.PlotAgent().inspect(df)
agent.ask("something surprising", mode="loose")

agent.last_prompt          # the prompt you sent
agent.last_code            # the code that ran (post-repair)
agent.last_raw_select      # raw model reply for the plot-choice step
agent.last_raw_generate    # raw model reply for the code step
agent.last_repairs         # each failed attempt + its error
agent.last_suggestions     # last suggest() result
```

Construct an agent with a specific model, or a custom repair budget:

```python
agent = plotpy.PlotAgent(chat=plotpy.chat_openai(), max_repairs=5).inspect(df)
```

---

## Theming

Every figure comes out "on-deck": Economist-style palette on a warm canvas,
IBM Plex Mono, no top/right spines. Use the same palette and theme appliers in
your own code:

```python
from plotpy.specs import (
    GREEN, BLUE, AMBER, RED, PURPLE, GREY, COURSE_PAL,   # colours
    apply_base_theme_mpl,     # matplotlib Axes
    apply_base_theme_sns,     # seaborn grid
    apply_base_theme_plotly,  # plotly Figure
    apply_base_theme_p9,      # plotnine ggplot
)

fig, ax = plt.subplots()
ax.scatter(df["x"], df["y"], color=GREEN)
apply_base_theme_mpl(ax)
```

---

## Troubleshooting

| Symptom                                                        | Fix                                                                                       |
| ------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| `RuntimeError: No active model` / `PLOTPY_API_KEY is not set` | `plotpy.use(plotpy.chat_groq(api_key="gsk_..."))`, or set a key env var / `.env`.         |
| `... needs a package that isn't installed`                    | Run the `pip install <package>` from the message (e.g. `upsetplot`, `PyComplexHeatmap`).  |
| `AttributeError: module 'plotpy' has no attribute 'datasets'` | First Colab install — **Restart runtime** so Python reloads the module.                   |
| Code still fails after repairs                                | Read `agent.last_repairs` / `agent.last_code`; try a stronger model or `mode="strict"`.   |
| `Could not parse plot-selection JSON`                         | A weak model dropped the JSON envelope — re-run, or pass `plot_type="..."` to skip it.    |

---

## License

MIT — © 2026 Loukas Theodosiou. See [LICENSE](LICENSE).
