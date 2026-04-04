import streamlit as st
import pandas as pd

from src.preprocess import get_all_game_files, load_match
from src.coordinate_mapper import add_minimap_coordinates
from src.plotting import build_match_plot


st.set_page_config(layout="wide")


@st.cache_data
def build_file_index():
    files = get_all_game_files()
    records = []

    for file_path in files:
        name = file_path.name

        if "_" not in name:
            continue

        _, match_id = name.split("_", 1)

        records.append(
            {
                "match_id": match_id,
                "source_day": file_path.parent.name,
            }
        )

    return pd.DataFrame(records).drop_duplicates()


@st.cache_data
def load_match_data(match_id):
    files = get_all_game_files()
    df = load_match(files, match_id)
    df = add_minimap_coordinates(df)
    return df


st.title("🎮 Player Journey Visualization Tool")

file_index = build_file_index()

# ---------- SIDEBAR ----------
st.sidebar.header("Filters")

dates = sorted(file_index["source_day"].unique())
selected_date = st.sidebar.selectbox("Select Date", dates)

filtered_index = file_index[file_index["source_day"] == selected_date]

match_list = sorted(filtered_index["match_id"].unique())
selected_match = st.sidebar.selectbox("Select Match", match_list)

map_options = ["All", "AmbroseValley", "GrandRift", "Lockdown"]
selected_map = st.sidebar.selectbox("Select Map", map_options)

st.sidebar.divider()

st.sidebar.header("Display")

show_humans = st.sidebar.checkbox("Show Humans", True)
show_bots = st.sidebar.checkbox("Show Bots", True)
show_events = st.sidebar.checkbox("Show Events", True)

st.sidebar.divider()

st.sidebar.header("Heatmap")

show_heatmap = st.sidebar.checkbox("Enable Heatmap", False)

heatmap_type = "movement"
if show_heatmap:
    heatmap_type = st.sidebar.selectbox(
        "Type",
        ["movement", "kill", "death"],
    )

# ---------- LOAD DATA ----------
df = load_match_data(selected_match).copy()
map_id = df["map_id"].iloc[0]

if selected_map != "All" and map_id != selected_map:
    st.warning(f"This match belongs to {map_id}, not {selected_map}")

st.subheader(f"Map: {map_id}")

# ---------- TIMELINE ----------
st.markdown("### ⏱ Match Timeline")

df["ts_ms"] = df["ts"].astype("int64") // 10**6
match_start = int(df["ts_ms"].min())
df["timeline_ms"] = df["ts_ms"] - match_start

min_t = int(df["timeline_ms"].min())
max_t = int(df["timeline_ms"].max())
timeline_span = max_t - min_t

single_timestamp_match = timeline_span == 0

if not single_timestamp_match:
    selected_t = st.slider(
        "Select Time in Match (ms)",
        min_value=min_t,
        max_value=max_t,
        value=max_t,
    )
    st.caption(f"Time into match: {selected_t / 1000:.2f} seconds")
    timeline_df = df[df["timeline_ms"] <= selected_t].copy()
else:
    st.info(
        "This match contains events within a single timestamp window, so playback is not shown. Displaying the full available match slice."
    )
    timeline_df = df.copy()

# ---------- DATA FILTERS ----------
filtered_df = timeline_df.copy()

if not show_humans:
    filtered_df = filtered_df[filtered_df["player_type"] != "human"]

if not show_bots:
    filtered_df = filtered_df[filtered_df["player_type"] != "bot"]

if show_heatmap:
    filtered_df = filtered_df[
        filtered_df["event"].isin(["Position", "BotPosition"])
    ]
elif not show_events:
    filtered_df = filtered_df[
        filtered_df["event"].isin(["Position", "BotPosition"])
    ]

# ---------- PLOT ----------
fig = build_match_plot(
    filtered_df,
    map_id,
    show_heatmap=show_heatmap,
    heatmap_type=heatmap_type,
)

st.plotly_chart(fig, width="stretch")

if len(filtered_df) > 0:
    st.caption(
        "Note: Player activity may be concentrated in specific regions depending on match dynamics."
    )

# ---------- STATS ----------
st.markdown("### 📊 Match Summary")

c1, c2, c3 = st.columns(3)
c1.metric("Visible Rows", len(filtered_df))
c2.metric("Players", filtered_df["user_id"].nunique())
c3.metric("Event Types", filtered_df["event"].nunique())

st.markdown("### Event Distribution")
st.write(
    filtered_df["event"]
    .value_counts()
    .rename_axis("event")
    .reset_index(name="count")
)

# ---------- HEATMAP SUMMARY ----------
if show_heatmap:
    st.markdown("### Heatmap Mode")
    if heatmap_type == "movement":
        st.write("Showing high-traffic movement density across the visible portion of the match.")
    elif heatmap_type == "kill":
        st.write("Showing kill concentration zones using Kill and BotKill events.")
    elif heatmap_type == "death":
        st.write("Showing death concentration zones using Killed, BotKilled, and KilledByStorm events.")

# ---------- DEBUG ----------
st.markdown("### Timeline Diagnostics")
d1, d2, d3 = st.columns(3)

if single_timestamp_match:
    d1.metric("Timeline Mode", "Single Window")
    d2.metric("Visible Time Points", df["timeline_ms"].nunique())
    d3.metric("Timeline Span (ms)", "N/A")
else:
    d1.metric("Start (ms)", min_t)
    d2.metric("End (ms)", max_t)
    d3.metric("Span (ms)", timeline_span)