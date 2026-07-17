import re
from rapidfuzz import fuzz


def extract_lipid_values(text):

    values = {
        "total_cholesterol": 0,
        "hdl": 0,
        "ldl": 0,
        "triglycerides": 0,
        "vldl": 0,
        "total_lipids": 0
    }

    tests = {
        "total_cholesterol": [
            "s. cholestrol",
            "serum cholesterol",
            "total cholesterol"
        ],
        "hdl": [
            "hdl cholesterol",
            "hdl",
            "hdl-c"
        ],
        "ldl": [
            "ldl cholesterol",
            "ldl",
            "ldl-c"
        ],
        "triglycerides": [
            "triglycerides",
            "triglyceride",
            "tg"
        ],
        "vldl": [
            "vldl cholesterol",
            "vldl",
            "vldl-c"
        ],
        "total_lipids": [
            "serum total lipids",
            "total lipids"
        ]
    }

    lines = text.split("\n")

    for line in lines:

        clean_line = line.lower().strip()

        if not clean_line:
            continue

        numbers = re.findall(r"\d+\.?\d*", line)

        if not numbers:
            continue

        result = float(numbers[0])

        for feature, names in tests.items():

            for name in names:

                score = fuzz.partial_ratio(name, clean_line)

                if score >= 80:

                    if values[feature] == 0:
                        values[feature] = result

                    break

    return values