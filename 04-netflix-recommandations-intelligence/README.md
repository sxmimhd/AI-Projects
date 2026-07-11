# 🎬 Netflix Recommendation Intelligence

<p align="center">
  <img src="images/dashboard.png" width="100%" alt="Netflix Recommendation Intelligence Dashboard">
</p>

> A business intelligence and recommendation analytics project built with **Python, SQLite, SQL, Pandas, and Plotly**. This project transforms raw Netflix catalog data into actionable insights through data engineering, SQL analytics, statistical analysis, and an executive dashboard.

---

# Executive Summary

Streaming platforms rely on data to understand their content libraries, optimize recommendations, and guide investment decisions.

This project simulates the workflow of a Data Analyst working for a streaming platform by answering questions such as:

* Which content categories dominate the platform?
* How has Netflix's catalog evolved over time?
* Which ratings are most common?
* What characteristics define recommended content?
* Which business decisions could improve user engagement?

The project combines SQL analytics, feature engineering, recommendation logic, and interactive business intelligence into one complete analytics pipeline.

---

# Project Objectives

* Clean and prepare a real-world dataset
* Engineer meaningful business features
* Build a SQLite analytical database
* Perform advanced SQL analysis
* Apply statistical analysis
* Create recommendation-oriented insights
* Build an executive dashboard
* Deliver actionable business recommendations

---

# Dataset

**Netflix Movies & TV Shows**

The dataset contains information about thousands of Netflix titles, including:

* Movies
* TV Shows
* Countries
* Directors
* Cast
* Genres
* Ratings
* Release Years
* Duration
* Date Added

**Dataset Source**

https://www.kaggle.com/datasets/shivamb/netflix-shows

*(The dataset is not included in this repository because of its size. Download it from Kaggle and place `netflix_titles.csv` inside the `data/` directory.)*

---

# Project Structure

```text
netflix-titles-analysis/

│
├── data/
│   ├── netflix_titles.csv
│   ├── processed_data.csv
│   └── analytics.db
│
├── images/
│
├── sql/
│   ├── queries.sql
│   ├── advanced_queries.sql
│   └── create_views.sql
│
├── src/
│   ├── main.py
│   ├── cleaning.py
│   ├── feature_engineering.py
│   ├── database.py
│   ├── analytics.py
│   ├── dashboard.py
│
├── sql_results/
│
├── insights.md
└── README.md
```

---

# Data Pipeline

```text
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
SQLite Database
      │
      ▼
SQL Analytics
      │
      ▼
Statistical Analysis
      │
      ▼
Recommendation Logic
      │
      ▼
Executive Dashboard
      │
      ▼
Business Recommendations
```

---

# Feature Engineering

Additional business-oriented features were created, including:

* Content Age
* Years on Netflix
* Duration Categories
* Duration in Minutes
* Number of Genres
* Number of Countries
* Number of Cast Members
* Popularity Score

These engineered features make SQL analysis and recommendation ranking significantly more informative.

---

# SQL Analytics

This project demonstrates practical SQL skills including:

## Fundamental SQL

* SELECT
* WHERE
* ORDER BY
* LIMIT
* GROUP BY
* HAVING
* COUNT
* SUM
* AVG
* MIN
* MAX

## Intermediate SQL

* CASE Statements
* Views
* Aggregations
* Ranking

## Advanced SQL

* Common Table Expressions (CTEs)
* Window Functions
* ROW_NUMBER()
* RANK()
* DENSE_RANK()
* Analytical Views

---

# Recommendation Intelligence

Instead of training a machine learning model, this project implements a rule-based recommendation strategy using engineered features.

Recommendations consider:

* Content age
* Duration
* Genre richness
* Country diversity
* Popularity score
* Catalog characteristics

This demonstrates how recommendation systems can begin with analytical ranking before introducing machine learning.

---

# Dashboard Features

The executive dashboard includes:

* Executive KPI Cards
* Movies vs TV Shows
* Ratings Distribution
* Release Timeline
* Yearly Content Growth
* Duration Categories
* Recent vs Classic Content
* Recommendation Candidates
* Correlation Heatmap
* Statistical Summary
* SQL Executive Tables
* Business Recommendation Panel

---

# Business Questions Answered

* How has Netflix's catalog changed over time?
* Which ratings dominate the platform?
* Which content types are most common?
* Which duration ranges are most successful?
* What characteristics define highly recommended titles?
* How should a streaming platform prioritize future investments?

---

# Technologies Used

* Python
* Pandas
* NumPy
* Plotly
* SQLite
* SQL
* Kaleido
* VS Code

---

# Key Skills Demonstrated

* Data Cleaning
* Feature Engineering
* SQL Database Design
* SQL Analytics
* Window Functions
* CTEs
* Recommendation Analytics
* Statistical Analysis
* Correlation Analysis
* Outlier Detection
* Executive Dashboard Design
* Business Intelligence
* Data Storytelling

---

# Business Impact

This project demonstrates how analytics can support strategic decision-making by transforming raw entertainment data into practical recommendations.

Potential business applications include:

* Content investment strategy
* Catalog optimization
* Recommendation systems
* Audience segmentation
* Executive reporting
* Business intelligence dashboards

---

# Future Improvements

* Streamlit web application
* Machine learning recommendation engine
* Content similarity search
* Interactive filtering
* REST API integration
* Real-time analytics
* Automated reporting
* User personalization

---

# Portfolio Progress

**Data Analytics Bootcamp**

* ✅ Project 1 — Steam Market Analysis
* ✅ Project 2 — AI Jobs & Salaries Analysis
* ✅ Project 3 — Video Game Industry Intelligence
* ✅ Project 4 — Netflix Recommendation Intelligence
* 🚀 Project 5 — AI Business Intelligence Platform (Coming Next)

---

## Author

**Sami Mahdadi**

Computer Science Student • AI Developer • Data Analyst • Game Developer

Building practical AI, analytics, and software engineering projects with a focus on business impact and clean engineering practices.
