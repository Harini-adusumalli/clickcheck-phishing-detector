import chromadb
import pandas as pd
from collections import Counter

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

df = pd.read_csv(r"D:\internship\clickcheck-phishing-detector\ml_model\dataset_with_23_features.csv")

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

    sample = df.head(1000)

    ids = [str(i) for i in range(len(sample))]

    embeddings = sample[feature_columns].values.tolist()

    documents = sample["label"].astype(str).tolist()

    if collection.count() == 0:

        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents
        )

        print("✅ Real dataset added to ChromaDB")

    else:
        print("⚠️ Collection already contains data")

# ================================
# SIMILARITY SEARCH
# ================================

def get_similar(vector):

    results = collection.query(
        query_embeddings=[vector],
        n_results=min(5, collection.count())
    )

    matches = results["documents"][0]
    distances = results["distances"][0]

    confidence = round(
        1 / (1 + distances[0]),
        2
    )

    return {
        "matches": matches,
        "distances": distances,
        "confidence": confidence
    }

# ================================
# MAJORITY VOTING DECISION
# ================================

def interpret_similarity(result):

    matches = result["matches"]

    vote = Counter(matches)

    majority_label = vote.most_common(1)[0][0]

    print("Vote Count:", dict(vote))

    if majority_label in ["1", "2", "3"]:
        return "phishing"

    return "safe"

# ================================
# TESTING
# ================================

if __name__ == "__main__":

    add_data()

    test_vector = (
        df[feature_columns]
        .iloc[100]
        .tolist()
    )

    result = get_similar(test_vector)

    decision = interpret_similarity(result)

    print("\n========== RESULTS ==========")
    print("Matches:", result["matches"])
    print("Distances:", result["distances"])
    print("Confidence:", result["confidence"])
    print("Decision:", decision)