from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .io import load_geodata
from .weights import build_graph_spatial_weights


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "build":
        districts, streets = load_geodata(args.districts, args.streets, target_crs=args.target_crs)
        matrix = build_graph_spatial_weights(
            districts,
            streets,
            district_id_col=args.district_id,
            buffer_distance=args.buffer_distance,
            normalize=args.normalize,
            fill_shortest_paths=args.fill_shortest_paths,
        )

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        matrix.to_csv(output_path)
        print(f"Spatial weight matrix saved to {output_path}")
        return 0

    parser.print_help()
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="graph-spatial-weights",
        description="Build graph-based spatial weight matrices from streets and districts.",
    )
    subparsers = parser.add_subparsers(dest="command")

    build = subparsers.add_parser("build", help="Build a graph-based spatial weight matrix.")
    build.add_argument("--districts", required=True, help="Path to the district geospatial file.")
    build.add_argument("--streets", required=True, help="Path to the street geospatial file.")
    build.add_argument("--district-id", default="BoroCD", help="District identifier column.")
    build.add_argument("--output", required=True, help="Output CSV path.")
    build.add_argument("--target-crs", default=None, help="Optional target CRS, such as EPSG:2263.")
    build.add_argument("--buffer-distance", type=float, default=5.0, help="Street buffer distance in CRS units.")
    build.add_argument("--no-normalize", dest="normalize", action="store_false", help="Keep raw connection counts.")
    build.add_argument(
        "--no-fill-shortest-paths",
        dest="fill_shortest_paths",
        action="store_false",
        help="Do not fill non-adjacent districts with shortest-path products.",
    )
    build.set_defaults(normalize=True, fill_shortest_paths=True)

    return parser


if __name__ == "__main__":
    raise SystemExit(main())
