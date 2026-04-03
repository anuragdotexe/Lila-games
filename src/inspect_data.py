from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd

RAW_DIR = Path("data/raw")


def decode_event(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def classify_player(user_id):
    user_id = str(user_id)
    return "bot" if user_id.isdigit() else "human"


def load_single_file(file_path: Path) -> pd.DataFrame:
    table = pq.read_table(file_path)
    df = table.to_pandas()

    df["event"] = df["event"].apply(decode_event)
    df["player_type"] = df["user_id"].astype(str).apply(classify_player)
    df["source_file"] = file_path.name
    df["source_day"] = file_path.parent.name

    return df


def get_all_game_files():
    files = []
    for day_folder in sorted(RAW_DIR.iterdir()):
        if day_folder.is_dir():
            for file_path in day_folder.iterdir():
                if file_path.is_file():
                    files.append(file_path)
    return files


def main():
    files = get_all_game_files()
    print(f"\nTotal raw files found: {len(files)}")

    sample_file = files[0]
    print(f"\nSample file: {sample_file}")

    sample_df = load_single_file(sample_file)

    print("\nSample file shape:")
    print(sample_df.shape)

    print("\nSample file columns:")
    print(sample_df.columns.tolist())

    print("\nSample rows:")
    print(sample_df.head(10))

    frames = []
    for file_path in files:
        try:
            frames.append(load_single_file(file_path))
        except Exception as e:
            print(f"Skipping {file_path.name}: {e}")

    full_df = pd.concat(frames, ignore_index=True)

    print("\n" + "=" * 60)
    print("FULL DATASET SUMMARY")
    print("=" * 60)

    print("\nShape:")
    print(full_df.shape)

    print("\nDate folders:")
    print(full_df["source_day"].value_counts().sort_index())

    print("\nMaps:")
    print(full_df["map_id"].value_counts())

    print("\nEvents:")
    print(full_df["event"].value_counts())

    print("\nPlayer types:")
    print(full_df["player_type"].value_counts())

    print("\nUnique players:")
    print(full_df["user_id"].nunique())

    print("\nUnique matches:")
    print(full_df["match_id"].nunique())

    print("\nEvent count per map:")
    print(full_df.groupby("map_id")["event"].count().sort_values(ascending=False))

    print("\nTop 10 matches by event rows:")
    print(full_df["match_id"].value_counts().head(10))

    print("\nTop 10 players by event rows:")
    print(full_df["user_id"].value_counts().head(10))

    print("\nTimestamp range:")
    print("Min ts:", full_df["ts"].min())
    print("Max ts:", full_df["ts"].max())


if __name__ == "__main__":
    main()