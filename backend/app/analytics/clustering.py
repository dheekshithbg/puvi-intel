from sklearn.cluster import DBSCAN
import numpy as np

def cluster_points(geo_points):
    if len(geo_points) < 2:
        return []

    coords = np.array([[p["lat"], p["lon"]] for p in geo_points])

    db = DBSCAN(eps=0.3, min_samples=1).fit(coords)
    labels = db.labels_.astype(int)

    clusters = {}
    for i, label in enumerate(labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(geo_points[i])

    return clusters
