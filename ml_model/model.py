import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("dataset.csv")

# ================================
# FEATURES (16 FEATURES)
# ================================
X = data[[
    "length","dots","https","subdomains","slashes","hyphens",
    "login","verify","bank","secure","update",
    "ip","at","special","redirect","http_only"
]]

# Label
y = data["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

def predict_url(features):
    sample = pd.DataFrame([features], columns=X.columns)
    prediction = model.predict(sample)[0]
    return "phishing" if prediction == 1 else "safe"


if __name__ == "__main__":
    test_features = [30,2,0,1,4,1,1,0,0,1,0,0,0,1,0,1]
    print(predict_url(test_features))