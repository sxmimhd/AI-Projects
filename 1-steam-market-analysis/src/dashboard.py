import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

df = pd.read_csv("data/games_processed.csv")

total_games = len(df)
avg_price = df["price"].mean()
avg_rating = df["pct_pos_total"].mean()
total_reviews = df["total_reviews"].sum()
avg_peak_ccu = df["peak_ccu"].mean()

games_per_year = (
    df.groupby("release_year")
    .size()
    .reset_index(name="games")
)

months = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

monthly = (
    df["release_month"]
    .value_counts()
    .reindex(months)
    .reset_index()
)

monthly.columns = ["Month","Games"]

top_publishers = (
    df["publishers"]
    .value_counts()
    .head(10)
    .sort_values()
)

top_developers = (
    df["developers"]
    .value_counts()
    .head(10)
    .sort_values()
)

top_genres = (
    df["genres"]
    .value_counts()
    .head(10)
    .sort_values()
)

corr = (
    df.select_dtypes(include="number")
    .corr()
)


fig = make_subplots(
    rows=4,
    cols=2,
    subplot_titles=(
        "Games Released Per Year",
        "Price Distribution",
        "Monthly Releases",
        "Top Publishers",
        "Top Developers",
        "Price vs Review %",
        "Top Genres",
        "Correlation Heatmap"
    ),
    vertical_spacing=0.12
)

fig.add_trace(

    go.Scatter(
        x=games_per_year["release_year"],
        y=games_per_year["games"],
        mode="lines+markers",
        name="Games"
    ),

    row=1,
    col=1

)

fig.add_trace(

    go.Histogram(
        x=df["price"],
        nbinsx=40,
        name="Price"
    ),

    row=1,
    col=2

)

fig.add_trace(

    go.Bar(
        x=monthly["Month"],
        y=monthly["Games"],
        name="Monthly"
    ),

    row=2,
    col=1

)

fig.add_trace(

    go.Bar(

        x=top_publishers.values,

        y=top_publishers.index,

        orientation="h",

        name="Publishers"

    ),

    row=2,

    col=2

)

fig.add_trace(

    go.Bar(

        x=top_developers.values,

        y=top_developers.index,

        orientation="h",

        name="Developers"

    ),

    row=3,

    col=1

)

sample = df.sample(min(5000, len(df)), random_state=42)

fig.add_trace(

    go.Scatter(

        x=sample["price"],

        y=sample["pct_pos_total"],

        mode="markers",

        text=sample["name"],

        marker=dict(size=5),

        name="Games"

    ),

    row=3,

    col=2

)

fig.add_trace(

    go.Bar(

        x=top_genres.values,

        y=top_genres.index,

        orientation="h",

        name="Genres"

    ),

    row=4,

    col=1

)

fig.add_trace(

    go.Heatmap(

        z=corr.values,

        x=corr.columns,

        y=corr.columns,

        showscale=True

    ),

    row=4,

    col=2

)

fig.update_layout(

    template="plotly_dark",

    height=1700,

    width=1600,

    title={

        "text":
        f"""
🎮 Steam Market Analysis Dashboard

Total Games: {total_games:,} |
Average Price: ${avg_price:.2f} |
Average Rating: {avg_rating:.1f}% |
Total Reviews: {total_reviews:,} |
Average Peak CCU: {avg_peak_ccu:,.0f}
""",

        "x":0.5

    },

    showlegend=False

)

fig.write_html("images/dashboard.html")

try:
    fig.write_image("images/dashboard.png", scale=2)
except:
    print("Install kaleido to export PNG.")

fig.show()