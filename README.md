[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Clones](https://img.shields.io/badge/Clones-View%20on%20GitHub-blue)](https://github.com/loukesio/dataviz-genomicsdata/graphs/traffic)
![Developmental Status](https://img.shields.io/badge/Status-Development-orange)
[![GitHub issues](https://img.shields.io/github/issues/loukesio/dataviz-genomicsdata)](https://github.com/loukesio/dataviz-genomicsdata/issues)
[![GitHub forks](https://img.shields.io/github/forks/loukesio/dataviz-genomicsdata?style=social)](https://github.com/loukesio/dataviz-genomicsdata/network/members)
[![GitHub stars](https://img.shields.io/github/stars/loukesio/dataviz-genomicsdata?style=social)](https://github.com/loukesio/dataviz-genomicsdata/stargazers)

## Instructions for Setting Up the LearnGenViz Package for the Course

 <img align="right" src="logo/github_physalia_dataviz_genomics.png" width=400>

Follow these steps to clone the course repository, set up the LearnGenViz package, and install all dependencies using renv:

### 1. Clone the Course Repository

Start by cloning the LearnGenViz course repository from GitHub to your local machine. Run this command in your terminal (or use a Git client):
```bash
# Clone the repository
git clone git@github.com:loukesio/dataviz-genomicsdata.git

# Navigate to the cloned repository
cd dataviz-genomicsdata
```
### 2. Open the Project in RStudio

- Open RStudio.

- Go to **File > Open Project** and select the `DataGenomics.Rproj` file in the `dataviz-genomicsdata` directory.

Note: <br>
This step activates the renv environment, which helps manage the project's dependencies.

### 3. Restore the Project Environment

Run the following command in the R console to install all the packages specified in the renv.lock file:
```
renv::restore()
```
Note: <br>
This command ensures that all required packages (and their correct versions) are installed automatically. This step may take some time, as it downloads and installs packages as specified in the renv.lock file.

### 4. Load the LearnGenViz Package

Once the environment has been restored, load the LearnGenViz package:
```
library(LearnGenViz)
```

### Additional Information
- Dependencies: renv will handle the installation of all CRAN, Bioconductor, and GitHub packages required for the course.
- Project-specific Libraries: The renv package will create a project-specific library, ensuring that your environment matches the course setup.

### Troubleshooting
If you encounter any issues:

- Ensure you have the latest version of R and RStudio installed.
- Verify that git is installed on your system for cloning the repository.
- Contact me at theodosiou@evolbio.mpg.de for assistance with any errors during the setup.

By following these steps, you'll have the LearnGenViz package and all required dependencies set up for the course.


## Heatmaps 

### 1. Understanding the Data
Before any analysis, it's crucial to understand the data. Use `skimr` to generate an overview of the dataset.

```r
# Install and load the package
devtools::install_github("loukesio/dataviz-genomicsdata")
library(LearnGenViz)
library(skimr)

# Load the dataset
data("five_disease")

# Overview of the dataset
five_disease %>% skim()
```

### 2. Creating Pairwise Scatter Plots
```
# Load GGally
library(GGally)

# Filter Alzheimer's data
alz <- five_disease %>% filter(disease == "Alzheimers")

# Select relevant columns
ggally_data <- alz %>% select(a, b, c)

# Create pairwise scatter plots
ggpairs(ggally_data, 
        title = "Pairwise Scatter Plots for Replicates a, b, c", 
        upper = list(continuous = "cor")) +
  theme_minimal()
```
### 3. Correlation Analysis with ggcorrplot

```
library(ggcorrplot)

# Select columns and calculate correlation matrix
cor_alz <- alz %>% select(a, b, c)
cor_matrix <- cor(cor_alz, use = "pairwise.complete.obs")

# Plot correlation matrix
ggcorrplot(cor_matrix, 
           method = "square", 
           type = "upper", 
           ggtheme = theme_minimal(),
           title = "Correlation Matrix for Alzheimer") +
  scale_fill_gradient2(low = "#BB4444", mid = "#FFFFFF", high = "#4477AA", midpoint = 0.5,
                       limits = c(0, 1)) +
  theme(legend.title = element_blank())

```
### R Heatmaps
```
library(MetBrewer)
pal <- met.brewer("Hokusai1", n = 256)

# Clean and scale data
df_clean <- cor_alz[complete.cases(cor_alz), ]
df_clean_scale <- scale(df_clean)

# Generate heatmap
heatmap(df_clean_scale, col = pal, main = "Correlation Heatmap")
```

### Interactive heatmaps
```
library(plotly)

# Convert to matrix
df_clean_scale <- as.matrix(df_clean_scale)

# Create an interactive heatmap
plot_ly(z = df_clean_scale, type = "heatmap") %>%
  layout(title = list(text = "Correlation Heatmap"),
         font = list(family = "Georgia", size = 12))
```

### Additional Heatmap Methods with heatmaply and Base R

```
# Install and load heatmaply
# https://www.datanovia.com/en/blog/how-to-create-a-beautiful-interactive-heatmap-in-r/
library("heatmaply")

# Basic interactive heatmap
heatmaply(df_clean)

# Static heatmap using ggheatmap
ggheatmap(df_clean)

# Static heatmap using gplots::heatmap.2
library(gplots)
gplots::heatmap.2(
  as.matrix(df_clean),
  trace = "none",
  col = viridis(100),
  key = FALSE
)

# Enhanced interactive heatmap with row dendrogram
heatmaply(
  as.matrix(df_clean),
  seriate = "mean", 
  row_dend_left = TRUE,
  plot_method = "plotly"
)
```

