import streamlit as st
import time
time.sleep(0.5)

from src.loader import load_dataset
from src.analyzer import dataset_profile
from src.utils import detect_dataset_type
from src.cleaner import (
    data_quality_report,
    remove_duplicates,
    fill_missing,
    drop_empty_columns
)
from src.statistics import statistics_report
from src.visualizer import Visualizer
from src.insights import InsightEngine, RecommendationEngine
from src.exporter import *

st.set_page_config(
    page_title="Analytica AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Analytica AI")

st.subheader("AI Business Intelligence Platform")

st.markdown(
    """
Upload any CSV file and receive:

- 📈 Automatic Visualizations
- 📊 Executive Dashboard
- 📉 Statistical Analysis
- 🤖 AI Insights
- 💼 Business Recommendations
- 📄 Exportable Reports
"""
)

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file:

    df, error = load_dataset(uploaded_file)

    if error:
        st.error(error)

    else:
        
        progress = st.progress(0)
        status = st.empty()

        status.text("Loading dataset...")
        progress.progress(10)

        profile = dataset_profile(df)
        dataset_type = detect_dataset_type(df)
        status.text("Checking data quality...")
        progress.progress(25)

        quality = data_quality_report(df)

        status.text("Computing statistics...")
        progress.progress(45)

        stats = statistics_report(df)

        status.text("Building visualization engine...")
        progress.progress(60)

        viz = Visualizer(df)

        status.text("Generating AI insights...")
        progress.progress(80)

        engine = InsightEngine(df, stats)
        recommendation_engine = RecommendationEngine(df)

        insights = engine.generate()
        recommendations = recommendation_engine.recommend()

        progress.progress(100)
        status.success("Analysis complete!")

        st.success("Dataset loaded successfully!")


        st.info(f"Detected Dataset Type: **{dataset_type}**")

        st.divider()

        st.subheader("Executive Overview")

        c1, c2, c3, c4 = st.columns(4)
        c5, c6, c7 = st.columns(3)

        c1.metric("Rows", f"{profile['rows']:,}")
        c2.metric("Columns", profile["columns"])
        c3.metric("Missing", profile["missing"])
        c4.metric("Duplicates", profile["duplicates"])
        c5.metric("Numeric", profile["numeric"])
        c6.metric("Categorical", profile["categorical"])
        c7.metric("Memory (MB)", profile["memory"])

        st.divider()

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "Overview",
            "Data Quality",
            "Cleaning",
            "Statistics",
            "Visualizations",
            "AI Insights",
            "Recommendations",
            "Export"
        ])

        # Overview
        with tab1:

            st.subheader("Dataset Preview")

            st.dataframe(df.head(10), use_container_width=True)

            st.write(f"Shape: {df.shape}")

        # Data Quality
        with tab2:

            st.subheader("Missing Values")

            st.dataframe(
                quality["missing"],
                use_container_width=True
            )

            st.subheader("Column Types")

            st.dataframe(
                quality["dtypes"],
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Duplicate Rows", quality["duplicates"])

            with col2:
                st.metric(
                    "Constant Columns",
                    len(quality["constant_columns"])
                )

            if quality["empty_columns"]:
                st.warning(f"Empty Columns: {quality['empty_columns']}")

            if quality["constant_columns"]:
                st.warning(f"Constant Columns: {quality['constant_columns']}")

        # Cleaning
        with tab3:

            cleaned = df.copy()

            st.subheader("Automatic Cleaning")

            if st.button("Remove Duplicates"):
                cleaned = remove_duplicates(cleaned)
                st.success("Duplicates removed.")

            if st.button("Fill Missing Values"):
                cleaned = fill_missing(cleaned)
                st.success("Missing values filled.")

            if st.button("Drop Empty Columns"):
                cleaned = drop_empty_columns(cleaned)
                st.success("Empty columns removed.")

            st.subheader("Preview")

            st.dataframe(cleaned.head(), use_container_width=True)

        with tab4:

            st.subheader("Statistical Summary")

            st.dataframe(
                stats,
                use_container_width=True
            )
            st.divider()

            st.subheader("Highlights")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Numeric Columns",
                len(stats)
            )

            c2.metric(
                "Total Outliers",
                int(stats["Outliers"].sum())
            )

            c3.metric(
                "Highest Variance",
                stats.sort_values(
                    "Variance",
                    ascending=False
                ).iloc[0]["Column"]
            )

            st.divider()

            st.subheader("Automatic Statistical Insights")

            for _, row in stats.iterrows():

                if row["Skewness"] > 1:

                    st.warning(
                        f"**{row['Column']}** is highly right-skewed."
                    )

                elif row["Skewness"] < -1:

                    st.warning(
                        f"**{row['Column']}** is highly left-skewed."
                    )

                if row["Outliers"] > 0:

                    st.info(
                        f"**{row['Column']}** contains {row['Outliers']} potential outliers."
                    )

                if row["Kurtosis"] > 3:

                    st.info(
                        f"**{row['Column']}** has a heavy-tailed distribution."
                    )

        with tab5:

            st.subheader("Automatic Visualization Engine")

            st.caption(
                "Charts are generated automatically based on detected column types."
            )

            # Correlation
            heatmap = viz.correlation()

            if heatmap:
                st.plotly_chart(
                    heatmap,
                    use_container_width=True
                )

            # Histograms
            st.subheader("Numeric Distributions")

            for fig in viz.histograms():
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Boxplots
            st.subheader("Outlier Analysis")

            for fig in viz.boxplots():
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Categories
            st.subheader("Categorical Analysis")

            for fig in viz.categorical():
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Pie Charts
            st.subheader("Category Shares")

            for fig in viz.pies():
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Scatter
            st.subheader("Relationships")

            for fig in viz.scatter():
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # Timeline
            timeline = viz.timeline()

            if timeline is not None:
                st.subheader("Time Series")

                st.plotly_chart(
                    timeline,
                    use_container_width=True
                )

        with tab6:

            st.subheader("AI Generated Insights")

            st.caption(
                "Automatically generated from statistical analysis."
            )

            for insight in insights:

                st.info(insight)

        with tab7:

            st.subheader("Business Recommendations")

            st.caption(
                "Automatically generated recommendations."
            )

            for rec in recommendations:

                st.success(rec)

        with tab8:

            st.subheader("Export Analysis")

            st.caption(
                "Download your analysis in multiple formats."
            )

            if st.button("Export Cleaned CSV"):

                path = export_csv(df)

                st.success(f"Saved to {path}")

            if st.button("Export Statistics Excel"):

                path = export_excel(stats)

                st.success(f"Saved to {path}")

            if st.button("Export SQLite Database"):

                path = export_sqlite(df)

                st.success(f"Saved to {path}")

            if st.button("Generate HTML Report"):

                path = export_html(

                    profile,

                    stats,

                    insights,

                    recommendations

                )

                st.success(f"Saved to {path}")