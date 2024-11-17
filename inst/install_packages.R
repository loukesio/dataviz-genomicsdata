# Create a vector of all required CRAN packages
cran_packages <- c(
  "ape", "beepr", "bipartite", "cowplot", "dplyr",
  "ggcorrplot", "GGally", "ggiraph", "ggplot2", "ggplotify", "gghighlight",
  "ggforce", "ggraph", "ggpubr", "ggrepel", "gplots", "grid", "gt",
  "gtools", "gtsummary", "here", "MetBrewer", "nlme", "patchwork", "pheatmap",
  "plotly", "RColorBrewer", "scales", "showtext", "tidygraph", "tidyverse",
  "vegan", "xlsx", "Rtsne", "uwot", "devtools"
)

# Create a vector of required Bioconductor packages
bioc_packages <- c(
  "BiocManager", "AnnotationHub", "circlize", "karyoploteR", "msa", "seqinr",
  "DECIPHER","Biostrings", "DESeq2"
)

# Install missing CRAN packages with verbose output
for (pkg in cran_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    message(paste("Installing", pkg, "from CRAN..."))
    install.packages(pkg, verbose = TRUE)  # Verbose installation
  } else {
    message(paste(pkg, "is already installed."))
  }
}

# Install BiocManager if not already installed
if (!requireNamespace("BiocManager", quietly = TRUE)) {
  message("Installing BiocManager from CRAN...")
  install.packages("BiocManager", verbose = TRUE)
}

# Install missing Bioconductor packages with verbose output
for (pkg in bioc_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    message(paste("Installing", pkg, "from Bioconductor..."))
    BiocManager::install(pkg, verbose = TRUE)  # Verbose installation
  } else {
    message(paste(pkg, "is already installed."))
  }
}

# Install GitHub packages with verbose output
github_packages <- c("loukesio/ggvolc", "loukesio/ltc_palettes", "loukesio/dataviz-genomicsdata")

for (pkg in github_packages) {
  package_name <- sub(".*/", "", pkg)
  if (!requireNamespace(package_name, quietly = TRUE)) {
    message(paste("Installing", package_name, "from GitHub..."))
    devtools::install_github(pkg, verbose = TRUE)  # Verbose installation
  } else {
    message(paste(package_name, "is already installed."))
  }
}

message("All required packages are installed.")
