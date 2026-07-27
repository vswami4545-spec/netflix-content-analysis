"""
Netflix Content Analytics
--------------------------
A beginner-friendly but complete data analysis project on the Netflix
Movies & TV Shows dataset, using pandas, numpy, and matplotlib.

What this script does:
1. Loads the raw dataset
2. Cleans it (handles missing values, fixes data types)
3. Engineers a few new columns (year_added, movie duration in minutes)
4. Answers 6 real analytical questions with numbers + charts
5. Saves every chart as a PNG into the /output folder

Run it with:
    python analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------
# 0. SETUP
# ---------------------------------------------------------------
DATA_PATH = "data/netflix_titles.csv"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)   # creates the output folder if it doesn't exist yet

# ---------------------------------------------------------------
# 1. LOAD THE DATA
# ---------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

print("Raw shape (rows, columns):", df.shape)
print("\nColumn data types:\n", df.dtypes)
print("\nMissing values per column:\n", df.isnull().sum())

# ---------------------------------------------------------------
# 2. CLEAN THE DATA
# ---------------------------------------------------------------

# 2a. Fill missing categorical text fields with a clear placeholder
#     instead of dropping rows -- we don't want to lose real titles
#     just because e.g. 'director' is unknown.
for col in ["director", "cast", "country"]:
    df[col] = df[col].fillna("Unknown")

# 2b. A handful of rows have no date_added or no rating.
#     Those rows are few (10 and 7 respectively) and not useful for
#     time-based analysis, so we drop just those rows.
df = df.dropna(subset=["date_added", "rating"])

# 2c. Convert date_added from text ("August 14, 2020") into a real
#     pandas datetime object, so we can extract the year easily.
df["date_added"] = pd.to_datetime(df["date_added"].str.strip())
df["year_added"] = df["date_added"].dt.year

# 2d. 'country' can contain multiple countries separated by commas,
#     e.g. "United States, France". For counting purposes we only
#     want the FIRST/primary country of production.
df["primary_country"] = df["country"].apply(lambda x: x.split(",")[0].strip())

# 2e. 'duration' is text and means different things for Movies vs
#     TV Shows: "90 min" for movies, "3 Seasons" for TV shows.
#     We split this into a numeric value + separate the two cases.
df["duration_value"] = df["duration"].str.extract(r"(\d+)").astype(float)
df["duration_unit"] = df["duration"].apply(
    lambda x: "min" if "min" in x else "Season(s)"
)

print("\nCleaned shape (rows, columns):", df.shape)

# ---------------------------------------------------------------
# 3. ANALYSIS + CHARTS
# ---------------------------------------------------------------

# ---- Q1: How many Movies vs TV Shows are there? ----
type_counts = df["type"].value_counts()
print("\n--- Movies vs TV Shows ---")
print(type_counts)

plt.figure(figsize=(6, 4))
plt.bar(type_counts.index, type_counts.values, color=["#E50914", "#221f1f"])
plt.title("Movies vs TV Shows on Netflix")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_movies_vs_tvshows.png")
plt.close()

# ---- Q2: How has content added to Netflix grown over the years? ----
content_by_year = df.groupby("year_added").size()
print("\n--- Content Added Per Year (last 6 years) ---")
print(content_by_year.tail(6))

plt.figure(figsize=(8, 4))
plt.plot(content_by_year.index, content_by_year.values, marker="o", color="#E50914")
plt.title("Netflix Content Added Per Year")
plt.xlabel("Year Added")
plt.ylabel("Number of Titles Added")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_content_growth_by_year.png")
plt.close()

# ---- Q3: Which countries produce the most content? (Top 10) ----
top_countries = (
    df[df["primary_country"] != "Unknown"]["primary_country"]
    .value_counts()
    .head(10)
)
print("\n--- Top 10 Countries by Content Count ---")
print(top_countries)

plt.figure(figsize=(8, 5))
plt.barh(top_countries.index[::-1], top_countries.values[::-1], color="#221f1f")
plt.title("Top 10 Countries by Netflix Content Count")
plt.xlabel("Number of Titles")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_top_countries.png")
plt.close()

# ---- Q4: What are the most common genres? (Top 10) ----
# 'listed_in' holds comma-separated genres per title, e.g.
# "Dramas, International Movies". We need to split and count each
# genre individually across ALL rows -- this uses a common pandas
# pattern: split into lists, then "explode" one genre per row.
all_genres = df["listed_in"].str.split(", ").explode()
top_genres = all_genres.value_counts().head(10)
print("\n--- Top 10 Genres ---")
print(top_genres)

plt.figure(figsize=(8, 5))
plt.barh(top_genres.index[::-1], top_genres.values[::-1], color="#B81D24")
plt.title("Top 10 Netflix Genres")
plt.xlabel("Number of Titles")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_top_genres.png")
plt.close()

# ---- Q5: What's the distribution of content ratings (age certification)? ----
rating_counts = df["rating"].value_counts().head(10)
print("\n--- Top Content Ratings ---")
print(rating_counts)

plt.figure(figsize=(8, 4))
plt.bar(rating_counts.index, rating_counts.values, color="#E50914")
plt.title("Netflix Content Ratings Distribution")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_rating_distribution.png")
plt.close()

# ---- Q6: How long are Movies, typically? (numpy stats + histogram) ----
movie_durations = df.loc[df["duration_unit"] == "min", "duration_value"].dropna()

# numpy is used here for the actual statistical calculations
mean_duration = np.mean(movie_durations)
median_duration = np.median(movie_durations)
std_duration = np.std(movie_durations)

print("\n--- Movie Duration Stats (minutes) ---")
print(f"Mean:   {mean_duration:.1f}")
print(f"Median: {median_duration:.1f}")
print(f"Std Dev:{std_duration:.1f}")

plt.figure(figsize=(8, 5))
plt.hist(movie_durations, bins=30, color="#221f1f", edgecolor="white")
plt.axvline(mean_duration, color="#E50914", linestyle="--", label=f"Mean = {mean_duration:.0f} min")
plt.title("Distribution of Movie Durations")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Movies")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_movie_duration_distribution.png")
plt.close()

# ---------------------------------------------------------------
# 4. SUMMARY
# ---------------------------------------------------------------
print("\n================ SUMMARY OF INSIGHTS ================")
print(f"1. Movies make up {type_counts['Movie'] / len(df) * 100:.1f}% of the catalog, "
      f"TV Shows make up {type_counts['TV Show'] / len(df) * 100:.1f}%.")
print(f"2. Content additions peaked in {content_by_year.idxmax()} "
      f"with {content_by_year.max()} titles added.")
print(f"3. The country producing the most content is {top_countries.index[0]} "
      f"with {top_countries.iloc[0]} titles.")
print(f"4. The most common genre is '{top_genres.index[0]}' "
      f"with {top_genres.iloc[0]} titles.")
print(f"5. The average movie runs about {mean_duration:.0f} minutes.")
print(f"\nAll charts saved to the '{OUTPUT_DIR}/' folder.")
