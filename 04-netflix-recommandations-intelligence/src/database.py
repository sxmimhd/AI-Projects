import sqlite3
import pandas as pd

df = pd.read_csv("data/processed_data.csv")

# CREATE DATABASE
connection = sqlite3.connect("data/analytics.db")

# EXPORT DATAFRAME TO SQL

df.to_sql(
    "netflix_titles",
    connection,
    if_exists="replace",
    index=False
)

print("Database created successfully!")

# VERIFY TABLE

cursor = connection.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM netflix_titles
""")

print("Rows inserted:", cursor.fetchone()[0])

cursor.execute("""
PRAGMA table_info(netflix_titles)
""")

print("\nColumns:\n")

for column in cursor.fetchall():
    print(column)

connection.close()

print("\nDone!")