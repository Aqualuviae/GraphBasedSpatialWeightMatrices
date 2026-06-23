import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import LineString, box

from graph_spatial_weights import (
    build_graph_spatial_weights,
    dataframe_to_libpysal_weights,
    load_geodata,
)


def _districts():
    return gpd.GeoDataFrame(
        {"BoroCD": ["A", "B", "C"]},
        geometry=[box(0, 0, 10, 10), box(10, 0, 20, 10), box(20, 0, 30, 10)],
        crs="EPSG:3857",
    )


def _streets():
    return gpd.GeoDataFrame(
        {"name": ["AB", "BC"]},
        geometry=[LineString([(10, -1), (10, 11)]), LineString([(20, -1), (20, 11)])],
        crs="EPSG:3857",
    )


def test_build_weights_from_street_connections():
    matrix = build_graph_spatial_weights(_districts(), _streets(), buffer_distance=0.5)

    assert list(matrix.index) == ["A", "B", "C"]
    assert matrix.loc["A", "B"] == pytest.approx(1.0)
    assert matrix.loc["B", "C"] == pytest.approx(1.0)
    assert matrix.loc["A", "C"] == pytest.approx(1.0)
    assert matrix.loc["A", "A"] == pytest.approx(0.0)
    assert matrix.equals(matrix.T)


def test_shortest_path_fill_can_be_disabled():
    matrix = build_graph_spatial_weights(
        _districts(),
        _streets(),
        buffer_distance=0.5,
        fill_shortest_paths=False,
    )

    assert matrix.loc["A", "B"] == pytest.approx(1.0)
    assert matrix.loc["B", "C"] == pytest.approx(1.0)
    assert matrix.loc["A", "C"] == pytest.approx(0.0)


def test_missing_district_id_column_raises_clear_error():
    with pytest.raises(ValueError, match="District id column 'CD' was not found"):
        build_graph_spatial_weights(_districts(), _streets(), district_id_col="CD")


def test_no_valid_street_connections_returns_zero_matrix():
    far_street = gpd.GeoDataFrame(
        {"name": ["far"]},
        geometry=[LineString([(100, 100), (110, 110)])],
        crs="EPSG:3857",
    )

    matrix = build_graph_spatial_weights(_districts(), far_street, buffer_distance=0.5)

    assert matrix.to_numpy().sum() == pytest.approx(0.0)
    assert matrix.equals(matrix.T)


def test_load_geodata_aligns_crs(tmp_path):
    districts_path = tmp_path / "districts.gpkg"
    streets_path = tmp_path / "streets.gpkg"

    districts = _districts()
    streets = _streets().to_crs("EPSG:4326")
    districts.to_file(districts_path, driver="GPKG")
    streets.to_file(streets_path, driver="GPKG")

    loaded_districts, loaded_streets = load_geodata(districts_path, streets_path)

    assert loaded_districts.crs == loaded_streets.crs
    assert loaded_districts.crs == districts.crs


def test_dataframe_to_libpysal_weights():
    matrix = pd.DataFrame(
        [[0.0, 1.0], [1.0, 0.0]],
        index=["A", "B"],
        columns=["A", "B"],
    )

    weights = dataframe_to_libpysal_weights(matrix)

    assert weights.neighbors["A"] == ["B"]
    assert weights.weights["A"] == [1.0]
