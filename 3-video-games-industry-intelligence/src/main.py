import pandas as pd

df = pd.read_csv("data/vgsales.csv")

print("="*60)
print("VIDEO GAME SALES DATASET")
print("="*60)

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

print("\nFirst 5 Rows:")
print(df.head())