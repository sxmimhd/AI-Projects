def detect_dataset_type(df):

    columns = [c.lower() for c in df.columns]

    sales = [
        "sales",
        "revenue",
        "profit",
        "customer",
        "order",
        "product"
    ]

    hr = [
        "employee",
        "salary",
        "department",
        "hire"
    ]

    healthcare = [
        "patient",
        "diagnosis",
        "hospital",
        "blood"
    ]

    gaming = [
        "game",
        "steam",
        "genre",
        "platform",
        "publisher"
    ]

    ai = [
        "salary_usd",
        "experience",
        "job",
        "skills"
    ]

    netflix = [
        "director",
        "cast",
        "listed_in",
        "duration"
    ]

    checks = {

        "Sales": sales,

        "HR": hr,

        "Healthcare": healthcare,

        "Gaming": gaming,

        "AI Jobs": ai,

        "Streaming": netflix

    }

    scores = {}

    for dataset, keywords in checks.items():

        score = 0

        for col in columns:

            for keyword in keywords:

                if keyword in col:

                    score += 1

        scores[dataset] = score

    best = max(scores, key=scores.get)

    if scores[best] == 0:

        return "Generic"

    return best