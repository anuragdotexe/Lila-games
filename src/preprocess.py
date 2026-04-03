from pathlib import Path
import pandas as pd
from src.load_data import load_single_file


def get_all_game_files():
    raw_dir = Path("data/raw")
    files = []

    for day_folder in sorted(raw_dir.iterdir()):
        if day_folder.is_dir():
            for file_path in day_folder.iterdir():
                if file_path.is_file():
                    files.append(file_path)

    return files


def get_match_files(all_files, match_id):
    return [f for f in all_files if match_id in f.name]


def load_match(all_files, match_id):
    match_files = get_match_files(all_files, match_id)

    frames = []
    for file_path in match_files:
        df = load_single_file(file_path)
        frames.append(df)

    match_df = pd.concat(frames, ignore_index=True)
    match_df = match_df.sort_values("ts").reset_index(drop=True)

    return match_df


def build_match_summary(all_files):
    records = []

    unique_match_ids = sorted(
        {
            file_path.name.split("_", 1)[1]
            for file_path in all_files
            if "_" in file_path.name
        }
    )

    for match_id in unique_match_ids:
        try:
            df = load_match(all_files, match_id)

            event_counts = df["event"].value_counts().to_dict()
            player_type_counts = df["player_type"].value_counts().to_dict()

            records.append(
                {
                    "match_id": match_id,
                    "map_id": df["map_id"].iloc[0],
                    "source_day": df["source_day"].iloc[0],
                    "rows": len(df),
                    "unique_players": df["user_id"].nunique(),
                    "human_rows": player_type_counts.get("human", 0),
                    "bot_rows": player_type_counts.get("bot", 0),
                    "position_events": event_counts.get("Position", 0),
                    "botposition_events": event_counts.get("BotPosition", 0),
                    "loot_events": event_counts.get("Loot", 0),
                    "kill_events": event_counts.get("Kill", 0),
                    "killed_events": event_counts.get("Killed", 0),
                    "botkill_events": event_counts.get("BotKill", 0),
                    "botkilled_events": event_counts.get("BotKilled", 0),
                    "storm_events": event_counts.get("KilledByStorm", 0),
                }
            )
        except Exception as e:
            print(f"Skipping match {match_id}: {e}")

    summary_df = pd.DataFrame(records)

    summary_df["total_combat_events"] = (
        summary_df["kill_events"]
        + summary_df["killed_events"]
        + summary_df["botkill_events"]
        + summary_df["botkilled_events"]
    )

    return summary_df.sort_values(
        ["human_rows", "loot_events", "total_combat_events", "rows"],
        ascending=False,
    ).reset_index(drop=True)


if __name__ == "__main__":
    files = get_all_game_files()
    summary_df = build_match_summary(files)

    print("\nTop 20 best candidate matches:\n")
    print(
        summary_df[
            [
                "match_id",
                "map_id",
                "source_day",
                "rows",
                "unique_players",
                "human_rows",
                "bot_rows",
                "loot_events",
                "kill_events",
                "killed_events",
                "botkill_events",
                "botkilled_events",
                "storm_events",
            ]
        ].head(20)
    )