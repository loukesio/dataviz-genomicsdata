# Title: Visualization of Gene Overlap using Venn Diagrams and UpSet Plots
# Author: [Your Name]
# Date: [Date of Upload]
# Description: This script generates Venn diagrams and UpSet plots to visualize overlaps
#              between gene sets. It includes customization for aesthetics and detailed annotations.

# Required Libraries
if (!requireNamespace("VennDiagram", quietly = TRUE)) install.packages("VennDiagram")
if (!requireNamespace("UpSetR", quietly = TRUE)) install.packages("UpSetR")

library(VennDiagram)
library(UpSetR)
library(grid)
library(scales)

# Example List of Human Gene Names
human_genes <- c(
  "BRCA1", "TP53", "EGFR", "VEGFA", "MYC", "PTEN", "CDKN2A", "RB1", "APC", "KRAS",
  "BRAF", "ATM", "ABL1", "JAK2", "SMAD4", "FGFR3", "PIK3CA", "NTRK1", "CTNNB1", "HNF1A",
  "GATA3", "RUNX1", "MLH1", "PMS2", "MSH2", "MSH6", "PDGFRA", "ERBB2", "MPL", "NOTCH1",
  "IDH1", "IDH2", "KIT", "FLT3", "CSF1R", "SRC", "CDH1", "MET", "ALK", "ROS1",
  "RET", "SMO", "FOXA1", "AR", "WT1", "NF1", "TSC1", "TSC2", "STK11", "VHL",
  "SDHB", "SDHD", "NFKB1", "STAT3", "ELANE", "CEBPA", "KLF4", "FOXP3", "SOX2", "TBX3",
  "TBX5", "HNF4A", "PPARG", "IRF4", "IRF8", "ZEB1", "ZEB2", "EZH2", "SMARCB1", "YAP1",
  "TAZ", "TEAD1", "TEAD4", "FOXM1", "E2F1", "E2F3", "MMP9", "MMP2", "BCL2", "BAX",
  "BID", "BAK1", "CYC1", "COX6A2", "COX7A2L", "ATP5F1", "ATP5MC1", "ATP5MC3", "ATP5PF", "ATP5PO",
  "ATP5SL", "ATP5MG", "NDUFA4", "NDUFB2", "NDUFB4", "NDUFB5", "NDUFB6", "NDUFB7", "NDUFB8", "NDUFS1",
  "NDUFS2", "NDUFS3", "NDUFS5", "NDUFS6", "NDUFV1", "NDUFV2", "NDUFV3", "SDHA", "SDHC", "UQCRC1"
)

# Create 5 Datasets with 100 Genes Each
set.seed(123)
dataset1 <- sample(human_genes, 100, replace = FALSE)
dataset2 <- sample(human_genes, 100, replace = FALSE)
dataset3 <- sample(human_genes, 100, replace = FALSE)
dataset4 <- sample(human_genes, 100, replace = FALSE)
dataset5 <- sample(human_genes, 100, replace = FALSE)

# Combine Datasets for Visualization
gene_sets_3 <- list(Dataset1 = dataset1, Dataset2 = dataset2, Dataset3 = dataset3)
gene_sets_5 <- list(Dataset1 = dataset1, Dataset2 = dataset2, Dataset3 = dataset3, Dataset4 = dataset4, Dataset5 = dataset5)

# Generate Venn Diagram for 3 Datasets
venn.plot_3 <- venn.diagram(
  x = gene_sets_3,
  category.names = names(gene_sets_3),
  filename = NULL,
  output = TRUE,
  imagetype = "png",
  height = 480,
  width = 480,
  resolution = 300,
  lwd = 1,
  col = c("#440154ff", "#21908dff", "#fde725ff"),
  fill = c(alpha("#440154ff", 0.3), alpha("#21908dff", 0.3), alpha("#fde725ff", 0.3))
)
grid.newpage()
grid.draw(venn.plot_3)

# Generate Venn Diagram for 5 Datasets
venn.plot_5 <- venn.diagram(
  x = gene_sets_5,
  category.names = names(gene_sets_5),
  filename = NULL,
  output = TRUE,
  imagetype = "png",
  height = 480,
  width = 480,
  resolution = 300,
  lwd = 1,
  col = c("#440154ff", "#21908dff", "#fde725ff", "#b73779", "#3b528b"),
  fill = c("#44015480", "#21908d80", "#fde72580", "#b7377980", "#3b528b80")
)
grid.newpage()
grid.draw(venn.plot_5)

# Generate UpSet Plot for 3 Datasets
upset_data_3 <- fromList(gene_sets_3)
upset(
  upset_data_3,
  sets = names(gene_sets_3),
  order.by = "freq",
  main.bar.color = "#21908dff",
  sets.bar.color = "#440154ff"
)

# Generate UpSet Plot for 5 Datasets
upset_data_5 <- fromList(gene_sets_5)
upset(
  upset_data_5,
  sets = names(gene_sets_5),
  order.by = "freq",
  main.bar.color = "#3b528b",
  sets.bar.color = "#b73779"
)
