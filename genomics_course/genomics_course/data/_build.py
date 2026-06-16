"""
genomics_course/data/_build.py
──────────────────────────────
Generates all course datasets ONCE and saves them to files/.
Run this when building the package. NEVER called during teaching.

  python -m genomics_course.data._build
"""

import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
FILES = os.path.join(HERE, "files")
SOURCES = os.path.join(HERE, "sources")
os.makedirs(FILES, exist_ok=True)


def build_admixture():
    """ADMIXTURE ancestry proportions: 120 individuals, 5 populations, K=5."""
    rng = np.random.default_rng(42)

    def pop(n, dom, K=5, purity=0.8):
        alpha = np.ones(K) * 0.3
        alpha[dom] = purity * 10
        return rng.dirichlet(alpha, size=n)

    specs = [("EUR", 0, 0.85, 25), ("AFR", 1, 0.88, 25), ("EAS", 2, 0.82, 25),
             ("SAS", 3, 0.75, 20), ("AMR", 4, 0.60, 25)]
    rows = []
    for name, dom, purity, n in specs:
        props = pop(n, dom, purity=purity)
        order = np.argsort(-props[:, dom])         # sort within population
        for i, p in enumerate(props[order]):
            rows.append({"individual": f"{name}_{i:03d}", "population": name,
                         **{f"K{k+1}": p[k] for k in range(5)}})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "admixture_k5.parquet"))
    print("✓ admixture_k5.parquet")


def build_gwas():
    """GWAS summary stats: ~20k SNPs across 22 chromosomes, a few real hits."""
    rng = np.random.default_rng(7)
    chrom_sizes = {c: int(900 - c * 25) for c in range(1, 23)}
    rows = []
    for c, size in chrom_sizes.items():
        pos = np.sort(rng.integers(1, 250_000_000, size))
        pval = rng.uniform(0, 1, size)
        rows.append(pd.DataFrame({"chrom": c, "pos": pos, "pval": pval}))
    df = pd.concat(rows, ignore_index=True)
    # inject genome-wide significant hits
    hit_idx = rng.choice(len(df), 12, replace=False)
    df.loc[hit_idx, "pval"] = 10 ** (-rng.uniform(8, 30, 12))
    df["snp"] = [f"rs{rng.integers(1e5, 9e6)}" for _ in range(len(df))]
    df.to_parquet(os.path.join(FILES, "gwas_height.parquet"))
    print("✓ gwas_height.parquet")


def build_deseq2():
    """DESeq2 differential expression: ~15k genes, drought vs control."""
    rng = np.random.default_rng(13)
    n = 15000
    base_mean = 10 ** rng.uniform(0, 4, n)
    lfc = rng.normal(0, 0.4, n)
    de = rng.choice(n, 400, replace=False)              # true DE genes
    lfc[de] += rng.choice([-1, 1], 400) * rng.uniform(1.5, 4, 400)
    # realistic standard error: shrinks with expression but floored
    se = np.clip(0.5 + 2.0 / np.sqrt(base_mean), 0.25, 2.0)
    stat = lfc / se
    pval = 2 * (1 - _norm_cdf(np.abs(stat)))
    pval = np.clip(pval, 1e-50, 1.0)                    # realistic floor
    # Benjamini-Hochberg adjustment
    order = np.argsort(pval)
    ranked = pval[order] * n / (np.arange(1, n + 1))
    padj = np.minimum.accumulate(ranked[::-1])[::-1]
    padj_full = np.empty(n)
    padj_full[order] = np.clip(padj, 0, 1)
    df = pd.DataFrame({
        "gene": [f"Gene_{i:05d}" for i in range(n)],
        "baseMean": base_mean, "log2FoldChange": lfc,
        "pvalue": pval, "padj": padj_full,
    })
    df.to_parquet(os.path.join(FILES, "deseq2_drought.parquet"))
    print("✓ deseq2_drought.parquet")


def build_variants():
    """Variant effect predictions (log-likelihood differences) — the LLD plot data."""
    data = [
        ("VHL", "c.475A>T", -322.81, "pathogenic"),
        ("BRCA2", "c.7976G>T", -102.56, "pathogenic"),
        ("F9", "c.1186T>A", -97.14, "pathogenic"),
        ("TP53", "c.712T>A", -52.22, "pathogenic"),
        ("HBB", "c.20A>T", -35.57, "pathogenic"),
        ("LDLR", "c.313+1G>T", -21.88, "pathogenic"),
        ("LRRK2", "c.6055G>A", -14.29, "risk"),
        ("VHL", "c.*820A>G", 0.27, "benign"),
    ]
    df = pd.DataFrame(data, columns=["gene", "variant", "lld", "classification"])
    df.to_parquet(os.path.join(FILES, "variants_lld.parquet"))
    print("✓ variants_lld.parquet")


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


def _norm_cdf(x):
    from math import erf, sqrt
    return np.array([0.5 * (1 + erf(v / sqrt(2))) for v in x])


if __name__ == "__main__":
    build_admixture()
    build_gwas()
    build_deseq2()
    build_variants()
    build_lineages()       # NEW
    build_timecourse()     # NEW
    build_coexpression()   # NEW
    build_anscombe()       # NEW
    build_datasaurus()     # NEW
    print("\nAll datasets built into files/")
