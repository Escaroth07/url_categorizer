from transformers import pipeline

# Load zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def predict_content_category(text, categories):
    result = classifier(text, categories)
    return result['labels'][0], result['scores'][0]
