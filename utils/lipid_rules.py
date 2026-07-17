def analyze_total_cholesterol(value):

    if value < 200:
        return {
            "value": value,
            "range": "< 200 mg/dL",
            "status": "Healthy",
            "score": 0
        }

    elif value <= 239:
        return {
            "value": value,
            "range": "200 - 239 mg/dL",
            "status": "Borderline High",
            "score": 1
        }

    else:
        return {
            "value": value,
            "range": "≥ 240 mg/dL",
            "status": "High",
            "score": 2
        }


def analyze_hdl(value, gender):

    if gender == 1:

        if value < 40:
            return {
                "value": value,
                "range": "≥ 40 mg/dL",
                "status": "Low",
                "score": 2
            }

        elif value < 60:
            return {
                "value": value,
                "range": "40 - 59 mg/dL",
                "status": "Healthy",
                "score": 0
            }

        else:
            return {
                "value": value,
                "range": "≥ 60 mg/dL",
                "status": "Protective",
                "score": 0
            }

    else:

        if value < 50:
            return {
                "value": value,
                "range": "≥ 50 mg/dL",
                "status": "Low",
                "score": 2
            }

        elif value < 60:
            return {
                "value": value,
                "range": "50 - 59 mg/dL",
                "status": "Healthy",
                "score": 0
            }

        else:
            return {
                "value": value,
                "range": "≥ 60 mg/dL",
                "status": "Protective",
                "score": 0
            }

def analyze_ldl(value):

    if value < 100:
        return {
            "value": value,
            "range": "< 100 mg/dL",
            "status": "Healthy",
            "score": 0
        }

    elif value <= 129:
        return {
            "value": value,
            "range": "100 - 129 mg/dL",
            "status": "Near Healthy",
            "score": 1
        }

    elif value <= 159:
        return {
            "value": value,
            "range": "130 - 159 mg/dL",
            "status": "Borderline High",
            "score": 2
        }

    elif value <= 189:
        return {
            "value": value,
            "range": "160 - 189 mg/dL",
            "status": "High",
            "score": 3
        }

    else:
        return {
            "value": value,
            "range": "≥ 190 mg/dL",
            "status": "Very High",
            "score": 4
        }

def analyze_triglycerides(value):

    if value < 150:
        return {
            "value": value,
            "range": "< 150 mg/dL",
            "status": "Healthy",
            "score": 0
        }

    elif value <= 199:
        return {
            "value": value,
            "range": "150 - 199 mg/dL",
            "status": "Borderline High",
            "score": 1
        }

    elif value <= 499:
        return {
            "value": value,
            "range": "200 - 499 mg/dL",
            "status": "High",
            "score": 3
        }

    else:
        return {
            "value": value,
            "range": "≥ 500 mg/dL",
            "status": "Very High",
            "score": 4
        }

def analyze_vldl(value):

    if value <= 40:
        return {
            "value": value,
            "range": "≤ 40 mg/dL",
            "status": "Healthy",
            "score": 0
        }

    else:
        return {
            "value": value,
            "range": "> 40 mg/dL",
            "status": "High",
            "score": 1
        }

def analyze_total_lipids(value):

    if value <= 600:
        return {
            "value": value,
            "range": "≤ 600 mg/dL",
            "status": "Healthy",
            "score": 0
        }

    else:
        return {
            "value": value,
            "range": "> 600 mg/dL",
            "status": "High",
            "score": 0
        }

def analyze_lipid_profile(values):

    results = {}

    results["Total Cholesterol"] = analyze_total_cholesterol(
        values["total_cholesterol"]
    )

    results["HDL Cholesterol"] = analyze_hdl(
        values["hdl"],
        values["gender"]
    )

    results["LDL Cholesterol"] = analyze_ldl(
        values["ldl"]
    )

    results["Triglycerides"] = analyze_triglycerides(
        values["triglycerides"]
    )

    results["VLDL Cholesterol"] = analyze_vldl(
        values["vldl"]
    )

    results["Serum Total Lipids"] = analyze_total_lipids(
        values["total_lipids"]
    )

    
    total_score = 0

    for test in results.values():
        total_score += test["score"]

   
    if total_score <= 2:

        overall = "Healthy Lipid Profile"
        summary = (
           "Your cholesterol and blood fat levels are generally within healthy limits. "
           "Maintain a balanced diet and an active lifestyle."
    )

    elif total_score <= 6:

        overall = "Some Lipid Levels Need Attention"
        summary = (
           "Some of your cholesterol or blood fat levels are outside the healthy range. "
           "Lifestyle changes and regular follow-up are recommended."
    )

    else:

        overall = "High Risk of Future Heart Problems"
        summary = (
           "Several cholesterol values are significantly outside the healthy range. "
           "This may increase your risk of future heart problems. "
           "Consult a healthcare professional for further evaluation."
    )

    
    health_effects = []

    if results["Total Cholesterol"]["status"] in ["Borderline High", "High"]:

        health_effects.append(
            "High cholesterol may slowly build up inside your blood vessels."
        )


    if results["LDL Cholesterol"]["status"] in ["Borderline High", "High", "Very High"]:

        health_effects.append(
            "High LDL ('bad cholesterol') may increase the chance of heart attack or stroke over time."
        )


    if results["HDL Cholesterol"]["status"] == "Low":

        health_effects.append(
            "Your body may remove less bad cholesterol from your blood."
        )


    if results["Triglycerides"]["status"] in ["Borderline High", "High", "Very High"]:

        health_effects.append(
            "High triglycerides may increase the risk of heart problems."
        )


    if results["VLDL Cholesterol"]["status"] == "High":

        health_effects.append(
           "Extra fat may gradually build up inside your blood vessels."
        )


    if results["Serum Total Lipids"]["status"] == "High":

        health_effects.append(
           "Your blood contains a higher than normal amount of fats."
        )


    diet = []
    lifestyle = []
    medical = []


    if results["Total Cholesterol"]["status"] in ["Borderline High", "High"]:

        diet.extend([
            "Reduce fried and oily foods.",
            "Eat more fruits and vegetables.",
            "Increase fibre-rich foods."
        ])

    if results["LDL Cholesterol"]["status"] in ["Borderline High", "High", "Very High"]:

        diet.extend([
            "Reduce saturated fats such as butter and processed foods.",
            "Choose whole grains and oats."
        ])

    if results["Triglycerides"]["status"] in ["Borderline High", "High", "Very High"]:

        diet.extend([
            "Reduce sugary foods and sweetened drinks.",
            "Limit alcohol consumption."
        ])


    if total_score > 2:

        lifestyle.extend([
            "Walk or exercise for at least 30 minutes most days.",
            "Maintain a healthy body weight.",
            "Avoid smoking."
        ])

    if total_score > 6:

        medical.extend([
            "Consult a healthcare professional.",
            "Repeat your lipid profile as advised.",
            "Follow prescribed medications if recommended."
        ])

    

    
    diet = list(dict.fromkeys(diet))

    lifestyle = list(dict.fromkeys(lifestyle))

    medical = list(dict.fromkeys(medical))

    return {

        "results": results,

        "score": total_score,

        "overall": overall,

        "summary": summary,

        "health_effects": health_effects,

        "diet": diet,

        "lifestyle": lifestyle,

        "medical": medical

    }

