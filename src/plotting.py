from PIL import Image
import plotly.graph_objects as go

from src.preprocess import get_all_game_files, load_match
from src.coordinate_mapper import add_minimap_coordinates


MINIMAP_PATHS = {
    "AmbroseValley": "assets/minimaps/AmbroseValley_Minimap.png",
    "GrandRift": "assets/minimaps/GrandRift_Minimap.png",
    "Lockdown": "assets/minimaps/Lockdown_Minimap.jpg",
}


EVENT_STYLE = {
    "Loot": {"symbol": "diamond", "size": 8},
    "BotKill": {"symbol": "x", "size": 9},
    "BotKilled": {"symbol": "cross", "size": 9},
    "Kill": {"symbol": "star", "size": 10},
    "Killed": {"symbol": "circle-x", "size": 10},
    "KilledByStorm": {"symbol": "triangle-up", "size": 10},
}


def build_match_plot(
    df,
    map_id,
    show_heatmap=False,
    heatmap_type="movement",
):
    image_path = MINIMAP_PATHS[map_id]
    img = Image.open(image_path)
    width, height = img.size

    fig = go.Figure()

    fig.add_layout_image(
        dict(
            source=img,
            x=0,
            y=0,
            sizex=width,
            sizey=height,
            xref="x",
            yref="y",
            layer="below",
        )
    )

    # ---------- HEATMAP ----------
    if show_heatmap:
        if heatmap_type == "movement":
            heat_df = df[df["event"].isin(["Position", "BotPosition"])].copy()
            heat_name = "Movement Heatmap"
        elif heatmap_type == "kill":
            heat_df = df[df["event"].isin(["Kill", "BotKill"])].copy()
            heat_name = "Kill Zone Heatmap"
        elif heatmap_type == "death":
            heat_df = df[df["event"].isin(["Killed", "BotKilled", "KilledByStorm"])].copy()
            heat_name = "Death Zone Heatmap"
        else:
            heat_df = df.copy()
            heat_name = "Heatmap"

        if not heat_df.empty:
            fig.add_trace(
                go.Histogram2dContour(
                    x=heat_df["pixel_x"],
                    y=heat_df["pixel_y"],
                    name=heat_name,
                    showscale=False,
                    contours=dict(coloring="heatmap"),
                    opacity=0.55,
                    hoverinfo="skip",
                )
            )

    # ---------- MOVEMENT ----------
    movement_df = df[df["event"].isin(["Position", "BotPosition"])].copy()
    movement_df = movement_df.iloc[::3]

    human_df = movement_df[movement_df["player_type"] == "human"]
    bot_df = movement_df[movement_df["player_type"] == "bot"]

    fig.add_trace(
        go.Scatter(
            x=human_df["pixel_x"],
            y=human_df["pixel_y"],
            mode="markers",
            name="Human Movement",
            marker=dict(size=4, opacity=0.75),
            text=human_df["user_id"],
            hovertemplate="Human<br>x=%{x:.1f}<br>y=%{y:.1f}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=bot_df["pixel_x"],
            y=bot_df["pixel_y"],
            mode="markers",
            name="Bot Movement",
            marker=dict(size=4, opacity=0.5),
            text=bot_df["user_id"],
            hovertemplate="Bot<br>x=%{x:.1f}<br>y=%{y:.1f}<extra></extra>",
        )
    )

    # ---------- EVENT MARKERS ----------
    for event_type, style in EVENT_STYLE.items():
        event_df = df[df["event"] == event_type]

        if not event_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=event_df["pixel_x"],
                    y=event_df["pixel_y"],
                    mode="markers",
                    name=event_type,
                    marker=dict(
                        size=style["size"],
                        symbol=style["symbol"],
                    ),
                    hovertemplate=f"{event_type}<br>x=%{{x:.1f}}<br>y=%{{y:.1f}}<extra></extra>",
                )
            )

    fig.update_xaxes(
        range=[0, width],
        showgrid=False,
        zeroline=False,
        visible=False,
    )

    fig.update_yaxes(
        range=[height, 0],
        showgrid=False,
        zeroline=False,
        visible=False,
        scaleanchor="x",
    )

    fig.update_layout(
        title=f"{map_id} — Match Visualization",
        width=950,
        height=950,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def main():
    match_id = "d3a3297e-2cdf-4a49-8450-09119b91a779.nakama-0"

    files = get_all_game_files()
    df = load_match(files, match_id)
    df = add_minimap_coordinates(df)

    map_id = df["map_id"].iloc[0]
    fig = build_match_plot(df, map_id, show_heatmap=True, heatmap_type="movement")
    fig.show()


if __name__ == "__main__":
    main()