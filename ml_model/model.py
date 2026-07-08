# ================================
# IMPORTS
# ================================
import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)
MODEL_PATH = "random_forest_model_cleaned.pkl"


FEATURES = [
    'web_is_live',
    'web_security_score',
    'web_forms_count',
    'web_password_fields',
    'web_has_login',
    'web_ssl_valid',
    'url_len',
    '@',
    '?',
    '-',
    '=',
    '.',
    '#',
    '%',
    '+',
    '$',
    'num_subdomains',
    'has_verify',
    'has_bank',
    'has_secure',
    'has_update',
    'has_ip_address',
    'has_redirect'
]
# ================================
# GLOBALS
# ================================

FEATURES = [
    'web_is_live',
    'web_security_score',
    'web_forms_count',
    'web_password_fields',
    'web_has_login',
    'web_ssl_valid',
    'url_len',
    '@',
    '?',
    '-',
    '=',
    '.',
    '#',
    '%',
    '+',
    '$',
    'num_subdomains',
    'has_verify',
    'has_bank',
    'has_secure',
    'has_update',
    'has_ip_address',
    'has_redirect'
]
def train_model():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "dataset_with_23_features.csv")

    data = pd.read_csv(file_path)
    print(data.columns.tolist())

    print(data["label"].value_counts())
    print(data["label"].value_counts(normalize=True) * 100)


    # Clean
    data = data.dropna(subset=["label"])
    data["label"] = data["label"].apply(lambda x: 1 if x != 0 else 0)
    data["label"] = data["label"].astype(int)

   





    missing = [f for f in FEATURES if f not in data.columns]
    print("Missing:", missing)

    if missing:
        print("Dataset needs feature generation first!")
        return

    X = data[FEATURES]
    y = data["label"]

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=20,
        min_samples_split=10,
        min_samples_leaf=3,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    )

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42
    )

    cv_scores = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        scoring="f1"
    )

    print("\n📊 Cross Validation Results")
    print("F1 Scores:", cv_scores)
    print("Average F1:", cv_scores.mean())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    try:
        model.fit(X_train, y_train)
        print("Model trained successfully.")
    except Exception as e:
        print("Training Error:", e)
        raise


    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    print("\nTop Features:")
    print(importance_df.head(15))
    print(X.columns.tolist())
    # Save model
    # Save model
    try:
        print("Saving model to:", os.path.abspath(MODEL_PATH))

        joblib.dump(model, MODEL_PATH)

        print("✅ Model saved successfully")

    except Exception as e:
        print("Save Error:", e)
        raise

    # Evaluation
    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)

    print("\nConfusion Matrix:")
    print(cm)

    print("\n🔍 Final Model Performance:\n")
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall   :", recall_score(y_test, y_pred))
    print("F1 Score :", f1_score(y_test, y_pred))


# ================================
# LOAD MODEL (FOR API)
# ================================

if not os.path.exists(MODEL_PATH):
    print("⚠️ Model not found. Training now...")
    train_model()

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model was not created because training failed.")

model = joblib.load(MODEL_PATH)


# ================================
# PREDICTION FUNCTION
# ================================

def predict_url(features):
    feature_df = pd.DataFrame([features], columns=FEATURES)
    prediction = model.predict(feature_df)[0]
    return prediction
    


# ================================
# MAIN
# ================================
if __name__ == "__main__":

    train_model()

    model = joblib.load(MODEL_PATH)

    from backend.feature_extraction import extract_features

    url = input("Enter URL: ")

    test_features = extract_features(url)
    base_dir = os.path.dirname(__file__)
    dataset = pd.read_csv(os.path.join(base_dir, "dataset_with_23_features.csv"))
    '''print(dataset[
    [
        "web_security_score",
        "web_is_live",
        "web_forms_count",
        "web_password_fields",
        "web_has_login",
        "web_ssl_valid"
    ]
].describe())'''
    row = dataset[dataset["url"] == url]
    if row.empty:
        print("This URL is not present in the dataset.")
    else:
        print("URL found in dataset!")
        dataset_features = row[FEATURES].iloc[0].tolist()
        print("\nFeature Comparison\n")

        for name, dataset_value, extracted_value in zip(
            FEATURES,
            dataset_features,
            test_features
        ):
            print(
                f"{name:20} Dataset: {dataset_value:<5} | Extracted: {extracted_value}"
            )

    print("Extracted Features:", test_features)
    print("Length:", len(test_features))

    result = predict_url(test_features)

    print("\n🧪 Test Prediction:")
    print("Phishing 🚨" if result == 1 else "Safe ✅")

else:

    if not os.path.exists(MODEL_PATH):
        train_model()

    model = joblib.load(MODEL_PATH)