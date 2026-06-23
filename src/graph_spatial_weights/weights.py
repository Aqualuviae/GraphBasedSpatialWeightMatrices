from __future__ import annotations

from itertools import combinations
from typing import Hashable
from warnings import warn

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd


def build_graph_spatial_weights(
    districts: gpd.GeoDataFrame,
    streets: gpd.GeoDataFrame,
    district_id_col: str = "BoroCD",
    buffer_distance: float = 5.0,
    normalize: bool = True,
    fill_shortest_paths: bool = True,
) -> pd.DataFrame:
    """Build a graph-based spatial weight matrix from districts and streets.

    The direct edge weight between two districts is the count of buffered street
    segments that intersect both district geometries. Direct weights are
    optionally normalized by the maximum direct count. Missing non-adjacent
    weights can then be filled with the product of edge weights along the
    strongest shortest path.
    """
    _validate_inputs(districts, streets, district_id_col)
    if buffer_distance < 0:
        raise ValueError("buffer_distance must be non-negative.")

    district_ids = list(districts[district_id_col])
    matrix = pd.DataFrame(0.0, index=district_ids, columns=district_ids)
    intersecting_streets = _filter_intersecting_streets(streets, districts)

    if not intersecting_streets.empty:
        if streets.crs is not None and getattr(streets.crs, "is_geographic", False):
            warn(
                "buffer_distance is interpreted in CRS units, but the street CRS is geographic.",
                UserWarning,
                stacklevel=2,
            )

        street_buffers = intersecting_streets.geometry.buffer(buffer_distance)
        for street_geometry in street_buffers:
            overlapping_ids = _overlapping_district_ids(districts, district_id_col, street_geometry)
            for left, right in combinations(overlapping_ids, 2):
                matrix.loc[left, right] += 1.0
                matrix.loc[right, left] += 1.0

    if normalize:
        max_value = matrix.to_numpy().max(initial=0.0)
        if max_value > 0:
            matrix = matrix / max_value

    if fill_shortest_paths:
        matrix = _fill_shortest_path_products(matrix)

    for district_id in matrix.index:
        matrix.loc[district_id, district_id] = 0.0
    return matrix


def dataframe_to_libpysal_weights(matrix: pd.DataFrame):
    """Convert a square DataFrame weight matrix to ``libpysal.weights.W``."""
    from libpysal.weights import W

    numeric = matrix.astype(float)
    neighbors: dict[Hashable, list[Hashable]] = {}
    weights: dict[Hashable, list[float]] = {}

    for row_id, row in numeric.iterrows():
        row_neighbors: list[Hashable] = []
        row_weights: list[float] = []
        for col_id, value in row.items():
            if row_id != col_id and value != 0:
                row_neighbors.append(col_id)
                row_weights.append(float(value))
        neighbors[row_id] = row_neighbors
        weights[row_id] = row_weights

    return W(neighbors, weights, silence_warnings=True)


def _validate_inputs(
    districts: gpd.GeoDataFrame,
    streets: gpd.GeoDataFrame,
    district_id_col: str,
) -> None:
    if district_id_col not in districts.columns:
        raise ValueError(f"District id column '{district_id_col}' was not found.")
    if districts.empty:
        raise ValueError("districts must contain at least one feature.")
    if districts[district_id_col].isna().any():
        raise ValueError(f"District id column '{district_id_col}' contains missing values.")
    if districts[district_id_col].duplicated().any():
        raise ValueError(f"District id column '{district_id_col}' must contain unique values.")
    if districts.geometry.isna().any():
        raise ValueError("districts contains missing geometries.")
    if streets.empty:
        return
    if streets.geometry.isna().any():
        raise ValueError("streets contains missing geometries.")


def _filter_intersecting_streets(
    streets: gpd.GeoDataFrame,
    districts: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    if streets.empty:
        return streets.copy()

    boundary = _union_geometries(districts.geometry.boundary)
    mask = streets.geometry.intersects(boundary)
    return streets.loc[mask].copy()


def _overlapping_district_ids(
    districts: gpd.GeoDataFrame,
    district_id_col: str,
    street_geometry,
) -> list[Hashable]:
    mask = districts.geometry.intersects(street_geometry)
    ids = districts.loc[mask, district_id_col].tolist()
    return list(dict.fromkeys(ids))


def _fill_shortest_path_products(matrix: pd.DataFrame) -> pd.DataFrame:
    graph = nx.Graph()
    graph.add_nodes_from(matrix.index)

    for left in matrix.index:
        for right in matrix.columns:
            weight = float(matrix.loc[left, right])
            if left != right and weight > 0:
                graph.add_edge(left, right, weight=weight, cost=1.0 / weight)

    filled = matrix.copy()
    for left, right in combinations(matrix.index, 2):
        if filled.loc[left, right] != 0:
            continue
        try:
            path = nx.shortest_path(graph, left, right, weight="cost")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            continue
        if len(path) < 2:
            continue

        product = 1.0
        for source, target in zip(path[:-1], path[1:]):
            product *= float(graph[source][target]["weight"])
        filled.loc[left, right] = product
        filled.loc[right, left] = product

    return filled


def _union_geometries(geometries):
    if hasattr(geometries, "union_all"):
        return geometries.union_all()
    return geometries.unary_union
