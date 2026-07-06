import pandas as pd
import plotly.express as px
import os

os.makedirs("images", exist_ok=True)
df = pd.read_csv("data/video_games_processed.csv")

# YEARLY SALES
yearly_sales = (
    df.groupby("Year_of_Release")["Global_Sales"]
      .sum()
      .reset_index()
      .sort_values("Year_of_Release")
)

# GLOBAL SALES OVER TIME

fig = px.line(
    yearly_sales,
    x="Year_of_Release",
    y="Global_Sales",
    markers=True,
    title="Global Video Game Sales Over Time"
)
fig.write_image("images/global_sales_overtime.png", scale=2)
fig.show()

# 5-YEAR MOVING AVERAGE

yearly_sales["Moving_Average"] = (
    yearly_sales["Global_Sales"]
    .rolling(window=5)
    .mean()
)

fig = px.line(
    yearly_sales,
    x="Year_of_Release",
    y=["Global_Sales", "Moving_Average"],
    title="5-Year Moving Average of Global Sales"
)
fig.write_image("images/5_years_avg.png", scale=2)
fig.show()

# YEAR-OVER-YEAR GROWTH

yearly_sales["YoY_Growth"] = (
    yearly_sales["Global_Sales"]
    .pct_change() * 100
)

fig = px.bar(
    yearly_sales,
    x="Year_of_Release",
    y="YoY_Growth",
    color="YoY_Growth",
    title="Year-over-Year Growth (%)"
)
fig.write_image("images/yoy.png", scale=2)
fig.show()

#  PLATFORM TRENDS

platform_trend = (
    df.groupby(["Year_of_Release", "Platform"])["Global_Sales"]
      .sum()
      .reset_index()
)

top_platforms = (
    df.groupby("Platform")["Global_Sales"]
      .sum()
      .nlargest(8)
      .index
)

platform_trend = platform_trend[
    platform_trend["Platform"].isin(top_platforms)
]

fig = px.line(
    platform_trend,
    x="Year_of_Release",
    y="Global_Sales",
    color="Platform",
    title="Platform Sales Trends"
)
fig.write_image("images/platform_trends.png", scale=2)
fig.show()

#  GENRE TRENDS

genre_trend = (
    df.groupby(["Year_of_Release", "Genre"])["Global_Sales"]
      .sum()
      .reset_index()
)

fig = px.line(
    genre_trend,
    x="Year_of_Release",
    y="Global_Sales",
    color="Genre",
    title="Genre Evolution Over Time"
)
fig.write_image("images/genre_trends.png", scale=2)
fig.show()

#  REGIONAL TRENDS
regional = (
    df.groupby("Year_of_Release")[
        ["NA_Sales",
         "EU_Sales",
         "JP_Sales",
         "Other_Sales"]
    ]
    .sum()
    .reset_index()
)

regional = regional.melt(
    id_vars="Year_of_Release",
    var_name="Region",
    value_name="Sales"
)

fig = px.line(
    regional,
    x="Year_of_Release",
    y="Sales",
    color="Region",
    title="Regional Sales Trends"
)
fig.write_image("images/regional_trends.png", scale=2)
fig.show()