import re


def extract_kidney_values(text):

    values = {}

    lines = text.split("\n")

    for line in lines:

        line_lower = line.lower()

        numbers = re.findall(r"\d+\.?\d*", line)

        if not numbers:
            continue

        value = float(numbers[0])

        if (
            "blood glucose random" in line_lower
            or "random blood sugar" in line_lower
            or "random glucose" in line_lower
            or "bgr" in line_lower
        ):

            values["bgr"] = value

        elif (
            "blood urea" in line_lower
            or "urea" in line_lower
            or "bu" in line_lower
        ):

            values["bu"] = value

        elif (
            "serum creatinine" in line_lower
            or "creatinine" in line_lower
            or "sc" in line_lower
        ):

            values["sc"] = value

        elif (
            "sodium" in line_lower
            
        ):

            values["sod"] = value

        elif (
            "potassium" in line_lower
            
        ):

            values["pot"] = value

        elif (
            "hemoglobin" in line_lower
            or "haemoglobin" in line_lower
            or "hb" in line_lower
            or "hemo" in line_lower
        ):

            values["hemo"] = value

        elif (
            "packed cell volume" in line_lower
            or "pcv" in line_lower
        ):

            values["pcv"] = value

        elif (
            "white blood cell" in line_lower
            or "wbc" in line_lower
            or "white cell count" in line_lower
        ):

            values["wc"] = value

        elif (
            "red blood cell" in line_lower
            or "rbc count" in line_lower
            or "red cell count" in line_lower
        ):

            values["rc"] = value

    return values