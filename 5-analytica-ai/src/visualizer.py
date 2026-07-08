import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff


class Visualizer:

    def __init__(self, df):

        self.df = df

        self.numeric_cols = df.select_dtypes(include="number").columns.tolist()

        self.categorical_cols = df.select_dtypes(include="object").columns.tolist()

        self.datetime_cols = [

            c for c in df.columns

            if "date" in c.lower()

            or "time" in c.lower()

            or pd.api.types.is_datetime64_any_dtype(df[c])

        ]

    # ---------------------------------------------------------
    # Histograms
    # ---------------------------------------------------------

    def histograms(self):

        figs = []

        for col in self.numeric_cols[:6]:

            fig = px.histogram(

                self.df,

                x=col,

                nbins=40,

                title=f"{col} Distribution"

            )

            figs.append(fig)

        return figs

    # ---------------------------------------------------------
    # Boxplots
    # ---------------------------------------------------------

    def boxplots(self):

        figs = []

        for col in self.numeric_cols[:6]:

            fig = px.box(

                self.df,

                y=col,

                title=f"{col} Boxplot"

            )

            figs.append(fig)

        return figs

    # ---------------------------------------------------------
    # Bar Charts
    # ---------------------------------------------------------

    def categorical(self):

        figs = []

        for col in self.categorical_cols[:5]:

            counts = (

                self.df[col]

                .dropna()

                .value_counts()

                .head(10)

                .reset_index()

            )

            if counts.empty:
                continue

            counts.columns = [col, "Count"]

            fig = px.bar(

                counts,

                x=col,

                y="Count",

                title=f"Top {col}"

            )

            figs.append(fig)

        return figs

    # ---------------------------------------------------------
    # Pie Charts
    # ---------------------------------------------------------

    def pies(self):

        figs = []

        for col in self.categorical_cols[:3]:

            counts = (

                self.df[col]

                .dropna()

                .value_counts()

                .head(8)

                .reset_index()

            )

            if counts.empty:
                continue

            counts.columns = [col, "Count"]

            fig = px.pie(

                counts,

                names=col,

                values="Count",

                hole=0.45,

                title=f"{col} Share"

            )

            figs.append(fig)

        return figs

    # ---------------------------------------------------------
    # Scatter Plots
    # ---------------------------------------------------------

    def scatter(self):

        figs = []

        if len(self.numeric_cols) < 2:
            return figs

        cols = self.numeric_cols[:4]

        for i in range(len(cols) - 1):

            fig = px.scatter(

                self.df,

                x=cols[i],

                y=cols[i + 1],

                title=f"{cols[i]} vs {cols[i + 1]}"

            )

            figs.append(fig)

        return figs

    # ---------------------------------------------------------
    # Correlation Heatmap
    # ---------------------------------------------------------

    def correlation(self):

        if len(self.numeric_cols) < 2:
            return None

        corr = self.df[self.numeric_cols].corr().round(2)

        fig = ff.create_annotated_heatmap(

            z=corr.values,

            x=list(corr.columns),

            y=list(corr.index),

            annotation_text=corr.values,

            colorscale="Viridis",

            showscale=True

        )

        fig.update_layout(

            title="Correlation Heatmap",

            height=700

        )

        return fig

    # ---------------------------------------------------------
    # Timeline
    # ---------------------------------------------------------

    def timeline(self):

        if len(self.datetime_cols) == 0:
            return None

        date_col = self.datetime_cols[0]

        temp = self.df.copy()

        temp[date_col] = pd.to_datetime(

            temp[date_col],

            errors="coerce"

        )

        temp = temp.dropna(subset=[date_col])

        if temp.empty:
            return None

        yearly = (

            temp

            .groupby(temp[date_col].dt.year)

            .size()

            .reset_index(name="Count")

        )

        yearly.columns = ["Year", "Count"]

        fig = px.line(

            yearly,

            x="Year",

            y="Count",

            markers=True,

            title="Timeline"

        )

        return fig