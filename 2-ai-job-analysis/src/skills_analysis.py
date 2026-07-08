import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_csv("data/ai_jobs_processed.csv")

# Count Individual Skills

all_skills = []

for skills in df["required_skills"]:
    for skill in skills.split(","):
        all_skills.append(skill.strip())

skill_counts = Counter(all_skills)

skills_df = (
    pd.DataFrame(
        skill_counts.items(),
        columns=["Skill", "Count"]
    )
    .sort_values("Count", ascending=False)
)

print(skills_df.head(20))

# Top 20 Skills

top20 = skills_df.head(20)

plt.figure(figsize=(10,8))

plt.barh(
    top20["Skill"][::-1],
    top20["Count"][::-1]
)

plt.title("Top 20 Most Requested AI Skills")
plt.xlabel("Frequency")

plt.tight_layout()

plt.savefig("images/top_skills.png")

plt.show()

# Highest Paying Skills

salary_per_skill = {}

for _, row in df.iterrows():

    skills = row["required_skills"].split(",")

    for skill in skills:

        skill = skill.strip()

        salary_per_skill.setdefault(skill, []).append(row["salary_usd"])

avg_salary_skill = {
    skill: sum(values) / len(values)
    for skill, values in salary_per_skill.items()
}

salary_df = (
    pd.DataFrame(
        avg_salary_skill.items(),
        columns=["Skill", "Average Salary"]
    )
    .sort_values("Average Salary", ascending=False)
)

print(salary_df.head(20))

top_salary = salary_df.head(20)

plt.figure(figsize=(10,8))

plt.barh(
    top_salary["Skill"][::-1],
    top_salary["Average Salary"][::-1]
)

plt.title("Highest Paying Skills")

plt.xlabel("Average Salary (USD)")

plt.tight_layout()

plt.savefig("images/highest_paying_skills.png")

plt.show()