import pandas as pd

df = pd.read_csv("data/ai_job_dataset.csv")  # Change filename if needed

# Convert dates
df["posting_date"] = pd.to_datetime(df["posting_date"])
df["application_deadline"] = pd.to_datetime(df["application_deadline"])

# Extract date features
df["posting_year"] = df["posting_date"].dt.year
df["posting_month"] = df["posting_date"].dt.month_name()
df["posting_day"] = df["posting_date"].dt.day_name()

# Number of required skills
df["skills_count"] = (
    df["required_skills"]
    .str.split(",")
    .apply(len)
)

# Days applications stay open
df["application_days"] = (
    df["application_deadline"] -
    df["posting_date"]
).dt.days

# Save cleaned dataset
df.to_csv("data/ai_jobs_processed.csv", index=False)

print(df.head())
print("\nProcessed dataset saved successfully.")