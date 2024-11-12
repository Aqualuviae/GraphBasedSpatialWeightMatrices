import networkx as nx
import numpy as np
from libpysal.weights import W

def calculate_distance_matrix(gdf):
    """Calculate a distance matrix for a GeoDataFrame."""
    coords = np.array([point.coords[0] for point in gdf.geometry.centroid])
    dist_matrix = distance_matrix(coords, coords)
    return dist_matrix

def generate_spatial_weights(cd, method="graph"):
    """Generate spatial weights matrix using specified method (default is graph)."""
    if method == "graph":
        # Construct a graph-based spatial weights matrix
        g = nx.Graph()

        for i, geom_i in enumerate(cd.geometry.centroid):
            for j, geom_j in enumerate(cd.geometry.centroid):
                if i != j:
                    distance = geom_i.distance(geom_j)
                    g.add_edge(i, j, weight=distance)
        w_matrix = nx.adjacency_matrix(g)
    else:
        # Placeholder for other methods
        w_matrix = np.zeros((len(cd), len(cd)))
    return W(w_matrix)
