import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Paths
DATA_CSV = r"C:\Users\HP\Downloads\netflix_data (1).csv"
OUT_DIR = r"C:\Users\HP\Downloads\Netflix_shows_movies"
CLEANED_CSV = os.path.join(OUT_DIR, "Netflix_shows_movies.csv")
PLOT1 = os.path.join(OUT_DIR, "most_watched_genres.png")
PLOT2 = os.path.join(OUT_DIR, "ratings_distribution.png")
ZIP_PATH = os.path.join(OUT_DIR, "Netflix_shows_movies.zip")

os.makedirs(OUT_DIR, exist_ok=True)

def parse_duration(d):
    """Return (minutes, seasons) tuple parsed from duration string."""
    if pd.isna(d):
        return (pd.NA, pd.NA)
    s = str(d).strip()
    # minutes
    m = re.search(r"(\d+)\s*min", s)
    if m:
        return (int(m.group(1)), pd.NA)
    # seasons like '1 Season' or '2 Seasons'
    s2 = re.search(r"(\d+)\s*Season", s, flags=re.I)
    if s2:
        return (pd.NA, int(s2.group(1)))
    return (pd.NA, pd.NA)

print("Reading CSV...", DATA_CSV)
df = pd.read_csv(DATA_CSV)
print("Initial shape:", df.shape)

# Trim whitespace in string columns
for c in df.select_dtypes(include=['object']).columns:
    df[c] = df[c].astype(str).str.strip()

# Fill common text columns with 'Unknown' where missing
text_cols = ['director', 'cast', 'country', 'date_added', 'rating', 'duration', 'listed_in', 'description']
for c in text_cols:
    if c in df.columns:
        df[c] = df[c].replace({'nan': pd.NA})
        df[c] = df[c].fillna('Unknown')

# Convert release_year
if 'release_year' in df.columns:
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce').astype('Int64')

# Parse date_added to datetime
if 'date_added' in df.columns:
    df['date_added_parsed'] = pd.to_datetime(df['date_added'], errors='coerce')

# Parse duration into minutes and seasons
if 'duration' in df.columns:
    parsed = df['duration'].apply(parse_duration)
    df['duration_minutes'] = parsed.apply(lambda x: x[0])
    df['num_seasons'] = parsed.apply(lambda x: x[1])

# Remove exact duplicate rows
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]
print(f"Dropped {before - after} duplicate rows")

# Save cleaned CSV
df.to_csv(CLEANED_CSV, index=False)
print("Saved cleaned CSV:", CLEANED_CSV)

# Data exploration (brief)
print(df.describe(include='all'))

# Visualization 1: Most frequent genres
if 'listed_in' in df.columns:
    genres = df['listed_in'].str.split(',').explode().str.strip()
    top_genres = genres.value_counts().nlargest(10)

    plt.figure(figsize=(10,6))
    sns.barplot(x=top_genres.values, y=top_genres.index, palette='viridis')
    plt.title('Top 10 Genres')
    plt.xlabel('Count')
    plt.tight_layout()
    plt.savefig(PLOT1)
    plt.close()
    print("Saved plot:", PLOT1)

# Visualization 2: Ratings distribution
if 'rating' in df.columns:
    plt.figure(figsize=(8,6))
    sns.countplot(y='rating', data=df, order=df['rating'].value_counts().index, palette='magma')
    plt.title('Ratings Distribution')
    plt.tight_layout()
    plt.savefig(PLOT2)
    plt.close()
    print("Saved plot:", PLOT2)

# Zip the project folder, include R plot if present
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(CLEANED_CSV, arcname=os.path.basename(CLEANED_CSV))
    if os.path.exists(PLOT1):
        z.write(PLOT1, arcname=os.path.basename(PLOT1))
    if os.path.exists(PLOT2):
        z.write(PLOT2, arcname=os.path.basename(PLOT2))
    # include original CSV for reference
    if os.path.exists(DATA_CSV):
        z.write(DATA_CSV, arcname=os.path.basename(DATA_CSV))
    # include R plot if available
    r_plot = os.path.join(OUT_DIR, 'top_genres_r.png')
    if os.path.exists(r_plot):
        z.write(r_plot, arcname=os.path.basename(r_plot))

print("Created ZIP:", ZIP_PATH)
