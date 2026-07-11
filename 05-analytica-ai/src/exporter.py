import pandas as pd
from openpyxl import Workbook
import sqlite3
import os


EXPORT_FOLDER = "exports"

os.makedirs(EXPORT_FOLDER, exist_ok=True)


def export_csv(df):

    path = f"{EXPORT_FOLDER}/cleaned_dataset.csv"

    df.to_csv(path, index=False)

    return path


def export_excel(stats):

    path = f"{EXPORT_FOLDER}/statistics.xlsx"

    wb = Workbook()

    ws = wb.active

    ws.title = "Statistics"

    ws.append(stats.columns.tolist())

    for row in stats.itertuples(index=False):

        ws.append(list(row))

    wb.save(path)

    return path


def export_sqlite(df):

    path = f"{EXPORT_FOLDER}/analysis.db"

    conn = sqlite3.connect(path)

    df.to_sql(
        "dataset",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    return path


def export_html(profile, stats, insights, recommendations):

    path = f"{EXPORT_FOLDER}/report.html"

    html = f"""

    <html>

    <head>

        <title>Analytica AI Report</title>

    </head>

    <body style="font-family:Arial;padding:40px;">

    <h1>Analytica AI Executive Report</h1>

    <hr>

    <h2>Dataset Overview</h2>

    <ul>

        <li>Rows : {profile['rows']}</li>

        <li>Columns : {profile['columns']}</li>

        <li>Missing : {profile['missing']}</li>

        <li>Duplicates : {profile['duplicates']}</li>

    </ul>

    <h2>Statistics</h2>

    {stats.to_html(index=False)}

    <h2>AI Insights</h2>

    <ul>

    """

    for i in insights:

        html += f"<li>{i}</li>"

    html += "</ul><h2>Business Recommendations</h2><ul>"

    for r in recommendations:

        html += f"<li>{r}</li>"

    html += """

    </ul>

    </body>

    </html>

    """

    with open(path, "w", encoding="utf-8") as f:

        f.write(html)

    return path