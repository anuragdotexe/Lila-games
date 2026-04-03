# Architecture

## Overview

This tool converts raw gameplay telemetry into an interactive visualization for level designers.

---

## Stack Choice

* Streamlit → fast UI development
* Pandas + PyArrow → efficient parquet processing
* Plotly → interactive layered visualization
* Pillow → minimap handling

---

## Data Flow

1. Load parquet files
2. Decode event column
3. Classify player type
4. Merge files → reconstruct matches
5. Sort by timestamp
6. Convert world → minimap coordinates
7. Apply filters + timeline
8. Render via Plotly

---

## Coordinate Mapping

* Uses map-specific:

  * scale
  * origin_x
  * origin_z

Formula:

u = (x - origin_x) / scale
v = (z - origin_z) / scale

pixel_x = u * 1024
pixel_y = (1 - v) * 1024

---

## Key Decisions

* Ignore y (elevation not needed for minimap)
* Use relative time for playback
* Include bot combat for better signal

---

## Tradeoffs

| Area     | Decision  | Tradeoff                              |
| -------- | --------- | ------------------------------------- |
| UI       | Streamlit | Less customizable but fast            |
| Data     | Pandas    | Not optimized for very large scale    |
| Heatmaps | Plotly    | Simpler vs high-performance rendering |

---

## Outcome

Prioritized:

* correctness
* speed of development
* usability for designers
