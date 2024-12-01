# Title: Sequence Alignment and Synteny Analysis
# Author: [Your Name]
# Date: [Date of Upload]
# Description: This script performs multiple sequence alignment, phylogenetic tree construction,
#              synteny analysis, and visualization of genomic sequences.

# Step 1: Install Required Packages
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
if (!requireNamespace("msa", quietly = TRUE)) BiocManager::install("msa")
if (!requireNamespace("ape", quietly = TRUE)) install.packages("ape")
if (!requireNamespace("seqinr", quietly = TRUE)) BiocManager::install("seqinr")
if (!requireNamespace("DECIPHER", quietly = TRUE)) BiocManager::install("DECIPHER")

# Step 2: Load Required Libraries
library(msa)       # For multiple sequence alignment
library(ape)       # For phylogenetic tree construction
library(seqinr)    # For sequence manipulation
library(DECIPHER)  # For synteny and genome alignment analysis

# Load Data from the Repository's `data` Folder
load("data/hglobin.rda")  # Ensure `hglobin.rda` is in the `data` folder
print(hglobin)  # Display loaded data to confirm successful import

# PART 1: MULTIPLE SEQUENCE ALIGNMENT AND PHYLOGENETIC TREE

# Step 1: Perform Multiple Sequence Alignment (Clustal Omega)
alignment <- msa(hglobin, method = "ClustalOmega")
print(alignment)  # View the alignment

# Step 2: Save Alignment as PDF
msaPrettyPrint(alignment, output = "pdf", showNames = "left",
               showLogo = "none", askForOverwrite = FALSE,
               verbose = FALSE, file = "whole_align.pdf")

# Step 3: Save Zoomed Alignment
msaPrettyPrint(alignment, c(10, 30), output = "pdf", showNames = "left",
               file = "zoomed_align.pdf", showLogo = "top",
               askForOverwrite = FALSE, verbose = FALSE)

# Step 4: Calculate Pairwise Distances and Create Phylogenetic Tree
alignment_seqinr <- msaConvert(alignment, type = "seqinr::alignment")
distances <- seqinr::dist.alignment(alignment_seqinr, "identity")
tree <- ape::nj(distances)

# Step 5: Plot the Phylogenetic Tree
plot(tree, main = "Phylogenetic Tree of HBA Sequences")

# PART 2: SYNTENY ANALYSIS

# Load Data from the Repository's `data` Folder
load("data/plastid_genomes.rda")  # Ensure `hglobin.rda` is in the `data` folder
print(plastid_genomes)  # Display loaded data to confirm successful import


# Step 2: Reorder Sequences by Length
Seqs2DB(plastid_genomes, "XStringSet", "long2_db", names(plastid_genomes))

# Step 4: Find and Plot Syntenic Blocks
synteny <- FindSynteny("long2_db")
pairs(synteny)

# Visualize Syntenic Relationships
plot(synteny)                    # General synteny plot
plot(synteny, "frequency")       # Plot by frequency
plot(synteny, "neighbor")        # Neighbor-based plot

# Step 5: Align Syntenic Blocks
alignment_blocks <- AlignSynteny(synteny, "long2_db")

# Step 6: Save Pairwise Alignments as FASTA
blocks <- unlist(alignment_blocks[[1]])
writeXStringSet(blocks, "genome_blocks_out.fa")
