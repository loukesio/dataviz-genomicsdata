# Package data layer — add three course datasets

> For Claude Code. Two small, additive edits to the existing package. Nothing is
> removed; existing datasets and loaders are untouched. After applying, run
> `python -m genomics_course.data._build` to generate the new parquet files.
>
> These three fill the chart types the four existing datasets don't cover:
> `lineages` → stacked area · `timecourse` → time series / build-up ·
> `coexpression` → scatter + fitted line.

---

## EDIT 1 — `genomics_course/data/_build.py`

Add these three functions (anywhere among the other `build_*` functions, e.g.
right after `build_variants`). They follow the existing pattern exactly: seeded
RNG, write one parquet into `FILES`, print a tick.

```python
def build_lineages(n_lineages=150, n_days=21):
    """Barcode lineage frequencies over time (lineage tracking).
    Tidy long form (lineage, day, freq); each day's frequencies sum to 1."""
    rng = np.random.default_rng(101)
    traj = np.abs(rng.normal(1, 0.07, (n_lineages, n_days)).cumprod(axis=1))
    traj *= rng.dirichlet(np.ones(n_lineages) * 0.5)[:, None] * 50
    freq = traj / traj.sum(axis=0, keepdims=True)
    freq = freq[np.argsort(freq.sum(axis=1))[::-1]]            # abundant lineages first
    rows = [{"lineage": f"BC_{li:03d}", "day": d, "freq": float(freq[li, d])}
            for li in range(n_lineages) for d in range(n_days)]
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "lineages_barcode.parquet"))
    print("✓ lineages_barcode.parquet")


def build_timecourse():
    """Gene expression time course: 6 genes x 5 timepoints, with TPM and SEM."""
    rng = np.random.default_rng(202)
    genes = ["BRCA1", "TP53", "EGFR", "MYC", "KRAS", "PTEN"]
    times = [0, 2, 6, 12, 24]
    rows = []
    for g in genes:
        traj = np.clip(rng.integers(10, 25) + np.cumsum(rng.integers(-3, 9, len(times))), 2, None)
        for t, v in zip(times, traj):
            rows.append({"gene": g, "time": int(t), "tpm": float(v),
                         "sem": float(rng.uniform(1, 4))})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "timecourse_expression.parquet"))
    print("✓ timecourse_expression.parquet")


def build_coexpression():
    """Two-gene co-expression across samples and tissues, for scatter + linear fit.
    gene_y is ~1.4 * gene_x + noise, with a per-tissue offset (corr ~0.9)."""
    rng = np.random.default_rng(303)
    offsets = {"Leaf": 0.0, "Root": 1.5, "Seed": -1.0}
    rows = []
    for tissue, off in offsets.items():
        gx = rng.uniform(2, 10, 60)
        gy = 1.4 * gx + rng.normal(0, 1.2, 60) + off
        for x, y in zip(gx, gy):
            rows.append({"sample": f"{tissue}_{rng.integers(1000, 9999)}",
                         "tissue": tissue, "gene_x": float(x), "gene_y": float(max(y, 0.0))})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "coexpression.parquet"))
    print("✓ coexpression.parquet")
```

And add the three calls to the `if __name__ == "__main__":` block at the bottom,
alongside the existing four:

```python
if __name__ == "__main__":
    build_admixture()
    build_gwas()
    build_deseq2()
    build_variants()
    build_lineages()       # NEW
    build_timecourse()     # NEW
    build_coexpression()   # NEW
    print("\nAll datasets built into files/")
```

## EDIT 2 — `genomics_course/data/__init__.py`

Add these three loaders (next to the existing `load_*` functions). Same `_load`
helper, same shape.

```python
def load_lineages():
    """Barcode lineage frequencies over time (lineage, day, freq).
    Tidy long form; each day's frequencies sum to 1. For stacked-area plots."""
    return _load("lineages_barcode.parquet")


def load_timecourse():
    """Gene expression time course (gene, time, tpm, sem). For line / time-series plots."""
    return _load("timecourse_expression.parquet")


def load_coexpression(tissue=None):
    """Two-gene co-expression (sample, tissue, gene_x, gene_y). For scatter + fit.
    Pass tissue= to filter to 'Leaf', 'Root', or 'Seed'."""
    df = _load("coexpression.parquet")
    if tissue:
        df = df[df["tissue"] == tissue].reset_index(drop=True)
    return df
```

And extend `__all__`:

```python
__all__ = ["load_admixture", "load_gwas", "load_deseq2", "load_variants",
           "load_lineages", "load_timecourse", "load_coexpression"]
```

## Build & verify

```bash
python -m genomics_course.data._build
```

Expected new files in `genomics_course/data/files/`:
`lineages_barcode.parquet`, `timecourse_expression.parquet`, `coexpression.parquet`.

Quick check in Python:

```python
from genomics_course.data import load_lineages, load_timecourse, load_coexpression
load_lineages().head()        # lineage, day, freq  (3150 rows; day 0 sums to 1.0)
load_timecourse()             # gene, time, tpm, sem (30 rows, 6 genes x 5 times)
load_coexpression("Leaf")     # sample, tissue, gene_x, gene_y (60 rows)
```

## Chart ↔ dataset map (for the section rewrites that follow)

| Chart type | Loader | How it's used |
|---|---|---|
| Volcano | `load_deseq2()` | log2FoldChange vs −log10(pvalue) |
| Box / violin | `load_deseq2()` | log2FC by regulation class (Up / Down / NS); DE genes are bimodal |
| Ridgeline | `load_deseq2()` | −log10(pvalue) distribution per |log2FC| bin (marches rightward) |
| Stacked bar / proportions | `load_admixture()` | ancestry K1–K5 per individual / per population |
| Bar / lollipop | `load_variants()` | lld by gene, coloured by classification |
| Stacked area | `load_lineages()` | freq over day, every band on the spectrum ramp |
| Time series / build-up | `load_timecourse()` | tpm over time with SEM band |
| Scatter + fit | `load_coexpression()` | gene_x vs gene_y with a regression line |

---

## EDIT 3 — add the two opener datasets (`load_anscombe`, `load_datasaurus`)

> These two power the "Why we visualise" openers in `day1_part1.qmd`. Anscombe is
> built network-free from hardcoded values; Datasaurus reads a CSV bundled into the
> package, so neither build step needs the internet.

### 3a — bundle the Datasaurus CSV

The repo already has the Datasaurus CSV (the old deck read `data/datasaurus.csv`).
Copy it into the package so the build is self-contained:

```bash
mkdir -p genomics_course/data/sources
cp slides/data/datasaurus.csv genomics_course/data/sources/datasaurus.csv
# if it isn't in the repo, fetch it once:
#   curl -fsSL https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-10-13/datasaurus.csv \
#     -o genomics_course/data/sources/datasaurus.csv
```

### 3b — `genomics_course/data/_build.py`

Near the top, next to `FILES`, add a sources path:

```python
SOURCES = os.path.join(os.path.dirname(__file__), "sources")
```

Then add these two build functions (verified: anscombe → 44 rows, datasaurus → 1846
rows / 13 shapes, both with columns `dataset, x, y`):

```python
def build_anscombe():
    """Anscombe's quartet: 4 datasets, identical summary stats, different shapes.
    Hardcoded canonical values (no network)."""
    x123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
    y = {
        "I":   [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
        "II":  [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
        "III": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
    }
    x4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]
    y4 = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
    rows = []
    for ds, xs in [("I", x123), ("II", x123), ("III", x123), ("IV", x4)]:
        ys = y4 if ds == "IV" else y[ds]
        for xi, yi in zip(xs, ys):
            rows.append({"dataset": ds, "x": float(xi), "y": float(yi)})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "anscombe.parquet"))
    print("✓ anscombe.parquet")


def build_datasaurus():
    """Datasaurus Dozen: 13 datasets, identical summary stats, different shapes.
    Reads the bundled CSV; columns normalised to dataset, x, y."""
    df = pd.read_csv(os.path.join(SOURCES, "datasaurus.csv"))
    df.columns = [c.strip().lower() for c in df.columns]
    df = df[["dataset", "x", "y"]]
    df.to_parquet(os.path.join(FILES, "datasaurus.parquet"))
    print("✓ datasaurus.parquet")
```

Add both to the `if __name__ == "__main__":` block (now seven build calls total):

```python
    build_lineages()
    build_timecourse()
    build_coexpression()
    build_anscombe()        # NEW
    build_datasaurus()      # NEW
```

### 3c — `genomics_course/data/__init__.py`

```python
def load_anscombe():
    """Anscombe's quartet (dataset, x, y). Four groups, identical summary stats."""
    return _load("anscombe.parquet")


def load_datasaurus(name=None):
    """Datasaurus Dozen (dataset, x, y). 13 shapes, identical summary stats.
    Pass name= to filter to one shape, e.g. 'dino'."""
    df = _load("datasaurus.parquet")
    if name:
        df = df[df["dataset"] == name].reset_index(drop=True)
    return df
```

Final `__all__` (all five new loaders, alongside the original four):

```python
__all__ = ["load_admixture", "load_gwas", "load_deseq2", "load_variants",
           "load_lineages", "load_timecourse", "load_coexpression",
           "load_anscombe", "load_datasaurus"]
```

### 3d — verify

```python
from genomics_course.data import load_anscombe, load_datasaurus
load_anscombe()              # 44 rows, datasets I/II/III/IV
load_datasaurus()            # 1846 rows, 13 shapes incl. "dino"
load_datasaurus("dino")      # one shape
```

| Chart | Loader | Use |
|---|---|---|
| Anscombe's quartet | `load_anscombe()` | 4-panel scatter + identical fit lines |
| Datasaurus dozen | `load_datasaurus()` | 13-panel scatter, same stats |
