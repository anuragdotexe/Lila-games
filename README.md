# Player Journey Visualization Tool

A web-based gameplay telemetry visualization tool built for the LILA APM Written Test.

This tool helps a Level Designer explore how players move through maps, where combat and loot cluster, and which areas are underutilized. It converts raw telemetry into an interactive minimap-based experience with filters, timeline playback, and heatmaps.

## Live App

https://anurag-lila-games.streamlit.app

## Features

* Load and parse raw parquet gameplay files
* Reconstruct matches using `match_id`
* Visualize player movement on actual minimaps
* Distinguish human vs bot players
* Event markers for loot, combat, and deaths
* Filters for date and match
* Timeline playback (match progression)
* Heatmap overlays:

  * movement density
  * kill zones
  * death zones

## Tech Stack

* Streamlit
* Pandas
* PyArrow
* Plotly
* Pillow

## Project Structure

.
├── assets/
│   └── minimaps/
├── data/
│   ├── raw/
├── src/
│   ├── load_data.py
│   ├── preprocess.py
│   ├── coordinate_mapper.py
│   ├── plotting.py
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── INSIGHTS.md
├── BUILD_LOG.md

## Running Locally

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py

## Key Logic

World to minimap mapping:

* u = (x - origin_x) / scale
* v = (z - origin_z) / scale
* pixel_x = u * 1024
* pixel_y = (1 - v) * 1024

Only x and z are used (y ignored).

## Notes

* Kill data is sparse → bot combat included for meaningful heatmaps
* Movement heatmaps are the strongest signal in this dataset
* Built for clarity and evaluation speed

* completed
