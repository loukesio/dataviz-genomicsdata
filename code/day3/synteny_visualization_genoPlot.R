# Title: Synteny Visualization with genoPlotR and ggplot2
# Author: [Your Name]
# Date: [Date of Upload]
# Description: This script demonstrates synteny visualization using genoPlotR and ggplot2.
#              It includes both basic and enhanced plotting techniques.

# Step 1: Install and Load Required Packages
if (!requireNamespace("genoPlotR", quietly = TRUE)) {
  install.packages("genoPlotR")
}
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  install.packages("ggplot2")
}

library(genoPlotR)  # For synteny visualization with gene segments
library(grid)       # For advanced plotting with genoPlotR
library(ggplot2)    # For custom synteny plots using ggplot2

# PART 1: Synteny Visualization with genoPlotR

# Step 2: Create DNA Segments for Synteny Plot
dna_seg1 <- dna_seg(data.frame(
  name = c("Gene1", "Gene2", "Gene3", "Gene4"),
  start = c(100, 500, 1000, 1500),
  end = c(400, 800, 1200, 1800),
  strand = c(1, -1, 1, -1),
  col = "#440154FF"  # Purple for segment 1
))
dna_seg1$fill <- "#440154FF"  # Fill color for arrows

dna_seg2 <- dna_seg(data.frame(
  name = c("Gene1", "GeneX", "Gene3", "GeneY"),
  start = c(50, 600, 950, 1300),
  end = c(350, 900, 1150, 1600),
  strand = c(1, -1, 1, 1),
  col = "#21908DFF"  # Teal for segment 2
))
dna_seg2$fill <- "#21908DFF"  # Fill color for arrows

# Step 3: Create Comparison Links
comparison <- comparison(data.frame(
  start1 = c(100, 500, 1000),
  end1 = c(400, 800, 1200),
  start2 = c(50, 600, 950),
  end2 = c(350, 900, 1150),
  col = "#FDE725FF",  # Bright yellow for contrast
  lty = 2,            # Dashed lines for links
  lwd = 1.5           # Line thickness
))

# Step 4: Plot Synteny Map with genoPlotR
plot_gene_map(
  dna_segs = list(dna_seg1, dna_seg2),
  comparisons = list(comparison),
  scale = TRUE,
  scale_cex = 0.75,    # Adjust scale label size
  gene_type = "side_blocks",  # Use side blocks to highlight segments
  arrow_head_len = 8,  # Customize arrowhead size
  lwd = 2.5,           # Thicker segment borders
  seg_labels = c("Segment 1", "Segment 2"),  # Segment labels
  label_cex = 0.9,     # Label size
  label_font = 2,       # Bold font for labels
  title="Synteny Plot"
  )

# PART 2: Custom Synteny Visualization with ggplot2

# Step 5: Create Data for ggplot2
data <- data.frame(
  segment = c("Segment 1", "Segment 2", "Segment 3", "Segment 4"),
  start1 = c(100, 500, 1000, 1500),
  end1 = c(400, 800, 1200, 1800),
  start2 = c(50, 600, 950, 1300),
  end2 = c(350, 900, 1150, 1600)
)

# Step 6: Plot with ggplot2
ggplot(data) +
  geom_segment(aes(x = start1, xend = end1, y = 1, yend = 1), color = "#440154FF", size = 2) +
  geom_segment(aes(x = start2, xend = end2, y = 2, yend = 2), color = "#21908DFF", size = 2) +
  geom_segment(aes(x = (start1 + end1) / 2, xend = (start2 + end2) / 2, y = 1, yend = 2),
               color = "#FDE725FF", linetype = "dashed", size = 1) +
  scale_y_continuous(breaks = 1:2, labels = c("Chromosome 1", "Chromosome 2")) +
  labs(title = "Custom Synteny Plot", x = "Genomic Position", y = "Chromosomes") +
  theme_minimal()

