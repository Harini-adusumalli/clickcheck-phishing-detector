import pandas as pd

original = pd.read_csv("ml_model/dataset_with_23_features.csv")
cleaned = pd.read_csv("ml_model/dataset_cleaned.csv")

print("Original Shape:", original.shape)
print("Cleaned Shape :", cleaned.shape)

print("\nRows Removed:",
      len(original) - len(cleaned))