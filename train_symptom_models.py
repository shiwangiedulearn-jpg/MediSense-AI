from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib
import pandas as pd
df = pd.read_csv("data/symptom_prediction/Training.csv")

df.drop(columns=["Unnamed: 133"], inplace=True)

df["prognosis"] = df["prognosis"].str.strip()

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

feature_order = X.columns.tolist()

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

feature_order = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=3000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True)
}

best_model = None
best_model_name = ""
best_accuracy = 0
best_recall = 0
best_f1 = 0

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)
    cm = confusion_matrix(
        y_test,
        prediction
    )
    report = classification_report(
        y_test,
        prediction,
        output_dict=True,
        zero_division=0
    )

    accuracy = accuracy_score(
        y_test,
        prediction
    )

    recall = report["macro avg"]["recall"]

    f1 = report["macro avg"]["f1-score"]
    print("=" * 60)
    print(name)
    print("Accuracy :", round(accuracy * 100, 2), "%")
    print("Recall :", round(recall * 100, 2), "%")
    print("F1 Score :", round(f1 * 100, 2), "%")
    print()

    print("Confusion Matrix")
    print(cm)
    print()

  
    if (
        recall > best_recall
        or
        (
            recall == best_recall
            and f1 > best_f1
        )
    ):

        best_model = model
        best_model_name = name
        best_accuracy = accuracy
        best_recall = recall
        best_f1 = f1

joblib.dump(
    models["Random Forest"],
    "models/symptom_model.pkl"
)

joblib.dump(
    feature_order,
    "models/symptom_feature_order.pkl"
)

print("=" * 60)
print("Selected Model : Random Foest")
print("Accuracy :", round(best_accuracy * 100, 2), "%")
print("Recall :", round(best_recall * 100, 2), "%")
print("F1 Score :", round(best_f1 * 100, 2), "%")
print("Model Saved Successfully")