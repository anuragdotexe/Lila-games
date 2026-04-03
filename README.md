# Player Journey Visualization Tool

A web-based gameplay telemetry visualization tool built for the LILA APM Written Test.

This tool helps a Level Designer explore how players actually move through maps, where combat and loot activity cluster, and which areas of the map are heavily used or underutilized. It turns raw production telemetry into an interactive browser-based view with map overlays, timeline playback, filters, and heatmaps.

## Live App

https://anurag-lila-games.streamlit.app

## Features

- Load and parse raw parquet gameplay files
- Reconstruct full matches by combining player-level files using `match_id`
- Display player journeys on the correct minimap
- Correct world-to-minimap coordinate mapping for all 3 maps
- Distinguish between human players and bots
- Show event markers for:
  - Loot
  - BotKill
  - BotKilled
  - Kill
  - Killed
  - KilledByStorm
- Filter by date and match
- Map awareness in UI
- Timeline playback to reveal match progression over time
- Heatmap overlays for:
  - high-traffic movement areas
  - kill zones
  - death zones

## Tech Stack

- **Frontend / App Layer:** Streamlit
- **Data Processing:** Python, Pandas, PyArrow
- **Visualization:** Plotly
- **Image Handling:** Pillow

## Dataset Notes

The input dataset contains 5 days of production gameplay data from LILA BLACK.  
Each file represents one player (human or bot) in one match.

Important dataset details handled in the tool:
- files are parquet even though they do not have `.parquet` extensions
- `event` values are stored as bytes and must be decoded
- bots are identified by numeric `user_id`
- humans are identified by UUID `user_id`
- timestamps represent match-relative event ordering
- minimap mapping uses map-specific scale and origin values

## Project Structure

```text
.
├── assets/
│   └── minimaps/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── load_data.py
│   ├── preprocess.py
│   ├── coordinate_mapper.py
│   ├── plotting.py
│   └── validate_mapping.py
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── INSIGHTS.md
├── BUILD_LOG.md
└── .gitignore
