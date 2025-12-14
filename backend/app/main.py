from fastapi import FastAPI

app = FastAPI(
    title="Insight Atlas",
    description="Unstructured Text to Geospatial Intelligence API",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "Insight Atlas API 🚀"
    }
