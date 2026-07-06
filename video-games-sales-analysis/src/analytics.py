import pandas as pd

df = pd.read_csv("data/video_games_processed.csv")

# YEARLY SALES

yearly = (
    df.groupby("Year_of_Release")["Global_Sales"]
      .sum()
      .sort_index()
)

# CAGR

start = yearly.iloc[0]
end = yearly.iloc[-1]
years = len(yearly) - 1

cagr = ((end / start) ** (1 / years) - 1) * 100

print("=" * 50)
print("BUSINESS ANALYTICS")
print("=" * 50)

print(f"CAGR : {cagr:.2f}%")

# BEST YEAR
best_year = yearly.idxmax()

print(f"Best Year : {best_year}")

print(f"Sales : {yearly.max():.2f} Million")

# MARKET SHARE

market_share = (
    df.groupby("Platform")["Global_Sales"]
      .sum()
)

market_share = (
    market_share /
    market_share.sum()
) * 100

print("\nTop Platforms")

print(
    market_share
    .sort_values(ascending=False)
    .head(10)
)

# TOP PUBLISHERS
publisher = (
    df.groupby("Publisher")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop Publishers")

print(
    publisher.head(10)
)

# TOP GENRES
genre = (
    df.groupby("Genre")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop Genres")

print(
    genre
)

# BEST SELLING GAME
best_game = (
    df.nlargest(1, "Global_Sales")
)

print("\nBest Selling Game")

print(
    best_game[
        [
            "Name",
            "Platform",
            "Publisher",
            "Global_Sales"
        ]
    ]
)