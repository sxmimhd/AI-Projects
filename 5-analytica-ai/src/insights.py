import pandas as pd
import numpy as np


class InsightEngine:

    def __init__(self, df, stats):

        self.df = df
        self.stats = stats

    def generate(self):

        insights = []

        # Dataset size
        insights.append(
            f"The dataset contains {len(self.df):,} rows and {len(self.df.columns)} columns."
        )

        # Missing values
        missing = self.df.isnull().sum()

        for col, value in missing.items():

            pct = value / len(self.df) * 100

            if pct > 40:

                insights.append(
                    f"{col} has {pct:.1f}% missing values. Consider removing or carefully imputing this column."
                )

            elif pct > 10:

                insights.append(
                    f"{col} has {pct:.1f}% missing values. Imputation is recommended before modeling."
                )

        # Numeric insights
        for _, row in self.stats.iterrows():

            col = row["Column"]

            if row["Skewness"] > 1:

                insights.append(
                    f"{col} is highly right-skewed. The median is likely more representative than the mean."
                )

            elif row["Skewness"] < -1:

                insights.append(
                    f"{col} is highly left-skewed."
                )

            if row["Outliers"] > 0:

                insights.append(
                    f"{col} contains {row['Outliers']} potential outliers."
                )

            if row["Variance"] > self.stats["Variance"].median():

                insights.append(
                    f"{col} shows high variability across observations."
                )

        return insights
    
class RecommendationEngine:

    def __init__(self, df):

        self.df = df

    def recommend(self):

        rec = []

        missing = self.df.isnull().sum()

        if missing.sum() > 0:

            rec.append(
                "Improve data quality by addressing missing values before advanced analysis."
            )

        if self.df.duplicated().sum() > 0:

            rec.append(
                "Remove duplicate records to improve analytical accuracy."
            )

        numeric = self.df.select_dtypes(include=np.number)

        if len(numeric.columns) >= 2:

            corr = numeric.corr().abs().copy()

            # Remove self-correlations
            for i in range(len(corr)):
                corr.iat[i, i] = 0

            strongest = corr.max().max()

            if strongest > 0.8:

                rec.append(
                    f"Strong relationships detected between numerical variables "
                    f"(max correlation: {strongest:.2f}). Consider predictive modeling."
                )

        if len(self.df) > 10000:

            rec.append(
                "Large dataset detected. Consider dashboards and automated monitoring."
            )

        if len(numeric.columns) >= 5:

            rec.append(
                "The dataset contains enough numerical information for forecasting or machine learning."
            )

        return rec