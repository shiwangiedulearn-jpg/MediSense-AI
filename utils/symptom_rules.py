import json

with open("data/symptom_prediction/disease_info.json", "r", encoding="utf-8") as f:
    DISEASE_INFO = json.load(f)


def analyze_symptom(prediction, confidence, values):

    default = {
        "overall": prediction,
        "summary": "The selected symptoms most closely match this condition. Please consult a healthcare professional for proper diagnosis and treatment.",
        "health_effects": [],
        "diet": [],
        "lifestyle": [],
        "medical": [
            "Consult a qualified healthcare professional.",
            "Do not rely solely on this AI prediction."
        ]
    }

    return DISEASE_INFO.get(prediction, default)