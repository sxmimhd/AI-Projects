import pandas as pd
import numpy as np

df = pd.read_csv("data/games_march2025_cleaned.csv")

print("=" * 50)
print("DATASET OVERVIEW")
print("=" * 50)

print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumn Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

duplicates = df.duplicated().sum()

print(f"\nDuplicate Rows: {duplicates}")

df = df.drop_duplicates()

df["release_date"] = pd.to_datetime(df["release_date"])
print(df["release_date"].dtype)

#Feature Engineering , We create new columns from existing ones.
df["release_year"] = df["release_date"].dt.year
df["release_month"] = df["release_date"].dt.month_name()
df["total_reviews"] = (
    df["positive"] +
    df["negative"]
)
df["review_ratio"] = (
    df["positive"] /
    df["total_reviews"]
)

missing = df.isnull().sum()

missing = missing[missing > 0]

print(missing.sort_values(ascending=False))

print(df.describe())

print(df["genres"].nunique())
print(df["developers"].nunique())
print(df["publishers"].nunique())
print(df["release_year"].unique())

df.to_csv(
    "data/games_processed.csv",
    index=False
)
print(df.head())