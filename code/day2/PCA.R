#####################
# Principal Component Analysis (PCA)
#####################

# Load required libraries
library(ggforce)    # For advanced plot annotations like geom_mark_ellipse
library(tidyverse)  # For data manipulation and visualization
library(gtools)     # For mixedsort functionality
library(ltc)
#devtools::install_github("loukesio/ltc_palettes")


# Define a custom theme for consistent plot aesthetics
physalia_theme <- function() {
  theme_bw() +  # Start with a clean white background
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", family = "Georgia"),  # Centered bold title
      panel.grid.minor = element_blank()  # Remove minor grid lines for clarity
    )
}

# Load the dataset
data("five_disease")

# Preview the first few rows of the dataset
five_disease %>% head()

#------------------------------------
# Step 1: Prepare the data for PCA
#------------------------------------

# Reshape the data and handle missing values
pca_data <- five_disease %>%
  pivot_longer(cols = c(a, b, c), names_to = "rep", values_to = "expression") %>%
  group_by(disease) %>%
  mutate(expression = ifelse(is.na(expression), mean(expression, na.rm = TRUE), expression)) %>%  # Impute NA with column mean
  pivot_wider(names_from = c(disease, rep), values_from = expression) %>%
  drop_na()  # Ensure no missing values remain for PCA

# Preview the reshaped data
pca_data

#------------------------------------
# Step 2: Perform PCA
#------------------------------------

# Convert data to matrix format and remove the first column (gene identifiers)
pca_matrix <- as.data.frame(t(pca_data[,-1]))  # Transpose for PCA

# Perform PCA and scale data
pca_result <- prcomp(pca_matrix, scale. = TRUE)

#------------------------------------
# Step 3: Prepare PCA results for plotting
#------------------------------------

# Create a data frame from PCA results for PC1 and PC2
pca_df <- data.frame(Sample = rownames(pca_result$x), pca_result$x[,1:2]) %>%
  mutate(disease = str_extract(Sample, "^[^_]+"),  # Extract disease name from Sample
         replicate = str_extract(Sample, "[^_]+$"))  # Extract replicate identifier from Sample

#------------------------------------
# Step 4: Plot PCA results
#------------------------------------

# Load a custom palette from the `ltc` package
pal <- ltc("alger", "continuous", n = 6)

# Create a scatter plot of PCA results
ggplot(pca_df, aes(x = PC1, y = PC2, color = disease, label = replicate)) +
  geom_point(size = 4) +  # Add points for each sample
  geom_mark_ellipse(aes(fill = disease, label = disease)) +  # Add ellipses for each disease group
  scale_fill_manual(values = pal) +  # Apply custom fill colors
  scale_color_manual(values = pal) +  # Apply custom point colors
  labs(
    x = paste0("PC1 (", round(summary(pca_result)$importance[2,1] * 100, 1), "%)"),  # Label PC1 with variance explained
    y = paste0("PC2 (", round(summary(pca_result)$importance[2,2] * 100, 1), "%)"),  # Label PC2 with variance explained
    title = "PCA of Gene Expression by Disease and Replicate"  # Plot title
  ) +
  theme_minimal() +  # Apply minimal theme
  theme(legend.position = "right") +  # Position legend to the right
  physalia_theme()  # Apply custom theme for consistency

#------------------------------------
# Step 5: Analyze Variance Explained by Each Principal Component
#------------------------------------

# Calculate variance explained by each principal component
variance_explained <- pca_result$sdev^2 / sum(pca_result$sdev^2)
variance_explained_percent <- round(variance_explained * 100, 1)

# Create a data frame for variance explained
variance_df <- data.frame(
  PC = paste0("PC", 1:length(variance_explained_percent)),  # Create PC names
  Variance = variance_explained_percent  # Store variance percentages
)

# Ensure 'PC' is a factor and ordered using mixedsort
variance_df <- variance_df %>%
  mutate(PC = factor(PC, levels = mixedsort(PC)))

#------------------------------------
# Step 6: Plot Variance Explained by Each PC
#------------------------------------

# Create a bar plot of variance explained by each principal component
ggplot(variance_df, aes(x = PC, y = Variance)) +
  geom_bar(stat = "identity", fill = "#009E73") +  # Add bars with custom color
  labs(
    title = "Variance Explained by Each Principal Component",  # Plot title
    x = "Principal Component",  # X-axis label
    y = "Variance Explained (%)"  # Y-axis label
  ) +
  physalia_theme()  # Apply custom theme for consistency

