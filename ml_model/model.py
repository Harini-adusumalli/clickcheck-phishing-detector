import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv("dataset.csv")

# Features (input)
X = data[["length", "dots", "https"]]

# Labels (output)
y = data["label"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Test accuracy
accuracy = model.score(X_test, y_test)

print("Model Accuracy:", accuracy)
import pandas as pd

test_input = pd.DataFrame([[25, 2, 0]], columns=["length", "dots", "https"])
prediction = model.predict(test_input)

print("Prediction (1=phishing, 0=safe):", prediction[0])