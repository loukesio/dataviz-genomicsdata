getwd() #getting working directory

data("metadata") #load the metadata data

library(tidyverse)
library(MetBrewer)
library(showtext)

font_add(family = "my/path/Arial.ttf")

font_add_google(name="Merriweather", family = "Georgia")
showtext_auto() #automatically uses showtext fore rendering plots

physalia_theme <- function(){
  theme_bw() +
    theme(
      plot.title = element_text(hjust = 0.5, face = "bold", family = "Georgia"),
      panel.grid.minor = element_blank()
    )
}


metadata %>% glimpse()
pal=met.brewer("Isfahan1")
pal1 = c("#0E7175", "#FD7901", "#C35BCA")

metadata  %>%  glimpse()
metadata_summary <- metadata %>%
  count(sex)

metadata_summary

p1 <-
ggplot(data = metadata) +
  geom_bar(aes(x = sex, fill = sex)) +
  geom_text(data = metadata_summary, aes(x = sex, y = n, label = n), vjust = -0.5, size = 5) +
  scale_fill_manual(values = pal1) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +  # Add space to the y-axis
  labs(title = "Sex counts") +
  physalia_theme()

p1




ggplot(data=metadata) + #we are always using the + sign
  geom_bar(aes(x=sex, fill=sex)) +
  scale_fill_manual(values = pal1) +
  geom_text(aes(x = sex, label = ..count..), stat = "count", vjust = -0.5, size = 5) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.1))) +   # Adjusts y-axis with extra space
  labs(title="Sex counts") +
  theme_bw() +
  theme(plot.title = element_text(hjust=0.5, face = "bold", family = "Georgia"),
        panel.grid.minor = element_blank())



p2 <-  ggplot(metadata) +
  geom_histogram(aes(x = age), fill = "#109B37", binwidth = 2) +  # Histogram for 'age' column with a specific color
  labs(title = "Age Distribution") +                # Add a title
   theme_bw() +
   theme(plot.title = element_text(hjust=0.5, face = "bold", family = "Georgia"),
         panel.grid.minor = element_blank())

p2

p3 <- ggplot(metadata) +
  geom_bar(aes(x = lineage), fill = "#d1422f") +    # Bar plot for 'lineage' column with a specific color
  labs(title = "Lineage Distribution") +            # Add a title
  theme_bw() +
  theme(plot.title = element_text(hjust=0.5, face = "bold", family = "Georgia"),
        axis.text.x = element_text(angle = 90),
        panel.grid.minor = element_blank())
p3

p4 <- ggplot(metadata) +
  geom_bar(aes(x = primary_disease), fill = "#FD7901") +  # Bar plot for 'primary_disease' column
  labs(title = "Primary Disease") +                      # Add a title
  theme_bw() +
  theme(plot.title = element_text(hjust=0.5, face = "bold", family = "Georgia"),
        axis.text.x = element_text(angle = 90),
        panel.grid.minor = element_blank())

p4

#put plots together
library(patchwork)

p1  | p2
p1 / p2

(p1 | p2) / (p3 | p4)

library("DataExplorer")
create_report(metadta)


####

set.seed(42)  # For reproducibility

# Simulate 250 FASTQ file names
fastq_files <- paste0("sample_", sprintf("%03d", 1:250), ".fastq")

# Simulate the number of reads with a realistic range (e.g., between 10,000 to 1,000,000 reads)
number_of_reads <- sample(10000:1000000, 250, replace = TRUE)

# Create a data frame
fastq_data <- data.frame(
  fastq_file = fastq_files,
  num_reads = number_of_reads
)

# have a look at the data
fastq_data %>% glimpse()

fastq_data

fastq_data <- fastq_data %>%
  arrange(num_reads)


ggplot(fastq_data) +
  geom_col(aes(x=reorder(fastq_file, num_reads), y=num_reads), fill="skyblue") +
  physalia_theme() +
  labs(title="Bar Plot of fastq files by Numbers of Reads",
       x= "Fastq file",
       y="Number of Reads") +
  theme(axis.text.x = element_text(angle = 90))  +
  scale_x_discrete(breaks=fastq_data$fastq_file[seq(1, nrow(fastq_data), by=25)]) +
  coord_flip() +
  geom_hline(yintercept = 75000)


ggplot(fastq_data) +
  geom_histogram(aes(num_reads), fill="#d1422f", alpha=0.9, color="#333333") +
  labs(title="Distribution of reads",
       x= "Fastq file",
       y="Number of Reads") +
  physalia_theme() +
  geom_vline(xintercept = 200000, linetype="dashed", color="#333333")







