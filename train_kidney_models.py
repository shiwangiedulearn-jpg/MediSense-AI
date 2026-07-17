import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

df = pd.read_csv("data/kidney/kidney.csv")

df = df.drop("id", axis=1)

df["classification"] = df["classification"].str.strip()

df["classification"] = df["classification"].map({
    "ckd": 1,
    "notckd": 0
})

categorical = [
    "rbc",
    "pc",
    "pcc",
    "ba",
    "htn",
    "dm",
    "cad",
    "appet",
    "pe",
    "ane"
]

for col in categorical:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", pd.NA)

numerical = [
    "age",
    "bp",
    "sg",
    "al",
    "su",
    "bgr",
    "bu",
    "sc",
    "sod",
    "pot",
    "hemo",
    "pcv",
    "wc",
    "rc"
]

for col in numerical:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

for col in categorical:
    df[col] = df[col].fillna(df[col].mode()[0])

df["rbc"] = df["rbc"].map({
    "normal": 0,
    "abnormal": 1
})

df["pc"] = df["pc"].map({
    "normal": 0,
    "abnormal": 1
})

df["pcc"] = df["pcc"].map({
    "notpresent": 0,
    "present": 1
})

df["ba"] = df["ba"].map({
    "notpresent": 0,
    "present": 1
})

df["htn"] = df["htn"].map({
    "no": 0,
    "yes": 1
})

df["dm"] = df["dm"].map({
    "no": 0,
    "yes": 1
})

df["cad"] = df["cad"].map({
    "no": 0,
    "yes": 1
})

df["appet"] = df["appet"].map({
    "good": 0,
    "poor": 1
})

df["pe"] = df["pe"].map({
    "no": 0,
    "yes": 1
})

df["ane"] = df["ane"].map({
    "no": 0,
    "yes": 1
})

X = df.drop("classification", axis=1)
y = df["classification"]

feature_order = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True)
}

best_model = None
best_model_name = ""
best_recall = 0
best_f1 = 0

for name, model in models.items():

    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    report = classification_report(
        y_test,
        prediction,
        output_dict=True
    )

    recall = report["1"]["recall"]
    f1 = report["1"]["f1-score"]

    accuracy = accuracy_score(y_test, prediction)

    print("=" * 60)
    print(name)
    print("Accuracy :", round(accuracy * 100, 2), "%")
    print()

    print(confusion_matrix(y_test, prediction))
    print()

    print(classification_report(y_test, prediction))

    if name == "Random Forest":
        best_model = model
        best_model_name = name
        best_recall = recall
        best_f1 = f1

joblib.dump(
    models["Random Forest"],
    "models/kidney_model.pkl"
)

joblib.dump(
    feature_order,
    "models/kidney_feature_order.pkl"
)

print("=" * 60)
print("Selected Model :", best_model)
print("Recall :", round(best_recall * 100, 2), "%")
print("F1 Score :", round(best_f1 * 100, 2), "%")
print("Model Saved Successfully")