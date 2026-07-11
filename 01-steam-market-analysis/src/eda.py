import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("data/games_processed.csv")

#how many games released everyyear with visualization
games_per_year = (
    df.groupby("release_year")
      .size()
      .sort_index()
)

print(games_per_year)

plt.figure(figsize=(12,6))

games_per_year.plot(kind="line")

plt.title("Steam Game Releases Per Year")

plt.xlabel("Year")

plt.ylabel("Number of Games")

plt.grid(True)

plt.show()

#most common genres
print(df["genres"].value_counts().head(20))
#price distribution
plt.figure(figsize=(10,6))

plt.hist(df["price"], bins=40)

plt.title("Game Price Distribution")

plt.xlabel("Price")

plt.ylabel("Games")

plt.show()

#most expensive games
print(
    df[
        ["name","price"]
    ]
    .sort_values(
        "price",
        ascending=False
    )
    .head(20)
)
#high rated games , must >1000
top_games = df[
    df["total_reviews"] > 1000
]
top_games = top_games.sort_values(
    "pct_pos_total",
    ascending=False
)

print(
    top_games[
        [
            "name",
            "pct_pos_total",
            "total_reviews"
        ]
    ].head(20)
)

# price vs review
plt.figure(figsize=(10,6))

plt.scatter(
    df["price"],
    df["pct_pos_total"],
    alpha=0.3
)

plt.xlabel("Price")

plt.ylabel("Positive Review %")

plt.title("Price vs Review Score")

plt.show()

# monthly releases
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly = (
    df["release_month"]
      .value_counts()
      .reindex(months)
)

monthly.plot(kind="bar")
plt.show()

#correlation matrix 
numeric = df.select_dtypes(include="number")

corr = numeric.corr()

plt.figure(figsize=(12,10))

plt.imshow(corr)

plt.xticks(
    range(len(corr.columns)),
    corr.columns,
    rotation=90
)

plt.yticks(
    range(len(corr.columns)),
    corr.columns
)

plt.colorbar()

plt.show()

#interactive bonus:
fig = px.scatter(
    df,

    x="price",

    y="pct_pos_total",

    color="release_year",

    hover_name="name"
)

fig.show()