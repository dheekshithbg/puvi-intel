def compute_risk_score(risks: list, base_confidence: float):
    weights = {
        "flood": 0.8,
        "fire": 0.9,
        "protest": 0.6,
        "health": 1.0,
        "infrastructure": 0.7
    }

    if not risks:
        return 0

    total = sum(weights.get(r, 0.5) for r in risks)
    average = total / len(risks)

    return float(round(average * base_confidence * 100, 2))

def city_summary(geo_points, risk_score):
    summary = {}

    for p in geo_points:
        city = p["name"]
        if city not in summary:
            summary[city] = {
                "events": 0,
                "risk_score": 0
            }

        summary[city]["events"] += 1
        summary[city]["risk_score"] = float(risk_score)
    
    return summary
