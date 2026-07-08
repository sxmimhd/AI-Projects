import pandas as pd


def data_quality_report(df):

    report = {}

    # Missing values
    missing = df.isnull().sum()

    report["missing"] = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values,
        "Missing %": (missing.values / len(df) * 100).round(2)
    }).sort_values("Missing %", ascending=False)

    # Duplicate rows
    report["duplicates"] = int(df.duplicated().sum())

    # Empty columns
    report["empty_columns"] = list(
        df.columns[df.isnull().all()]
    )

    # Constant columns
    report["constant_columns"] = list(
        df.columns[df.nunique(dropna=False) <= 1]
    )

    # Data types
    report["dtypes"] = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str)
    })

    return report
def remove_duplicates(df):
    return df.drop_duplicates()


def fill_missing(df):

    new_df = df.copy()

    for col in new_df.columns:

        if new_df[col].dtype == "object":

            mode = new_df[col].mode()

            if len(mode):
                new_df[col] = new_df[col].fillna(mode[0])

        else:

            new_df[col] = new_df[col].fillna(
                new_df[col].median()
            )

    return new_df


def drop_empty_columns(df):

    return df.dropna(axis=1, how="all")