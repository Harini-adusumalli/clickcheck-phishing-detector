import chromadb
import pandas as pd
from collections import Counter
from backend.feature_extraction import extract_features


# ================================
# CHROMADB SETUP
# ================================

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="url_features"
)

# ================================
# LOAD DATASET
# ================================

df = pd.read_csv(r"D:\internship\clickcheck-phishing-detector\ml_model\dataset_cleaned.csv")

feature_columns = [
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
# ADD DATA TO CHROMADB
# ================================

def add_data():

    safe = df[df["label"] == 0].sample(n=3000, random_state=42)
    phishing = df[df["label"] != 0].sample(n=3000, random_state=42)

    sample = pd.concat([safe, phishing]).sample(frac=1, random_state=42)

    print(sample["label"].value_counts())
    if collection.count() > 0:
        print("⚠️ Collection already contains data")
        return

    batch_size = 5000  # Must be less than 5461

    for start in range(0, len(sample), batch_size):
        end = min(start + batch_size, len(sample))

        batch = sample.iloc[start:end]

        ids = [str(i) for i in range(start, end)]
        embeddings = batch[feature_columns].values.tolist()
        documents = batch["url"].tolist()
        metadatas=[{"label": str(label)}
                   for label in batch["label"]
                   ]

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        print(f"Added vectors {start} to {end-1}")

    print(f"\n✅ Total vectors stored: {collection.count()}")

# ================================
# SIMILARITY SEARCH
# ================================

def get_similar(vector):

    results = collection.query(
        query_embeddings=[vector],
        n_results=min(5, collection.count())
    )

    matches = results["documents"][0]
    labels = [item["label"] for item in results["metadatas"][0]]
    distances = results["distances"][0]

    confidence = round(
        1 / (1 + distances[0]),
        2
    )

    return {
        "matches": matches,
        "labels": labels,
        "distances": distances,
        "confidence": confidence
    }

# ================================
# MAJORITY VOTING DECISION
# ================================

def interpret_similarity(result):

    labels = result["labels"]

    vote = Counter(labels)

    majority_label = vote.most_common(1)[0][0]

    print("Vote Count:", dict(vote))

    if majority_label in ["1.0", "2.0", "3.0"]:
        return "phishing"

    return "safe"

# ================================
# TESTING
# ================================

if __name__ == "__main__":

    add_data()

    url = input("Enter URL: ")
    test_vector = extract_features(url)
    print(test_vector)
    print(len(test_vector))

    result = get_similar(test_vector)

    decision = interpret_similarity(result)

    print("\n========== RESULTS ==========")
    print("Similar URLs:")
    for url in result["matches"]:
        print(url)

    print("\nLabels:", result["labels"])
    print("Distances:", result["distances"])
    print("Confidence:", result["confidence"])
    print("Decision:", decision)
    
