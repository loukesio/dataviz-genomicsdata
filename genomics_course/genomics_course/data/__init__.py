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


__all__ = ["load_admixture", "load_gwas", "load_deseq2", "load_variants",
           "load_lineages", "load_timecourse", "load_coexpression",
           "load_anscombe", "load_datasaurus"]
