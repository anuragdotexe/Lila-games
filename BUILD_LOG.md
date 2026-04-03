# Build Log

## Day 1 — Data + Mapping

### What I did

* Loaded parquet files
* Decoded events
* Classified bots vs humans
* Reconstructed matches
* Implemented coordinate mapping
* Built first visualization

### Issues

* import errors (`src` module issue)
* missing loader file
* cluttered visual

### Fixes

* switched to module execution
* structured code properly
* downsampled movement

---

## Day 2 — Interactivity

### What I built

* filters
* timeline playback
* heatmaps

### Major issue (important)

Timeline slider initially failed:

* using pandas timestamps → Streamlit error
* converting to seconds → all values collapsed
* slider error: min == max

### Fix

* switched to **relative milliseconds**
* ensured time progression works
* added fallback for single timestamp matches

### Learning

Small data transformations can break UI logic.

---

## Day 3 — Deployment + Docs

### What I did

* deployed app
* cleaned repo
* wrote documentation
* extracted insights

Live App:
https://anurag-lila-games.streamlit.app

---

## Final Reflection

Key challenges:

* match reconstruction
* coordinate accuracy
* timeline stability

This project evolved from raw data → usable product.
