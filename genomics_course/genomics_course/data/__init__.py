"""
genomics_course.data
────────────────────
Loaders for pre-built course datasets. Students call these — no simulation.

    from genomics_course.data import load_admixture, load_gwas, load_deseq2, load_variants
    df = load_admixture(K=5)
"""

import os
import pandas as pd

FILES = os.path.join(os.path.dirname(__file__), "files")


def _load(name):
    path = os.path.join(FILES, name)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{name} not found. Build datasets once with:\n"
            f"  python -m genomics_course.data._build")
    return pd.read_parquet(path)


def load_admixture(K=5, population=None):
    """Ancestry proportions. K currently fixed at 5; population filters to one group."""
    df = _load("admixture_k5.parquet")
    if population:
        df = df[df["population"] == population].reset_index(drop=True)
    return df


def load_gwas(trait="height"):
    """GWAS summary statistics (chrom, pos, pval, snp)."""
    return _load(f"gwas_{trait}.parquet")


def load_deseq2(contrast="drought"):
    """DESeq2 differential expression results."""
    return _load(f"deseq2_{contrast}.parquet")


def load_variants():
    """Variant effect predictions (log-likelihood differences)."""
    return _load("variants_lld.parquet")


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

def load_qc():
    """Per-sample sequencing QC: raw mapping rate vs callable rate after QC.
    Columns: sample, raw, callable, loss (12 samples; two flagged droppers)."""
    return _load("qc_callable.parquet")

def load_tissue_expression():
    """BRCA1 expression across tissues (tissue, tpm). Heart highest."""
    return _load("tissue_expression.parquet")


def load_assay_counts():
    """Public datasets per assay type (assay, n_datasets)."""
    return _load("assay_counts.parquet")


def load_reads_per_sample():
    """Reads per sample in millions (sample, reads)."""
    return _load("reads_per_sample.parquet")

def load_scatter_demo():
    """Control vs Treatment scatter demo (log2fc, expression, group).
    For the step-by-step 'Building a Plot' slides."""
    return _load("scatter_demo.parquet")

def load_wine():
    """UCI Wine clustering dataset: 178 samples × 13 chemistry features.
    No class labels — meant for unsupervised student exercises
    (PCA, k-means / hierarchical clustering, feature scaling)."""
    return _load("wine.parquet")

def load_microbiome():
    """Longitudinal gut microbiome phylum abundances (day, phase, taxon, abundance).
    Tidy long form; each day sums to 1. Phases: baseline → antibiotic (days 5-7,
    Proteobacteria bloom) → recovery. For composition-over-time stacked bars."""
    return _load("microbiome_phyla.parquet")

def load_expression():
    """Drought RNA-seq log2 expression matrix (40 genes × 24 samples), genes as index."""
    return _load("expression_matrix.parquet").set_index("gene")

def load_expression_meta():
    """Sample metadata for the drought expression matrix (sample, condition, batch, qc).
    Use as annotation tracks alongside load_expression()."""
    return _load("expression_meta.parquet")

def load_pseudotime():
    """Single-cell marker expression along pseudotime (cell, stage, expression); 8 ordered
    stages, the gene switches from OFF to ON. For ridgeline distribution plots."""
    return _load("pseudotime.parquet")

def load_grape_snps():
    """Synthetic Vitis SNP genotypes: 90 vines × 300 SNPs across 3 grape species
    (vinifera, labrusca, riparia). Columns: sample, species, SNP_0000..SNP_0299
    (0/1/2 minor-allele count). For PCA / t-SNE / UMAP student exercises —
    PCA pulls the 3 species into clean clusters."""
    return _load("grape_snps.parquet")

def load_variant_classes():
    """Clinical variant interpretation counts (classification, n)."""
    return _load("variant_classes.parquet")

def load_tmb_cohort():
    """Tumour mutation burden cohort (patient, tmb, subtype, msi)."""
    return _load("tmb_cohort.parquet")

def load_peaks():
    """Epigenomic signal tracks (position, H3K27ac, H3K4me3, ATAC) over 20 kb."""
    return _load("peaks_signal.parquet")

def load_peak_genes():
    """Gene annotations for the peak window (name, start, end, strand)."""
    return _load("peaks_genes.parquet")

def load_enrichment():
    """Pathway enrichment for the drought DE genes (pathway, direction, p_adj,
    gene_count, gene_ratio, category)."""
    return _load("enrichment.parquet")

__all__ = ["load_admixture", "load_gwas", "load_deseq2", "load_variants",
           "load_lineages", "load_timecourse", "load_coexpression",
           "load_anscombe", "load_datasaurus", "load_qc",
           "load_tissue_expression", "load_assay_counts", "load_reads_per_sample",
           "load_scatter_demo", "load_wine", "load_microbiome",
           "load_expression", "load_expression_meta", "load_pseudotime",
           "load_grape_snps",
           "load_variant_classes", "load_tmb_cohort",
           "load_peaks", "load_peak_genes", "load_enrichment"]
