import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString, box

from graph_spatial_weights.cli import main


def test_cli_build_writes_matrix_csv(tmp_path):
    districts_path = tmp_path / "districts.gpkg"
    streets_path = tmp_path / "streets.gpkg"
    output_path = tmp_path / "outputs" / "spatial_weights.csv"

    districts = gpd.GeoDataFrame(
        {"BoroCD": ["A", "B"]},
        geometry=[box(0, 0, 10, 10), box(10, 0, 20, 10)],
        crs="EPSG:3857",
    )
    streets = gpd.GeoDataFrame(
        {"name": ["AB"]},
        geometry=[LineString([(10, -1), (10, 11)])],
        crs="EPSG:3857",
    )
    districts.to_file(districts_path, driver="GPKG")
    streets.to_file(streets_path, driver="GPKG")

    exit_code = main(
        [
            "build",
            "--districts",
            str(districts_path),
            "--streets",
            str(streets_path),
            "--district-id",
            "BoroCD",
            "--buffer-distance",
            "0.5",
            "--output",
            str(output_path),
        ]
    )

    matrix = pd.read_csv(output_path, index_col=0)
    assert exit_code == 0
    assert output_path.exists()
    assert matrix.loc["A", "B"] == 1.0
    assert matrix.loc["B", "A"] == 1.0
