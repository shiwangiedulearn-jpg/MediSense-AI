import re


def extract_diabetes_values(text):

    values = {
        "Pregnancies": 0,
        "Glucose": 120,
        "BloodPressure": 80,
        "SkinThickness": 20,
        "Insulin": 80,
        "BMI": 0,
        "DiabetesPedigreeFunction": 0.47
    }
    lines = text.split("\n")

    for line in lines:

        line_lower = line.lower()

        numbers = re.findall(r"\d+\.?\d*", line)

        if not numbers:
            continue
        

        value = float(numbers[0])

        if (
            (
                "fasting blood glucose" in line_lower
                or "fasting glucose" in line_lower
                or "fasting blood sugar" in line_lower
                or "fbs" in line_lower
            )
            and "mg/dl" in line_lower
        ):
            values["Glucose"] = float(numbers[0])


        elif (
            "blood pressure" in line_lower
            or "bp" in line_lower
        ):

            values["BloodPressure"] = value

        elif "bmi" in line_lower:

            values["BMI"] = value      

        elif "insulin" in line_lower:

            values["Insulin"] = value
       
    print("final values",values)
    return values