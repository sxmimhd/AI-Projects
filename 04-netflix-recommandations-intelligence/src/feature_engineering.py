import pandas as pd
import numpy as np

df = pd.read_csv("data/processed_data.csv")

# CONTENT AGE
CURRENT_YEAR = 2025

df["content_age"] = CURRENT_YEAR - df["release_year"]

# YEARS AVAILABLE ON NETFLIX

df["year_added"] = pd.to_datetime(df["date_added"]).dt.year
df["years_on_netflix"] = CURRENT_YEAR - df["year_added"]

# NUMBER OF GENRES

df["genre_count"] = (
    df["listed_in"]
    .str.split(",")
    .apply(len)
)

# NUMBER OF COUNTRIES

df["country_count"] = (
    df["country"]
    .str.split(",")
    .apply(len)
)

# NUMBER OF CAST MEMBERS

df["cast_count"] = (
    df["cast"]
    .str.split(",")
    .apply(len)
)

# DURATION

df["duration_value"] = (
    df["duration"]
    .str.extract(r"(\d+)")
    .astype(int)
)

# MOVIE / TV SEASONS

df["duration_minutes"] = np.where(
    df["type"] == "Movie",
    df["duration_value"],
    np.nan
)

df["season_count"] = np.where(
    df["type"] == "TV Show",
    df["duration_value"],
    np.nan
)

# DURATION CATEGORY

movie_mask = df["type"] == "Movie"

df.loc[
    movie_mask & (df["duration_minutes"] < 60),
    "duration_category"
] = "Short"

df.loc[
    movie_mask &
    (df["duration_minutes"] >= 60) &
    (df["duration_minutes"] <= 120),
    "duration_category"
] = "Medium"

df.loc[
    movie_mask &
    (df["duration_minutes"] > 120),
    "duration_category"
] = "Long"

df.loc[
    df["type"] == "TV Show",
    "duration_category"
] = "Series"

# SIMPLE POPULARITY SCORE

df["popularity_score"] = (
    df["genre_count"] * 2 +
    df["country_count"] * 2 +
    df["cast_count"] +
    (2025 - df["release_year"]) * (-0.1)
)



df.to_csv(
    "data/processed_data.csv",
    index=False
)

print("\nNew Columns Created:\n")

new_cols = [
    "content_age",
    "years_on_netflix",
    "genre_count",
    "country_count",
    "cast_count",
    "duration_value",
    "duration_minutes",
    "season_count",
    "duration_category",
    "popularity_score"
]

for col in new_cols:
    print("✓", col)

print("\nDataset Shape:")
print(df.shape)

print("\nPreview:")
print(df[new_cols].head())