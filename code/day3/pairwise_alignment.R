# Title: Pairwise Alignment of DNA Sequences
# Author: [Your Name]
# Date: [Date of Upload]
# Description: This script performs pairwise alignment of DNA sequences between two groups
#              and calculates mismatches and percentage dissimilarity.

# Install required packages if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}
if (!requireNamespace("Biostrings", quietly = TRUE)) {
  BiocManager::install("Biostrings")
}
if (!requireNamespace("pwalign", quietly = TRUE)) {
  install.packages("pwalign")
}

# Load required libraries
library(Biostrings)
library(pwalign)

# Create a data frame with sequences
df <- data.frame(
  group = c(1, 1, 2, 2),
  sequence = c("AAATCG", "ATTTGG", "TTTGGGA", "ATCCGCC")
)

# Group sequences based on group ID
grouped_seqs <- split(df$sequence, df$group)

# Create an empty data frame to store alignment results
alignment_df <- data.frame(
  Group1_Seq = character(),
  Group2_Seq = character(),
  Alignment = character(),
  Mismatches = numeric(),
  Dissimilarity = numeric(),
  stringsAsFactors = FALSE
)

# Compare sequences from group 1 with group 2
for (i in 1:length(grouped_seqs[[1]])) {
  for (j in 1:length(grouped_seqs[[2]])) {
    # Convert sequences to DNAString objects
    seq1 <- DNAString(grouped_seqs[[1]][i])
    seq2 <- DNAString(grouped_seqs[[2]][j])

    # Perform pairwise sequence alignment
    alignment <- pairwiseAlignment(pattern = seq1, subject = seq2)

    # Calculate the number of mismatches
    mismatches <- nmismatch(alignment)

    # Calculate the percentage of dissimilarity
    dissimilarity <- mismatches / nchar(seq1) * 100

    # Store the alignment result in the data frame
    alignment_df <- rbind(alignment_df, data.frame(
      Group1_Seq = grouped_seqs[[1]][i],
      Group2_Seq = grouped_seqs[[2]][j],
      Alignment = toString(alignment),
      Mismatches = mismatches,
      Dissimilarity = dissimilarity
    ))
  }
}

# Print the alignment results
print(alignment_df)

# Save the results to a CSV file
write.csv(alignment_df, "alignment_results.csv", row.names = FALSE)
