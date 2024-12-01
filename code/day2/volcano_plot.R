#_________________________________________________________________________________________________________________
#
# ██╗   ██╗ ██████╗ ██╗      ██████╗ █████╗ ███╗   ██╗ ██████╗     ██████╗ ██╗      ██████╗ ████████╗███████╗
# ██║   ██║██╔═══██╗██║     ██╔════╝██╔══██╗████╗  ██║██╔═══██╗    ██╔══██╗██║     ██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██║   ██║██║     ██║     ███████║██╔██╗ ██║██║   ██║    ██████╔╝██║     ██║   ██║   ██║   ███████╗
# ╚██╗ ██╔╝██║   ██║██║     ██║     ██╔══██║██║╚██╗██║██║   ██║    ██╔═══╝ ██║     ██║   ██║   ██║   ╚════██║
#  ╚████╔╝ ╚██████╔╝███████╗╚██████╗██║  ██║██║ ╚████║╚██████╔╝    ██║     ███████╗╚██████╔╝   ██║   ███████║
#   ╚═══╝   ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝     ╚═╝     ╚══════╝ ╚═════╝    ╚═╝   ╚══════╝
#
#_________________________________________________________________________________________________________________

# Load necessary libraries for plotting and data manipulation
library(ggvolc)    # For creating enhanced volcano plots
library(tidyverse) # For data manipulation and visualization

# Load a dataset of gene data provided by the ggvolc package
data("all_genes")  # Example dataset containing gene information
data("attention_genes")

# Display the structure of the dataset (optional, for understanding the data)
all_genes

#------------------------------------
# Make a volcano plot using ggplot2
#------------------------------------

# Basic volcano plot
ggplot(all_genes, aes(x = log2FoldChange, y = -log10(pvalue), label = genes)) +
  geom_point(aes(color = padj < 0.05), size = 2) +  # Color points based on significance (padj < 0.05)
  scale_color_manual(values = c("gray", "red")) +   # Define colors: red for significant, gray for non-significant
  geom_text(
    data = subset(all_genes, padj < 0.05 & abs(log2FoldChange) > 2) %>%
      arrange(padj) %>%
      head(10),  # Select the top 10 most significant genes based on padj
    vjust = -1, hjust = 1, size = 3  # Adjust text position for clarity
  ) +
  labs(
    title = "Volcano Plot",  # Title of the plot
    x = "Log2 Fold Change",  # Label for the x-axis
    y = "-Log10(P-value)"    # Label for the y-axis
  ) +
  geom_vline(xintercept = c(-2, 2), linetype = "dashed", color = "black") +  # Vertical dashed lines at log2FC thresholds
  geom_hline(yintercept = -log10(0.005), linetype = "dashed", color = "black") +  # Horizontal dashed line at p-value threshold
  theme_minimal()  # Apply a minimal theme for a clean appearance

#------------------------------------
# Enhanced volcano plot with upregulated/downregulated gene highlighting
#------------------------------------

# Add custom labels for upregulated and downregulated genes
ggplot(all_genes, aes(x = log2FoldChange, y = -log10(pvalue), label = genes)) +
  geom_point(aes(color = factor(case_when(
    log2FoldChange > 2 & padj < 0.05 ~ "Upregulated",  # High log2FC and significant p-value
    log2FoldChange < -2 & padj < 0.05 ~ "Downregulated",  # Low log2FC and significant p-value
    TRUE ~ "Not Significant"  # Otherwise, not significant
  ))), size = 2) +
  scale_color_manual(values = c("Upregulated" = "red", "Downregulated" = "blue", "Not Significant" = "gray")) +
  geom_text(
    data = subset(all_genes, padj < 0.05 & abs(log2FoldChange) > 2) %>%
      arrange(padj) %>%
      head(10),
    vjust = -1, hjust = 1, size = 3
  ) +
  geom_vline(xintercept = c(-2, 2), linetype = "dashed", color = "blue") +
  geom_hline(yintercept = -log10(0.005), linetype = "dashed", color = "blue") +
  labs(
    title = "Volcano Plot with Highlighted Upregulated and Downregulated Genes",
    x = "Log2 Fold Change",
    y = "-Log10(P-value)",
    color = "Gene Status"
  ) +
  theme_minimal()

#------------------------------------
# Make volcano plots using ggvolc
#------------------------------------

# Basic volcano plot using ggvolc for simplicity
ggvolc(all_genes)

# Highlight specific genes of interest (replace attention_genes with a vector of genes)
# Example: attention_genes <- c("Gene1", "Gene2")
ggvolc(all_genes, attention_genes)

# Advanced volcano plot with segments and variable point size based on log2FoldChange
ggvolc(all_genes, attention_genes, add_seg = TRUE, size_var = "log2FoldChange")

# Create an enhanced volcano plot with a custom title
plot <- ggvolc(all_genes, attention_genes, add_seg = TRUE) +
  labs(title = "Volcano Plot with Highlighted Genes of Interest")

# Add a table of selected genes to the enhanced volcano plot
plot %>%
  genes_table(attention_genes)

