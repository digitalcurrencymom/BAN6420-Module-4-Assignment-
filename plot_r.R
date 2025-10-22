# plot_r.R
# This script reads the cleaned CSV and recreates the 'Top 10 Genres' plot using ggplot2
# It suppresses package startup messages and includes optional conflict resolution lines.

suppressPackageStartupMessages({
  library(ggplot2)
  library(readr)
  library(dplyr)
  library(tidyr)
})

# Optional: use the 'conflicted' package to explicitly prefer dplyr::filter etc.
# Uncomment and run once if you want explicit conflict preferences.
# if (!requireNamespace("conflicted", quietly = TRUE)) install.packages("conflicted")
# library(conflicted)
# conflicted::conflict_prefer("filter", "dplyr")

csv_path <- "C:/Users/HP/Downloads/Netflix_shows_movies/Netflix_shows_movies.csv"
if (!file.exists(csv_path)) {
  stop("Cleaned CSV not found at: ", csv_path)
}

df <- read_csv(csv_path)

# Split genres and count
genres <- df %>%
  mutate(listed_in = ifelse(is.na(listed_in), 'Unknown', listed_in)) %>%
  mutate(listed_in = strsplit(as.character(listed_in), ",")) %>%
  tidyr::unnest(listed_in) %>%
  mutate(listed_in = trimws(listed_in)) %>%
  count(listed_in, sort = TRUE)

top_genres <- genres %>% slice_max(n, n = 10)

p <- ggplot(top_genres, aes(x = reorder(listed_in, n), y = n)) +
  geom_col(fill = 'steelblue') +
  coord_flip() +
  labs(title = 'Top 10 Genres', x = '', y = 'Count') +
  theme_minimal()

out_path <- "C:/Users/HP/Downloads/Netflix_shows_movies/top_genres_r.png"
ggsave(filename = out_path, plot = p, width = 8, height = 6)

message("Saved R plot: ", out_path)
