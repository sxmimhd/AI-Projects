import pandas as pd
from collections import Counter

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv("data/ai_jobs_processed.csv")

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

average_salary = df["salary_usd"].mean()

highest_paying_role = (
    df.groupby("job_title")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

highest_country = (
    df.groupby("company_location")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .index[0]
)

highest_country_salary = (
    df.groupby("company_location")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .iloc[0]
)

remote_jobs = round(
    (df["remote_ratio"] == 100).mean() * 100,
    1
)

most_common_job = (
    df["job_title"]
    .value_counts()
    .index[0]
)

most_common_education = (
    df["education_required"]
    .mode()[0]
)

# ==========================================================
# SKILLS
# ==========================================================

all_skills = []

for skills in df["required_skills"]:
    for skill in skills.split(","):
        all_skills.append(skill.strip())

skill_counter = Counter(all_skills)

top_skill = skill_counter.most_common(1)[0][0]

salary_per_skill = {}

for _, row in df.iterrows():

    skills = row["required_skills"].split(",")

    for skill in skills:

        skill = skill.strip()

        salary_per_skill.setdefault(skill, []).append(row["salary_usd"])

average_skill_salary = {
    skill: sum(values) / len(values)
    for skill, values in salary_per_skill.items()
}

# ==========================================================
# DASHBOARD
# ==========================================================

fig = make_subplots(

    rows=4,
    cols=3,

    subplot_titles=(

        "Top AI Jobs",
        "Highest Paying Roles",
        "Salary by Experience",

        "Salary by Company Size",
        "Salary by Education",
        "Remote Distribution",

        "Top Hiring Countries",
        "Top Industries",
        "Experience vs Salary",

        "Top Requested Skills",
        "Highest Paying Skills",
        "Benefits Distribution"

    ),

    specs=[

        [{"type":"bar"},{"type":"bar"},{"type":"bar"}],

        [{"type":"bar"},{"type":"bar"},{"type":"pie"}],

        [{"type":"bar"},{"type":"bar"},{"type":"scatter"}],

        [{"type":"bar"},{"type":"bar"},{"type":"histogram"}]

    ],

    vertical_spacing=0.10,
    horizontal_spacing=0.08

)

# ==========================================================
# KPI CARDS
# ==========================================================

fig.add_annotation(

    text=f"<b>Average Salary</b><br>${average_salary:,.0f}",

    x=0.08,
    y=1.12,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

fig.add_annotation(

    text=f"<b>Highest Paying Role</b><br>{highest_paying_role}",

    x=0.32,
    y=1.12,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

fig.add_annotation(

    text=f"<b>Highest Paying Country</b><br>{highest_country}<br>${highest_country_salary:,.0f}",

    x=0.57,
    y=1.12,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

fig.add_annotation(

    text=f"<b>Remote Jobs</b><br>{remote_jobs}%",

    x=0.82,
    y=1.12,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

fig.add_annotation(

    text=f"<b>Top Skill</b><br>{top_skill}",

    x=0.18,
    y=1.04,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

fig.add_annotation(

    text=f"<b>Education</b><br>{most_common_education}",

    x=0.72,
    y=1.04,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(size=16)

)

# ==========================================================
# 1. TOP AI JOBS
# ==========================================================

top_jobs = (
    df["job_title"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig.add_trace(

    go.Bar(

        x=top_jobs.values,
        y=top_jobs.index,
        orientation="h",
        name="Jobs"

    ),

    row=1,
    col=1

)

# ==========================================================
# 2. HIGHEST PAYING ROLES
# ==========================================================

highest_roles = (
    df.groupby("job_title")["salary_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

fig.add_trace(

    go.Bar(

        x=highest_roles.values,
        y=highest_roles.index,
        orientation="h",
        name="Salary"

    ),

    row=1,
    col=2

)

# ==========================================================
# 3. SALARY BY EXPERIENCE
# ==========================================================

experience_salary = (
    df.groupby("experience_level")["salary_usd"]
    .mean()
    .reindex(["EN","MI","SE","EX"])
)

fig.add_trace(

    go.Bar(

        x=experience_salary.index,
        y=experience_salary.values,
        name="Experience"

    ),

    row=1,
    col=3

)

# ==========================================================
# 4. SALARY BY COMPANY SIZE
# ==========================================================

company_salary = (
    df.groupby("company_size")["salary_usd"]
    .mean()
)

fig.add_trace(

    go.Bar(

        x=company_salary.index,
        y=company_salary.values,
        name="Company"

    ),

    row=2,
    col=1

)

# ==========================================================
# 5. SALARY BY EDUCATION
# ==========================================================

education_salary = (
    df.groupby("education_required")["salary_usd"]
    .mean()
)

fig.add_trace(

    go.Bar(

        x=education_salary.index,
        y=education_salary.values,
        name="Education"

    ),

    row=2,
    col=2

)

# ==========================================================
# 6. REMOTE DISTRIBUTION
# ==========================================================

remote = (
    df["remote_ratio"]
    .value_counts()
    .sort_index()
)

labels = []

for value in remote.index:

    if value == 0:
        labels.append("On-site")

    elif value == 50:
        labels.append("Hybrid")

    else:
        labels.append("Remote")

fig.add_trace(

    go.Pie(

        labels=labels,
        values=remote.values,
        hole=0.45,
        showlegend=False

    ),

    row=2,
    col=3

)

# ==========================================================
# 7. TOP HIRING COUNTRIES
# ==========================================================

countries = (
    df["company_location"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig.add_trace(

    go.Bar(

        x=countries.values,
        y=countries.index,
        orientation="h",
        name="Countries"

    ),

    row=3,
    col=1

)

# ==========================================================
# 8. TOP INDUSTRIES
# ==========================================================

industries = (
    df["industry"]
    .value_counts()
    .head(10)
    .sort_values()
)

fig.add_trace(

    go.Bar(

        x=industries.values,
        y=industries.index,
        orientation="h",
        name="Industries"

    ),

    row=3,
    col=2

)

# ==========================================================
# 9. EXPERIENCE VS SALARY
# ==========================================================

fig.add_trace(

    go.Scatter(

        x=df["years_experience"],
        y=df["salary_usd"],

        mode="markers",

        marker=dict(
            size=6,
            opacity=0.5
        ),

        text=df["job_title"],

        hovertemplate=
        "<b>%{text}</b><br>"
        "Experience: %{x} years<br>"
        "Salary: $%{y:,.0f}<extra></extra>"

    ),

    row=3,
    col=3

)

# ==========================================================
# 10. TOP REQUESTED SKILLS
# ==========================================================

skills_df = (
    pd.DataFrame(
        skill_counter.items(),
        columns=["Skill", "Count"]
    )
    .sort_values("Count", ascending=False)
    .head(10)
    .sort_values("Count")
)

fig.add_trace(

    go.Bar(

        x=skills_df["Count"],
        y=skills_df["Skill"],

        orientation="h",

        name="Skills",

        hovertemplate="<b>%{y}</b><br>Requests: %{x}<extra></extra>"

    ),

    row=4,
    col=1

)

# ==========================================================
# 11. HIGHEST PAYING SKILLS
# ==========================================================

salary_df = (
    pd.DataFrame(

        average_skill_salary.items(),

        columns=["Skill", "Average Salary"]

    )

    .sort_values(

        "Average Salary",

        ascending=False

    )

    .head(10)

    .sort_values("Average Salary")

)

fig.add_trace(

    go.Bar(

        x=salary_df["Average Salary"],

        y=salary_df["Skill"],

        orientation="h",

        name="Salary",

        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>"

    ),

    row=4,
    col=2

)

# ==========================================================
# 12. BENEFITS DISTRIBUTION
# ==========================================================

fig.add_trace(

    go.Histogram(

        x=df["benefits_score"],

        nbinsx=20,

        name="Benefits"

    ),

    row=4,
    col=3

)

# ==========================================================
# LAYOUT
# ==========================================================

fig.update_layout(

    title={

        "text":"<b>AI Job Market & Salary Analysis Dashboard</b>",

        "x":0.5,

        "font":{"size":28}

    },

    height=1700,

    width=1800,

    template="plotly_dark",

    showlegend=False,

    margin=dict(

        t=180,

        l=40,

        r=40,

        b=40

    )

)

# ==========================================================
# AXES
# ==========================================================

fig.update_xaxes(showgrid=True)

fig.update_yaxes(showgrid=True)

# ==========================================================
# EXPORT
# ==========================================================

fig.write_html(

    "images/executive_dashboard.html",

    include_plotlyjs="cdn"

)

# Optional static image (requires: pip install kaleido)
try:
    fig.write_image(
        "images/executive_dashboard.png",
        width=1800,
        height=1700,
        scale=2
    )
except Exception:
    print("PNG export skipped (install 'kaleido' if you want PNG export).")

# ==========================================================
# SHOW
# ==========================================================

fig.show()

print("\nDashboard created successfully!")
print("Saved to:")
print(" - images/executive_dashboard.html")
print(" - images/executive_dashboard.png (if kaleido is installed)")