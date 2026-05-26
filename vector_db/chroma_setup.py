import chromadb

# Initialize ChromaDB client
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="url_features")

# Function to add sample data
def add_data():
    collection.add(
        documents=[
            "safe",
            "phishing",
            "phishing"
        ],
        embeddings=[
            # Example SAFE URL features
            # length, dots, https, subdomains, slashes, hyphens,
            # login, verify, bank, secure, update,
            # ip, @, special, redirect, http_only
            [18, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

            # Example PHISHING URL features
            [35, 3, 0, 2, 5, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],

            # Another PHISHING example
            [28, 2, 0, 1, 4, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
        ],
        ids=["1", "2", "3"]
    )


# Function to find similar vectors
def get_similar(vector):
    results = collection.query(
        query_embeddings=[vector],
        n_results=2
    )

    return {
        "matches": results["documents"],
        "distances": results["distances"]
    }


# ================================
# TEST BLOCK
# ================================
if __name__ == "__main__":
    add_data()

    # Test vector (same 16 feature format)
    test_vector = [
        30, 2, 0, 1, 4, 1,   # structure
        1, 0, 0, 1, 0,       # keywords
        0, 0, 1, 0, 1        # security/behavior
    ]

    result = get_similar(test_vector)

    print("Result:")
    print(result)