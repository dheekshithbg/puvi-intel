from shapely.geometry import Point, MultiPoint
import folium

def add_cluster_polygons(map_obj, clusters):
    for cluster_id, points in clusters.items():
        if cluster_id == -1 or len(points) < 3:
            continue
        
        coords = [(p["lat"], p["lon"]) for p in points]
        polygon = MultiPoint([Point(c[1], c[0]) for c in coords]).convex_hull
        
        folium.GeoJson(
            polygon.__geo_interface__,
            style_function=lambda x: {
                "fillColor": "#3186cc",
                "color": "#3186cc",
                "opacity": 0.4,
                "weight": 2,
                "fillOpacity": 0.2
            },
            name=f"Cluster {cluster_id}"
        ).add_to(map_obj)
