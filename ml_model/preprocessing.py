import pandas as pd
import os

# ================================
# LOAD DATASET
# ================================

base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "dataset_with_23_features.csv")

original_df = pd.read_csv(file_path)
df = original_df.copy()

print("Original Shape:", df.shape)

# ================================
# CHECK DUPLICATES
# ================================

duplicate_count = df.duplicated().sum()
print(f"\nDuplicate Rows: {duplicate_count}")

# Remove exact duplicates
if duplicate_count > 0:
    df = df.drop_duplicates()
    print("Duplicates removed.")

# ================================
# CHECK NULL VALUES
# ================================

print("\nNull Values Per Column:")
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0])

# ================================
# HANDLE LABEL COLUMN
# ================================

if "label" in df.columns:
    label_nulls = df["label"].isnull().sum()

    if label_nulls > 0:
        print(f"\nRemoving {label_nulls} rows with missing labels...")
        df = df.dropna(subset=["label"])

# ================================
# HANDLE FEATURE NULLS
# ================================

for col in df.columns:

    # Skip label column
    if col == "label":
        continue

    if df[col].isnull().sum() > 0:

        # Binary columns
        unique_values = set(df[col].dropna().unique())

        if unique_values.issubset({0, 1}):
            fill_value = df[col].mode()[0]
            df[col] = df[col].fillna(fill_value)

            print(
                f"Filled nulls in binary column "
                f"'{col}' using mode ({fill_value})"
            )

        # Numeric columns
        elif pd.api.types.is_numeric_dtype(df[col]):
            fill_value = df[col].median()
            df[col] = df[col].fillna(fill_value)

            print(
                f"Filled nulls in numeric column "
                f"'{col}' using median ({fill_value})"
            )

        # Text columns
        else:
            fill_value = df[col].mode()[0]
            df[col] = df[col].fillna(fill_value)

            print(
                f"Filled nulls in text column "
                f"'{col}' using mode ({fill_value})"
            )

# ================================
# VALIDATION
# ================================

print("\nAfter Cleaning")
print("Shape:", df.shape)

remaining_nulls = df.isnull().sum().sum()
print("Remaining Null Values:", remaining_nulls)

print("Remaining Duplicates:", df.duplicated().sum())

# ================================
# SAVE CLEANED DATASET
# ================================

cleaned_file = os.path.join(base_dir, "dataset_cleaned.csv")

df.to_csv(cleaned_file, index=False)

print(f"\n✅ Cleaned dataset saved to:")
print(cleaned_file)

# ================================
# DATASET SUMMARY
# ================================

print("\nLabel Distribution:")

if "label" in df.columns:
    print(df["label"].value_counts())
    print("\nPercentage Distribution:")
    print(df["label"].value_counts(normalize=True) * 100)

# ================================
# VALIDATION SUMMARY
# ================================

print("\n===== DATASET VALIDATION =====")

print("Original Shape:", original_df.shape)
print("Cleaned Shape :", df.shape)

print("\nOriginal Duplicates:", original_df.duplicated().sum())
print("Cleaned Duplicates :", df.duplicated().sum())

print("\nOriginal Nulls:", original_df.isnull().sum().sum())
print("Cleaned Nulls :", df.isnull().sum().sum())

print("\nLabel Distribution:")
print(df["label"].value_counts())

print("\nLabel Distribution (%):")
print(df["label"].value_counts(normalize=True) * 100)