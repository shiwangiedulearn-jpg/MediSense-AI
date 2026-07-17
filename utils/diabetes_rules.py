def analyze_diabetes(prediction, probability, values):

    score = 0

    health_effects = []

    diet = []

    lifestyle = []

    medical = []

    glucose = values["Glucose"]
    bmi = values["BMI"]
    age = values["Age"]
    dpf = values["DiabetesPedigreeFunction"]
    pregnancies = values["Pregnancies"]    


    if glucose >= 200:

        score += 4

    elif glucose >= 126:

        score += 3

    elif glucose >= 100:

        score += 1



    if bmi >= 35:

        score += 3

    elif bmi >= 30:

        score += 2

    elif bmi >= 25:

        score += 1



    if age >= 60:

        score += 2

    elif age >= 45:

        score += 1



    if dpf >= 1:

        score += 2

    elif dpf >= 0.5:

        score += 1



    if pregnancies >= 5:

        score += 1

    if prediction == 1:

        score += 3



    if probability >= 80:

        score += 2

    elif probability >= 60:

        score += 1



    if score <= 3:

        overall = "Low Diabetes Risk"

        summary = (
            "Your blood sugar and other risk factors are generally within a healthy range. "
            "Continue maintaining a healthy lifestyle."
        )

    elif score <= 7:

        overall = "Moderate Diabetes Risk"

        summary = (
            "Some of your values suggest an increased risk of diabetes. "
            "Healthy lifestyle changes and regular monitoring are recommended."
        )

    else:

        overall = "High Diabetes Risk"

        summary = (
            "Several factors indicate a high likelihood of diabetes. "
            "Consult a healthcare professional for further evaluation and testing."
        )

    # Health Effects

    if glucose >= 126:

        health_effects.append(
            "Your blood sugar level is higher than the normal range, which may indicate diabetes or poor blood sugar control."
        )

    if bmi >= 30:

        health_effects.append(
            "A high BMI can reduce the body's ability to use insulin effectively (insulin resistance)."
        )

    if age >= 45:

        health_effects.append(
            "The risk of developing Type 2 diabetes increases with age."
        )

    if dpf >= 0.5:

        health_effects.append(
            "A family history of diabetes may increase your overall risk."
        )

    if prediction == 1:

        health_effects.append(
            "The machine learning model predicts an increased likelihood of diabetes based on the provided information."
        )

    # Diet Recommendations

    if glucose >= 100:

        diet.extend([
            "Reduce sugary foods, sweets and sweetened beverages.",
            "Choose whole grains instead of refined carbohydrates.",
            "Increase fibre-rich foods such as vegetables, fruits and legumes."
        ])

    if bmi >= 25:

        diet.extend([
            "Reduce high-calorie and processed foods.",
            "Control portion sizes to maintain a healthy weight."
        ])

    if prediction == 1:

        diet.extend([
            "Choose low glycemic index (GI) foods.",
            "Limit foods high in saturated fat and trans fat."
        ])

    # Remove duplicate recommendations

    diet = list(dict.fromkeys(diet))

    # Lifestyle Recommendations

    if glucose >= 100 or prediction == 1:

        lifestyle.extend([
            "Engage in at least 150 minutes of moderate physical activity every week.",
            "Monitor your blood sugar levels regularly as advised by your healthcare provider.",
            "Maintain a healthy body weight through regular exercise and balanced nutrition."
        ])

    if bmi >= 25:

        lifestyle.append(
            "Aim for gradual weight loss if you are overweight or obese."
        )

    if age >= 45:

        lifestyle.append(
            "Schedule regular health check-ups to monitor your blood sugar and overall health."
        )


    lifestyle = list(dict.fromkeys(lifestyle))

    # Medical Advice

    if prediction == 1 or glucose >= 126:

        medical.extend([
            "Consult a healthcare professional for a comprehensive diabetes evaluation.",
            "Get an HbA1c test to assess your average blood sugar levels over the past 2–3 months.",
            "Monitor your fasting and post-meal blood glucose levels regularly."
        ])

    if bmi >= 30:

        medical.append(
            "Discuss a personalized weight management plan with your healthcare provider."
        )

    if age >= 45:

        medical.append(
            "Schedule regular diabetes screening and routine health check-ups."
        )

   

    medical = list(dict.fromkeys(medical))

    return {

        "overall": overall,

        "summary": summary,

        "score": score,

        "probability": probability,

        "health_effects": health_effects,

        "diet": diet,

        "lifestyle": lifestyle,

        "medical": medical

    }

        

