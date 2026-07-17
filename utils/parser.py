import re

def extract_values(text):

    values = {}

    patterns = {

        "chol": [
            r"Serum\s*Cholesterol\s*:?\s*(\d+\.?\d*)",
            r"Total\s*Cholesterol\s*:?\s*(\d+\.?\d*)",
            r"Cholesterol\s*:?\s*(\d+\.?\d*)"
        ],

        "trestbps": [
            r"Resting\s*Blood\s*Pressure\s*:?\s*(\d+)",
            r"Blood\s*Pressure\s*:?\s*(\d+)"
        ],

        "thalach": [
            r"Maximum\s*Heart\s*Rate\s*Achieved\s*:?\s*(\d+)",
            r"Max(?:imum)?\s*Heart\s*Rate\s*:?\s*(\d+)"
        ],

        "oldpeak": [
            r"Oldpeak\s*:?\s*(\d+\.?\d*)",
            r"ST\s*Depression\s*\(Oldpeak\)\s*:?\s*(\d+\.?\d*)"
        ],

        "ca": [
            r"Number\s*of\s*Major\s*Vessels.*?:?\s*(\d+)",
            r"Major\s*Vessels.*?:?\s*(\d+)"
        ]

    }

    for feature, pattern_list in patterns.items():

        for pattern in pattern_list:

            match = re.search(pattern, text, re.IGNORECASE)

            if match:

                number = match.group(1)

                if "." in number:
                    values[feature] = float(number)
                else:
                    values[feature] = int(number)

                break

    if re.search(r"Fasting\s*Blood\s*Sugar.*Yes", text, re.IGNORECASE):
        values["fbs"] = 1
    elif re.search(r"Fasting\s*Blood\s*Sugar.*No", text, re.IGNORECASE):
        values["fbs"] = 0

    if re.search(r"Exercise.*Angina.*Yes", text, re.IGNORECASE):
        values["exang"] = 1
    elif re.search(r"Exercise.*Angina.*No", text, re.IGNORECASE):
        values["exang"] = 0

    if re.search(r"Resting\s*ECG.*ST[- ]?T", text, re.IGNORECASE):
        values["restecg"] = 1
    elif re.search(r"Resting\s*ECG.*Hypertrophy", text, re.IGNORECASE):
        values["restecg"] = 2
    elif re.search(r"Resting\s*ECG.*Normal", text, re.IGNORECASE):
        values["restecg"] = 0
    if re.search(r"Slope.*Upsloping", text, re.IGNORECASE):
        values["slope"] = 0
    elif re.search(r"Slope.*Flat", text, re.IGNORECASE):
        values["slope"] = 1
    elif re.search(r"Slope.*Downsloping", text, re.IGNORECASE):
        values["slope"] = 2

    if re.search(r"Thal.*Normal", text, re.IGNORECASE):
        values["thal"] = 1
    elif re.search(r"Thal.*Fixed", text, re.IGNORECASE):
        values["thal"] = 2
    elif re.search(r"Thal.*Reversible", text, re.IGNORECASE):
        values["thal"] = 3

    if re.search(r"Typical\s*Angina", text, re.IGNORECASE):
        values["cp"] = 0
    elif re.search(r"Atypical\s*Angina", text, re.IGNORECASE):
        values["cp"] = 1
    elif re.search(r"Non[- ]?Anginal", text, re.IGNORECASE):
        values["cp"] = 2
    elif re.search(r"Asymptomatic", text, re.IGNORECASE):
        values["cp"] = 3

    return values