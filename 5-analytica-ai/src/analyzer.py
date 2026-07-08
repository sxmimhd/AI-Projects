import pandas as pd


def dataset_profile(df):

    profile = {

        "rows": len(df),

        "columns": len(df.columns),

        "missing": int(df.isna().sum().sum()),

        "duplicates": int(df.duplicated().sum()),

        "memory": round(df.memory_usage(deep=True).sum() / 1024**2, 2),

        "numeric":

            len(
                df.select_dtypes(include="number").columns
            ),

        "categorical":

            len(
                df.select_dtypes(include="object").columns
            ),

        "datetime":

            len(
                df.select_dtypes(include="datetime").columns
            )

    }

    return profile