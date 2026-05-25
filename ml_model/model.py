import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("ml_model/dataset.csv")

# Features (input)
X = data[["length", "dots", "https"]]

# Labels (output)
y = data["label"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)


# Prediction function (IMPORTANT)
def predict_url(features):
    prediction = model.predict([features])
    return int(prediction[0])

if __name__ == "__main__":
    print(predict_url([25, 2, 0]))