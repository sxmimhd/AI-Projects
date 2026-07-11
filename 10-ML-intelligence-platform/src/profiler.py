import pandas as pd


class DatasetProfiler:

    def __init__(self, dataset: pd.DataFrame):

        self.dataset = dataset

        self.numeric = dataset.select_dtypes(include="number")

        self.statistics = None
        self.correlation = None
        self.skewness = None
        self.kurtosis = None
        self.outliers = None

    def profile(self):

        self._statistics()

        self._correlation()

        self._skewness()

        self._kurtosis()

        self._outliers()

    def _statistics(self):

        self.statistics = self.numeric.describe().T

    def _correlation(self):

        self.correlation = self.numeric.corr(numeric_only=True)

    def _skewness(self):

        self.skewness = self.numeric.skew()

    def _kurtosis(self):

        self.kurtosis = self.numeric.kurt()

    def _outliers(self):

        results = {}

        for column in self.numeric.columns:

            q1 = self.numeric[column].quantile(0.25)

            q3 = self.numeric[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr

            upper = q3 + 1.5 * iqr

            count = (
                (self.numeric[column] < lower)
                |
                (self.numeric[column] > upper)
            ).sum()

            results[column] = count

        self.outliers = pd.Series(results)