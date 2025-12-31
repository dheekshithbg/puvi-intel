import folium
from folium.plugins import HeatMap

from app.visualization.polygon import add_cluster_polygons

def generate_map(geo_points, city_summary, clusters):
    # Initial map – center on first city
    if not geo_points:
        return None

    start = geo_points[0]
    m = folium.Map(location=[start["lat"], start["lon"]], zoom_start=7)

    # Add markers
    for city in geo_points:
        name = city["name"]
        lat = city["lat"]
        lon = city["lon"]

        # risk color based on score
        risk = city_summary.get(name, {}).get("risk_score", 0)

        if risk > 75:
            color = "red"
        elif risk > 40:
            color = "orange"
        else:
            color = "green"

        folium.CircleMarker(
            location=[lat, lon],
            radius=10,
            popup=f"{name} — Risk: {risk}",
            color=color,
            fill=True,
            fill_opacity=0.8,
            fill_color=color,
        ).add_to(m)

    # Add cluster lines
    for cluster_id, points in clusters.items():
        cluster_coords = [(p["lat"], p["lon"]) for p in points]
        folium.PolyLine(cluster_coords, color="blue", weight=2).add_to(m)

    # Add heatmap
    heatdata = [(p["lat"], p["lon"]) for p in geo_points]
    HeatMap(heatdata, radius=25, blur=15).add_to(m)
    add_cluster_polygons(m, clusters)
    return m._repr_html_()
