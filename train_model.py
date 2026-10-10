import os

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.linear_model import LogisticRegression

from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from feature_extraction import extract_features


# ==========================================
# 1. LOAD DATASET
# ==========================================

data = pd.read_csv("dataset.csv")

print("=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("Total URLs:", len(data))

print("\nDataset preview:")
print(data.head())


# ==========================================
# 2. EXTRACT FEATURES
# ==========================================

print("\nExtracting URL features...")

feature_data = []

for url in data["url"]:

    features = extract_features(url)

    feature_data.append(features)


X = pd.DataFrame(feature_data)

y = data["label"]


print("\nNumber of features:", X.shape[1])

print("\nFeature names:")

for feature in X.columns:

    print("-", feature)


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nTraining samples:", len(X_train))

print("Testing samples:", len(X_test))


# ==========================================
# 4. CREATE MODELS
# ==========================================

models = {

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "Logistic Regression":
        LogisticRegression(
            max_iter=2000
        ),

    "SVM":
        SVC(
            probability=True,
            random_state=42
        )
}


# ==========================================
# 5. CREATE MODELS DIRECTORY
# ==========================================

os.makedirs("models", exist_ok=True)


# ==========================================
# 6. TRAIN MODELS
# ==========================================

results = []

best_model = None
best_model_name = None
best_accuracy = 0


for model_name, model in models.items():

    print("\n")
    print("=" * 60)

    print("Training:", model_name)

    print("=" * 60)


    # Train
    model.fit(X_train, y_train)


    # Predict
    predictions = model.predict(X_test)


    # Metrics
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )


    print("Accuracy :", round(accuracy * 100, 2), "%")

    print("Precision:", round(precision * 100, 2), "%")

    print("Recall   :", round(recall * 100, 2), "%")

    print("F1 Score :", round(f1 * 100, 2), "%")


    # Store results
    results.append({

        "Model": model_name,

        "Accuracy": round(
            accuracy * 100,
            2
        ),

        "Precision": round(
            precision * 100,
            2
        ),

        "Recall": round(
            recall * 100,
            2
        ),

        "F1 Score": round(
            f1 * 100,
            2
        )

    })


    # Save individual model
    filename = model_name.lower().replace(
        " ",
        "_"
    )

    joblib.dump(
        model,
        f"models/{filename}.pkl"
    )


    # Find best model
    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model

        best_model_name = model_name


# ==========================================
# 7. DISPLAY COMPARISON
# ==========================================

results_df = pd.DataFrame(results)

print("\n")
print("=" * 60)

print("MODEL COMPARISON")

print("=" * 60)

print(results_df.to_string(index=False))


# ==========================================
# 8. SAVE RESULTS
# ==========================================

results_df.to_csv(
    "models/model_comparison.csv",
    index=False
)


# ==========================================
# 9. SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "models/best_model.pkl"
)


print("\n")
print("=" * 60)

print("BEST MODEL")

print("=" * 60)

print("Model:", best_model_name)

print(
    "Accuracy:",
    round(best_accuracy * 100, 2),
    "%"
)

print("\nBest model saved to:")

print("models/best_model.pkl")


# ==========================================
# 10. CLASSIFICATION REPORT
# ==========================================

best_predictions = best_model.predict(X_test)

print("\n")
print("=" * 60)

print("CLASSIFICATION REPORT - BEST MODEL")

print("=" * 60)

print(
    classification_report(
        y_test,
        best_predictions,
        zero_division=0
    )
)


print("\nTraining completed successfully!")