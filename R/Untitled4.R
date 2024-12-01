# Load necessary libraries
library(circlize)

# Load data
source_links <- read.delim("/Users/theodosiou/Desktop/ch7/out_links.bed", header = FALSE)
target_links <- read.delim("/Users/theodosiou/Desktop/ch7/in_links.bed", header = FALSE)

# Add a color column with different colors for each link
link_colors <- c("#f4ab5c", "#1f77b4")
source_links$color <- sample(link_colors, nrow(source_links), replace = TRUE)

# Initialize the circular plot
circos.genomicInitialize(df)

# Plot genomic links with varying colors
for (i in 1:nrow(source_links)) {
  circos.link(
    source_links[i, 1], source_links[i, 2:3],
    target_links[i, 1], target_links[i, 2:3],
    col = source_links$color[i]
  )
}

# Clear the plot after rendering
circos.clear()
