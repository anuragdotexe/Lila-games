from pathlib import Path
import pyarrow.parquet as pq
import pandas as pd


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