import pandas as pd
import numpy as np


def statistics_report(df):

    numeric = df.select_dtypes(include=np.number)

    reports = []

    for col in numeric.columns:

        s = numeric[col].dropna()

        if len(s) == 0:
            continue

        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = ((s < lower) | (s > upper)).sum()

        mode = s.mode()

        reports.append({

            "Column": col,

            "Mean": round(s.mean(), 2),

            "Median": round(s.median(), 2),

            "Mode": round(mode.iloc[0], 2) if len(mode) else np.nan,

            "Std": round(s.std(), 2),

            "Variance": round(s.var(), 2),

            "Minimum": round(s.min(), 2),

            "Q1": round(q1, 2),

            "Q3": round(q3, 2),

            "Maximum": round(s.max(), 2),

            "IQR": round(iqr, 2),

            "Skewness": round(s.skew(), 2),

            "Kurtosis": round(s.kurt(), 2),

            "Outliers": int(outliers)

        })

    return pd.DataFrame(reports)