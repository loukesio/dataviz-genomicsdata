############################
# Circular Genomic Visualization
############################

# Load necessary libraries for visualization
library(circlize)     # For circular genomic plots
library(grid)         # For custom plot layouts
library(cowplot)      # For combining multiple plots
library(ggplotify)    # For converting plots to ggplot2 objects for customization

#------------------------------------
# Step 1: Load chromosome data
#------------------------------------

# Read chromosome length information from a GFF file
df <- readr::read_tsv("/Users/theodosiou/Desktop/ch7/ara.gff", col_names = FALSE) %>%
  dplyr::select(X1, X4, X5)  # Select columns for chromosome name, start, and end positions

# Preview the chromosome data
df

#------------------------------------
# Step 2: Initialize circular plot and add a single link
#------------------------------------

# Initialize the circular plot with chromosome data
circos.genomicInitialize(df)

# Add a single link between regions in different chromosomes
circos.link("Chr4", c(9000000, 1200000), "Chr5", c(12000000, 15000000), col = "#d1422f")

# Clear the circular plot environment
circos.clear()

#------------------------------------
# Step 3: Draw multiple genomic links
#------------------------------------

# Load source and target link data from BED files
source_links <- read.delim("/Users/theodosiou/Desktop/ch7/arabidopsis_out_links.bed", header = FALSE)
target_links <- read.delim("/Users/theodosiou/Desktop/ch7/arabidopsis_in_links.bed", header = FALSE)

# Initialize the circular plot and add links
circos.genomicInitialize(df)
circos.genomicLink(source_links, target_links, col = "#f4ab5c")  # Draw links with specified color

#------------------------------------
# Step 4: Add a density track
#------------------------------------

# Load gene positions from a BED file
gene_positions <- read.delim("/Users/theodosiou/Desktop/ch7/arabidopsis_genes.bed", header = FALSE)

# Initialize the circular plot and add a density track
circos.genomicInitialize(df)
circos.genomicDensity(gene_positions, window.size = 1e6, col = "#3d5a80", track.height = 0.1)

#------------------------------------
# Step 5: Add a heatmap track
#------------------------------------

# Load heatmap data from a BED file
heatmap_data <- read.delim("/Users/theodosiou/Desktop/ch7/arabidopsis_quant_data.bed", header = FALSE)

# Create a color function for the heatmap
col_fun <- colorRamp2(c(10, 12, 15), c("#000000", "#03707E", "#66BCB0"))

# Initialize the circular plot and add a heatmap track
circos.genomicInitialize(df)
circos.genomicHeatmap(heatmap_data, col = col_fun, side = "outside", border = "white")

#------------------------------------
# Step 6: Combine tracks
#------------------------------------

# Clear and reinitialize the plot
circos.clear()
circos.genomicInitialize(df)

# Add combined tracks: heatmap, density, and links
circos.genomicHeatmap(heatmap_data, col = col_fun, side = "outside", border = "white")
circos.genomicDensity(gene_positions, window.size = 1e6, col = "#9B2226", track.height = 0.1)
circos.link("Chr4", c(9000000, 1200000), "Chr5", c(12000000, 15000000), col = "#E28900")
circos.genomicLink(source_links, target_links, col = "#E9D8A6")

#------------------------------------
# Step 7: Create a genome coverage plot
#------------------------------------

# Create example genome coverage data
set.seed(123)
chr1_data <- data.frame(
  chr = rep("chr1", 100),
  start = seq(1, 1000000, length.out = 100),
  end = seq(100000, 1100000, length.out = 100),
  coverage = runif(100, 0, 100)
)

chr2_data <- data.frame(
  chr = rep("chr2", 100),
  start = seq(1, 800000, length.out = 100),
  end = seq(80000, 880000, length.out = 100),
  coverage = runif(100, 0, 100)
)

chr3_data <- data.frame(
  chr = rep("chr3", 100),
  start = seq(1, 600000, length.out = 100),
  end = seq(60000, 660000, length.out = 100),
  coverage = runif(100, 0, 100)
)

# Combine genome data
genome_data <- rbind(chr1_data, chr2_data, chr3_data)

# Initialize circular layout
circos.clear()
circos.par("start.degree" = 90, "track.height" = 0.3, "gap.degree" = 4)
circos.initialize(
  factors = unique(genome_data$chr),
  xlim = matrix(
    c(
      0, max(chr1_data$end),
      0, max(chr2_data$end),
      0, max(chr3_data$end)
    ),
    ncol = 2,
    byrow = TRUE
  )
)

# Add base track with chromosome names
circos.track(
  ylim = c(0, 1),
  bg.border = NA,
  track.height = 0.05,
  panel.fun = function(x, y) {
    chr <- CELL_META$sector.index
    circos.text(CELL_META$xcenter, CELL_META$ycenter, chr, facing = "inside", niceFacing = TRUE)
  }
)

# Add coverage track
circos.track(
  factors = genome_data$chr,
  x = (genome_data$start + genome_data$end) / 2,
  y = genome_data$coverage,
  panel.fun = function(x, y) {
    circos.lines(x, y, col = "#FF000080")
    circos.polygon(
      c(x, rev(x)),
      c(rep(0, length(x)), rev(y)),
      col = "#FF000040",
      border = NA
    )
  }
)

# Add axis for genome coverage
circos.track(
  track.index = get.current.track.index(),
  panel.fun = function(x, y) {
    circos.axis(
      h = "top",
      major.at = seq(0, CELL_META$xlim[2], by = 2e5),
      labels.cex = 0.4,
      labels = paste0(seq(0, CELL_META$xlim[2] / 1e6, by = 0.2), "Mb")
    )
  }
)

# Add a title to the genome coverage plot
title("Genome Coverage Plot")

# Reset Circos plot environment
circos.clear()
