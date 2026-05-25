import chromadb

# Initialize database
client = chromadb.Client()

# Create or get collection
collection = client.get_or_create_collection(name="url_features")


# Function to add sample data
def add_data():
    collection.add(
        documents=["safe", "phishing", "phishing"],
        embeddings=[
            [18, 1, 1],
            [30, 2, 0],
            [25, 2, 0]
        ],
        ids=["1", "2", "3"]
    )


# Function to get similar vectors
def get_similar(vector):
    results = collection.query(
        query_embeddings=[vector],
        n_results=2
    )
    return results


# Testing block
if __name__ == "__main__":
    add_data()

    test_vector = [26, 2, 0]
    result = get_similar(test_vector)

    print(result)