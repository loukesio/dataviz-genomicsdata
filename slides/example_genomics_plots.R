# Example Genomics Plots for Your Presentation
# Use these as templates for your own data

library(ggplot2)
library(dplyr)
library(pheatmap)

# =============================================================================
# 1. PCA SCATTER PLOT - For dimensionality reduction visualization
# =============================================================================

# Example: RNA-seq or SNP data reduced to 2D
create_pca_plot <- function() {
  set.seed(42)
  n_samples <- 200
  
  pca_data <- data.frame(
    PC1 = c(rnorm(100, mean = -2, sd = 2), rnorm(100, mean = 2, sd = 2)),
    PC2 = c(rnorm(100, mean = 1, sd = 1.5), rnorm(100, mean = -1, sd = 1.5)),
    condition = rep(c("Wild Type", "Mutant"), each = 100),
    batch = rep(c("Batch1", "Batch2"), times = 100)
  )
  
  p <- ggplot(pca_data, aes(x = PC1, y = PC2, color = condition, shape = batch)) +
    geom_point(size = 3, alpha = 0.7) +
    stat_ellipse(aes(group = condition), level = 0.95, linewidth = 1) +
    geom_vline(xintercept = 0, linetype = "dashed", color = "gray60") +
    geom_hline(yintercept = 0, linetype = "dashed", color = "gray60") +
    scale_color_manual(
      values = c("Wild Type" = "#0077BE", "Mutant" = "#E8A627"),
      name = "Condition"
    ) +
    scale_shape_manual(values = c(16, 17), name = "Batch") +
    labs(
      title = "Principal Component Analysis",
      subtitle = "RNA-seq data from 200 samples",
      x = "PC1 (44.3% variance explained)",
      y = "PC2 (28.1% variance explained)"
    ) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title = element_text(face = "bold", size = 16),
      plot.subtitle = element_text(color = "gray40", size = 12),
      legend.position = "bottom",
      panel.grid.minor = element_blank(),
      panel.border = element_rect(fill = NA, color = "gray80")
    )
  
  return(p)
}

# =============================================================================
# 2. DIFFERENTIAL EXPRESSION HEATMAP
# =============================================================================

create_de_heatmap <- function() {
  set.seed(123)
  
  # Simulate gene expression data (log2 fold change)
  genes <- paste0("Gene_", 1:20)
  samples <- c("WT_1", "WT_2", "WT_3", "MUT_1", "MUT_2", "MUT_3")
  
  # Create expression matrix
  expr_matrix <- matrix(
    rnorm(20 * 6, mean = 0, sd = 1),
    nrow = 20,
    ncol = 6,
    dimnames = list(genes, samples)
  )
  
  # Add some differentially expressed genes
  expr_matrix[1:5, 4:6] <- expr_matrix[1:5, 4:6] + 2  # Upregulated in mutant
  expr_matrix[6:10, 4:6] <- expr_matrix[6:10, 4:6] - 2  # Downregulated in mutant
  
  # Create annotation
  annotation_col <- data.frame(
    Condition = c(rep("WT", 3), rep("MUT", 3)),
    row.names = samples
  )
  
  # Color scheme
  ann_colors <- list(
    Condition = c(WT = "#0077BE", MUT = "#E8A627")
  )
  
  # Create heatmap
  pheatmap(
    expr_matrix,
    color = colorRampPalette(c("#0077BE", "white", "#D45B00"))(100),
    scale = "row",  # Z-score scaling
    cluster_rows = TRUE,
    cluster_cols = TRUE,
    annotation_col = annotation_col,
    annotation_colors = ann_colors,
    show_rownames = TRUE,
    show_colnames = TRUE,
    main = "Differential Gene Expression Heatmap",
    fontsize = 10,
    fontsize_row = 8,
    fontsize_col = 10,
    border_color = "gray90",
    cellwidth = 30,
    cellheight = 15
  )
}

# =============================================================================
# 3. VOLCANO PLOT - For differential expression
# =============================================================================

create_volcano_plot <- function() {
  set.seed(42)
  n_genes <- 1000
  
  volcano_data <- data.frame(
    gene = paste0("Gene_", 1:n_genes),
    log2FC = rnorm(n_genes, mean = 0, sd = 1.5),
    pvalue = runif(n_genes, 0, 0.1)
  ) |>
    mutate(
      log10p = -log10(pvalue),
      significant = case_when(
        log2FC > 1 & pvalue < 0.05 ~ "Up",
        log2FC < -1 & pvalue < 0.05 ~ "Down",
        TRUE ~ "NS"
      )
    )
  
  p <- ggplot(volcano_data, aes(x = log2FC, y = log10p, color = significant)) +
    geom_point(alpha = 0.6, size = 2) +
    geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "gray40") +
    geom_vline(xintercept = c(-1, 1), linetype = "dashed", color = "gray40") +
    scale_color_manual(
      values = c("Up" = "#D45B00", "Down" = "#0077BE", "NS" = "gray60"),
      labels = c("Upregulated", "Downregulated", "Not Significant"),
      name = ""
    ) +
    labs(
      title = "Volcano Plot",
      subtitle = "Differential expression analysis",
      x = "Log2 Fold Change",
      y = "-Log10(p-value)"
    ) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title = element_text(face = "bold", size = 16),
      plot.subtitle = element_text(color = "gray40"),
      legend.position = "bottom",
      panel.grid.minor = element_blank()
    )
  
  return(p)
}

# =============================================================================
# 4. MANHATTAN PLOT - For GWAS results
# =============================================================================

create_manhattan_plot <- function() {
  set.seed(123)
  
  # Simulate GWAS data
  chromosomes <- rep(1:22, each = 1000)
  positions <- rep(1:1000, times = 22)
  pvalues <- runif(22000, 0, 1)
  
  # Add some significant SNPs
  sig_indices <- sample(1:22000, 50)
  pvalues[sig_indices] <- runif(50, 0, 1e-8)
  
  gwas_data <- data.frame(
    chr = chromosomes,
    pos = positions,
    pvalue = pvalues
  ) |>
    mutate(
      log10p = -log10(pvalue),
      chr_color = ifelse(chr %% 2 == 0, "even", "odd")
    ) |>
    group_by(chr) |>
    mutate(
      bp_cum = pos + (chr - 1) * 1000
    ) |>
    ungroup()
  
  # Chromosome centers for x-axis
  axis_data <- gwas_data |>
    group_by(chr) |>
    summarize(center = mean(bp_cum))
  
  p <- ggplot(gwas_data, aes(x = bp_cum, y = log10p, color = chr_color)) +
    geom_point(alpha = 0.6, size = 1.5) +
    geom_hline(yintercept = -log10(5e-8), linetype = "dashed", color = "#D45B00") +
    scale_color_manual(values = c("even" = "#0077BE", "odd" = "#00A651")) +
    scale_x_continuous(
      breaks = axis_data$center,
      labels = axis_data$chr
    ) +
    labs(
      title = "Manhattan Plot",
      subtitle = "Genome-wide association study results",
      x = "Chromosome",
      y = "-Log10(p-value)"
    ) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title = element_text(face = "bold", size = 16),
      plot.subtitle = element_text(color = "gray40"),
      legend.position = "none",
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text.x = element_text(angle = 0)
    )
  
  return(p)
}

# =============================================================================
# 5. BOX PLOT WITH VIOLIN - Gene expression across conditions
# =============================================================================

create_expression_boxplot <- function() {
  set.seed(42)
  
  expr_data <- data.frame(
    condition = rep(c("Control", "Treatment_A", "Treatment_B", "Treatment_C"), each = 50),
    expression = c(
      rnorm(50, mean = 5, sd = 0.8),
      rnorm(50, mean = 7, sd = 1.2),
      rnorm(50, mean = 6, sd = 0.9),
      rnorm(50, mean = 8.5, sd = 1.5)
    ),
    replicate = rep(1:50, times = 4)
  )
  
  p <- ggplot(expr_data, aes(x = condition, y = expression, fill = condition)) +
    geom_violin(alpha = 0.5, draw_quantiles = c(0.25, 0.5, 0.75)) +
    geom_boxplot(width = 0.2, alpha = 0.7, outlier.shape = 16) +
    geom_jitter(width = 0.1, alpha = 0.2, size = 0.8) +
    scale_fill_manual(
      values = c(
        "Control" = "#888888",
        "Treatment_A" = "#0077BE",
        "Treatment_B" = "#00A651",
        "Treatment_C" = "#E8A627"
      )
    ) +
    labs(
      title = "Gene Expression Across Conditions",
      subtitle = "Target gene XYZ (n=50 per group)",
      x = "",
      y = "Expression Level (log2 TPM)"
    ) +
    theme_minimal(base_size = 14) +
    theme(
      plot.title = element_text(face = "bold", size = 16),
      plot.subtitle = element_text(color = "gray40"),
      legend.position = "none",
      panel.grid.major.x = element_blank(),
      axis.text.x = element_text(angle = 45, hjust = 1)
    )
  
  return(p)
}

# =============================================================================
# USAGE EXAMPLES
# =============================================================================

# To use in your presentation:
# 1. Copy these functions to your .qmd file setup chunk
# 2. Call them in individual slide chunks like this:

# ```{r}
# #| echo: false
# #| fig-width: 8
# #| fig-height: 6
# create_pca_plot()
# ```

# Or save them as separate R files and source:
# source("plot_functions.R")
