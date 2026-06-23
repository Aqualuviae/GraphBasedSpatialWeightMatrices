from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from graph_spatial_weights import build_graph_spatial_weights, dataframe_to_libpysal_weights


def generate_spatial_weights(
    districts,
    streets,
    district_id_col="BoroCD",
    buffer_distance=5.0,
    normalize=True,
    fill_shortest_paths=True,
):
    """Backward-compatible wrapper returning a libpysal W object."""
    matrix = build_graph_spatial_weights(
        districts,
        streets,
        district_id_col=district_id_col,
        buffer_distance=buffer_distance,
        normalize=normalize,
        fill_shortest_paths=fill_shortest_paths,
    )
    return dataframe_to_libpysal_weights(matrix)


__all__ = [
    "build_graph_spatial_weights",
    "dataframe_to_libpysal_weights",
    "generate_spatial_weights",
]
