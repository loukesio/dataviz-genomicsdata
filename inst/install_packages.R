# Create a vector of all required CRAN packages
cran_packages <- c(
  "ape", "beepr", "bipartite", "cowplot", "dplyr", "ggcorrplot",
  "GGally", "ggiraph", "ggplot2", "ggplotify", "gghighlight", "ggforce",
  "ggraph", "ggpubr", "ggrepel", "gplots", "grid", "gt", "gtools", "gtsummary",
  "here", "MetBrewer", "nlme", "patchwork", "pheatmap", "plotly",
  "RColorBrewer", "scales", "showtext", "tidygraph", "tidyverse", "vegan", "xlsx",
  "Rtsne", "uwot","devtools"
)

# Create a vector of required Bioconductor packages
bioc_packages <- c(
  "BiocManager", "AnnotationHub", "circlize", "karyoploteR", "msa", "seqinr",
  "DECIPHER", "DESeq2"
)

# Function to install missing CRAN packages
for (pkg in cran_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    message(paste("Installing", pkg, "from CRAN..."))
    install.packages(pkg)
  } else {
    message(paste(pkg, "is already installed."))
  }
}

# Install BiocManager if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  install.packages("BiocManager")
}

# Function to install missing Bioconductor packages
for (pkg in bioc_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    message(paste("Installing", pkg, "from Bioconductor..."))
    BiocManager::install(pkg)
  } else {
    message(paste(pkg, "is already installed."))
  }
}

message("All required packages are installed.")
