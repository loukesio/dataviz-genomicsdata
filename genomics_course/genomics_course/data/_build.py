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

def build_qc(n=12):
    """Sequencing QC: per-sample raw mapping rate vs callable rate after QC.
    Two samples deliberately lose >15 points to QC, for the dumbbell story.
    Columns: sample, raw, callable, loss."""
    rng = np.random.default_rng(404)
    samples = [f"S{i:02d}" for i in range(1, n + 1)]
    raw = rng.uniform(90, 99, n).round(1)                  # raw mapping rate (%)
    drop = np.r_[rng.uniform(2, 8, n - 2), [22.0, 26.0]]   # QC loss; two bad ones
    rng.shuffle(drop)
    callable_ = (raw - drop).round(1)
    df = pd.DataFrame({"sample": samples, "raw": raw, "callable": callable_})
    df["loss"] = (df.raw - df.callable).round(1)
    df.to_parquet(os.path.join(FILES, "qc_callable.parquet"))
    print("✓ qc_callable.parquet")

def _norm_cdf(x):
    from math import erf, sqrt
    return np.array([0.5 * (1 + erf(v / sqrt(2))) for v in x])

def build_tissue_expression():
    """BRCA1 expression across five tissues (tissue, tpm). Heart highest.
    For bar, ranking, data-ink, and editorial-angle demos."""
    df = pd.DataFrame({"tissue": ["Heart", "Lung", "Liver", "Kidney", "Brain"],
                       "tpm":    [91, 85, 72, 63, 58]})
    df.to_parquet(os.path.join(FILES, "tissue_expression.parquet"))
    print("✓ tissue_expression.parquet")


def build_assay_counts():
    """Public datasets per assay type (assay, n_datasets). For the memorability demo."""
    df = pd.DataFrame({"assay": ["RNA-seq", "ATAC-seq", "ChIP-seq", "WGS"],
                       "n_datasets": [342, 187, 156, 98]})
    df.to_parquet(os.path.join(FILES, "assay_counts.parquet"))
    print("✓ assay_counts.parquet")


def build_reads_per_sample():
    """Reads per sample in millions (sample, reads). For the lie-factor / baseline demo."""
    df = pd.DataFrame({"sample": ["S01", "S02", "S03", "S04", "S05"],
                       "reads":  [41.2, 38.6, 38.4, 37.8, 33.1]})
    df.to_parquet(os.path.join(FILES, "reads_per_sample.parquet"))
    print("✓ reads_per_sample.parquet")

def build_scatter_demo(n=120):
    """Control vs Treatment scatter demo for the 'Building a Plot' steps.
    Columns: log2fc (x), expression (y ~ 0.8*x + noise), group."""
    rng = np.random.default_rng(42)
    log2fc = rng.normal(0, 1, n)
    expression = 0.8 * log2fc + rng.normal(0, 0.5, n)
    group = rng.choice(["Control", "Treatment"], n)
    df = pd.DataFrame({"log2fc": log2fc, "expression": expression, "group": group})
    df.to_parquet(os.path.join(FILES, "scatter_demo.parquet"))
    print("✓ scatter_demo.parquet")

def build_wine():
    """UCI Wine clustering dataset (no class labels).
    178 samples × 13 chemistry features. For student exercises:
    PCA, k-means / hierarchical clustering, feature scaling.
    Reads the bundled CSV; columns kept as-is from source."""
    df = pd.read_csv(os.path.join(FILES, "wine-clustering.csv"))
    df.to_parquet(os.path.join(FILES, "wine.parquet"))
    print("✓ wine.parquet")

def build_microbiome(n_days=16):
    """Longitudinal gut microbiome: phylum relative abundance sampled daily across an
    antibiotic perturbation (days 5-7). Tidy long (day, phase, taxon, abundance); each
    day sums to 1. Proteobacteria blooms during antibiotics, then recovers. For
    composition-over-time stacked bars."""
    rng = np.random.default_rng(11)
    taxa = ["Firmicutes", "Bacteroidetes", "Proteobacteria",
            "Actinobacteria", "Verrucomicrobia", "Other"]
    keys = {1:  [.46, .34, .05, .07, .05, .03],   # baseline community
            5:  [.40, .30, .12, .08, .06, .04],   # antibiotics begin
            7:  [.16, .12, .50, .09, .05, .08],   # bloom peak
            10: [.30, .24, .24, .10, .06, .06],   # recovering
            16: [.44, .33, .07, .07, .05, .04]}   # recovered
    kdays = sorted(keys)
    rows = []
    for d in range(1, n_days + 1):
        lo = max(k for k in kdays if k <= d)            # nearest keyframe at/below day d
        hi = min(k for k in kdays if k >= d)            # nearest keyframe at/above day d
        if lo == hi:
            m = np.array(keys[lo])
        else:                                           # linear interpolation between keyframes
            w = (d - lo) / (hi - lo)
            m = (1 - w) * np.array(keys[lo]) + w * np.array(keys[hi])
        p = rng.dirichlet(m * 200)                      # tight sampling around the mean
        phase = "baseline" if d <= 4 else "antibiotic" if d <= 7 else "recovery"
        for t, a in zip(taxa, p):
            rows.append({"day": d, "phase": phase, "taxon": t, "abundance": float(a)})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "microbiome_phyla.parquet"))
    print("✓ microbiome_phyla.parquet")

def build_expression():
    """Drought RNA-seq: log2 expression matrix, 40 genes × 24 samples (12 Control, 12 Drought).
    Two gene modules — G000-G019 induced by drought, G020-G039 repressed. Saves the matrix
    plus a sample metadata table (condition, batch, qc) for annotation tracks."""
    rng = np.random.default_rng(7)
    n_genes, n_ctrl, n_drt = 40, 12, 12
    samples = [f"C{i:02d}" for i in range(1, n_ctrl + 1)] + [f"D{i:02d}" for i in range(1, n_drt + 1)]
    genes = [f"G{i:03d}" for i in range(n_genes)]
    X = rng.normal(8, 1.0, (n_genes, 1)) + rng.normal(0, 0.5, (n_genes, n_ctrl + n_drt))  # baseline + noise
    is_drt = np.array([False] * n_ctrl + [True] * n_drt)
    X[:20,  is_drt]  += 2.5     # module 1: induced by drought
    X[20:, ~is_drt]  += 2.5     # module 2: repressed by drought (high in control)
    pd.DataFrame(X, index=genes, columns=samples).reset_index(names="gene") \
        .to_parquet(os.path.join(FILES, "expression_matrix.parquet"))
    pd.DataFrame({"sample": samples,
                  "condition": ["Control"] * n_ctrl + ["Drought"] * n_drt,
                  "batch": (["A", "B", "C"] * 8)[:n_ctrl + n_drt],
                  "qc": rng.uniform(0.85, 1.0, n_ctrl + n_drt).round(3)}) \
        .to_parquet(os.path.join(FILES, "expression_meta.parquet"))
    print("✓ expression_matrix.parquet + expression_meta.parquet")

def build_pseudotime(n_per_stage=250, n_stages=8):
    """Single-cell expression of a differentiation marker (NEUROD1) along pseudotime,
    binned into 8 ordered stages. Tidy long (cell, stage, expression). The gene switches
    on: early stages mostly OFF, late mostly ON, bimodal in between. For ridgeline plots."""
    rng = np.random.default_rng(3)
    rows = []
    for s in range(1, n_stages + 1):
        p_on = 1 / (1 + np.exp(-1.4 * (s - 4.5)))                 # ON fraction rises along pseudotime
        on = rng.random(n_per_stage) < p_on                       # which cells have switched on
        expr = np.where(on, rng.normal(8.0, 1.1, n_per_stage),    # ON mode  ~ 8
                            rng.normal(1.2, 0.6, n_per_stage))    # OFF mode ~ 1
        for i, e in enumerate(np.clip(expr, 0, None)):
            rows.append({"cell": f"S{s}_{i:03d}", "stage": s, "expression": float(e)})
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "pseudotime.parquet"))
    print("✓ pseudotime.parquet")

def build_grape_snps(n_per_species=30, n_snps=300):
    """Synthetic Vitis SNP genotypes: 90 vines × 300 SNPs across 3 grape species
    (V. vinifera, V. labrusca, V. riparia). Encoded 0/1/2 (minor-allele count, like PLINK).
    60% of SNPs are species-informative (independent allele frequencies per species),
    40% are species-shared noise — so PCA cleanly separates the 3 groups while still
    looking realistic. Wide format: sample, species, SNP_0000..SNP_0299.
    For dimensionality-reduction student exercises."""
    rng = np.random.default_rng(2024)
    species = ["vinifera", "labrusca", "riparia"]
    n_informative = int(0.6 * n_snps)
    freqs = np.empty((3, n_snps))
    # Informative SNPs: each species draws independent frequencies — U-shaped beta means
    # most SNPs are near-fixed for one allele in each species, so species differ markedly.
    freqs[:, :n_informative] = rng.beta(0.5, 0.5, (3, n_informative))
    # Shared SNPs: one frequency reused across all species (no information about identity).
    freqs[:, n_informative:] = rng.beta(1, 1, n_snps - n_informative)[None, :]
    rows = []
    for s_idx, sp in enumerate(species):
        for v in range(n_per_species):
            geno = rng.binomial(2, freqs[s_idx])              # one diploid sample
            row = {"sample": f"{sp[:3].upper()}{v + 1:02d}", "species": sp}
            row.update({f"SNP_{j:04d}": int(g) for j, g in enumerate(geno)})
            rows.append(row)
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "grape_snps.parquet"))
    print("✓ grape_snps.parquet")

def build_variant_classes():
    """Clinical variant interpretation counts from a gene-panel screen
    (classification, n) — ACMG categories. For part-to-whole waffle charts."""
    pd.DataFrame({"classification": ["Pathogenic", "Likely pathogenic", "VUS",
                                     "Likely benign", "Benign"],
                  "n": [12, 18, 55, 24, 41]}).to_parquet(
        os.path.join(FILES, "variant_classes.parquet"))
    print("✓ variant_classes.parquet")

def build_tmb_cohort(n=60):
    """Tumour mutation burden across a cohort (patient, tmb, subtype, msi). TMB is
    lognormal; MSI-H tumours are hypermutated. For ranked 'waterfall' bar plots."""
    rng = np.random.default_rng(5)
    tmb = rng.lognormal(2.4, 0.9, n)                          # most tumours low-TMB
    subtype = rng.choice(["Luminal A", "Luminal B", "HER2+", "TNBC"], n, p=[.4, .25, .2, .15])
    msi = rng.random(n) < 0.12                                # ~12% MSI-high
    tmb[msi] *= rng.uniform(2, 4, msi.sum())                  # MSI-H tumours hypermutate
    pd.DataFrame({"patient": [f"P{i:03d}" for i in range(n)], "tmb": tmb.round(1),
                  "subtype": subtype, "msi": np.where(msi, "MSI-H", "MSS")}).to_parquet(
        os.path.join(FILES, "tmb_cohort.parquet"))
    print("✓ tmb_cohort.parquet")

def build_peaks():
    """Epigenomic signal over a 20 kb window for three marks, plus gene annotations.
    Deterministic Gaussian peaks: all marks at the two promoters (TSS), but the enhancer
    (~8.5 kb) carries H3K27ac + ATAC and NO H3K4me3. For multi-track browser plots."""
    rng = np.random.default_rng(8)
    x = np.linspace(0, 20000, 1000)
    def track(centers, width=450, noise=0.04):
        s = noise * np.abs(rng.standard_normal(len(x)))     # flat background
        for c, a in centers:                                # add each Gaussian peak
            s += a * np.exp(-((x - c) ** 2) / (2 * width ** 2))
        return np.clip(s, 0, None)
    sig = pd.DataFrame({"position": x,
        "H3K27ac": track([(1800, 1.0), (8500, 1.1), (13800, 0.9)]),  # promoters + enhancer
        "H3K4me3": track([(1800, 1.2), (13800, 1.0)]),               # promoters only
        "ATAC":    track([(1800, 1.0), (8500, 1.0), (13800, 0.9)], width=300)})  # all open
    sig.to_parquet(os.path.join(FILES, "peaks_signal.parquet"))
    pd.DataFrame({"name": ["GeneA", "GeneB", "GeneC"], "start": [1500, 7000, 13500],
                  "end": [4500, 10500, 17000], "strand": ["+", "-", "+"]}).to_parquet(
        os.path.join(FILES, "peaks_genes.parquet"))
    print("✓ peaks_signal.parquet + peaks_genes.parquet")

def build_enrichment():
    """Pathway over-representation results for the drought DE genes
    (pathway, direction, p_adj, gene_count, gene_ratio, category). Pre-computed (e.g. with
    gget enrichr) so the deck renders offline. up = drought-induced, down = drought-repressed."""
    up = [("response to water deprivation", 1.2e-9, 38, 0.42, "Stress"),
          ("abscisic acid signaling", 4.5e-8, 27, 0.31, "Signaling"),
          ("response to osmotic stress", 7.0e-7, 31, 0.28, "Stress"),
          ("proline biosynthesis", 3.1e-5, 9, 0.50, "Metabolism"),
          ("regulation of stomatal closure", 6.0e-5, 12, 0.34, "Signaling"),
          ("response to reactive oxygen species", 2.0e-4, 22, 0.19, "Stress"),
          ("trehalose biosynthesis", 9.0e-4, 7, 0.41, "Metabolism"),
          ("heat acclimation", 8.0e-3, 10, 0.16, "Stress")]
    down = [("photosynthesis, light harvesting", 5.0e-11, 45, 0.55, "Photosynthesis"),
            ("chlorophyll biosynthesis", 2.0e-8, 19, 0.48, "Photosynthesis"),
            ("cell wall biogenesis", 1.5e-6, 33, 0.30, "Growth"),
            ("photosystem II assembly", 4.0e-6, 14, 0.44, "Photosynthesis"),
            ("carbon fixation", 9.0e-5, 17, 0.26, "Metabolism"),
            ("cell division", 3.0e-4, 28, 0.18, "Growth"),
            ("ribosome biogenesis", 1.2e-3, 24, 0.15, "Growth"),
            ("DNA replication", 1.1e-2, 16, 0.12, "Growth")]
    rows = [dict(pathway=p, direction=d, p_adj=pa, gene_count=n, gene_ratio=r, category=c)
            for d, grp in [("up", up), ("down", down)] for p, pa, n, r, c in grp]
    pd.DataFrame(rows).to_parquet(os.path.join(FILES, "enrichment.parquet"))
    print("✓ enrichment.parquet")


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
    build_qc()             # NEW
    build_tissue_expression()
    build_assay_counts()
    build_reads_per_sample()
    build_scatter_demo()
    build_wine()
    build_microbiome()
    build_expression()
    build_pseudotime()
    build_grape_snps()
    build_variant_classes()
    build_tmb_cohort()
    build_peaks()
    build_enrichment()

    print("\nAll datasets built into files/")
