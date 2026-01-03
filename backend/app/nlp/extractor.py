import spacy

# Lazy load model to reduce memory usage
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        # Use small model (13MB) instead of large (750MB+)
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def extract_entities(text: str) -> dict:
    nlp = get_nlp()
    doc = nlp(text)

    locations = set()
    organizations = set()
    entities = []

    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            locations.add(ent.text)
        elif ent.label_ == "ORG":
            organizations.add(ent.text)

        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return {
        "locations": list(locations),
        "organizations": list(organizations),
        "entities": entities
    }
