from math import radians, cos, sin, sqrt, atan2
from app.story.llm_connector import call_llm

def compute_distance(lat1, lon1, lat2, lon2):
    """Returns distance (km) between two lat/lon points."""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = (sin(dlat/2)**2 +
         cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c


def generate_story(entities, risk, geo, clusters, summary):
    # Compute basic spatial insights
    distances = []
    for i in range(len(geo)):
        for j in range(i+1, len(geo)):
            d = compute_distance(
                geo[i]["lat"], geo[i]["lon"],
                geo[j]["lat"], geo[j]["lon"]
            )
            distances.append(round(d, 2))

    max_distance = max(distances) if distances else 0
    min_distance = min(distances) if distances else 0

    prompt = f"""
You are a geospatial intelligence analyst.

Below are extracted facts from an incident report. 
Generate clear, concise insights:

Facts:
- Locations: {entities['locations']}
- Risks detected: {risk['risks']}
- Confidence: {risk['confidence']}
- Risk Index Score: {risk['risk_index'] if 'risk_index' in risk else 'N/A'}
- Geo points: {geo}
- City summary: {summary}
- Cluster count: {len(clusters)}
- Farthest distance between affected places: {max_distance} km
- Closest distance: {min_distance} km

Your output MUST contain these sections:

1. Event Summary  
2. Spatial Pattern Insight  
3. Severity Interpretation  
4. Predicted Next Impact Zones  
5. Recommended Immediate Actions  

Keep it:
- crisp  
- professional  
- actionable  
- no fluff  

Generate the final response.
"""

    llm_output = call_llm(prompt)

    return {
        "event_summary": llm_output
    }
