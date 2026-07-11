import pandas as pd


def load_dataset(uploaded_file):
    """
    Load CSV file safely.
    """

    try:
        df = pd.read_csv(uploaded_file)

        return df, None

    except Exception as e:
        return None, str(e)