
#install libraries

library("VennDiagram")
library("UpSetR")

# Example list of human gene names
human_genes <- c("BRCA1", "TP53", "EGFR", "VEGFA", "MYC", "PTEN", "CDKN2A", "RB1", "APC", "KRAS",
                 "BRAF", "ATM", "ABL1", "JAK2", "SMAD4", "FGFR3", "PIK3CA", "NTRK1", "CTNNB1", "HNF1A",
                 "GATA3", "RUNX1", "MLH1", "PMS2", "MSH2", "MSH6", "PDGFRA", "ERBB2", "MPL", "NOTCH1",
                 "IDH1", "IDH2", "KIT", "FLT3", "CSF1R", "SRC", "CDH1", "MET", "ALK", "ROS1",
                 "RET", "SMO", "FOXA1", "AR", "WT1", "NF1", "TSC1", "TSC2", "STK11", "VHL",
                 "SDHB", "SDHD", "NFKB1", "STAT3", "ELANE", "CEBPA", "KLF4", "FOXP3", "SOX2", "TBX3",
                 "TBX5", "HNF4A", "PPARG", "IRF4", "IRF8", "ZEB1", "ZEB2", "EZH2", "SMARCB1", "YAP1",
                 "TAZ", "TEAD1", "TEAD4", "FOXM1", "E2F1", "E2F3", "MMP9", "MMP2", "BCL2", "BAX",
                 "BID", "BAK1", "CYC1", "COX6A2", "COX7A2L", "ATP5F1", "ATP5MC1", "ATP5MC3", "ATP5PF", "ATP5PO",
                 "ATP5SL", "ATP5MG", "NDUFA4", "NDUFB2", "NDUFB4", "NDUFB5", "NDUFB6", "NDUFB7", "NDUFB8", "NDUFS1",
                 "NDUFS2", "NDUFS3", "NDUFS5", "NDUFS6", "NDUFV1", "NDUFV2", "NDUFV3", "SDHA", "SDHC", "UQCRC1")

# Create 5 datasets with 100 genes each, ensuring some overlap and some unique genes
set.seed(123)  # Set seed for reproducibility
dataset1 <- sample(human_genes, 50, replace = FALSE)
dataset2 <- sample(human_genes, 50, replace = FALSE)
dataset3 <- sample(human_genes, 50, replace = FALSE)
dataset4 <- sample(human_genes, 50, replace = FALSE)
dataset5 <- sample(human_genes, 50, replace = FALSE)

dataset1

#combine datasets into a list

# Create 5 datasets with 100 genes each, ensuring some overlap and some unique genes
set.seed(123)  # Set seed for reproducibility
dataset1 <- sample(human_genes, 100, replace = FALSE)
dataset2 <- sample(human_genes, 100, replace = FALSE)
dataset3 <- sample(human_genes, 100, replace = FALSE)
dataset4 <- sample(human_genes, 100, replace = FALSE)
dataset5 <- sample(human_genes, 100, replace = FALSE)


# Combine datasets into a list for visualization
gene_sets_3 <- list(Dataset1 = dataset1, Dataset2 = dataset2, Dataset3 = dataset3)
gene_sets_5 <- list(Dataset1 = dataset1, Dataset2 = dataset2, Dataset3 = dataset3, Dataset4 = dataset4, Dataset5 = dataset5)


#Create Venn Diagram for 3 datasets
library(ggplot2)

venn3 <- venn.diagram(
  x = gene_sets_3,
  filename = NULL,
  category.names = names(gene_sets_3),
  height = 480,
  width = 480,
  lwd=0,
  col=c("#440154ff", "#d1422f", "#21908dff"),
  fill=c(alpha("#440154ff",  0.3), alpha("#d1422f",0.3), alpha("#21908dff", 0.3)),
  cat.fontfamily="Georgia",
  # Circles
  lty = 'blank',
  cat.cex=0.5,
  rotation=2
)


grid.newpage()
grid.draw(venn3)



library(colorspace)

# Original palette
original_palette <- c("#4CAF50", "#2196F3", "#FFC107") # A custom palette

# Adjust transparency
transparent_palette <- adjust_transparency(original_palette, alpha = 0.5) # Alpha between 0 and 1

# Plot to visualize
barplot(rep(1, 3), col = original_palette, main = "Original Palette", border = NA)
barplot(rep(1, 3), col = transparent_palette, main = "Transparent Palette (alpha = 0.5)", border = NA)





venn5 <- venn.diagram(
  x = gene_sets_5,
  filename = NULL,
  category.names = names(gene_sets_5))

grid.newpage()
grid.draw(venn5)


# upset plots

upset_data_3 <- fromList(gene_sets_3)
upset_data_3

?upset

library(ltc)

dev.off()
upset(upset_data_3, sets = names(gene_sets_3), order.by = "freq",
      main.bar="#333333",
      sets.bar.color = "#d1422f",
      matrix.color = "#333333",
      line.size = 0.5,
      point.size = 3
      )


grid.text("My_Title",x = 0.65, y=0.95, gp=gpar(fontsize=20))







