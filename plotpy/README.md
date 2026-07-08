# PlotPy

An LLM-driven plotting agent — Python sibling of [PlotR](https://github.com/loukesio/PlotR).

PlotPy takes a `pandas.DataFrame` and a sentence ("show me which genes go up in drought"), picks the right chart from a catalog of recipes pulled from the **Genomics Viz with Python** course, and generates the matplotlib / seaborn / plotnine / plotly code to draw it. The recipe is either **strict** (verbatim course template, fastest, on-deck aesthetics) or **loose** (prose conventions the LLM adapts to your data).

It is a teaching tool first and a library second: every plot you ask for comes back with the *source code that produced it* — read `result.code`, paste it into your own notebook, modify it. The agent is the on-ramp; matplotlib is still the road.

---

## Install

PlotPy lives inside the course repo at [`plotpy/`](.) — install it from there:

```bash
# In a Colab cell (or any terminal) — install the agent directly from GitHub:
pip install "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"

# Or if you already cloned the course repo:
git clone https://github.com/loukesio/dataviz-genomicsdata.git
cd dataviz-genomicsdata
pip install -e ./plotpy

# Then set your key (Groq's fast free tier is the default provider):
cp plotpy/.env.example .env         # then edit PLOTPY_API_KEY=...
```

Provider defaults to [Groq](https://console.groq.com). Swap to OpenAI / Together / Fireworks / Ollama / vLLM by changing one env var — see [Swap provider](#swap-provider) below.

Some plots in `CATALOG` reference optional packages (adjustText, pywaffle, squarify, ternary-diagram, pypalettes, scipy, scikit-learn). Install them on demand:

```bash
pip install "plotpy[extras] @ git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"
```

The agent emits a clean error if a missing import is hit during `exec()`; nothing crashes silently.

---

## Run it in Google Colab — step by step

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/loukesio/dataviz-genomicsdata/blob/Python_2026/plotpy/notebooks/00_colab_quickstart.ipynb)

Click the badge above to open a ready-made notebook ([`notebooks/00_colab_quickstart.ipynb`](notebooks/00_colab_quickstart.ipynb)) — every cell below is already there.  The walkthrough below is the same content for skim-reading.

### 0. Get a free Groq API key (one time, ~30 seconds)

Open [console.groq.com](https://console.groq.com), sign up (no credit card), click **API Keys → Create API Key**, copy the `gsk_...` string somewhere private.  This is what the agent uses to call the LLM.

### 1. Install PlotPy — Cell 1

```python
!pip install -q "plotpy[extras] @ git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"
```

The `[extras]` pulls in scikit-learn, pywaffle, squarify, ternary-diagram — a few catalog entries need them.

> **Already installed once and want to update?**  Pip caches GitHub installs, so a plain re-install is a no-op.  Force a fresh download:
> ```python
> !pip install -q --upgrade --force-reinstall --no-deps "git+https://github.com/loukesio/dataviz-genomicsdata.git@Python_2026#subdirectory=plotpy"
> ```

### 2. Restart the runtime ⚠️

**Runtime → Restart session** (or `Ctrl+M` then `.`).  This is required after the first install — otherwise the old `plotpy` is already in memory and Python won't see the new module.  Skipping this step is the #1 source of `AttributeError: module 'plotpy' has no attribute 'datasets'`.

### 3. Import and set your key — Cell 2

```python
import plotpy
plotpy.set_key("gsk_...")           # paste your Groq key here
```

### 4. Your first plot — Cell 3

Strict mode is the safe path — it uses the verbatim course template, no LLM freelancing:

```python
df = plotpy.datasets.expression()   # synthetic time-course, no download needed
plotpy.timecourse(df)               # one of the per-plot wrappers in plotpy.plots
```

Let the agent pick the chart instead:

```python
res = plotpy.ask(df, "Show how expression changes over time, with uncertainty.")
res.plot                            # the matplotlib figure (auto-displays in Colab)
res.chosen                          # which catalog entry it picked
res.code                            # the Python source the LLM produced
```

### 5. Try the other plots — Cell 4

```python
plotpy.datasets.list_datasets()     # full menu: dataset → plot → schema
plotpy.manhattan(plotpy.datasets.gwas(), interactive=True)
plotpy.volcano(plotpy.datasets.deseq2())
plotpy.heatmap(plotpy.datasets.expression_matrix()[0])   # generator returns (expr, meta) — heatmap wants expr
```

### 6. Bring your own data — Cell 5

Two parts: get your file into Colab, then either let the agent explore it or force a specific chart.

**Upload your CSV — drag and drop:**

1. Click the **folder icon** in the left sidebar of Colab.
2. Drag the `.csv` from your computer into the file list — it lands at `/content/your_file.csv`.

```python
import pandas as pd
df = pd.read_csv("/content/your_file.csv")
df.head()                       # confirm it loaded
df.columns                      # see the column names
```

**Or — file-picker widget (no sidebar fiddling):**

```python
from google.colab import files
import pandas as pd
uploaded = files.upload()       # opens a native file picker
df = pd.read_csv(next(iter(uploaded)))
df.head()
```

**Let the agent explore — it picks the chart:**

```python
res = plotpy.ask(df, "Explore this dataset — pick the best chart for it.")
res.plot                        # the figure
res.chosen                      # which catalog entry it picked
res.alternatives                # two runners-up
res.code                        # the source the LLM produced
```

Re-run with different prompts to see what the agent suggests:

```python
plotpy.ask(df, "Compare distributions across groups.").plot
plotpy.ask(df, "Show me how my measurement changes across conditions.").plot
plotpy.ask(df, "Show the correlation between two variables.").plot
```

**Force a specific chart (e.g. time-course):**

Works directly if your columns match the course schema (`gene, time, tpm, sem`):

```python
plotpy.timecourse(df)
```

If they don't, either rename to match:

```python
df = df.rename(columns={
    "feature":    "gene",       # whatever your category column is called
    "hour":       "time",       # …your time column
    "expression": "tpm",        # …your measurement
    "stderr":     "sem",        # …your uncertainty
})
plotpy.timecourse(df)
```

…or let the LLM adapt your columns on the fly with `mode="loose"`:

```python
plotpy.ask(df, "Plot a time-course line, one line per category, with error bars.", mode="loose")
```

`plotpy.datasets.list_datasets()` shows the schema each per-plot wrapper expects — handy for knowing what to rename to.

### If something breaks

| Symptom                                                                  | Fix                                                                                                                                                                |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AttributeError: module 'plotpy' has no attribute 'datasets'`            | Old install is cached.  Run the `--force-reinstall` cell in step 1, then **Restart runtime**.                                                                      |
| `NameError` from generated code in `mode="loose"`                        | LLMs are stochastic — re-run the cell, or fall back to `mode="strict"`.  Read what the model wrote with `agent.last_code` (see *advanced* in the API section).     |
| `ModuleNotFoundError: pywaffle / squarify / ternary_diagram / sklearn`   | Reinstall with the `[extras]` form from step 1.                                                                                                                    |
| `Could not parse plot-selection JSON`                                    | The free Groq model occasionally drops the JSON envelope.  Re-run, or pass `plot_type="..."` to skip the selection step.                                            |

---

## Quick start

```python
import plotpy

plotpy.set_key("gsk_...")            # or put it in .env once

df = plotpy.datasets.expression()    # synthetic gene, time, tpm, sem — no download needed
res = plotpy.ask(df, "Show how expression changes over time, with uncertainty.")

res.plot                             # the matplotlib figure
res.chosen                           # 'timecourse_line'
res.alternatives                     # ['ridgeline_pseudotime', 'boxplot_distributions']
res.code                             # the Python source the LLM produced
```

Already know what you want? Skip the LLM selection step:

```python
plotpy.scatter(plotpy.datasets.coexpression(), "Two genes, colour by tissue.", mode="loose")
plotpy.manhattan(plotpy.datasets.gwas(), interactive=True)
```

### Bring-your-own data

Every example above uses :mod:`plotpy.datasets`, which ships deterministic synthetic data for each catalog entry — no CSVs to download. When you want to use your own data instead, just pass any DataFrame whose columns match the schema printed by `plotpy.datasets.list_datasets()`:

```python
plotpy.datasets.list_datasets()      # table: dataset, plot, schema
```

---

## The four files (mirror of PlotR)

PlotPy mirrors PlotR's architecture so students can flip between the two repos line-by-line.

| PlotR (R)         | PlotPy (Python)         | Role                                                          |
| ----------------- | ----------------------- | ------------------------------------------------------------- |
| `R/api_key.R`     | `plotpy/providers.py`   | ellmer-style multi-LLM: `chat_*` constructors + `use()`       |
| —                 | `plotpy/api_key.py`     | Legacy `set_key` / `.env` shim over `providers.py`            |
| `R/plotr_agent.R` | `plotpy/agent.py`       | `PlotAgent` — suggest + select + generate + **self-repair**   |
| `R/specs.R`       | `plotpy/specs.py`       | `CATALOG` of strict/loose plot recipes + BASE_THEME appliers  |
| `R/plots.R`       | `plotpy/plots.py`       | Public `ask()` / `suggest()` + per-plot wrappers              |
| `DESCRIPTION`     | `pyproject.toml`        | Package metadata + deps                                       |
| `LICENSE`         | `LICENSE`               | MIT, same copyright holder                                    |

Class fields / methods also line up: `last_code`, `last_raw`, `last_prompt`, `inspect(df)`, `ask(prompt)`.

---

## Strict vs Loose

Side-by-side for the scatter plot.

```python
df = plotpy.datasets.coexpression()    # sample, tissue, gene_x, gene_y
prompt = "Show how the two genes covary across tissues."
```

### `mode="strict"`

The LLM gets the **course's exact code** as a template and is told to change *only* the column names. Output is predictable, matches the deck visually, and survives ambiguous prompts.

```python
plotpy.ask(df, prompt, mode="strict")
```

Roughly produces (verbatim from `specs.py:CATALOG['scatter_coexpression']['strict']`):

```python
pal = {"Leaf": GREEN, "Root": BLUE, "Seed": AMBER}
fig, ax = plt.subplots(figsize=(5.6, 4.8))
for tissue, c in pal.items():
    g = df[df["tissue"] == tissue]
    ax.scatter(g["gene_x"], g["gene_y"], color=c, s=50, alpha=.4,
               edgecolors=CREAM, label=tissue, zorder=3)
m, b = np.polyfit(df["gene_x"], df["gene_y"], 1)
xs = np.array([df["gene_x"].min(), df["gene_x"].max()])
ax.plot(xs, m * xs + b, color=RED, lw=2.2, zorder=1)
ax.set_title("Two genes, one trend")
p = fig
```

### `mode="loose"`

The LLM gets **prose conventions** instead of code, and adapts the chart to whatever your DataFrame actually contains. Works on data the course never saw.

```python
plotpy.ask(df, prompt, mode="loose")
```

The model receives this instead of code:

> Scatter of two continuous variables, coloured by a categorical column.
> - mark every point with low alpha so density reads
> - overlay a single linear fit across ALL groups (np.polyfit then ax.plot)
> - title states the finding ("X and Y co-vary" etc.)
> - legend in the empty corner, no frame

… and freelances the column names from your `df`. Reach for loose when your column names don't match the course's (e.g. `protein_A` / `protein_B` instead of `gene_x` / `gene_y`).

**Rule of thumb:** start strict; fall through to loose when the strict result looks wrong because your columns aren't named like the course.

---

## Pick your LLM — one constructor per provider (ellmer-style)

Like R's [`ellmer`](https://ellmer.tidyverse.org), PlotPy gives you one `chat_*`
constructor per provider. They all return the same `Chat` object, so you can
**swap the model behind your code at any time** with `plotpy.use(...)`:

```python
import plotpy
from plotpy import chat_groq, chat_openai, chat_anthropic, chat_ollama

plotpy.use(chat_groq())                          # free default (llama-3.3-70b)
plotpy.use(chat_openai(model="gpt-4o-mini"))     # stronger first-try code
plotpy.use(chat_anthropic())                     # Claude, via its OpenAI-compat endpoint
plotpy.use(chat_ollama(model="llama3.1"))        # fully local, no key

# …or use a specific model for one call only, without changing the default:
plotpy.ask(df, "interactive GWAS plot", interactive=True, llm=chat_openai())
```

Each constructor finds its key from the `api_key=` argument, the provider's
usual env var (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, …), or the
generic `PLOTPY_API_KEY`. Local servers (Ollama, vLLM) need no key.

| Constructor        | Provider  | Default model                                  | Key env var          |
| ------------------ | --------- | ---------------------------------------------- | -------------------- |
| `chat_groq()`      | Groq      | `llama-3.3-70b-versatile`                      | `GROQ_API_KEY`       |
| `chat_openai()`    | OpenAI    | `gpt-4o-mini`                                  | `OPENAI_API_KEY`     |
| `chat_anthropic()` | Anthropic | `claude-3-5-sonnet-latest`                     | `ANTHROPIC_API_KEY`  |
| `chat_google()`    | Google    | `gemini-1.5-flash`                             | `GEMINI_API_KEY`     |
| `chat_together()`  | Together  | `Meta-Llama-3.1-70B-Instruct-Turbo`            | `TOGETHER_API_KEY`   |
| `chat_fireworks()` | Fireworks | `llama-v3p3-70b-instruct`                      | `FIREWORKS_API_KEY`  |
| `chat_ollama()`    | Ollama    | `llama3.1`                                     | — (local)            |
| `chat_vllm(model)` | vLLM      | (you name it)                                  | — (local)            |

The legacy `plotpy.set_key("sk-...", base_url=..., model=...)` and `.env`
(`PLOTPY_API_KEY` / `PLOTPY_BASE_URL` / `PLOTPY_MODEL`) still work — they now
just install a matching active `Chat` under the hood.

---

## Suggest, free mode, and self-repair

Three things the redesign added on top of strict/loose:

**`suggest(df)` — a ranked menu, no code yet.** Ask "what should I even plot?"
and get catalog-grounded ideas (plus custom ones the catalog doesn't cover),
each with a one-line reason:

```python
for s in plotpy.suggest(df):
    print(s.name, "⚡" if s.interactive else "", "—", s.reason)
# manhattan_gwas ⚡ — genome-wide p-values across chromosomes
# volcano_deseq2   — log2FC vs -log10(p) separates up/down hits
# …then render the one you like:
plotpy.ask(df, "make the manhattan interactive", interactive=True)
```

**`mode="free"` — open-ended, beyond the catalog.** No template; the model
writes the chart from scratch, still grounded in the course theme/palette. This
is how you get Day-3 / novel plots on data the catalog never saw:

```python
plotpy.ask(df, "interactive GWAS Manhattan, colour alternate chromosomes", mode="free", interactive=True)
```

**Self-repair — the reliability fix.** Every generated snippet is executed; if
it raises (wrong column, bad API call), the traceback is fed back to the model
and the code is regenerated, up to `max_repairs` times (default 3). Inspect what
happened:

```python
res = plotpy.ask(df, "…", mode="free")
res.repairs          # 0 if it worked first try, else how many fixes it took
agent = plotpy.PlotAgent().inspect(df)
agent.ask("…", mode="free")
agent.last_repairs   # [{"error": "...", "code": "..."}] per failed attempt
```

This is why the free Groq model went from flaky to usable: first-try failures
get fixed instead of surfacing as an exception.

---

## Catalog — what PlotPy knows how to draw

Every entry has both `strict` (code) and `loose` (prose) specs. Browse with `plotpy.list_plots(day=1)`.

### Day 1 — Foundations & differential expression

| Plot name                          | Library    | Interactive | Summary                                                       |
| ---------------------------------- | ---------- | ----------- | ------------------------------------------------------------- |
| `timecourse_line`                  | matplotlib | —           | Gene expression over time, one line per gene, SEM error bars  |
| `timecourse_line_interactive`      | plotly     | hover       | Same — hover for gene/value, click to toggle traces           |
| `bar_simple`                       | matplotlib | —           | Sorted horizontal bar, one bar highlighted in RED             |
| `scatter_coexpression`             | matplotlib | —           | Two-gene scatter coloured by tissue, with linear fit          |
| `scatter_coexpression_interactive` | plotly     | hover       | Same — hover for sample id, toggle by tissue                  |
| `boxplot_distributions`            | matplotlib | —           | Boxplot across groups with jittered raw points                |
| `violin_shape`                     | matplotlib | —           | Violin + inner boxplot — reveals bimodality                   |
| `ridgeline_pseudotime`             | matplotlib | —           | Stacked KDE distributions along an ordered axis               |
| `volcano_deseq2`                   | matplotlib | —           | Differential expression — log2FC vs −log10(p), red/green/grey |
| `volcano_interactive`              | plotly     | hover       | Same — hover for gene + raw p, toggle up/down                 |
| `pca_population`                   | matplotlib | —           | 2-component PCA scatter coloured by population                |
| `heatmap_expression`               | seaborn    | —           | Clustered z-scored heatmap with sample annotation strip       |
| `heatmap_expression_interactive`   | plotly     | hover       | Same as a static heatmap — no dendrograms                     |
| `ternary_admixture`                | matplotlib | —           | Three-component composition on a ternary triangle             |
| `waffle_variant_classes`           | matplotlib | —           | 10×10 waffle of categorical counts                            |
| `waterfall_tmb`                    | matplotlib | —           | Patients ranked by mutation burden, coloured by subtype       |

### Day 2 — Genome-scale charts

| Plot name                | Library    | Interactive | Summary                                                                |
| ------------------------ | ---------- | ----------- | ---------------------------------------------------------------------- |
| `stacked_bar_admixture`  | matplotlib | —           | One bar per individual summing to 1, sorted within each population     |
| `stacked_bar_microbiome` | matplotlib | —           | Composition over time, taxa ordered by mean abundance                  |
| `manhattan_gwas`         | matplotlib | —           | GWAS Manhattan with cumulative bp x-axis and threshold lines           |
| `manhattan_interactive`  | plotly     | hover       | Same Manhattan — hover for rsID                                        |
| `treemap_microbiome`     | matplotlib | —           | Area-proportional treemap of taxon abundance                           |

### Day 3 — Production-grade packages

| Plot name           | Library    | Interactive | Summary                                                                    |
| ------------------- | ---------- | ----------- | -------------------------------------------------------------------------- |
| `upset_gene_sets`   | matplotlib | —           | UpSet plot of set intersections — the scalable Venn for 4+ sets            |
| `heatmap_annotated` | matplotlib | —           | Clustered heatmap with annotation tracks (PyComplexHeatmap)                |

These two Day-3 tools take a DataFrame directly, so they fit the catalog
(`plotpy.upset(df)`, `plotpy.complexheatmap(df)`). They need optional packages
(`pip install upsetplot PyComplexHeatmap`); if one is missing the agent fails
fast with an install hint rather than guessing.

The rest of Day 3 — pyCirclize, Toytree, pyMSAviz, DashBio, pyGenomeTracks,
dna_features_viewer, JCVI, gget, Biopython — takes non-DataFrame inputs (newick
trees, alignments, feature records), so it doesn't reduce to "DataFrame in →
plot out." For those, reach for `mode="free"` (the agent writes the code
grounded in the course theme) or the Day-3 course notebooks directly.

---

## Public API

```python
plotpy.ask(df, prompt, mode="strict", interactive=None, llm=None, max_repairs=None)  # main entry
plotpy.suggest(df, n=6, interactive=None, llm=None)       # ranked menu of ideas, no code
plotpy.list_plots(library=None, interactive=None, day=None)

# pick / switch the model (ellmer-style)
plotpy.use(plotpy.chat_openai(model="gpt-4o-mini"))       # active model for bare ask()
plotpy.chat_groq(), plotpy.chat_anthropic(), plotpy.chat_ollama()  # …one per provider

# mode="free" — open-ended, no catalog template (Day-3 / novel charts)
plotpy.ask(df, "interactive GWAS Manhattan", mode="free", interactive=True)

# direct (skip LLM selection)
plotpy.scatter(df, ...)         plotpy.bar(df, ...)
plotpy.boxplot(df, ...)         plotpy.violin(df, ...)
plotpy.volcano(df, ...)         plotpy.manhattan(df, ...)
plotpy.timecourse(df, ...)      plotpy.heatmap(df, ...)
plotpy.pca(df, ...)             plotpy.admixture(df, ...)
plotpy.microbiome(df, ...)      plotpy.waterfall(df, ...)
plotpy.ternary(df, ...)         plotpy.waffle(df, ...)
plotpy.ridgeline(df, ...)       plotpy.treemap(df, ...)

# advanced
agent = plotpy.PlotAgent().inspect(df)
agent.ask(prompt, mode="loose")
agent.last_prompt          # the user prompt
agent.last_code            # the executed Python
agent.last_raw_select      # raw selection-step response (which plot the LLM picked)
agent.last_raw_generate    # raw generation-step response (the LLM's code reply)
agent.last_raw             # alias — most recent of the two
```

Pass `interactive=True` to any per-plot wrapper that has a plotly sibling (`scatter`, `timecourse`, `volcano`, `manhattan`, `heatmap`) to switch to the hoverable variant.

---

## Theming

`plotpy.specs` exports four library-specific theme appliers so every figure looks "on-deck" — Economist palette on cream canvas, IBM Plex Mono, no top/right spines, dashed major grid where it helps.

```python
from plotpy.specs import (
    apply_base_theme_mpl,      # matplotlib Axes
    apply_base_theme_sns,      # seaborn FacetGrid / ClusterGrid
    apply_base_theme_p9,       # plotnine ggplot
    apply_base_theme_plotly,   # plotly Figure
)

fig, ax = plt.subplots()
ax.scatter(df["x"], df["y"])
apply_base_theme_mpl(ax)        # cream + spines + grid + font
```

The palette constants (`GREEN`, `BLUE`, `AMBER`, `RED`, `PURPLE`, `GREY`, `INK`, `CREAM`, `LINE`, `MUTED`, `COURSE_PAL`) are exported from `plotpy.specs` too — use them in any code you write outside the agent.

---

## Notebooks vs app

Notebooks are the course; an app is dessert. The agent exposes a four-step pipeline (data summary → plot choice → generated code → rendered figure), and a notebook is the medium that *shows every step*. A Streamlit button hides those steps behind a click, which is the opposite of what a teaching tool should do.

Planned shape:

```
notebooks/
  01_intro.ipynb              the smallest plotpy.ask example
  02_strict_vs_loose.ipynb    same prompt + DataFrame, two modes side by side
  03_agent_internals.ipynb    last_raw / last_code / last_prompt walkthrough

app.py                        ~50 lines of Streamlit — the "give it to my PI" demo
```

---

## License

MIT — © 2026 Loukas Theodosiou. See [LICENSE](LICENSE).
