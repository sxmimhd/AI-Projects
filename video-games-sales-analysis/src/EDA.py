import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

os.makedirs("images", exist_ok=True)

df = pd.read_csv("data/video_games_processed.csv")

# Dataset Overview
print("=" * 70)
print("VIDEO GAME INDUSTRY EDA")
print("=" * 70)

print("\nShape:")
print(df.shape)

print("\nStatistics:")
print(df.describe())

# Top Selling Games
top_games = (
    df.nlargest(10, "Global_Sales")
)

fig = px.bar(
    top_games,
    x="Global_Sales",
    y="Name",
    orientation="h",
    color="Platform",
    title="Top 10 Best-Selling Games"
)
fig.write_image("images/top_selling_games.png", scale=2)
fig.show()

# Platform Sales
platform_sales = (
    df.groupby("Platform")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

fig = px.bar(
    platform_sales.head(15),
    x="Platform",
    y="Global_Sales",
    color="Global_Sales",
    title="Top Platforms by Global Sales"
)
fig.write_image("images/platform_sales.png", scale=2)
fig.show()

#  Genre Sales
genre_sales = (
    df.groupby("Genre")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .reset_index()
)

fig = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    color="Global_Sales",
    title="Global Sales by Genre"
)
fig.write_image("images/genre_sales.png", scale=2)
fig.show()

# Publisher Sales

publisher_sales = (
    df.groupby("Publisher")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(15)
      .reset_index()
)

fig = px.bar(
    publisher_sales,
    x="Publisher",
    y="Global_Sales",
    color="Global_Sales",
    title="Top Publishers"
)
fig.write_image("images/publisher_sales.png", scale=2)
fig.show()

#  Regional Sales
regional = pd.DataFrame({

    "Region": [
        "North America",
        "Europe",
        "Japan",
        "Other"
    ],

    "Sales": [

        df["NA_Sales"].sum(),
        df["EU_Sales"].sum(),
        df["JP_Sales"].sum(),
        df["Other_Sales"].sum()

    ]

})

fig = px.pie(
    regional,
    names="Region",
    values="Sales",
    hole=0.45,
    title="Regional Market Share"
)
fig.write_image("images/regional_sales.png", scale=2)
fig.show()

#  Sales Distribution
fig = px.histogram(
    df,
    x="Global_Sales",
    nbins=60,
    title="Distribution of Global Sales"
)
fig.write_image("images/sales_distribution.png", scale=2)
fig.show()

# Critic Score vs Sales
fig = px.scatter(
    df,
    x="Critic_Score",
    y="Global_Sales",
    color="Genre",
    hover_name="Name",
    title="Critic Score vs Global Sales"
)
fig.write_image("images/critic_score_vs_sales.png", scale=2)
fig.show()

# User Score vs Sales
fig = px.scatter(
    df,
    x="User_Score",
    y="Global_Sales",
    color="Platform",
    hover_name="Name",
    title="User Score vs Global Sales"
)
fig.write_image("images/user_score_vs_sales.png", scale=2)
fig.show()

# Decade Comparison
decade_sales = (
    df.groupby("Decade")["Global_Sales"]
      .sum()
      .reset_index()
)

fig = px.bar(
    decade_sales,
    x="Decade",
    y="Global_Sales",
    color="Global_Sales",
    title="Global Sales by Decade"
)
fig.write_image("images/decade_sales.png", scale=2)
fig.show()