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
    # Compute spatial insights
    distances = []
    for i in range(len(geo)):
        for j in range(i + 1, len(geo)):
            d = compute_distance(
                geo[i]["lat"], geo[i]["lon"],
                geo[j]["lat"], geo[j]["lon"]
            )
            distances.append(round(d, 2))

    max_distance = max(distances) if distances else 0
    min_distance = min(distances) if distances else 0

    # ---------------------------------------
    # SUPER-HARDENED, NON-HALLUCINATING PROMPT
    # ---------------------------------------
    prompt = f"""
You are a geospatial risk intelligence analyst. 
You MUST follow all constraints below with ZERO exceptions.

-----------------------------------------
STRICT RULES (VIOLATION = WRONG OUTPUT)
-----------------------------------------

1. You MUST NOT create or modify any locations.
   - Only use the locations exactly as given in the "Geo points" list.
   - Do NOT replace a location name.
   - Do NOT add new cities.

2. You MUST NOT create or modify coordinates.
   - Use the exact lat/lon provided in the "Geo points".
   - Never invent new numbers.

3. You MUST NOT create or modify clusters.
   - Use cluster IDs exactly as provided.

4. You MUST NOT wrap JSON in backticks.
   - Output raw JSON only.

5. You MUST NOT hallucinate distances, bounding boxes, or risk scores.
   - Only use values given in the input or obvious calculations.

6. You MUST output BOTH:
   - JSON_DASHBOARD (strict JSON)
   - NARRATIVE_STORY (structured text)

7. JSON must be valid and parseable.

-----------------------------------------
FACTS BELOW (USE EXACTLY AS GIVEN)
-----------------------------------------

Locations: {entities['locations']}
Risks detected: {risk['risks']}
Confidence: {risk['confidence']}
Risk Index Score: {risk.get('risk_index', 'N/A')}
Geo points: {geo}
City summary: {summary}
Cluster count: {len(clusters)}
Farthest distance: {max_distance} km
Closest distance: {min_distance} km

-----------------------------------------
JSON_DASHBOARD MUST FOLLOW THIS STRUCTURE:
-----------------------------------------

{{
  "title": "Geospatial Risk Intelligence Report",
  "event": {{
      "locations": {entities['locations']},
      "risks": {risk['risks']},
      "confidence": {risk['confidence']},
      "summary": "<short summary>"
  }},
  "map_layers": {{
      "points": [
          {{
              "name": "<from geo>",
              "lat": <float>,
              "lon": <float>,
              "risk_score": <float>,
              "cluster_id": <int>
          }}
      ],
      "risk_radius_km": <float>,
      "bounding_box": {{
          "min_lat": <float>, "max_lat": <float>,
          "min_lon": <float>, "max_lon": <float>
      }}
  }},
  "spatial_insights": [
      "<insight 1>",
      "<insight 2>",
      "<insight 3>"
  ],
  "predicted_impact_zones": [
      {{
        "name": "<area>",
        "reason": "<why>"
      }}
  ],
  "risk_interpretation": {{
      "severity_level": "<Low/Moderate/High>",
      "explanation": "<reason>",
      "factors": ["<factor1>", "<factor2>"]
  }},
  "recommended_actions": [
      "<action 1>",
      "<action 2>",
      "<action 3>",
      "<action 4>"
  ]
}}

-----------------------------------------
NARRATIVE_STORY MUST HAVE:
-----------------------------------------

1. Event Summary  
2. Spatial Pattern Insight  
3. Severity Interpretation  
4. Predicted Next Impact Zones  
5. Recommended Immediate Actions  

Tone:
- crisp  
- analytical  
- executive-friendly  
- zero fluff  

-----------------------------------------
OUTPUT FORMAT:
-----------------------------------------

1. First, output the JSON_DASHBOARD (raw JSON, no markdown code blocks)
2. Then output exactly: ---NARRATIVE_START---
3. Then output the NARRATIVE_STORY

Example:
{{
  "title": "..."
}}
---NARRATIVE_START---
# Event Summary
...
"""

    llm_output = call_llm(prompt)

    return {
        "event_summary": llm_output
    }
