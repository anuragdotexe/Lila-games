from src.preprocess import get_all_game_files, load_match
from src.coordinate_mapper import add_minimap_coordinates


def main():
    match_id = "d3a3297e-2cdf-4a49-8450-09119b91a779.nakama-0"

    files = get_all_game_files()
    df = load_match(files, match_id)
    df = add_minimap_coordinates(df)

    print("\nMatch used:", match_id)
    print("Map:", df["map_id"].iloc[0])
    print("Rows:", len(df))

    print("\nWorld X range:")
    print("min =", round(df["x"].min(), 2))
    print("max =", round(df["x"].max(), 2))

    print("\nWorld Z range:")
    print("min =", round(df["z"].min(), 2))
    print("max =", round(df["z"].max(), 2))

    print("\nPixel X range:")
    print("min =", round(df["pixel_x"].min(), 2))
    print("max =", round(df["pixel_x"].max(), 2))

    print("\nPixel Y range:")
    print("min =", round(df["pixel_y"].min(), 2))
    print("max =", round(df["pixel_y"].max(), 2))

    print("\nRows outside minimap bounds:")
    outside = df[
        (df["pixel_x"] < 0)
        | (df["pixel_x"] > 1024)
        | (df["pixel_y"] < 0)
        | (df["pixel_y"] > 1024)
    ]
    print(len(outside))

    print("\nSample mapped rows:")
    print(df[["map_id", "x", "z", "pixel_x", "pixel_y", "event"]].head(10))


if __name__ == "__main__":
    main()