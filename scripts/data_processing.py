import geopandas as gpd


def load_geodata (cd_path, sc_path):
    """Loads and aligns Community Districts (CD) and Street Centerline (SC) shapefiles."""
    cd = gpd.read_file(cd_path)
    sc = gpd.read_file(sc_path)

    # Align CRS
    if cd.crs != sc.crs:
        sc = sc.to_crs(cd.crs)

    return cd, sc
