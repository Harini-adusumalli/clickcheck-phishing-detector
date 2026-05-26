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

    prediction = predict_url(features)

    similar = get_similar(features)
    return {
        "url": url,
        "features": features,
        "prediction": prediction,
        "similarity": similar
    }