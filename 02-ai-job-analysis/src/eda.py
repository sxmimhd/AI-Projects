import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/ai_jobs_processed.csv")

plt.style.use("ggplot")

# Most Common AI Jobs

top_jobs = df["job_title"].value_counts().head(10)

plt.figure(figsize=(10,6))
top_jobs.sort_values().plot(kind="barh")
plt.title("Top 10 AI Job Titles")
plt.xlabel("Number of Jobs")
plt.tight_layout()
plt.savefig("images/top_jobs.png")
plt.show()

# Highest Paying Roles

salary_roles = (
    df.groupby("job_title")["salary_usd"]
      .mean()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(10,6))
salary_roles.sort_values().plot(kind="barh")
plt.title("Highest Paying AI Roles")
plt.xlabel("Average Salary (USD)")
plt.tight_layout()
plt.savefig("images/highest_paying_roles.png")
plt.show()

# Salary by Experience

experience_salary = (
    df.groupby("experience_level")["salary_usd"]
      .mean()
)

plt.figure(figsize=(8,5))
experience_salary.plot(kind="bar")
plt.title("Salary by Experience Level")
plt.ylabel("Average Salary")
plt.tight_layout()
plt.savefig("images/salary_experience.png")
plt.show()

# Salary by Company Size

company_salary = (
    df.groupby("company_size")["salary_usd"]
      .mean()
)

plt.figure(figsize=(8,5))
company_salary.plot(kind="bar")
plt.title("Salary by Company Size")
plt.ylabel("Average Salary")
plt.tight_layout()
plt.savefig("images/company_size_salary.png")
plt.show()

# 5. Salary by Education

education_salary = (
    df.groupby("education_required")["salary_usd"]
      .mean()
)

plt.figure(figsize=(8,5))
education_salary.plot(kind="bar")
plt.title("Salary by Education")
plt.ylabel("Average Salary")
plt.tight_layout()
plt.savefig("images/education_salary.png")
plt.show()

# Remote Ratio

remote = df["remote_ratio"].value_counts().sort_index()

plt.figure(figsize=(7,7))
plt.pie(remote.values,
        labels=remote.index,
        autopct="%1.1f%%")
plt.title("Remote Work Distribution")
plt.savefig("images/remote_ratio.png")
plt.show()

# Top Hiring Countries

countries = df["company_location"].value_counts().head(10)

plt.figure(figsize=(10,6))
countries.sort_values().plot(kind="barh")
plt.title("Top Hiring Countries")
plt.tight_layout()
plt.savefig("images/top_countries.png")
plt.show()

# Top Industries

industries = df["industry"].value_counts().head(10)

plt.figure(figsize=(10,6))
industries.sort_values().plot(kind="barh")
plt.title("Top Industries")
plt.tight_layout()
plt.savefig("images/top_industries.png")
plt.show()

# 9. Experience vs Salary

plt.figure(figsize=(8,6))
plt.scatter(df["years_experience"],
            df["salary_usd"],
            alpha=0.3)

plt.title("Experience vs Salary")
plt.xlabel("Years of Experience")
plt.ylabel("Salary (USD)")
plt.tight_layout()
plt.savefig("images/experience_salary_scatter.png")
plt.show()

# 10. Benefits Score Distribution

plt.figure(figsize=(8,5))
plt.hist(df["benefits_score"], bins=20)
plt.title("Benefits Score Distribution")
plt.tight_layout()
plt.savefig("images/benefits_distribution.png")
plt.show()