import pandas as pd

df = pd.read_csv("data/vgsales.csv")

# Missing Values
df["Year_of_Release"] = df["Year_of_Release"].fillna(
    df["Year_of_Release"].median()
)

df["Publisher"] = df["Publisher"].fillna("Unknown")

df["Developer"] = df["Developer"].fillna("Unknown")

df["Rating"] = df["Rating"].fillna("Unrated")

df["Critic_Score"] = df["Critic_Score"].fillna(0)

df["User_Score"] = df["User_Score"].replace("tbd", None)
df["User_Score"] = pd.to_numeric(df["User_Score"], errors="coerce")
df["User_Score"] = df["User_Score"].fillna(0)


df["Year_of_Release"] = df["Year_of_Release"].astype(int)


# New Features
df["Decade"] = (df["Year_of_Release"] // 10) * 10

df["Release_Date"] = pd.to_datetime(
    df["Year_of_Release"].astype(str),
    format="%Y"
)

df["Sales_per_Critic"] = (
    df["Global_Sales"] /
    (df["Critic_Count"] + 1)
)

df["Sales_per_User"] = (
    df["Global_Sales"] /
    (df["User_Count"] + 1)
)

# Save
df.to_csv(
    "data/video_games_processed.csv",
    index=False
)

print(df.head())