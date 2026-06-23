from __future__ import annotations

from pathlib import Path
from typing import Any

import geopandas as gpd


def load_geodata(
    districts_path: str | Path,
    streets_path: str | Path,
    target_crs: Any | None = None,
) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Load district and street files, then align their coordinate systems.

    If ``target_crs`` is provided, both layers are projected to that CRS.
    Otherwise, streets are projected to the district CRS when both files have
    CRS metadata and they differ.
    """
    districts = gpd.read_file(districts_path)
    streets = gpd.read_file(streets_path)

    if target_crs is not None:
        if districts.crs is None or streets.crs is None:
            raise ValueError("Both input layers must define a CRS when target_crs is used.")
        districts = districts.to_crs(target_crs)
        streets = streets.to_crs(target_crs)
    elif districts.crs is not None and streets.crs is not None and districts.crs != streets.crs:
        streets = streets.to_crs(districts.crs)

    return districts, streets
