five_disease

library(tidyverse)
library(showtext)

# Add a Google font, e.g., "Merriweather", and refer to it as "Georgia" for usage
font_add_google(name = "Merriweather", family = "Georgia")

# Enable showtext for rendering fonts automatically in plots
showtext_auto()


physalia_theme <- function(){
  theme_bw() +
    theme(plot.title = element_text(hjust = 0.5, face="bold", family="Georgia"),
          panel.grid.minor = element_blank())
}

five_disease %>%
  glimpse()

head(five_disease)
#prcomp
my_data <- five_disease %>% distinct(disease)


my_data <- five_disease %>%
  filter(disease=="Alzheimers" | disease=="control")

# create pca_data
pca_data <-
five_disease %>%
  pivot_longer(cols = c(a,b,c), names_to="rep", values_to="expression") %>%
  group_by(disease) %>%
  mutate(expression = ifelse(is.na(expression), mean(expression, na.rm = TRUE), expression)) %>%    # Impute NA with column mean
  ungroup() %>%
  pivot_wider(names_from = c(disease,rep), values_from = expression) %>%
  drop_na()

pca_data

# convert data into a matrix

pca_matrix <- as.data.frame(t(pca_data[,-1]))
pca_result <-  prcomp(pca_matrix)

pca_df <- data.frame(Sample=rownames(pca_result$x), pca_result$x[,1:2]) %>%
mutate(disease=str_extract(Sample, "^[^_]+"),
       replicate=str_extract(Sample, "[^_]+$"))


pca_df %>% head()

library(ggforce)

pal=met.brewer(name = "Hokusai1", n=6)
pal

summary(pca_result)$importance[2,1]
summary(pca_result)$importance[2,2]
summary(pca_result)$importance[2,3]


ggplot(pca_df, aes(PC1, PC2, color = disease)) +
  geom_point(size = 4) +
  geom_text(aes(label = replicate), vjust = -0.5, size = 3, show.legend = FALSE) +  # Add replicate labels without affecting the legend
  geom_mark_ellipse(aes(fill = disease, label = disease)) +
  scale_color_manual(values = pal) +
  scale_fill_manual(values = pal) +
  physalia_theme() +
  labs(
    title = "PCA of Gene Expression by Disease",
    x = paste0("PC1 (", round(summary(pca_result)$importance[2, 1] * 100, 1), "%)"),
    y = paste0("PC2 (", round(summary(pca_result)$importance[2, 2] * 100, 1), "%)")
  )


variance_explained <- pca_result$sdev^2 / sum(pca_result$sdev^2)
variance_explained_percent <- round(variance_explained*100,1)
variance_explained_percent

variance_df <- data.frame(
  PC = paste0("PC", 1:length(variance_explained_percent)),
  Variance = variance_explained_percent
)


library(gtools)

# Ensure 'PC' is a factor and ordered using mixedsort
variance_df <- variance_df %>%
  mutate(PC = factor(PC, levels = mixedsort(PC)))

# Plot the histogram with the correctly ordered PCs

vplot <- ggplot(variance_df, aes(x = PC, y = Variance)) +
  geom_bar(stat = "identity", fill = "#009E73") +
  labs(
    title = "Variance Explained by Each Principal Component",
    x = "Principal Component",
    y = "Variance Explained (%)"
  ) +
  physalia_theme()

ggplotly(vplot)

loadings <- pca_result$rotation %>%
  as_tibble()

loadings %>%
  dplyr::mutate(genes=rownames(pca_result$rotation)) %>%
  relocate(genes) %>%
  mutate(genes=str_replace(genes, "V", "")) %>%
  arrange(abs(PC1))





