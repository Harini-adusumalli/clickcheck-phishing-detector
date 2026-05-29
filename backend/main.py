from fastapi import FastAPI
from backend.feature_extraction import extract_features
from ml_model.model import predict_url
from vector_db.chroma_setup import get_similar , add_data , collection

if collection.count() == 0:
    add_data()
    
app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/scan-url")
def scan_url(url: str):
    features = extract_features(url)

    # ML prediction
    prediction = predict_url(features)
    ml_result = "phishing" if prediction == 1 else "safe"

    # Similarity
    similar = get_similar(features)

    # 👉 Extract similarity decision
    sim_match = similar["matches"][0][0]

    # FINAL DECISION
    if ml_result == "phishing" or sim_match == "phishing":
        final_result = "phishing"
    else:
        final_result = "safe"

    return {
        "url": url,
        "features": features,
        "ml_prediction": ml_result,
        "similarity": similar,
        "final_result": final_result
    }