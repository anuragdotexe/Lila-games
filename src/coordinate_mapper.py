import pandas as pd

MAP_CONFIG = {
    "AmbroseValley": {
        "scale": 900,
        "origin_x": -370,
        "origin_z": -473,
        "image_size": 1024,
    },
    "GrandRift": {
        "scale": 581,
        "origin_x": -290,
        "origin_z": -290,
        "image_size": 1024,
    },
    "Lockdown": {
        "scale": 1000,
        "origin_x": -500,
        "origin_z": -500,
        "image_size": 1024,
    },
}


def world_to_minimap(x, z, map_id):
    config = MAP_CONFIG[map_id]

    scale = config["scale"]
    origin_x = config["origin_x"]
    origin_z = config["origin_z"]
    image_size = config["image_size"]

    u = (x - origin_x) / scale
    v = (z - origin_z) / scale

    pixel_x = u * image_size
    pixel_y = (1 - v) * image_size

    return pixel_x, pixel_y


def add_minimap_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    pixel_x_list = []
    pixel_y_list = []

    for _, row in df.iterrows():
        pixel_x, pixel_y = world_to_minimap(row["x"], row["z"], row["map_id"])
        pixel_x_list.append(pixel_x)
        pixel_y_list.append(pixel_y)

    df["pixel_x"] = pixel_x_list
    df["pixel_y"] = pixel_y_list

    return df


if __name__ == "__main__":
    sample_x = -301.45
    sample_z = -355.55
    sample_map = "AmbroseValley"

    px, py = world_to_minimap(sample_x, sample_z, sample_map)

    print("Sample pixel_x:", round(px, 2))
    print("Sample pixel_y:", round(py, 2))