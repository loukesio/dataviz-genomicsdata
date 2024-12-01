# Load the ts_data dataset provided by a package or as a built-in dataset
data("ts_data")

# Split the 'day.snp.frequency' column into separate components
ts_data_new <- str_split_fixed(ts_data$day.snp.frequency, ' ', 4)  # Split the string by spaces into 4 parts

# Convert the resulting matrix into a data frame and rename columns
ts_data <- ts_data_new %>%
  as.data.frame() %>%  # Convert matrix to data frame for further manipulation
  dplyr::rename(day = V2, snp = V3, frequency = V4) %>%  # Rename columns for clarity (assuming the columns are V2, V3, V4)
  select(-V1) %>%  # Remove the first column (not needed after splitting)
  as_tibble()  # Convert to tibble for a cleaner display and easier manipulation

# Explanation for Students:
# - `data("ts_data")`: Loads the `ts_data` dataset.
# - `str_split_fixed()`: Splits strings into a fixed number of pieces (in this case, 4 parts).
# - `as.data.frame()`: Converts a matrix to a data frame.
# - `dplyr::rename()`: Renames columns to more meaningful names (e.g., 'day', 'snp', 'frequency').
# - `select(-V1)`: Drops the first column which was created during the splitting and is not needed.
# - `as_tibble()`: Converts the data frame to a tibble for better data handling and readability in R.

# Install gghighlight package if not already installed
if (!requireNamespace("gghighlight", quietly = TRUE)) {
  install.packages("gghighlight")  # Install if missing
}

# Install gtools package if not already installed
if (!requireNamespace("gtools", quietly = TRUE)) {
  install.packages("gtools")  # Install if missing
}

# Load necessary libraries
library(gghighlight)  # For highlighting specific lines in ggplot
library(ggplot2)      # For creating plots
library(dplyr)        # For data manipulation
library(gtools)       # For mixed sorting of character vectors
library(MetBrewer)    # For creating aesthetically pleasing color palettes


# Create a custom color palette using MetBrewer
snp_pal <- met.brewer("Hokusai1", n = 20)  # Generate a color palette with 20 colors


# Preview the dataset structure (optional for understanding data)
glimpse(ts_data)

# Reorder the 'snp' column using mixed sorting of unique values
ts_data <- ts_data %>%
  mutate(snp = factor(snp, levels = mixedsort(unique(snp))))  # Reorder 'snp' column for plotting

# Optionally reorder the 'snp' column with a custom order for plotting
ts_data <- ts_data %>%
  mutate(snp = factor(snp, levels = c("SNP1", "SNP2", "SNP3", "SNP4", "SNP5",
                                      "SNP6", "SNP7", "SNP8", "SNP9", "SNP10",
                                      "SNP11", "SNP12", "SNP13", "SNP14", "SNP15",
                                      "SNP16", "SNP17", "SNP18", "SNP19", "SNP20")))

ts_data$frequency <- as.numeric(ts_data$frequency)
ts_data$day <- as.numeric(ts_data$day)

# Plot 1: Basic plot of SNP frequencies over time with facets
ggplot(ts_data, aes(x = day, y = frequency, color = snp, group = snp)) +
  geom_line() +  # Add lines representing SNP frequencies
  labs(
    title = "Simulated SNP Frequencies Over 20 Days",  # Add title to the plot
    x = "Day",  # Label for x-axis
    y = "Frequency (%)"  # Label for y-axis
  ) +
  theme_minimal() +  # Apply a minimal theme for a clean look
  facet_wrap(~snp)  # Create separate panels for each SNP

# Plot 2: Highlight specific SNPs with custom color and direct labeling
ggplot(ts_data, aes(x = day, y = frequency, color = snp, group = snp)) +
  geom_line() +  # Plot lines for all SNPs
  scale_color_manual(values = c("SNP19" = "#D1422F", "SNP20" = "#1A5b5b")) +  # Custom color for highlighted SNPs
  labs(
    title = "Simulated SNP Frequencies Over 20 Days",  # Title for the plot
    x = "Day",  # X-axis label
    y = "Frequency (%)"  # Y-axis label
  ) +
  gghighlight(
    snp %in% c("SNP20", "SNP19"),  # Highlight SNP20 and SNP19
    use_direct_label = TRUE,  # Directly label highlighted lines
    unhighlighted_params = list(color = "gray80", alpha = 0.25)  # Customize non-highlighted lines appearance
  ) +
  theme_minimal()  # Ensure the minimal theme is applied for consistency

# Plot 3: Custom line sizes for highlighted and non-highlighted SNPs
ggplot(ts_data, aes(x = day, y = frequency, group = snp)) +
  geom_line(data = subset(ts_data, snp %in% c("SNP19", "SNP20")),
            aes(color = snp), size = 1.5) +  # Highlighted SNPs with larger line size
  geom_line(data = subset(ts_data, !snp %in% c("SNP19", "SNP20")),
            aes(color = snp), size = 0.5, color = "gray80", alpha = 0.25) +  # Smaller lines for non-highlighted SNPs
  scale_color_manual(values = c("SNP19" = "#D1422F", "SNP20" = "#1A5b5b")) +  # Apply custom colors to highlighted SNPs
  labs(
    title = "Simulated SNP Frequencies Over 20 Days",  # Add plot title
    x = "Day",  # X-axis label
    y = "Frequency (%)"  # Y-axis label
  ) +
  theme_minimal()  # Maintain a consistent theme across all plots
