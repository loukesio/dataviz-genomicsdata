library(MetBrewer)
library(RColorBrewer)

# Set seed for reproducibility
set.seed(42)

# Create column and row names
columns <- c("Sample", paste0("OTU", 1:11))
samples <- paste0("Day", 1:12)

# Generate random float data for OTU columns (12 rows, 11 columns)
data <- matrix(runif(12 * 11, min = 0, max = 100), nrow = 12, ncol = 11)

# Create a data frame
simulated_df <- data.frame(Sample = samples, data)
names(simulated_df) <- columns

# Print the data frame
print(simulated_df)

simulated_df

simulated_long_df <- simulated_df %>%
  pivot_longer(cols = -Sample, names_to = "OTU", values_to = "Value") %>%
  group_by(Sample) %>%
  mutate(Percentage = Value / sum(Value) * 100) %>%
  ungroup()

# Set 'Sample' as a factor with levels in the order of appearance
simulated_long_df <- simulated_long_df %>%
  mutate(OTU = factor(OTU, levels = unique(OTU)))

simulated_long_df_2 <- simulated_long_df %>%
  mutate(OTU = factor(OTU, levels = mixedsort(unique(OTU))))

# Generate a palette with 11 colors from RColorBrewer
color_palette <- brewer.pal(11, "Spectral") # You can change "Spectral" to another palette name
color_palette <- met.brewer("Cross",11)

simulated_long_df
# Create the plot with the custom colors
ggplot(simulated_long_df, aes(x = Sample, y = Percentage, fill = OTU)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Stacked Bar Plot of OTUs by Sample",
       x = "Sample",
       y = "Percentage (%)",
       fill = "OTU") +
  scale_fill_manual(values = color_palette) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Create the plot with the custom colors
ggplot(simulated_long_df_2, aes(x = Sample, y = Percentage, fill = OTU)) +
  geom_bar(stat = "identity") +
  theme_minimal() +
  labs(title = "Stacked Bar Plot of OTUs by Sample",
       x = "Sample",
       y = "Percentage (%)",
       fill = "OTU") +
  scale_fill_manual(values = color_palette) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#----------------------

# stacked geom area

#-----------------------


# Ensure data is sorted by Sample and OTU
simulated_long_df <- simulated_long_df %>%
  arrange(Sample, OTU)

# Create the stacked area plot
ggplot(simulated_long_df, aes(x = Sample, y = Percentage, fill = OTU, group = OTU)) +
  geom_area(position = "stack") +
  theme_minimal() +
  labs(title = "Stacked Area Plot of OTUs by Sample",
       x = "Sample",
       y = "Percentage (%)",
       fill = "OTU") +
  scale_fill_manual(values = color_palette) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  physalia_theme() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))




library(tidyverse)
library(MetBrewer)
library(RColorBrewer)

# Custom function to create a stacked bar plot with user-specified or default color palette
create_stacked_bar_plot <- function(data, palette_name = NULL, custom_palette = NULL) {
  # Ensure the data is in long format and calculate percentages
  long_data <- data %>%
    pivot_longer(cols = -Sample, names_to = "OTU", values_to = "Value") %>%
    group_by(Sample) %>%
    mutate(Percentage = Value / sum(Value) * 100) %>%
    ungroup() %>%
    mutate(Sample = factor(Sample, levels = unique(Sample)))

  # Determine the number of unique OTUs
  n_otus <- length(unique(long_data$OTU))

  # Select the color palette
  if (!is.null(custom_palette)) {
    # Use the custom color palette provided by the user
    if (length(custom_palette) >= n_otus) {
      color_palette <- custom_palette[1:n_otus]  # Use only as many colors as needed
    } else {
      stop("Custom palette does not have enough colors for the number of OTUs.")
    }
  } else if (!is.null(palette_name) && palette_name %in% names(MetBrewer::MetPalettes)) {
    # Use a MetBrewer palette if specified and valid
    color_palette <- MetBrewer::met.brewer(palette_name, n_otus)
  } else {
    # Default to an RColorBrewer palette if no valid MetBrewer palette or custom palette is specified
    color_palette <- brewer.pal(min(n_otus, 12), "Set3")
  }

  # Create the plot
  ggplot(long_data, aes(x = Sample, y = Percentage, fill = OTU)) +
    geom_bar(stat = "identity") +
    theme_minimal() +
    labs(title = "Stacked Bar Plot of OTUs by Sample",
         x = "Sample",
         y = "Percentage (%)",
         fill = "OTU") +
    scale_fill_manual(values = color_palette) +
    custom_theme() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# Example usage with a custom color palette
custom_palette <- c("#FF5733", "#33FF57", "#3357FF", "#F1C40F", "#8E44AD", "#2ECC71", "#E74C3C", "#3498DB", "#1ABC9C", "#9B59B6", "#34495E")

# Run the function using the custom palette
create_stacked_bar_plot(simulated_df, palette_name = "Cross")
