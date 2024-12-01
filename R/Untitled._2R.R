# Step 1: Load data from an online source
data = read.table("/Users/theodosiou/Desktop/heatmap_circus.txt")

# Step 2: Transform data into a matrix format
data.mat <- as.matrix(data[,-1])
data.mat

rownames(data.mat) <- data$Mol  # Set row names to the first column (Molecule names)
data.mat
t_data.mat <- t(data.mat)  # Transpose the matrix for plotting
t_data.mat
# Step 3: Create a dendrogram for clustering columns
dend_list = as.dendrogram(hclust(dist(t(t_data.mat))))  # Generate dendrogram for the transposed matrix

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






