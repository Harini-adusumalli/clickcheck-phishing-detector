import chromadb

# Initialize ChromaDB client
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="url_features")

# ================================
# ADD DATA (ONLY ONCE)
# ================================
def add_data():
    # Dummy data (for now)
    documents = [
        "safe",
        "phishing",
        "phishing"
    ]

    embeddings = [
        [18, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [35, 3, 0, 2, 5, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [28, 2, 0, 1, 4, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
    ]

    ids = ["1", "2", "3"]

    # ✅ Prevent duplicates
    if collection.count() == 0:
        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )
        print("✅ Data added to DB")
    else:
        print("⚠️ Data already exists, skipping...")


# ================================
# SIMILARITY FUNCTION
# ================================
def get_similar(vector):
    results = collection.query(
        query_embeddings=[vector],
        n_results=2
    )

    matches = results["documents"]
    distances = results["distances"]

    # Convert distance → confidence
    top_distance = distances[0][0]
    confidence = round(1 / (1 + top_distance), 2)

    return {
        "matches": matches,
        "distances": distances,
        "confidence": confidence,
        "top_match": matches[0][0]
    }


# ================================
# INTERPRET RESULT
# ================================
def interpret_similarity(similar):
    match = similar["top_match"]
    confidence = similar["confidence"]

    if match == "phishing" and confidence > 0.5:
        return "phishing"
    return "safe"


# ================================
# TEST BLOCK
# ================================
if __name__ == "__main__":
    add_data()

    test_vectors = [
        [18,1,1,0,2,0,0,0,0,0,0,0,0,0,0,0],  # safe
        [35,3,0,2,5,1,1,1,0,1,0,1,0,1,1,1],  # phishing
        [25,2,0,1,3,1,1,0,0,0,0,0,0,0,0,1] # mixed
    ]

    for vec in test_vectors:
        result = get_similar(vec)
        decision = interpret_similarity(result)

        print("\nVector:", vec)
        print("Top Match:", result["top_match"])
        print("Confidence:", result["confidence"])
        print("Decision:", decision)
        