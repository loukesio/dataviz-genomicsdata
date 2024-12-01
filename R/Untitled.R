# Step 1: Load required libraries for creating circular genomic plots and additional customizations
library(circlize)     # Core library for circular plots in R
library(tidyverse)


df <- readr::read_tsv("/Users/theodosiou/Desktop/ch7/ara.gff", col_names = FALSE) %>%
  dplyr::select(X1, X4, X5)  # Select columns for chromosome name, start, and end positions

df

# Step 3: Inixtialize circular plot and add a single link
circos.genomicInitialize(df)

circos.link("Chr4", c(9000000,1200000), "Chr5", c(12000000, 15000000), col="#d1422f")

#clear plot
circos.clear()

# interactions
source_links <- read.delim("/Users/theodosiou/Desktop/ch7/out_links.bed", header = FALSE)
source_links

target_links <- read.delim("/Users/theodosiou/Desktop/ch7/in_links.bed", header = FALSE)
target_links

circos.genomicInitialize(df)
circos.genomicLink(source_links, target_links, col=c("#f4ab5c", "red"))

circos.clear()

# gene density
gene_positions <- read.delim("/Users/theodosiou/Desktop/ch7/ara_genes.bed", header = FALSE)
gene_positions %>%  head()

circos.genomicInitialize(df)
circos.genomicDensity(gene_positions, col="#3d5a80")

circos.clear()

#heatmap

heatmap_data <- read.delim("/Users/theodosiou/Desktop/ch7/quant_data.bed", header = FALSE)
heatmap_data %>%  head()

#we need to define a color function
col_fun = colorRamp2(c(10, 12, 15), c("#000000", "#03707E", "#66BCB0"))

circos.genomicInitialize(df)
circos.genomicHeatmap(heatmap_data, col=col_fun, connection_height = NULL)

circos.clear()

circos.genomicInitialize(df)
circos.genomicHeatmap(heatmap_data, col=col_fun, connection_height = NULL)
circos.genomicDensity(gene_positions, col="#3d5a80")
circos.genomicLink(source_links, target_links, col=c("#f4ab5c", "red"))

title("This my first Circus plot")

####################################
# circus plot 2
######################################

Step 1: Load data from an online source
dataURL <- "https://pastebin.com/raw/whLr21ZA"
expData.df <- read.table(dataURL, header = TRUE, sep = "\t", stringsAsFactors = FALSE)

# Step 2: Transform data into a matrix format
expData.mat <- as.matrix(expData.df[-c(1)])  # Exclude the first column and convert to matrix
rownames(expData.mat) <- expData.df$Mol  # Set row names to the first column (Molecule names)
useT.mat <- t(expData.mat)  # Transpose the matrix for plotting

# Step 3: Create a dendrogram for clustering columns
dend_list = as.dendrogram(hclust(dist(t(useT.mat))))  # Generate dendrogram for the transposed matrix

# Step 4: Define color function for the heatmap
col_fun = colorRamp2(
  breaks = c(-13.288, -5.265, -6.674, -2.544, 4.694, 5.000),
  colors = c("blue4", "lightblue", "yellow", "orange", "orangered", "red")
)  # Map data values to colors

# Step 5: Initialize Circos plot parameters
circos.par("start.degree" = 90, cell.padding = c(0, 0, 0, 0), gap.degree = 15)  # Set plot start degree and cell padding
circos.initialize("a", xlim = c(0, 292))  # Initialize the plot with one sector

# Step 6: Add track for column labels
circos.track(
  ylim = c(0, 1), bg.border = NA, track.height = 0.05,
  panel.fun = function(x, y) {
    for (i in seq_len(ncol(useT.mat))) {
      circos.text(
        i - 0.5, 0, colnames(useT.mat)[order.dendrogram(dend_list)][i],
        adj = c(0, 0.5), facing = "clockwise", niceFacing = TRUE, cex = 0.5
      )  # Add column labels arranged clockwise
    }
  }
)

# Step 7: Draw the main circular heatmap
circos.track(
  ylim = c(0, 2), bg.border = NA, panel.fun = function(x, y) {
    m = mat_list
    dend = dend_list
    m2 = m[, order.dendrogram(dend)]  # Order columns based on dendrogram
    col_mat = col_fun(m2)  # Apply color function to matrix
    nr = nrow(m2)  # Number of rows
    nc = ncol(m2)  # Number of columns
    for (i in 1:nr) {
      circos.rect(
        1:nc - 1, rep(nr - i, nc),
        1:nc, rep(nr - i + 1, nc),
        border = col_mat[i, ], col = col_mat[i, ]
      )  # Draw rectangles for each heatmap cell
    }
    # Add row labels facing downward
    circos.text(rep(1, 2), 1:2, rownames(useT.mat), facing = "downward", adj = c(1.45, 1.1), cex = 0.7)
  }
)

# Step 8: Add dendrogram track
max_height = attr(dend_list, "height")  # Get maximum height of the dendrogram
circos.track(
  ylim = c(0, max_height), bg.border = NA, track.height = 0.3,
  panel.fun = function(x, y) {
    dend = dend_list
    circos.dendrogram(dend, max_height = max_height)  # Draw the dendrogram
  }
)

# Step 9: Clear Circos plot after completion
circos.clear()  # Reset the Circos environment

# Step 10: Add a legend for the heatmap values
# Install and load the ComplexHeatmap package if not already installed
BiocManager::install("ComplexHeatmap")
library(ComplexHeatmap)

# Create and draw the legend
lgd_links = Legend(
  at = c(-15, -5, 0, 5), col_fun = col_fun,
  title_position = "topleft", title = "Value", direction = "horizontal"
)
draw(
  lgd_links, x = unit(1, "npc") - unit(2, "mm"), y = unit(4, "mm"),
  just = c("right", "bottom")
)  # Draw the legend at the specified position



#keep in here the ggfortify as a trick

# Load necessary libraries
library(circlize)
library(ggplotify)
library(cowplot)

# Customize Circos parameters to show the circular plot with axis labels and remove ticks
circos.par("start.degree" = 90, cell.padding = c(0, 0, 0, 0), gap.degree = 15)

# Initialize the circular plot and show only the axis labels (no tick marks)
circos.genomicInitialize(df, plotType = "labels")  # Only shows chromosome labels, no ticks

# Add a single link between two regions in different chromosomes
circos.link("Chr4", c(9000000, 1200000), "Chr5", c(12000000, 15000000), col = "#d1422f")

# Record the current chord diagram and save it as `p`
p <- recordPlot()

# Convert the recorded chord diagram to a ggplot object and customize it
as.ggplot(ggdraw(p)) +
  labs(title = "what do we see") +
  theme(
    text = element_text(family = "Georgia"),
    plot.title = element_text(hjust = 0.5, face = "bold", size = 18),
    plot.subtitle = element_text(hjust = 0.5, size = 12, margin = margin(t = 10)),
    plot.caption = element_text(size = 10, hjust = 0.95, margin = margin(b = 12)),
    plot.margin = margin(t = 20)  # Sets the top margin to 20 units
  )

# Clear the plot for reinitialization
circos.clear()



