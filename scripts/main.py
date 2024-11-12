from scripts.data_loading import load_geodata
from scripts.spatial_weights import generate_spatial_weights
from scripts.utils import save_matrix


def main ():
    # Paths for Community District and Street Centerline data
    cd_path = "data/CommunityDistrict/nycd.shp"
    sc_path = "data/StreetCenterline/geo_export_5271be70-8d47-4770-8855-7a022145252c.shp"

    # 1. Load and align spatial data
    cd, sc = load_geodata(cd_path, sc_path)
    print("Loaded and aligned spatial data.")

    # 2. Generate spatial weight matrix
    spatial_weights = generate_spatial_weights(cd, method="graph")
    print("Generated spatial weights matrix.")

    # 3. Save spatial weight matrix
    output_path = "output/spatial_weights.csv"
    save_matrix(spatial_weights.full()[0], output_path)  # Use .full() to convert W to array
    print(f"Spatial weights matrix saved to {output_path}")


if __name__ == "__main__":
    main()
