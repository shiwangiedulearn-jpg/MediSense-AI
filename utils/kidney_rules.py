def analyze_kidney(prediction, probability, values):

    score = 0

    health_effects = []

    diet = []

    lifestyle = []

    medical = []

    bgr = values["bgr"]
    bu = values["bu"]
    sc = values["sc"]
    sod = values["sod"]
    pot = values["pot"]
    hemo = values["hemo"]
    pcv = values["pcv"]
    wc = values["wc"]
    rc = values["rc"]

    if bgr >= 200:
        score += 3
    elif bgr >= 140:
        score += 2

    if bu >= 60:
        score += 3
    elif bu >= 20:
        score += 1

    if sc >= 5:
        score += 4
    elif sc >= 1.3:
        score += 2

    if sod < 135:
        score += 1

    if pot > 5.5:
        score += 2
    elif pot < 3.5:
        score += 1

    if hemo < 10:
        score += 3
    elif hemo < 13:
        score += 1

    if pcv < 30:
        score += 2
    elif pcv < 40:
        score += 1

    if wc > 11000:
        score += 1

    if rc < 4:
        score += 2

    if prediction == 1:
        score += 3

    if score <= 4:

        overall = "Low Kidney Disease Risk"

        summary = (
            "Your kidney-related test values are mostly within the expected range. "
            "Continue maintaining a healthy lifestyle and regular health check-ups."
        )

    elif score <= 9:

        overall = "Moderate Kidney Disease Risk"

        summary = (
            "Some kidney function values are outside the normal range. "
            "Regular monitoring and lifestyle changes are recommended."
        )

    else:

        overall = "High Kidney Disease Risk"

        summary = (
            "Several kidney function values are abnormal and may indicate chronic kidney disease. "
            "Please consult a nephrologist or physician as soon as possible."
        )

    if sc > 1.3:
        health_effects.append(
            "High serum creatinine may indicate reduced kidney function."
        )

    if bu > 20:
        health_effects.append(
            "High blood urea may suggest the kidneys are not removing waste efficiently."
        )

    if hemo < 13:
        health_effects.append(
            "Low hemoglobin may indicate anemia, which is common in chronic kidney disease."
        )

    if pot > 5.5:
        health_effects.append(
            "High potassium levels can affect normal heart rhythm."
        )

    if sod < 135:
        health_effects.append(
            "Low sodium levels may cause weakness, confusion, or fatigue."
        )

    if rc < 4:
        health_effects.append(
            "Low red blood cell count may reduce oxygen supply to body tissues."
        )

    diet.extend([
        "Drink enough water unless your doctor has advised fluid restriction.",
        "Reduce salt intake.",
        "Limit processed and packaged foods.",
        "Choose fresh fruits and vegetables suitable for kidney health.",
        "Avoid excessive protein intake unless recommended by your doctor."
    ])

    lifestyle.extend([
        "Keep your blood pressure under control.",
        "Keep your blood sugar under control if you have diabetes.",
        "Exercise regularly.",
        "Avoid smoking and alcohol.",
        "Take medicines only as prescribed."
    ])

    if score >= 5:

        medical.extend([
            "Consult a kidney specialist (nephrologist).",
            "Repeat kidney function tests if advised.",
            "Monitor kidney function regularly.",
            "Follow all prescribed medications and follow-up visits."
        ])

    return {
        "overall": overall,
        "summary": summary,
        "health_effects": health_effects,
        "diet": diet,
        "lifestyle": lifestyle,
        "medical": medical
    }