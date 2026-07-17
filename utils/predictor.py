import pandas as pd

def predict_heart_disease(values, model, feature_order):

    input_df = pd.DataFrame([values])

    input_df = input_df[feature_order]

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    return prediction, probability


def predict_diabetes(values, model, feature_order):

    input_df = pd.DataFrame([values])

    input_df = input_df[feature_order]

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    return prediction, probability

def predict_liver_disease(values, model, feature_order):

    input_df = pd.DataFrame([values])

    input_df = input_df[feature_order]

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    return prediction, probability

def predict_kidney_disease(values, model, feature_order):

    input_df = pd.DataFrame([values])

    input_df = input_df[feature_order]

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0]

    return prediction, probability

def predict_symptom_disease(values, model, feature_order):
    """
    Predict disease based on selected symptoms.
    """

    input_data = []

    for feature in feature_order:
        input_data.append(values.get(feature, 0))

    prediction = model.predict([input_data])[0]

    probability = model.predict_proba([input_data])[0]

    return prediction, probability