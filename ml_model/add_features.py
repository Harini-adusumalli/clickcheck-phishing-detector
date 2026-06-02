import pandas as pd
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
from backend.feature_extraction import extract_features

# Load dataset
df = pd.read_csv("ml_model/dataset_with_all_features v2.csv")

print("Loaded:", df.shape)

# Generate all 7 agreed features
df["num_subdomains"] = 0
df["has_verify"] = 0
df["has_bank"] = 0
df["has_secure"] = 0
df["has_update"] = 0
df["has_ip_address"] = 0
df["has_redirect"] = 0

for i, url in enumerate(df["url"]):

    f = extract_features(str(url))

    df.at[i, "num_subdomains"] = f[3]
    df.at[i, "has_verify"] = f[7]
    df.at[i, "has_bank"] = f[8]
    df.at[i, "has_secure"] = f[9]
    df.at[i, "has_update"] = f[10]
    df.at[i, "has_ip_address"] = f[11]
    df.at[i, "has_redirect"] = f[14]

    if i % 50000 == 0:
        print(f"Processed {i}")

# Save new dataset
df.to_csv("ml_model/dataset_with_23_features.csv", index=False)

print("✅ Done")
print("New Shape:", df.shape)

print(df[[
    "num_subdomains",
    "has_verify",
    "has_bank",
    "has_secure",
    "has_update",
    "has_ip_address",
    "has_redirect"
]].head())

print(df["has_verify"].sum())
print(df["has_bank"].sum())
print(df["has_secure"].sum())
print(df["has_update"].sum())
print(df["has_ip_address"].sum())
print(df["has_redirect"].sum())