import chromadb

# Create client (this is your database)
client = chromadb.Client()

# Create a collection (like a table)
collection = client.create_collection(name="url_features")

# Add some sample feature vectors
collection.add(
    documents=["safe site", "phishing site", "another phishing"],
    embeddings=[
        [18, 1, 1],   # safe
        [30, 2, 0],   # phishing
        [25, 2, 0]    # phishing
    ],
    ids=["1", "2", "3"]
)

# Now query (search similar vectors)
query = [[26, 2, 0]]

results = collection.query(
    query_embeddings=query,
    n_results=2
)

top_result = results['documents'][0][0]

if "phishing" in top_result:
    print("Prediction: PHISHING ⚠️")
else:
    print("Prediction: SAFE ✅")
