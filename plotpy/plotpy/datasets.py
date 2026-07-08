"""Synthetic example datasets — one per CATALOG entry.

Every generator returns a deterministic ``pandas.DataFrame`` (seeded with
``numpy.random.default_rng``) whose columns match the strict template in
:mod:`plotpy.specs`.  Students can run the README and notebook examples
without downloading any files::

    import plotpy
    df = plotpy.datasets.expression()
    plotpy.ask(df, "Show expression over time.")

The numbers are biologically plausible but entirely synthetic — they
exist to demonstrate the *plot*, not the science.

Each function takes a ``seed`` integer.  Default seeds are pinned per
dataset so two students running the same call get the same data.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

__all__ = [
    "list_datasets",
    # Day 1
    "expression",
    "coexpression",
    "tissue_expression",
    "expression_groups",
    "pseudotime",
    "deseq2",
    "pca_features",
    "expression_matrix",
    "admixture_components",
    "variant_classes",
    "tmb_cohort",
    # Day 2
    "admixture_kinship",
    "microbiome_timeseries",
    "gwas",
    "microbiome_abundance",
    # Day 3
    "gene_sets",
]


# --------------------------------------------------------------------- Day 1
def expression(seed: int = 0) -> pd.DataFrame:
    """Time-course expression — columns: gene, time, tpm, sem.

    Used by ``timecourse_line`` and ``timecourse_line_interactive``.
    Five genes measured at seven timepoints with biological replicates.
    """
    rng = np.random.default_rng(seed)
    genes = ["BRCA1", "TP53", "EGFR", "MYC", "GAPDH"]
    times = np.array([0, 2, 4, 8, 12, 18, 24])
    rows = []
    for i, gene in enumerate(genes):
        amplitude = rng.uniform(20, 80)
        phase = rng.uniform(0, np.pi)
        baseline = rng.uniform(20, 60)
        for t in times:
            replicates = baseline + amplitude * np.sin((t / 24) * np.pi + phase) \
                         + rng.normal(0, 4, size=4)
            rows.append(dict(gene=gene, time=int(t),
                             tpm=float(np.mean(replicates)),
                             sem=float(np.std(replicates, ddof=1) / np.sqrt(len(replicates)))))
        _ = i
    return pd.DataFrame(rows)


def coexpression(seed: int = 1) -> pd.DataFrame:
    """Two-gene scatter — columns: sample, tissue, gene_x, gene_y.

    Used by ``scatter_coexpression`` and its interactive sibling.
    Three tissues (Leaf, Root, Seed) with a shared linear trend + noise.
    """
    rng = np.random.default_rng(seed)
    tissues = {"Leaf": 0, "Root": 4, "Seed": 8}
    rows = []
    sid = 1
    for tissue, offset in tissues.items():
        n = 40
        gene_x = rng.uniform(0, 20, n) + offset
        gene_y = 0.85 * gene_x + rng.normal(0, 2.2, n) + 5
        for x, y in zip(gene_x, gene_y):
            rows.append(dict(sample=f"S{sid:03d}", tissue=tissue,
                             gene_x=float(x), gene_y=float(y)))
            sid += 1
    return pd.DataFrame(rows)


def tissue_expression(seed: int = 2) -> pd.DataFrame:
    """One gene across tissues — columns: tissue, tpm.

    Used by ``bar_simple``.  Heart is the highest expressing tissue
    (it is the highlight bar in the strict template).
    """
    rng = np.random.default_rng(seed)
    tissues = ["Brain", "Liver", "Kidney", "Muscle", "Heart"]
    base = np.array([35, 50, 42, 28, 90])
    tpm = base + rng.normal(0, 3, len(base))
    return pd.DataFrame({"tissue": tissues, "tpm": tpm.round(1)})


def expression_groups(seed: int = 3) -> pd.DataFrame:
    """Expression values across discrete groups — columns: group, value.

    Used by ``boxplot_distributions`` and ``violin_shape``.  Four
    conditions with different means; the WT distribution is unimodal,
    KO is bimodal so the violin can show it.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for label, mean in [("WT", 5.0), ("Mut1", 6.5), ("Mut2", 8.0)]:
        vals = rng.normal(mean, 1.0, 60)
        rows.extend({"group": label, "value": float(v)} for v in vals)
    # bimodal KO: two underlying peaks
    ko = np.concatenate([rng.normal(4.0, 0.6, 30), rng.normal(8.5, 0.6, 30)])
    rows.extend({"group": "KO", "value": float(v)} for v in ko)
    return pd.DataFrame(rows)


def pseudotime(seed: int = 4) -> pd.DataFrame:
    """Pseudotime ridges — columns: id, stage, value.

    Used by ``ridgeline_pseudotime``.  Six ordered stages with the
    value distribution shifting and broadening as stage increases.
    """
    rng = np.random.default_rng(seed)
    rows = []
    n_per_stage = 80
    uid = 1
    for stage in range(6):
        mean = 2.0 + stage * 1.3
        spread = 0.8 + stage * 0.15
        vals = rng.normal(mean, spread, n_per_stage)
        for v in vals:
            rows.append(dict(id=f"C{uid:04d}", stage=int(stage), value=float(v)))
            uid += 1
    return pd.DataFrame(rows)


def deseq2(seed: int = 5, n_genes: int = 2000) -> pd.DataFrame:
    """Differential-expression results — columns: gene, log2FoldChange, pvalue, padj.

    Used by ``volcano_deseq2`` and ``volcano_interactive``.  Most genes
    are not significant; ~5% are up-regulated, ~5% down-regulated.
    """
    rng = np.random.default_rng(seed)
    n_up = n_genes // 20
    n_down = n_genes // 20
    n_ns = n_genes - n_up - n_down

    log2fc = np.concatenate([
        rng.normal(2.2, 0.7, n_up),
        rng.normal(-2.2, 0.7, n_down),
        rng.normal(0.0, 0.6, n_ns),
    ])
    pvalue = np.concatenate([
        rng.uniform(1e-12, 1e-3, n_up),
        rng.uniform(1e-12, 1e-3, n_down),
        rng.uniform(1e-3, 1.0, n_ns),
    ])
    # Benjamini-Hochberg-style padj from sorted pvalues (close enough for demo)
    order = np.argsort(pvalue)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, n_genes + 1)
    padj = np.clip(pvalue * n_genes / ranks, 0, 1)

    genes = [f"GENE{i:05d}" for i in range(n_genes)]
    df = pd.DataFrame(dict(gene=genes, log2FoldChange=log2fc,
                           pvalue=pvalue, padj=padj))
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def pca_features(seed: int = 6) -> pd.DataFrame:
    """PCA feature matrix — columns: individual, population, feature_0..feature_19.

    Used by ``pca_population``.  Five super-populations with cluster
    centres pulled apart in the first few feature dimensions.
    """
    rng = np.random.default_rng(seed)
    pops = ["EUR", "AFR", "EAS", "SAS", "AMR"]
    n_features = 20
    n_per_pop = 30
    rows = []
    pid = 1
    for i, pop in enumerate(pops):
        centre = np.zeros(n_features)
        centre[i % n_features] = 3.0
        centre[(i + 2) % n_features] = -2.0
        X = centre + rng.normal(0, 1.0, (n_per_pop, n_features))
        for row in X:
            entry = {"individual": f"IND{pid:04d}", "population": pop}
            entry.update({f"feature_{j}": float(row[j]) for j in range(n_features)})
            rows.append(entry)
            pid += 1
    return pd.DataFrame(rows)


def expression_matrix(seed: int = 7) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gene × sample expression matrix + sample metadata.

    Used by ``heatmap_expression`` and ``heatmap_expression_interactive``.
    Returns ``(expr, meta)`` where:

    - ``expr`` is a gene×sample matrix (rows = genes, cols = samples)
    - ``meta`` has columns ``sample, condition`` (Control / Drought)

    The strict template reads ``meta`` from ``globals()`` if present;
    pass the two together to render the annotation bar.
    """
    rng = np.random.default_rng(seed)
    n_genes = 40
    n_per_cond = 12
    samples_c = [f"C{i+1:02d}" for i in range(n_per_cond)]
    samples_d = [f"D{i+1:02d}" for i in range(n_per_cond)]
    samples = samples_c + samples_d
    genes = [f"GENE{i:03d}" for i in range(n_genes)]

    # Half the genes go up under drought, half down, the rest are flat-ish.
    base = rng.normal(8, 1.0, (n_genes, len(samples)))
    up_idx = rng.choice(n_genes, size=n_genes // 3, replace=False)
    down_idx = rng.choice(
        [i for i in range(n_genes) if i not in up_idx],
        size=n_genes // 3, replace=False,
    )
    drought_cols = np.arange(n_per_cond, len(samples))
    base[np.ix_(up_idx, drought_cols)] += rng.uniform(2.0, 3.5, (len(up_idx), 1))
    base[np.ix_(down_idx, drought_cols)] -= rng.uniform(2.0, 3.5, (len(down_idx), 1))

    expr = pd.DataFrame(base, index=genes, columns=samples)
    meta = pd.DataFrame({
        "sample": samples,
        "condition": ["Control"] * n_per_cond + ["Drought"] * n_per_cond,
    })
    return expr, meta


def admixture_components(seed: int = 8) -> pd.DataFrame:
    """Three-component compositions — columns: A, B, C (sum to 1).

    Used by ``ternary_admixture``.  100 individuals drawn from three
    Dirichlet clusters so the ternary triangle shows visible structure.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for alpha in [(6, 1, 1), (1, 6, 1), (1, 1, 6)]:
        rows.append(rng.dirichlet(alpha, size=33))
    comp = np.vstack(rows)
    return pd.DataFrame(comp, columns=["A", "B", "C"])


def variant_classes(seed: int = 9) -> pd.DataFrame:
    """Variant classification counts — columns: classification, n.

    Used by ``waffle_variant_classes``.  Five ACMG-style classes with
    counts that sum to 100.
    """
    _ = seed  # deterministic by construction
    return pd.DataFrame({
        "classification": ["Pathogenic", "Likely pathogenic", "VUS",
                            "Likely benign", "Benign"],
        "n": [12, 18, 35, 20, 15],
    })


def tmb_cohort(seed: int = 10) -> pd.DataFrame:
    """Tumour-mutation-burden cohort — columns: patient, value, subtype, msi.

    Used by ``waterfall_tmb``.  100 patients across four breast-cancer
    subtypes; ~8% MSI-H are starred in the strict template.
    """
    rng = np.random.default_rng(seed)
    n = 100
    subtypes = rng.choice(
        ["Luminal A", "Luminal B", "HER2+", "TNBC"],
        size=n, p=[0.40, 0.25, 0.20, 0.15],
    )
    value = rng.exponential(scale=6.0, size=n) + 0.5
    msi = np.where(rng.random(n) < 0.08, "MSI-H", "MSS")
    patients = [f"P{i:03d}" for i in range(1, n + 1)]
    return pd.DataFrame(dict(patient=patients, value=value.round(2),
                             subtype=subtypes, msi=msi))


# --------------------------------------------------------------------- Day 2
def admixture_kinship(seed: int = 11) -> pd.DataFrame:
    """Per-individual ancestry — columns: individual, population, K1..K5.

    Used by ``stacked_bar_admixture``.  Five populations, each dominated
    by a different K component but with mixing at the edges.
    """
    rng = np.random.default_rng(seed)
    pops = ["EUR", "AFR", "EAS", "SAS", "AMR"]
    n_per_pop = 30
    rows = []
    iid = 1
    for i, pop in enumerate(pops):
        alpha = [0.4] * 5
        alpha[i] = 6.0  # dominant K for this population
        props = rng.dirichlet(alpha, size=n_per_pop)
        for row in props:
            rows.append({
                "individual": f"IND{iid:04d}", "population": pop,
                **{f"K{k+1}": float(row[k]) for k in range(5)},
            })
            iid += 1
    return pd.DataFrame(rows)


def microbiome_timeseries(seed: int = 12) -> pd.DataFrame:
    """Microbiome composition over time — columns: day, phase, taxon, abundance.

    Used by ``stacked_bar_microbiome``.  Six taxa across 21 days; the
    phase column flips at the antibiotic intervention on day 10.
    """
    rng = np.random.default_rng(seed)
    taxa = ["Bacteroidetes", "Firmicutes", "Proteobacteria",
            "Actinobacteria", "Verrucomicrobia", "Other"]
    days = list(range(21))
    rows = []
    for d in days:
        if d < 10:
            phase = "pre-abx"
            alpha = [6, 5, 1, 2, 1, 1]
        else:
            phase = "post-abx"
            alpha = [2, 2, 6, 3, 1, 1]
        props = rng.dirichlet(alpha)
        for t, a in zip(taxa, props):
            rows.append(dict(day=d, phase=phase, taxon=t, abundance=float(a)))
    return pd.DataFrame(rows)


def gwas(seed: int = 13) -> pd.DataFrame:
    """GWAS summary statistics — columns: chrom, pos, pval, snp.

    Used by ``manhattan_gwas`` and ``manhattan_interactive``.  22
    autosomes, ~500 SNPs each, with a handful of genome-wide-significant
    hits seeded on chromosomes 2, 6 and 11.
    """
    rng = np.random.default_rng(seed)
    rows = []
    rs = 1
    chrom_lengths = {c: rng.integers(120_000_000, 250_000_000) for c in range(1, 23)}
    for c, length in chrom_lengths.items():
        n_snps = 500
        pos = np.sort(rng.integers(1, length, n_snps))
        pval = rng.uniform(1e-4, 1.0, n_snps)
        for p, pv in zip(pos, pval):
            rows.append(dict(chrom=int(c), pos=int(p), pval=float(pv),
                             snp=f"rs{rs}"))
            rs += 1
    df = pd.DataFrame(rows)

    # Seed a few real hits so the Manhattan has something to point at.
    for c in (2, 6, 11):
        hit_idx = df[df["chrom"] == c].sample(3, random_state=seed + c).index
        df.loc[hit_idx, "pval"] = rng.uniform(1e-10, 5e-9, len(hit_idx))
    return df


def microbiome_abundance(seed: int = 14) -> pd.DataFrame:
    """Average taxon abundance — columns: taxon, abundance.

    Used by ``treemap_microbiome``.  Eight taxa whose abundances sum
    to 1.0 — the treemap uses the values as tile areas directly.
    """
    rng = np.random.default_rng(seed)
    taxa = ["Bacteroidetes", "Firmicutes", "Proteobacteria",
            "Actinobacteria", "Verrucomicrobia", "Fusobacteria",
            "Tenericutes", "Other"]
    props = rng.dirichlet([10, 8, 4, 3, 2, 1.5, 1, 1])
    return pd.DataFrame({"taxon": taxa, "abundance": props})


# --------------------------------------------------------------------- Day 3
def gene_sets(seed: int = 15) -> pd.DataFrame:
    """Boolean set-membership matrix — index ``gene``, columns are the sets.

    Used by ``upset_gene_sets``.  200 genes × 5 boolean columns
    (DE, Leaf, Root, Photo, Stress), each ~40% True, so intersections
    emerge naturally.  Feed straight to ``upsetplot.from_indicators``.
    """
    rng = np.random.default_rng(seed)
    genes = [f"G{i:03d}" for i in range(200)]
    df = pd.DataFrame(index=pd.Index(genes, name="gene"))
    for s in ["DE", "Leaf", "Root", "Photo", "Stress"]:
        df[s] = rng.random(len(genes)) < 0.40
    return df


# ---------------------------------------------------------------- catalogue
_DATASET_INDEX: dict[str, dict[str, str]] = {
    "expression":            {"plot": "timecourse_line",            "schema": "gene, time, tpm, sem"},
    "coexpression":          {"plot": "scatter_coexpression",       "schema": "sample, tissue, gene_x, gene_y"},
    "tissue_expression":     {"plot": "bar_simple",                 "schema": "tissue, tpm"},
    "expression_groups":     {"plot": "boxplot_distributions",      "schema": "group, value"},
    "pseudotime":            {"plot": "ridgeline_pseudotime",       "schema": "id, stage, value"},
    "deseq2":                {"plot": "volcano_deseq2",             "schema": "gene, log2FoldChange, pvalue, padj"},
    "pca_features":          {"plot": "pca_population",             "schema": "individual, population, feature_0..feature_19"},
    "expression_matrix":     {"plot": "heatmap_expression",         "schema": "(expr matrix, meta DataFrame)"},
    "admixture_components":  {"plot": "ternary_admixture",          "schema": "A, B, C (rows sum to 1)"},
    "variant_classes":       {"plot": "waffle_variant_classes",     "schema": "classification, n"},
    "tmb_cohort":            {"plot": "waterfall_tmb",              "schema": "patient, value, subtype, msi"},
    "admixture_kinship":     {"plot": "stacked_bar_admixture",      "schema": "individual, population, K1..K5"},
    "microbiome_timeseries": {"plot": "stacked_bar_microbiome",     "schema": "day, phase, taxon, abundance"},
    "gwas":                  {"plot": "manhattan_gwas",             "schema": "chrom, pos, pval, snp"},
    "microbiome_abundance":  {"plot": "treemap_microbiome",         "schema": "taxon, abundance"},
    "gene_sets":             {"plot": "upset_gene_sets",            "schema": "gene index, 5 bool set columns"},
}


def list_datasets() -> pd.DataFrame:
    """Return a table of every available synthetic dataset.

    Columns: ``dataset`` (the function name), ``plot`` (the catalog
    entry it feeds), ``schema`` (the columns it produces).
    """
    return pd.DataFrame([
        {"dataset": name, **info} for name, info in _DATASET_INDEX.items()
    ])
