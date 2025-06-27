from fastapi import FastAPI
from categorizer.preprocessing import preprocess_url, extract_domain_features
from categorizer.feature_extract import fetch_content, extract_text_features
from categorizer.models import predict_content_category
from categorizer.ensemble import combine_predictions
from categorizer.heuristics import (
    match_blacklist,
    load_steven_black_blacklists,
    load_urlhaus_blacklist,
)
from config import CATEGORIES

app = FastAPI()
domain_blacklists = {}

@app.on_event("startup")
async def load_blacklists():
    global domain_blacklists
    print("Loading blacklists (Steven Black hosts and URLHaus)... This may take up to a minute on first run.")
    sb = load_steven_black_blacklists()
    uh = load_urlhaus_blacklist()
    # Merge both sets
    domain_blacklists = sb
    for key in uh:
        if key in domain_blacklists:
            domain_blacklists[key].update(uh[key])
        else:
            domain_blacklists[key] = uh[key]
    print(f"Loaded blacklists: { {k: len(v) for k, v in domain_blacklists.items()} }")

@app.get("/")
def read_root():
    return {"msg": "URL Categorizer API"}

@app.post("/categorize")
async def categorize(url: str):
    url_clean = preprocess_url(url)
    category = match_blacklist(url_clean, domain_blacklists)
    if category:
        return {
            "url": url_clean,
            "predicted_category": category,
            "confidence": 1.0,
            "method": "blacklist"
        }
    # ML fallback
    content = await fetch_content(url_clean)
    text_features = extract_text_features(content)
    if not text_features["text"].strip():
        return {
            "url": url_clean,
            "predicted_category": "unknown",
            "confidence": 0.0,
            "method": "empty"
        }
    category, conf = predict_content_category(text_features['text'], CATEGORIES)
    category, conf = combine_predictions(category, conf)
    return {
        "url": url_clean,
        "predicted_category": category,
        "confidence": conf,
        "method": "ml"
    }
