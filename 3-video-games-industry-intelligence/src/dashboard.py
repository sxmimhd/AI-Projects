import pandas as pd
import plotly.graph_objects as go

from plotly.subplots import make_subplots

df = pd.read_csv("data/video_games_processed.csv")

total_sales = df["Global_Sales"].sum()

best_platform = (
    df.groupby("Platform")["Global_Sales"]
      .sum()
      .idxmax()
)

best_genre = (
    df.groupby("Genre")["Global_Sales"]
      .sum()
      .idxmax()
)

best_publisher = (
    df.groupby("Publisher")["Global_Sales"]
      .sum()
      .idxmax()
)

best_year = (
    df.groupby("Year_of_Release")["Global_Sales"]
      .sum()
      .idxmax()
)

average_sales = df["Global_Sales"].mean()

best_game = (
    df.loc[
        df["Global_Sales"].idxmax(),
        "Name"
    ]
)

games_count = len(df)

# YEARLY SALES
yearly_sales = (
    df.groupby("Year_of_Release")["Global_Sales"]
      .sum()
      .reset_index()
      .sort_values("Year_of_Release")
)

yearly_sales["Moving_Average"] = (
    yearly_sales["Global_Sales"]
    .rolling(5)
    .mean()
)

yearly_sales["YoY"] = (
    yearly_sales["Global_Sales"]
    .pct_change() * 100
)

# SUBPLOTS
fig = make_subplots(

    rows=4,
    cols=3,

    subplot_titles=(

        "📈 Global Sales Over Time",
        "📊 5-Year Moving Average",
        "📉 YoY Growth (%)",

        "🎮 Top Platforms",
        "🏆 Top Publishers",
        "🕹 Genre Market Share",

        "🌍 Regional Sales",
        "📅 Sales by Decade",
        "⭐ Critic Score vs Sales",

        "👑 Top Selling Games",
        "🎯 Platform Market Share",
        "📦 Global Sales Distribution"

    ),

    specs=[

        [{"type":"scatter"},
         {"type":"scatter"},
         {"type":"bar"}],

        [{"type":"bar"},
         {"type":"bar"},
         {"type":"pie"}],

        [{"type":"bar"},
         {"type":"bar"},
         {"type":"scatter"}],

        [{"type":"bar"},
         {"type":"pie"},
         {"type":"histogram"}]

    ],

    vertical_spacing=0.08,
    horizontal_spacing=0.08

)

# KPI CARDS
cards = [

    f"<b>Total Sales</b><br>{total_sales:,.0f} M",

    f"<b>Best Platform</b><br>{best_platform}",

    f"<b>Best Genre</b><br>{best_genre}",

    f"<b>Best Publisher</b><br>{best_publisher}",

    f"<b>Best Year</b><br>{best_year}",

    f"<b>Average Sales</b><br>{average_sales:.2f} M",

    f"<b>Top Game</b><br>{best_game}",

    f"<b>Total Games</b><br>{games_count:,}"

]

x_positions = [
    0.05,
    0.18,
    0.31,
    0.44,
    0.57,
    0.70,
    0.83,
    0.95
]

for x, text in zip(x_positions, cards):

    fig.add_annotation(

        x=x,
        y=1.16,

        xref="paper",
        yref="paper",

        showarrow=False,

        text=text,

        bgcolor="#1f2937",

        bordercolor="#60a5fa",

        borderwidth=2,

        font=dict(
            size=12,
            color="white"
        )

    )

# 1. GLOBAL SALES OVER TIME
fig.add_trace(

    go.Scatter(

        x=yearly_sales["Year_of_Release"],
        y=yearly_sales["Global_Sales"],

        mode="lines+markers",

        name="Sales",

        hovertemplate=
        "<b>%{x}</b><br>"
        "Sales: %{y:.2f} M<extra></extra>"

    ),

    row=1,
    col=1

)

# 2. MOVING AVERAGE
fig.add_trace(

    go.Scatter(

        x=yearly_sales["Year_of_Release"],
        y=yearly_sales["Moving_Average"],

        mode="lines",

        name="Moving Average",

        hovertemplate=
        "<b>%{x}</b><br>"
        "5-Year Average: %{y:.2f} M<extra></extra>"

    ),

    row=1,
    col=2

)

# 3. YEAR OVER YEAR GROWTH

fig.add_trace(

    go.Bar(

        x=yearly_sales["Year_of_Release"],
        y=yearly_sales["YoY"],

        name="YoY",

        hovertemplate=
        "<b>%{x}</b><br>"
        "Growth: %{y:.2f}%<extra></extra>"

    ),

    row=1,
    col=3

)


# 4. TOP PLATFORMS
platform_sales = (

    df.groupby("Platform")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .sort_values()

)

fig.add_trace(

    go.Bar(

        x=platform_sales.values,
        y=platform_sales.index,

        orientation="h",

        hovertemplate=
        "<b>%{y}</b><br>"
        "Sales: %{x:.2f} M<extra></extra>"

    ),

    row=2,
    col=1

)

# 5. TOP PUBLISHERS

publisher_sales = (

    df.groupby("Publisher")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .sort_values()

)

fig.add_trace(

    go.Bar(

        x=publisher_sales.values,
        y=publisher_sales.index,

        orientation="h",

        hovertemplate=
        "<b>%{y}</b><br>"
        "Sales: %{x:.2f} M<extra></extra>"

    ),

    row=2,
    col=2

)

# 6. GENRE MARKET SHARE
genre_sales = (

    df.groupby("Genre")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)

)

fig.add_trace(

    go.Pie(

        labels=genre_sales.index,
        values=genre_sales.values,

        hole=0.45,

        showlegend=False,

        hovertemplate=
        "<b>%{label}</b><br>"
        "%{percent}<br>"
        "%{value:.2f} M<extra></extra>"

    ),

    row=2,
    col=3

)

# 7. REGIONAL SALES
regional_sales = {

    "North America": df["NA_Sales"].sum(),
    "Europe": df["EU_Sales"].sum(),
    "Japan": df["JP_Sales"].sum(),
    "Other": df["Other_Sales"].sum()

}

fig.add_trace(

    go.Bar(

        x=list(regional_sales.keys()),
        y=list(regional_sales.values()),

        hovertemplate=
        "<b>%{x}</b><br>"
        "Sales: %{y:.2f} M<extra></extra>"

    ),

    row=3,
    col=1

)

decade_sales = (

    df.groupby("Decade")["Global_Sales"]
      .sum()
      .reset_index()

)

fig.add_trace(

    go.Bar(

        x=decade_sales["Decade"].astype(str),
        y=decade_sales["Global_Sales"],

        hovertemplate=
        "<b>%{x}s</b><br>"
        "Sales: %{y:.2f} M<extra></extra>"

    ),

    row=3,
    col=2

)

# 9. CRITIC SCORE VS SALES
fig.add_trace(

    go.Scatter(

        x=df["Critic_Score"],
        y=df["Global_Sales"],

        mode="markers",

        marker=dict(
            size=5,
            opacity=0.55
        ),

        text=df["Name"],

        hovertemplate=
        "<b>%{text}</b><br>"
        "Critic Score: %{x}<br>"
        "Sales: %{y:.2f} M<extra></extra>"

    ),

    row=3,
    col=3

)


# 10. TOP SELLING GAMES
top_games = (

    df.nlargest(10, "Global_Sales")
      .sort_values("Global_Sales")

)

fig.add_trace(

    go.Bar(

        x=top_games["Global_Sales"],
        y=top_games["Name"],

        orientation="h",

        hovertemplate=
        "<b>%{y}</b><br>"
        "Sales: %{x:.2f} M<extra></extra>"

    ),

    row=4,
    col=1

)


# 11. PLATFORM MARKET SHARE
market_share = (

    df.groupby("Platform")["Global_Sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)

)

fig.add_trace(

    go.Pie(

        labels=market_share.index,
        values=market_share.values,

        hole=0.45,

        showlegend=False,

        hovertemplate=
        "<b>%{label}</b><br>"
        "%{percent}<br>"
        "%{value:.2f} M<extra></extra>"

    ),

    row=4,
    col=2

)

# 12. SALES DISTRIBUTION
fig.add_trace(

    go.Histogram(

        x=df["Global_Sales"],

        nbinsx=40,

        hovertemplate=
        "Sales: %{x:.2f} M<br>"
        "Games: %{y}<extra></extra>"

    ),

    row=4,
    col=3

)

# ==========================================================
# LAYOUT

fig.update_layout(

    title={

        "text":"<b>Video Game Industry Intelligence Dashboard</b>",

        "x":0.5,

        "font":{"size":30}

    },

    template="plotly_dark",

    height=1750,

    width=1850,

    showlegend=False,

    margin=dict(

        t=190,
        l=40,
        r=40,
        b=40

    )

)

# GRID
fig.update_xaxes(showgrid=True)

fig.update_yaxes(showgrid=True)

# EXPORT
fig.write_html(

    "images/executive_dashboard.html",

    include_plotlyjs="cdn"

)

try:

    fig.write_image(

        "images/executive_dashboard.png",

        width=1850,
        height=1750,
        scale=2

    )

except Exception:

    print("Install kaleido for PNG export.")


fig.show()

print("\nDashboard exported successfully!")
print("HTML : images/executive_dashboard.html")
print("PNG  : images/executive_dashboard.png")