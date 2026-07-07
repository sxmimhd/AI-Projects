import sqlite3
import pandas as pd
import plotly.express as px
from pathlib import Path

print("=" * 70)
print("NETFLIX SQL ANALYTICS")
print("=" * 70)

# =====================================================
# DATABASE CONNECTION
# =====================================================

connection = sqlite3.connect("data/analytics.db")

# =====================================================
# CREATE OUTPUT FOLDER
# =====================================================

Path("sql_results").mkdir(exist_ok=True)

# =====================================================
# LOAD SQL VIEWS
# =====================================================

print("\nCreating SQL Views...")

with open("sql/create_views.sql", "r", encoding="utf-8") as file:
    connection.executescript(file.read())

print("Views created successfully!")

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

executive = pd.read_sql_query(
    """
    SELECT *
    FROM executive_summary
    """,
    connection
)

print("\nExecutive Summary")
print(executive)

executive.to_csv(
    "sql_results/executive_summary.csv",
    index=False
)

# =====================================================
# YEARLY PRODUCTION
# =====================================================

yearly = pd.read_sql_query(
    """
    SELECT *
    FROM yearly_production
    ORDER BY release_year
    """,
    connection
)

yearly.to_csv(
    "sql_results/yearly_production.csv",
    index=False
)

fig = px.line(
    yearly,
    x="release_year",
    y="total_titles",
    markers=True,
    title="Netflix Content Production Over Time"
)

fig.write_image("images/yearly_production.png")
fig.show()

# =====================================================
# RATING DISTRIBUTION
# =====================================================

ratings = pd.read_sql_query(
    """
    SELECT *
    FROM rating_distribution
    ORDER BY total_titles DESC
    """,
    connection
)

ratings.to_csv(
    "sql_results/rating_distribution.csv",
    index=False
)

fig = px.bar(
    ratings,
    x="rating",
    y="total_titles",
    color="total_titles",
    title="Content Ratings Distribution"
)

fig.write_image("images/rating_distribution.png")
fig.show()
# =====================================================
# MOVIES VS TV SHOWS
# =====================================================

content_type = pd.read_sql_query(
    """
    SELECT
        type,
        COUNT(*) AS total_titles
    FROM netflix_titles
    GROUP BY type
    """,
    connection
)

content_type.to_csv(
    "sql_results/content_type.csv",
    index=False
)

fig = px.pie(
    content_type,
    names="type",
    values="total_titles",
    hole=0.45,
    title="Movies vs TV Shows"
)

fig.write_image("images/content_type.png")
fig.show()

# =====================================================
# FAMILY VS MATURE CONTENT
# =====================================================

family = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM family_content
    """,
    connection
)

mature = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM mature_content
    """,
    connection
)

comparison = pd.DataFrame({

    "Category": [
        "Family",
        "Mature"
    ],

    "Titles": [
        family.iloc[0,0],
        mature.iloc[0,0]
    ]

})

comparison.to_csv(
    "sql_results/family_vs_mature.csv",
    index=False
)

fig = px.bar(
    comparison,
    x="Category",
    y="Titles",
    color="Category",
    title="Family vs Mature Content"
)

fig.write_image("images/family_vs_mature.png")
fig.show()

# =====================================================
# DURATION STATISTICS
# =====================================================

duration = pd.read_sql_query(
    """
    SELECT *
    FROM duration_statistics
    """,
    connection
)

duration.to_csv(
    "sql_results/duration_statistics.csv",
    index=False
)

fig = px.bar(
    duration,
    x="duration_category",
    y="total_titles",
    color="avg_duration",
    title="Movie Duration Categories"
)

fig.write_image("images/duration_statistics.png")
fig.show()

# =====================================================
# RECENT VS CLASSIC CONTENT
# =====================================================

recent = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM recent_content
    """,
    connection
)

classic = pd.read_sql_query(
    """
    SELECT COUNT(*) AS total
    FROM classic_content
    """,
    connection
)

age_df = pd.DataFrame({

    "Content": [
        "Recent",
        "Classic"
    ],

    "Titles": [
        recent.iloc[0,0],
        classic.iloc[0,0]
    ]

})

age_df.to_csv(
    "sql_results/content_age.csv",
    index=False
)

fig = px.pie(
    age_df,
    names="Content",
    values="Titles",
    hole=0.45,
    title="Recent vs Classic Content"
)

fig.write_image("images/content_age.png")
fig.show()

# =====================================================
# TOP RECOMMENDATION CANDIDATES
# =====================================================

recommendations = pd.read_sql_query(
    """
    SELECT *
    FROM recommendation_candidates
    LIMIT 20
    """,
    connection
)

recommendations.to_csv(
    "sql_results/recommendations.csv",
    index=False
)

print("\nTop Recommendation Candidates\n")
print(recommendations.head(10))

# =====================================================
# CONTENT ADDED PER YEAR
# =====================================================

added = pd.read_sql_query(
    """
    SELECT *
    FROM yearly_additions
    ORDER BY year_added
    """,
    connection
)

added.to_csv(
    "sql_results/yearly_additions.csv",
    index=False
)

fig = px.area(
    added,
    x="year_added",
    y="titles_added",
    title="Titles Added to Netflix by Year"
)

fig.write_image("images/yearly_additions.png")
fig.show()

# =====================================================
# TOP 20 LONGEST MOVIES
# =====================================================

long_movies = pd.read_sql_query(
    """
    SELECT
        title,
        duration_minutes
    FROM long_movies
    ORDER BY duration_minutes DESC
    LIMIT 20
    """,
    connection
)

long_movies.to_csv(
    "sql_results/long_movies.csv",
    index=False
)

fig = px.bar(
    long_movies,
    x="duration_minutes",
    y="title",
    orientation="h",
    title="Top 20 Longest Movies"
)

fig.write_image("images/long_movies.png")
fig.show()
# =====================================================
# LOAD COMPLETE DATASET
# =====================================================

df = pd.read_csv("data/processed_data.csv")

# =====================================================
# CORRELATION ANALYSIS
# =====================================================

numeric = df.select_dtypes(include=["int64", "float64"])

corr = numeric.corr(numeric_only=True)

corr.to_csv(
    "sql_results/correlation_matrix.csv"
)

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto",
    title="Correlation Heatmap"
)

fig.write_image("images/correlation_heatmap.png")
fig.show()

# =====================================================
# OUTLIER DETECTION
# =====================================================

fig = px.box(
    df,
    y="duration_minutes",
    title="Movie Duration Outliers"
)

fig.write_image("images/duration_boxplot.png")
fig.show()

fig = px.box(
    df,
    y="popularity_score",
    title="Popularity Score Outliers"
)

fig.write_image("images/popularity_boxplot.png")
fig.show()

# =====================================================
# POPULARITY DISTRIBUTION
# =====================================================

fig = px.histogram(
    df,
    x="popularity_score",
    nbins=30,
    title="Popularity Score Distribution"
)

fig.write_image("images/popularity_distribution.png")
fig.show()

# =====================================================
# DURATION DISTRIBUTION
# =====================================================

movies = df[df["type"] == "Movie"]

fig = px.histogram(
    movies,
    x="duration_minutes",
    nbins=40,
    title="Movie Duration Distribution"
)

fig.write_image("images/duration_distribution.png")
fig.show()

# =====================================================
# RELEASE YEAR DISTRIBUTION
# =====================================================

fig = px.histogram(
    df,
    x="release_year",
    nbins=40,
    title="Release Year Distribution"
)

fig.write_image("images/release_distribution.png")
fig.show()

# =====================================================
# STATISTICAL SUMMARY
# =====================================================

stats = numeric.describe().T

stats["median"] = numeric.median()

stats["variance"] = numeric.var()

stats["std"] = numeric.std()

stats["skewness"] = numeric.skew()

stats.to_csv(
    "sql_results/statistical_summary.csv"
)

print("\nStatistical Summary")
print(stats)

# =====================================================
# EXECUTIVE KPI REPORT
# =====================================================

kpis = pd.DataFrame({

    "Metric":[

        "Total Titles",
        "Movies",
        "TV Shows",
        "Countries",
        "Genres",
        "Average Movie Length",
        "Average Popularity Score",
        "Newest Release",
        "Oldest Release"

    ],

    "Value":[

        len(df),

        (df["type"]=="Movie").sum(),

        (df["type"]=="TV Show").sum(),

        df["country"].nunique(),

        df["listed_in"].nunique(),

        round(df["duration_minutes"].mean(),1),

        round(df["popularity_score"].mean(),2),

        df["release_year"].max(),

        df["release_year"].min()

    ]

})

kpis.to_csv(
    "sql_results/kpi_report.csv",
    index=False
)

print("\nExecutive KPIs\n")
print(kpis)

# =====================================================
# RECOMMENDATION SCORE ANALYSIS
# =====================================================

top = df.nlargest(
    25,
    "popularity_score"
)

fig = px.bar(
    top,
    x="popularity_score",
    y="title",
    orientation="h",
    color="type",
    title="Top Recommendation Candidates"
)

fig.write_image(
    "images/recommendation_engine.png"
)

fig.show()

# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n" + "=" * 70)
print("ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 70)

print(f"Dataset Size: {len(df):,} titles")
print(f"Movies: {(df['type']=='Movie').sum():,}")
print(f"TV Shows: {(df['type']=='TV Show').sum():,}")
print(f"Countries: {df['country'].nunique():,}")
print(f"Unique Genre Combinations: {df['listed_in'].nunique():,}")

print("\nImages saved inside images/")
print("SQL reports saved inside sql_results/")

connection.close()