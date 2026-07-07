import pandas as pd

print("=" * 60)
print("NETFLIX RECOMMENDATION INTELLIGENCE")
print("=" * 60)

df = pd.read_csv("data/netflix_titles.csv")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nInfo:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nStatistics:")
print(df.describe(include="all"))

print("\nFirst 5 Rows:")
print(df.head())