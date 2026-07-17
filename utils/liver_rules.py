def analyze_liver(prediction, probability, values):

    score = 0

    health_effects = []

    diet = []

    lifestyle = []

    medical = []

    bilirubin = values["tot_bilirubin"]
    direct_bilirubin = values["direct_bilirubin"]
    sgpt = values["sgpt"]
    sgot = values["sgot"]
    alkphos = values["alkphos"]
    albumin = values["albumin"]
    proteins = values["tot_proteins"]
    ag_ratio = values["ag_ratio"]

    if bilirubin > 3:
        score += 3
    elif bilirubin > 1.2:
        score += 2

    if direct_bilirubin > 1:
        score += 2
    elif direct_bilirubin > 0.3:
        score += 1

    if sgpt > 200:
        score += 3
    elif sgpt > 56:
        score += 2

    if sgot > 200:
        score += 3
    elif sgot > 40:
        score += 2

    if alkphos > 300:
        score += 2
    elif alkphos > 147:
        score += 1

    if albumin < 3.5:
        score += 2

    if proteins < 6.0:
        score += 1

    if ag_ratio < 1:
        score += 2

    if prediction == 1:
        score += 3

    if score <= 4:

        overall = "Healthy Liver"

        summary = (
            "Your liver function values are largely within the normal range. "
            "Maintain a healthy lifestyle and continue regular health check-ups."
        )

    elif score <= 9:

        overall = "Moderate Liver Risk"

        summary = (
            "Some liver function parameters are outside the normal range. "
            "Further monitoring and healthy lifestyle changes are recommended."
        )

    else:

        overall = "High Liver Disease Risk"

        summary = (
            "Multiple liver function tests are abnormal and indicate a high risk of liver disease. "
            "Medical evaluation is strongly recommended."
        )

    if bilirubin > 1.2:

        health_effects.append(
            "High bilirubin may indicate jaundice or impaired liver function."
        )

    if sgpt > 56 or sgot > 40:

        health_effects.append(
            "Elevated liver enzymes may indicate liver inflammation or liver cell injury."
        )

    if alkphos > 147:

        health_effects.append(
            "High alkaline phosphatase may suggest bile duct obstruction or liver disease."
        )

    if albumin < 3.5:

        health_effects.append(
            "Low albumin may indicate reduced liver protein synthesis."
        )

    diet.extend([
        "Eat plenty of fresh fruits and green leafy vegetables.",
        "Choose whole grains instead of refined carbohydrates.",
        "Limit fried, oily and processed foods.",
        "Drink adequate water throughout the day.",
        "Reduce sugary beverages and packaged foods."
    ])

    lifestyle.extend([
        "Avoid alcohol consumption.",
        "Exercise regularly for at least 30 minutes daily.",
        "Maintain a healthy body weight.",
        "Avoid unnecessary medications unless prescribed.",
        "Sleep 7–8 hours every night."
    ])

    if score >= 5:

        medical.extend([
            "Consult a gastroenterologist or physician.",
            "Repeat liver function tests if advised.",
            "Ultrasound abdomen may be recommended.",
            "Follow prescribed medications and attend follow-up visits."
        ])

    return {
        "overall": overall,
        "summary": summary,
        "health_effects": health_effects,
        "diet": diet,
        "lifestyle": lifestyle,
        "medical": medical
    }