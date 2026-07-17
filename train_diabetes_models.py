import pandas as pd
import numpy as np

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


df = pd.read_csv("data\diabetes\diabetes.csv")
columns = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI"
]

for col in columns:
    df[col] = df[col].replace(0, df[col].median())

X = df.drop("Outcome", axis=1)

y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

models = {

    "Logistic Regression":
        LogisticRegression(max_iter=1000),

    "Decision Tree":
        DecisionTreeClassifier(random_state=42),

    "Random Forest":
        RandomForestClassifier(random_state=42),

    "KNN":
        KNeighborsClassifier(),

    "SVM":
        SVC()
}
results = []

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    print("=" * 50)

    print(name)

    print("Accuracy :", round(accuracy * 100, 2), "%")

    print()

    print(confusion_matrix(y_test, prediction))

    print()

    print(classification_report(y_test, prediction))

    results.append(
        [name, accuracy]
    )

results_df = pd.DataFrame(
    results,
    columns=["Model", "Accuracy"]
)

results_df.sort_values(
    by="Accuracy",
    ascending=False
)


model = RandomForestClassifier(
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(
    model,
    "models/diabetes_model.pkl"
)
joblib.dump(
    list(X.columns),
    "models/diabetes_feature_order.pkl"
)