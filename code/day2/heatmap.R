
# Load the dataset included in LearnGenViz
data("five_disease")

# Glimpse the dataset to understand its structure and contents
five_disease %>% glimpse()

install.packages("skimr")
library(skimr)
skim(five_disease)

# Filter the data to focus on Alzheimer's disease only
alz <- five_disease %>%
  filter(disease == "Alzheimers")

# Preview the first few rows of the filtered dataset
alz %>% head()

# Load the necessary library for creating correlation plots
library(ggcorrplot)

# Select numeric columns (a, b, c) for correlation analysis
cor_alz <- alz %>% select(a, b, c)

# Preview the selected columns
cor_alz %>% head()

# Create a correlation matrix with pairwise complete observations
cor_matrix <- cor(cor_alz, use = "pairwise.complete.obs")

# Display the correlation matrix in the console
cor_matrix

# Generate a correlation plot using ggcorrplot
ggcorrplot(cor_matrix,
           method = "square",             # Square style for correlation cells
           type = "upper",                # Display only the upper triangle
           lab_col = "white",             # Label color for values
           ggtheme = theme_minimal(),     # Minimal theme for clarity
           title = "Correlation Matrix for Alzheimer") +
  scale_fill_gradientn(colors = colorRampPalette(rev(c("#BB4444", "#EE9988", "#FFFFFF", "#77AADD", "#4477AA")))(200)) +
  theme(legend.title = element_blank())  # Remove legend title for simplicity

# Simplified version of the correlation plot with gradient colors
ggcorrplot(cor_matrix,
           method = "square",
           type = "upper",
           lab_col = "white",
           ggtheme = theme_minimal(),
           title = "Correlation Matrix for Alzheimer") +
  scale_fill_gradient2(low = "#BB4444", mid = "#FFFFFF", high = "#4477AA", midpoint = 0.5,
                       limits = c(0, 1), space = "Lab", na.value = "grey50") +
  theme(legend.title = element_blank(),
        panel.grid.major = element_blank())

# Heatmap generation using base R's heatmap function
library(MetBrewer)

# Define a color palette for the heatmap
pal <- met.brewer("Hokusai1", n = 256)

# Clean the dataset by removing rows with missing values
df_clean <- cor_alz[complete.cases(cor_alz), ]

# Standardize the data (mean = 0, standard deviation = 1)
df_clean_scale <- scale(df_clean)

# Generate a basic heatmap using the standardized data
heatmap(df_clean_scale, col = pal, main = "Correlation Heatmap of Alzheimer's Data",
        xlab = "Variables", ylab = "Observations")

# Alternative heatmap with viridis color scheme
library(viridis)
heatmap(df_clean_scale, col = viridis(256, option = "C"),
        main = "Correlation Heatmap of Alzheimer's Data",
        xlab = "Variables", ylab = "Observations")

# Heatmap with RColorBrewer palette
library(RColorBrewer)
pal <- colorRampPalette(brewer.pal(11, "RdBu"))(256)
heatmap(df_clean_scale, col = pal,
        main = "Correlation Heatmap of Alzheimer's Data",
        xlab = "Variables", ylab = "Observations")

# Interactive heatmap using plotly
library(plotly)

# Convert the scaled data frame to a matrix for use in plotly
df_clean_scale <- as.matrix(df_clean_scale)

# Create an interactive heatmap with plotly
plot_ly(
  z = df_clean_scale,
  type = "heatmap"
) %>%
  layout(
    title = list(text = "Correlation Heatmap"),
    font = list(family = "Georgia", size = 12)
  )

# Scatter plot using ggplot2
library(ggplot2)
library(ggpubr)

# Create a scatter plot with a linear regression line and correlation coefficient
p1 <- ggplot(alz, aes(x = a, y = b)) +
  geom_point(alpha = 0.6, color = "#333333", size = 4, shape = 16) +  # Scatter points
  geom_smooth(method = "lm", color = "blue", se = FALSE) +            # Linear regression line
  stat_cor(method = "pearson", label.x = 1, label.y = 4.2) +          # Add correlation coefficient
  theme_minimal() +                                                   # Minimal theme for clarity
  labs(title = "Scatter Plot", x = "rep a", y = "rep b")              # Add titles and axis labels

# Make the scatter plot interactive using plotly
library(plotly)
ggplotly(p1)

# Pairwise scatter plots using GGally
library(GGally)

# Select relevant columns for pairwise scatter plots
ggally_data <- alz %>% select(a, b, c)

# Create pairwise scatter plots with correlation coefficients
ggpairs(ggally_data,
        title = "Pairwise Scatter Plots for Replicates a, b, c",
        upper = list(continuous = "cor")) +
  theme_minimal() +                      # Apply a minimal theme for clarity
  theme(strip.background = element_blank())  # Remove strip backgrounds for a cleaner look
