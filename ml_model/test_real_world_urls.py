import pandas as pd

# Load URL dataset
df = pd.read_csv("ml_model/real_world_test_urls.csv")

print("Dataset Shape:", df.shape)
print("\nLabel Distribution:")
print(df["label"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate URLs:")
print(df["url"].duplicated().sum())

print("\nSample URLs:")
print(df.sample(10))