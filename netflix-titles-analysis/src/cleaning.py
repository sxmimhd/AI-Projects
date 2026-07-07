import pandas as pd

df = pd.read_csv("data/netflix_titles.csv")

print("=" * 60)
print("DATA CLEANING")
print("=" * 60)

# HANDLE MISSING VALUES


df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")

df = df.dropna(subset=["date_added", "duration"])

# CONVERT DATE

# Remove leading/trailing spaces
df["date_added"] = df["date_added"].str.strip()

# Convert to datetime
df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)

# Remove rows that still couldn't be converted
df = df.dropna(subset=["date_added"])

# DATE FEATURES

df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month_name()
df["day_added"] = df["date_added"].dt.day_name()

# CLEAN TEXT

df["title"] = df["title"].str.strip()
df["country"] = df["country"].str.strip()
df["director"] = df["director"].str.strip()

# SAVE

df.to_csv(
    "data/processed_data.csv",
    index=False
)

print("\nCleaning completed.")

print("\nNew Shape:")
print(df.shape)

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nProcessed dataset saved.")