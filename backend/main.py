from fastapi import FastAPI
from backend.feature_extraction import extract_features

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API is working"}

@app.get("/scan-url")
def scan_url(url: str):
    features = extract_features(url)
    return {
        "url": url,
        "features": features
    }