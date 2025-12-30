from fastapi import FastAPI
from app.nlp.extractor import extract_entities
from app.risk.classifier import classify_risk
from app.geo.geocode import geocode_locations, to_geojson
from app.analytics.scoring import compute_risk_score, city_summary
from app.analytics.clustering import cluster_points
from app.utils import convert_numpy_to_python
from app.utils import clean_geocoded_data as clean_geo_points

app = FastAPI(
    title="PuviIntel",
    description="Unstructured Text to Geospatial Intelligence API",
    version="0.2.0"
)

#Check Endpoint
@app.get("/")
def check():
    return {"message": "FastAPI Running"}

#NLP Entity Extraction Endpoint
@app.post("/nlp/extract")
def extract(data: dict):
    text = data.get("text", "")
    return extract_entities(text)

#Analysis Endpoint
@app.post("/analyze")
def analyze(data: dict):
    text = data.get("text", "")

    entities = extract_entities(text)
    risk = classify_risk(text)

    geo_points = geocode_locations(entities["locations"])
    cleaned_geo = clean_geo_points(geo_points)
    geojson = to_geojson(cleaned_geo)

    score = compute_risk_score(risk["risks"], risk["confidence"])

    clusters = cluster_points(geo_points)
    summary = city_summary(geo_points, score)

    response = {
        "entities": entities,
        "risk_analysis": risk,
        "risk_index": score,
        "geo": geo_points,
        "geojson": geojson,
        "clusters": clusters,
        "city_summary": summary
    }
    
    return convert_numpy_to_python(response)
