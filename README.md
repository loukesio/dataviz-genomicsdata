# 🧬 Data Visualization for Genomics & Biological Sciences

A comprehensive 3-day workshop on creating publication-quality visualizations for genomics and biological data using R and ggplot2.

## 📚 Course Materials

### Day 1: Foundations
- **Introduction to Data Visualization**
  - Why visualization matters (Anscombe's Quartet, Datasaurus Dozen)
  - Big data challenges in biology
  - Typography and color theory
  - Color palettes for genomics
- **ggplot2 Fundamentals**
  - Grammar of Graphics philosophy
  - Building plots layer by layer
  - Custom themes and styling
- **Essential Plot Types**
  - Scatter plots (PCA, correlations)
  - Bar charts (expression comparisons)
  - Box plots & violin plots (distributions)
  - Stacked plots (microbiome composition)

### Day 2: Advanced Genomics Visualizations
- **Dimensionality Reduction**
  - PCA, UMAP, t-SNE theory and implementation
  - Choosing the right method
  - Practical examples with gene expression data
- **Volcano Plots**
  - Step-by-step construction
  - Methods: base ggplot2, EnhancedVolcano, ggvolc
  - Multi-level classifications
- **Peak Visualization**
  - ChIP-seq and ATAC-seq data
  - Track plots with karyoploteR
  - Detailed locus views with Gviz

### Day 3: Specialized Visualizations
- **Set Comparisons**
  - Venn diagrams (ggvenn, ggVennDiagram)
  - UpSet plots for complex overlaps
  - When to use each method
- **Phylogenetic Trees**
  - Multiple layouts (rectangular, circular, radial)
  - Highlighting clades and adding metadata
  - Advanced annotations with ggtreeExtra
- **Circular Genome Plots**
  - circlize package fundamentals
  - Multi-track visualizations
  - Links for structural variants
- **Gene Arrangements & Synteny**
  - gggenes for gene-level detail
  - Comparative genomics
  - Prophage insertion visualization

## 🎨 Key Features

- **Publication-ready outputs** using custom themes
- **Cross color palette** throughout for consistency
- **Real biological examples** from genomics research
- **Hands-on exercises** for each major topic
- **Best practices** for scientific visualization
- **Colorblind-friendly** design principles

## 📦 Required Packages

### Core Visualization
```r
library(tidyverse)      # Data manipulation & ggplot2
library(patchwork)      # Combine plots
library(MetBrewer)      # Color palettes
library(RColorBrewer)   
library(pheatmap)       # Heatmaps
```

### Specialized Genomics
```r
library(ggtree)         # Phylogenetic trees
library(circlize)       # Circular plots
library(karyoploteR)    # Karyotype visualization
library(Gviz)           # Genomic tracks
library(gggenes)        # Gene arrangements
library(UpSetR)         # Set comparisons
library(ggvenn)         # Venn diagrams
```

### Dimensionality Reduction
```r
library(umap)
library(Rtsne)
```

## 🚀 Getting Started

1. Clone this repository
2. Install required packages
3. Open the `.Rproj` file in RStudio
4. Navigate to `slides/` for presentation materials
5. Follow along with the embedded code examples

## 📖 Resources

- **Custom theme function** included for consistent styling
- **Example datasets** provided for all exercises
- **Color palette guide** (Cross palette from MetBrewer)
- **Links to awesome-genome-visualization** collection

## 🎓 Learning Outcomes

By the end of this workshop, you will be able to:

- ✅ Create publication-quality figures for genomics research
- ✅ Choose appropriate visualizations for different data types
- ✅ Customize plots extensively using ggplot2
- ✅ Visualize complex genomic relationships
- ✅ Apply best practices in scientific data visualization
- ✅ Integrate multiple data types in comprehensive figures

## 👨‍🏫 Instructor

**Dr. Loukas Theodosiou**  
Senior Data Scientist | Population Genomics & AI/ML  
[GitHub](https://github.com/loukesio)

---

**Course Materials**: December 2024  
**License**: Materials are provided for educational purposes
