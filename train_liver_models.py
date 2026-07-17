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


df = pd.read_csv("data/liver_disease/liver.csv")

# Handle Missing Values
df["alkphos"] = df["alkphos"].fillna(df["alkphos"].median())


df["gender"] = df["gender"].map({
    "Male": 1,
    "Female": 0
})


df["is_patient"] = df["is_patient"].replace({
    2: 0
})


X = df.drop("is_patient", axis=1)
y = df["is_patient"]


feature_order = X.columns.tolist()


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y #as the data is imbalanced
)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True)
}

logistic_model = None

for name, model in models.items():

    model.fit(X_train, y_train)

    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)

    print("=" * 60)
    print(name)
    print("Accuracy :", round(accuracy * 100, 2), "%")
    print()

    print(confusion_matrix(y_test, prediction))
    print()
    print(classification_report(y_test, prediction))

    if name == "Logistic Regression":
        logistic_model = model

joblib.dump(
    logistic_model,
    "models/liver_model.pkl"
)

joblib.dump(
    feature_order,
    "models/liver_feature_order.pkl"
)

print("=" * 60)
print("Logistic Regression model saved successfully.")