library(tidyverse)

# Set parameters for data generation
set.seed(123)  # Ensure reproducibility of random data
num_snps <- 1000  # Total number of simulated SNPs
num_qtls <- 5     # Number of significant QTLs to highlight

# Generate random data for SNPs
eQTL_data <- data.frame(
  pos = sample(40250000:42000000, num_snps, replace = TRUE),  # Random genomic positions on chromosome 3
  chr = rep("chr3", num_snps),  # Assign chromosome label
  pvalue = runif(num_snps, 0.01, 1),  # Random p-values between 0.01 and 1
  snps = paste0("chr3_", sample(40250000:42000000, num_snps, replace = TRUE))  # Unique SNP identifiers
)

# Identify significant QTLs and assign very low p-values
qtls <- sample(1:num_snps, num_qtls)  # Randomly select indices for QTLs


eQTL_data$pvalue[qtls] <- runif(num_qtls, 1e-10, 1e-6)  # Assign extremely low p-values for these QTLs
eQTL_data$is_qtl <- ifelse(1:num_snps %in% qtls, "QTL", "Non-QTL")  # Label data points as "QTL" or "Non-QTL"

eQTL_data


ggplot(eQTL_data, aes(x=pos, y=-log10(pvalue), color=is_qtl)) +
  geom_point(size=2, alpha=0.7) +
  physalia_theme()  +
  geom_text_repel(
     data = subset(eQTL_data, is_qtl == "QTL"),  # Only label significant QTLs
     aes(label = snps), color = "#d1422f", size = 3  # Label with SNP identifiers in red
   ) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "#009E73") +  # Horizontal line representing a significance threshold at p=0.05
  scale_color_manual(values = c("Non-QTL" = "black", "QTL" = "#d1422f")) +  # Custom color scheme for Non-QTLs (black) and QTLs (red)
  labs(
    title = "eQTL SNP Connectivity with Highlighted QTLs",  # Title of the plot
    x = "Genomic Position (chr3)",  # X-axis label
    y = expression(-log[10](p-value)),  # Y-axis label in mathematical notation
    color = "SNP Type"  # Legend title for the color coding
  )








# Load the library
install.packages("qqman")
library(qqman)

gwasResults
# Make the Manhattan plot on the gwasResults dataset
manhattan(gwasResults, chr="CHR", bp="BP", snp="SNP", p="P" )
snpsOfInterest

manhattan(gwasResults, highlight = snpsOfInterest)

