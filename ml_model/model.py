import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
import os
import pandas as pd
MODEL_PATH = "random_forest_model.pkl"

# ================================
# TRAINING FUNCTION
# ================================
def train_model():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "dataset_with_23_features.csv")

    data = pd.read_csv(file_path)

    print(data["label"].value_counts())
    print(data["label"].value_counts(normalize=True) * 100)


    # Clean
    data = data.dropna(subset=["label"])
    data["label"] = data["label"].apply(lambda x: 1 if x != 0 else 0)
    data["label"] = data["label"].astype(int)

    # Features
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

    
    missing = [f for f in FEATURES if f not in data.columns]
    print("Missing:", missing)

    if missing:
        print("Dataset needs feature generation first!")
        return
    X = data[FEATURES]
    y = data["label"]

    model = RandomForestClassifier(
        n_estimators=1000,
        max_depth=40,
        min_samples_split=5,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )


    from sklearn.model_selection import StratifiedKFold, cross_val_score

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
        X, y,
        test_size=0.2,
        random_state=42
    )

    model.fit(X_train, y_train)


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
    joblib.dump(model, MODEL_PATH)
    print("✅ Model saved successfully")

    # Evaluation
    y_pred = model.predict(X_test)

    
    from sklearn.metrics import confusion_matrix

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
import os
import joblib

MODEL_PATH = "random_forest_model.pkl"

if not os.path.exists(MODEL_PATH):
    print("⚠️ Model not found. Training now...")
    train_model()

model = joblib.load(MODEL_PATH)

# ================================
# PREDICTION FUNCTION
# ================================
def predict_url(features):
    prediction = model.predict([features])[0]
    return prediction




# ================================
# RUN TRAINING ONLY MANUALLY
# ================================
if __name__ == "__main__":
    train_model()

    # Test
    test_features = [
    1, 90, 2, 1, 1, 1,
    30, 0, 0, 1, 0, 5, 0, 0, 0, 0,
    2, 0, 0, 1, 0, 0, 0
]
    result = predict_url(test_features)

    print("\n🧪 Test Prediction:")
    print("Phishing 🚨" if result == 1 else "Safe ✅")