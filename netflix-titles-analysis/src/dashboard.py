import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# =====================================================
# LOAD DATA
# =====================================================

connection = sqlite3.connect("data/analytics.db")

df = pd.read_sql_query(
    "SELECT * FROM netflix_titles",
    connection
)

executive = pd.read_sql_query(
    "SELECT * FROM executive_summary",
    connection
)

recommendations = pd.read_sql_query(
    """
    SELECT *
    FROM recommendation_candidates
    LIMIT 15
    """,
    connection
)

# =====================================================
# KPI VALUES
# =====================================================

total_titles = len(df)

movies = (df["type"] == "Movie").sum()

tv_shows = (df["type"] == "TV Show").sum()

countries = df["country"].nunique()

avg_duration = round(df["duration_minutes"].mean(), 1)

avg_popularity = round(df["popularity_score"].mean(), 2)

# =====================================================
# DASHBOARD
# =====================================================

fig = make_subplots(

    rows=10,
    cols=2,

    specs=[

        [{"type":"indicator"},{"type":"indicator"}],
        [{"type":"indicator"},{"type":"indicator"}],
        [{"type":"indicator"},{"type":"indicator"}],

        [{"type":"table"},{"type":"table"}],

        [{"type":"xy"},{"type":"domain"}],

        [{"type":"xy"},{"type":"xy"}],

        [{"type":"xy"},{"type":"xy"}],

        [{"type":"xy"},{"type":"xy"}],

        [{"type":"table"},{"type":"table"}],

        [{"type":"table"},{"type":"table"}]

    ],

    subplot_titles=(

        "Total Titles",
        "Movies",

        "TV Shows",
        "Countries",

        "Average Duration",
        "Popularity Score",

        "Executive Summary",
        "Recommendation Candidates",

        "Release Timeline",
        "Movies vs TV Shows",

        "Ratings",
        "Duration Categories",

        "Recent vs Classic",
        "Yearly Additions",

        "Correlation Heatmap",
        "Recommendation Scores",

        "Statistical Summary",
        "Business Recommendations",

        "",
        ""

    ),

    vertical_spacing=0.05

)

# =====================================================
# KPI CARDS
# =====================================================

fig.add_trace(

    go.Indicator(

        mode="number",

        value=total_titles,

        title={"text":"Total Titles"}

    ),

    row=1,
    col=1

)

fig.add_trace(

    go.Indicator(

        mode="number",

        value=movies,

        title={"text":"Movies"}

    ),

    row=1,
    col=2

)

fig.add_trace(

    go.Indicator(

        mode="number",

        value=tv_shows,

        title={"text":"TV Shows"}

    ),

    row=2,
    col=1

)

fig.add_trace(

    go.Indicator(

        mode="number",

        value=countries,

        title={"text":"Countries"}

    ),

    row=2,
    col=2

)

fig.add_trace(

    go.Indicator(

    mode="number",

    value=avg_duration,

    number={"suffix": " min"},

    title={"text":"Average Movie Length"}

    ),

    row=3,
    col=1

)

fig.add_trace(

    go.Indicator(

        mode="number",

        value=avg_popularity,

        title={"text":"Average Popularity Score"}

    ),

    row=3,
    col=2

)

# =====================================================
# EXECUTIVE SUMMARY TABLE
# =====================================================

fig.add_trace(

    go.Table(

        header=dict(

            values=list(executive.columns)

        ),

        cells=dict(

            values=[executive[col] for col in executive.columns]

        )

    ),

    row=4,
    col=1

)

# =====================================================
# RECOMMENDATION TABLE
# =====================================================

fig.add_trace(

    go.Table(

        header=dict(

            values=list(recommendations.columns)

        ),

        cells=dict(

            values=[recommendations[col] for col in recommendations.columns]

        )

    ),

    row=4,
    col=2

)
# =====================================================
# RELEASE TIMELINE
# =====================================================

timeline = pd.read_sql_query("""
SELECT
    release_year,
    COUNT(*) AS total_titles
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year
""", connection)

fig.add_trace(

    go.Scatter(

        x=timeline["release_year"],
        y=timeline["total_titles"],
        mode="lines+markers",
        name="Titles"

    ),

    row=5,
    col=1

)

# =====================================================
# MOVIES VS TV SHOWS
# =====================================================

content = pd.read_sql_query("""
SELECT
    type,
    COUNT(*) AS total
FROM netflix_titles
GROUP BY type
""", connection)

fig.add_trace(

    go.Pie(

        labels=content["type"],
        values=content["total"],
        hole=0.45,
        showlegend=True

    ),

    row=5,
    col=2

)

# =====================================================
# RATINGS DISTRIBUTION
# =====================================================

ratings = pd.read_sql_query("""
SELECT
    rating,
    COUNT(*) AS total
FROM netflix_titles
GROUP BY rating
ORDER BY total DESC
""", connection)

fig.add_trace(

    go.Bar(

        x=ratings["rating"],
        y=ratings["total"],
        name="Ratings"

    ),

    row=6,
    col=1

)

# =====================================================
# DURATION CATEGORY
# =====================================================

duration = pd.read_sql_query("""
SELECT
    duration_category,
    COUNT(*) AS total
FROM netflix_titles
GROUP BY duration_category
""", connection)

fig.add_trace(

    go.Bar(

        x=duration["duration_category"],
        y=duration["total"],
        name="Duration"

    ),

    row=6,
    col=2

)

# =====================================================
# RECENT VS CLASSIC
# =====================================================

recent = pd.read_sql_query("""

SELECT

CASE

WHEN release_year>=2018 THEN 'Recent'

ELSE 'Classic'

END AS category,

COUNT(*) AS total

FROM netflix_titles

GROUP BY category

""", connection)

fig.add_trace(

    go.Bar(

        x=recent["category"],
        y=recent["total"]

    ),

    row=7,
    col=1

)

# =====================================================
# YEARLY ADDITIONS
# =====================================================

added = pd.read_sql_query("""

SELECT

year_added,

COUNT(*) AS total

FROM netflix_titles

GROUP BY year_added

ORDER BY year_added

""", connection)

fig.add_trace(

    go.Scatter(

        x=added["year_added"],
        y=added["total"],
        mode="lines+markers",
        fill="tozeroy"

    ),

    row=7,
    col=2

)


# =====================================================
# TOP RECOMMENDATIONS
# =====================================================

top = df.nlargest(15, "popularity_score")

fig.add_trace(

    go.Bar(

        x=top["popularity_score"],
        y=top["title"],
        orientation="h"

    ),

    row=8,
    col=2

)

# =====================================================
# CORRELATION HEATMAP
# =====================================================

numeric = df.select_dtypes(include=["int64", "float64"])

corr = numeric.corr(numeric_only=True)

fig.add_trace(

    go.Heatmap(

        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        showscale=True

    ),

    row=8,
    col=1

)

# =====================================================
# STATISTICAL SUMMARY
# =====================================================

stats = numeric.describe().T

stats["Median"] = numeric.median()
stats["Variance"] = numeric.var()
stats["Std"] = numeric.std()
stats["Skewness"] = numeric.skew()

stats = stats.round(2)

fig.add_trace(

    go.Table(

        header=dict(

            values=["Metric"] + list(stats.columns),

            fill_color="#1f77b4",
            font=dict(color="white", size=12),
            align="center"

        ),

        cells=dict(

            values=[stats.index] + [stats[col] for col in stats.columns],

            align="center"

        )

    ),

    row=9,
    col=1

)

# =====================================================
# BUSINESS RECOMMENDATIONS
# =====================================================

recommendation_text = """
<b>1.</b> Continue investing in Movies, which dominate the catalog.<br><br>

<b>2.</b> Increase production of high-performing genres such as Drama,
International Movies and Documentaries.<br><br>

<b>3.</b> Expand localized productions in countries with growing catalogs.<br><br>

<b>4.</b> Maintain a balanced mix of family-friendly and mature content
to maximize audience reach.<br><br>

<b>5.</b> Prioritize long-form, high-popularity content when expanding
the recommendation engine.
"""

fig.add_trace(

    go.Table(

        header=dict(

            values=["Business Recommendations"],

            fill_color="green",

            font=dict(color="white", size=13),

            align="left"

        ),

        cells=dict(

            values=[[recommendation_text]],

            align="left",

            height=220

        )

    ),

    row=9,
    col=2

)

# =====================================================
# FOOTER
# =====================================================

summary = pd.DataFrame({

    "Metric":[

        "Project",
        "Dataset",
        "Database",
        "Analytics",
        "Recommendation Engine",
        "Dashboard"

    ],

    "Value":[

        "Netflix Recommendation Intelligence",

        f"{len(df):,} Titles",

        "SQLite",

        "Python + SQL",

        "Rule-Based Ranking",

        "Plotly Executive Dashboard"

    ]

})

fig.add_trace(

    go.Table(

        header=dict(

            values=["Project Summary","Value"],

            fill_color="#2d3436",

            font=dict(color="white")

        ),

        cells=dict(

            values=[

                summary["Metric"],

                summary["Value"]

            ]

        )

    ),

    row=10,
    col=1

)

# =====================================================
# AUTHOR
# =====================================================

fig.add_annotation(

    text="<b>Netflix Recommendation Intelligence Dashboard</b><br>"
         "AI Projects Bootcamp • Project 4<br>"
         "Built with Python • SQLite • Pandas • Plotly",

    x=0.5,
    y=-0.08,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=15)

)

# =====================================================
# LAYOUT
# =====================================================

fig.update_layout(

    title={

        "text":"🎬 Netflix Recommendation Intelligence Dashboard",

        "x":0.5,

        "font":{

            "size":30

        }

    },

    template="plotly_dark",

    height=5200,

    width=1700,

    showlegend=False,

    margin=dict(

        t=120,
        l=40,
        r=40,
        b=120

    )

)

# =====================================================
# SAVE DASHBOARD
# =====================================================

fig.write_html(
    "images/dashboard.html"
)

fig.write_image(
    "images/dashboard.png",
    scale=2
)

print("\nDashboard saved successfully!")

fig.show()

connection.close()
