# graph-based-spatial-weights

Python toolkit for constructing graph-based spatial weight matrices from urban street networks and administrative districts.

This repository supports the workflow described in *Optimizing Spatial Weight Matrices in Spatial Econometrics: A Graph-Theoretic Approach Based on Shortest Path Algorithms* by Y. Song and A. Cibin (2024). It turns street-district intersections into a graph, normalizes direct district connections, and can fill non-adjacent district weights using shortest-path products.

## Method Overview

The implemented workflow is:

1. Load administrative districts and street centerlines.
2. Align coordinate reference systems.
3. Select streets intersecting district boundaries.
4. Buffer selected streets by a configurable distance.
5. Count district pairs touched by each buffered street segment.
6. Normalize direct connection counts into a spatial weight matrix.
7. Optionally fill non-adjacent pairs using products along graph shortest paths.

## Installation

```bash
git clone git@github.com:Aqualuviae/graph-based-spatial-weights.git
cd graph-based-spatial-weights
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

For notebook-based analysis, install the same environment and open `notebooks/graph_based_spatial_weights.ipynb`.

## Data

The original project data is not tracked in Git because it contains local geospatial files and derived analysis outputs.

Download the data from the external folder:

- [Google Drive Data Folder](https://drive.google.com/drive/folders/1ps9J-7VWHT5K7ePWXEboW1x9wvuQdGb2?usp=sharing)

Place downloaded files under a local `data/` folder. The default examples expect:

```text
data/
├── CommunityDistrict/
│   └── nycd.shp
└── StreetCenterline/
    └── geo_export_5271be70-8d47-4770-8855-7a022145252c.shp
```

## CLI Usage

Build a graph-based spatial weight matrix:

```bash
graph-spatial-weights build ^
  --districts data/CommunityDistrict/nycd.shp ^
  --streets data/StreetCenterline/geo_export_5271be70-8d47-4770-8855-7a022145252c.shp ^
  --district-id BoroCD ^
  --buffer-distance 5 ^
  --output outputs/spatial_weights.csv
```

The compatibility script calls the same CLI:

```bash
python scripts/main.py build --districts <districts-path> --streets <streets-path> --output outputs/spatial_weights.csv
```

## Python API

```python
from graph_spatial_weights import (
    build_graph_spatial_weights,
    dataframe_to_libpysal_weights,
    load_geodata,
)

districts, streets = load_geodata(
    "data/CommunityDistrict/nycd.shp",
    "data/StreetCenterline/geo_export_5271be70-8d47-4770-8855-7a022145252c.shp",
)

matrix = build_graph_spatial_weights(
    districts,
    streets,
    district_id_col="BoroCD",
    buffer_distance=5,
)

w = dataframe_to_libpysal_weights(matrix)
```

## Project Structure

```text
graph-based-spatial-weights/
├── article/
│   └── graph-based-spatial-weights.pdf
├── notebooks/
│   └── graph_based_spatial_weights.ipynb
├── scripts/
│   ├── main.py
│   ├── data_processing.py
│   ├── spatial_weights.py
│   └── utils.py
├── src/
│   └── graph_spatial_weights/
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
```

Generated files should be written to `outputs/`, which is ignored by Git.

## Testing

```bash
python -m compileall src scripts
pytest
```

Tests use small synthetic geometries instead of the original research data.

## Citation

Song, Y., & Cibin, A. (2024). *Optimizing Spatial Weight Matrices in Spatial Econometrics: A Graph-Theoretic Approach Based on Shortest Path Algorithms*. International Review for Spatial Planning and Sustainable Development.
