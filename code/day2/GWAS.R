# Load the showtext package to enable the use of custom fonts in plots
library(showtext)

# Add a Google font (e.g., "Merriweather") and refer to it as "Georgia" for usage in the custom theme
font_add_google(name = "Merriweather", family = "Georgia")

# Enable automatic rendering of fonts in plots using the showtext package
showtext_auto()

# Define a custom theme function for ggplot2 to enhance plot aesthetics
custom_theme <- function(base_size = 16, title_size_rel = 2.25, subtitle_size_rel = 1.25,
                         axis_title_size_rel = 1.5, axis_text_size_rel = 1.5, strip_text_size_rel = 1.25) {
  # Use the theme_bw base theme with a specified font family ("Georgia")
  theme_bw(base_size = base_size, base_family = "Georgia") +
    theme(
      # Customize the title: center-align and set relative size
      plot.title = element_text(hjust = 0.5, size = rel(title_size_rel)),
      # Customize the subtitle: center-align and set relative size
      plot.subtitle = element_text(hjust = 0.5, size = rel(subtitle_size_rel)),
      # Customize the x-axis title: set size and add a top margin
      axis.title.x = element_text(size = rel(axis_title_size_rel), margin = margin(t = 12.5)),
      # Customize the y-axis title: set size and add a right margin
      axis.title.y = element_text(size = rel(axis_title_size_rel), margin = margin(r = 12.5)),
      # Customize the x-axis text: set size
      axis.text.x = element_text(size = rel(axis_text_size_rel)),
      # Customize the y-axis text: set size
      axis.text.y = element_text(size = rel(axis_text_size_rel)),
      # Customize facet strip text size
      strip.text = element_text(size = rel(strip_text_size_rel)),
      # Add margins around the plot
      plot.margin = unit(c(1, 1, 1, 2), "cm"),
      # Remove major grid lines on the x-axis
      panel.grid.major.x = element_blank(),
      # Remove minor grid lines
      panel.grid.minor = element_blank(),
      # Remove background from facet strips
      strip.background = element_blank()
    )
}

# Load essential libraries for data manipulation and plotting
library(ggplot2)
library(dplyr)

# Set parameters for data generation
set.seed(123)  # Ensure reproducibility of random data
num_snps <- 1000  # Total number of simulated SNPs
num_qtls <- 5     # Number of significant QTLs to highlight

# Generate random data for SNPs
eQTL_data <- data.frame(
  pos = sample(40250000:42000000, num_snps, replace = TRUE),  # Random genomic positions on chromosome 3
  chr = rep("chr3", num_snps),  # Assign chromosome label for all SNPs
  pvalue = runif(num_snps, 0.01, 1),  # Generate random p-values between 0.01 and 1
  snps = paste0("chr3_", sample(40250000:42000000, num_snps, replace = TRUE))  # Create unique SNP identifiers
)

# Identify significant QTLs by randomly selecting indices and assigning very low p-values
qtls <- sample(1:num_snps, num_qtls)  # Randomly select indices for QTLs
eQTL_data$pvalue[qtls] <- runif(num_qtls, 1e-10, 1e-6)  # Assign extremely low p-values for these QTLs
eQTL_data$is_qtl <- ifelse(1:num_snps %in% qtls, "QTL", "Non-QTL")  # Label SNPs as "QTL" or "Non-QTL"

# Add a -log10 transformation of p-values for better visualization in the plot
eQTL_data <- eQTL_data %>%
  mutate(log_pvalue = -log10(pvalue))  # Transform p-values to a -log10 scale

# Load ggplot2 extension for better label positioning
library(ggrepel)

# Create the scatter plot
ggplot(eQTL_data, aes(x = pos, y = log_pvalue, color = is_qtl)) +  # Map genomic position and transformed p-value
  geom_point(size = 2, alpha = 0.7) +  # Add points with slight transparency for better visualization
  geom_text_repel(
    data = subset(eQTL_data, is_qtl == "QTL"),  # Only label significant QTLs
    aes(label = snps), color = "#d1422f", size = 3  # Label QTLs with SNP identifiers in red
  ) +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "#009E73") +  # Add a horizontal line at the p=0.05 threshold
  scale_color_manual(values = c("Non-QTL" = "black", "QTL" = "#d1422f")) +  # Define custom colors for QTLs and Non-QTLs
  labs(
    title = "eQTL SNP Connectivity with Highlighted QTLs",  # Add a plot title
    x = "Genomic Position (chr3)",  # Label the x-axis
    y = expression(-log[10](p-value)),  # Label the y-axis with mathematical notation
    color = "SNP Type"  # Legend title for the color scale
  ) +
  custom_theme()  # Apply the custom theme for enhanced aesthetics

