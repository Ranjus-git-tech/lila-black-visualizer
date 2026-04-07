import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import plotly.graph_objects as go
import os
import random
from PIL import Image

st.set_page_config(layout="wide", page_title="LILA BLACK | Level Designer Tool")

# ---------------- MAP CONFIG ----------------
MAP_CONFIG = {
    "AmbroseValley": {"scale": 900, "origin_x": -370, "origin_z": -473, "img": "minimaps/AmbroseValley_Minimap.png"},
    "GrandRift": {"scale": 581, "origin_x": -290, "origin_z": -290, "img": "minimaps/GrandRift_Minimap.png"},
    "Lockdown": {"scale": 1000, "origin_x": -500, "origin_z": -500, "img": "minimaps/Lockdown_Minimap.jpg"}
}
COLORS = {
    "human": "#00cfff",   # bright blue 🔵
    "bot": "#ff2e2e",     # bright red 🔴

    "Kill": "#00ff66",    # neon green 🟢
    "Death": "#ffffff",   # white ⚪ (visible everywhere)
    "Loot": "#ffcc00",    # strong yellow 🟡
    "Storm": "#a64dff"    # bright violet 🟣
}

DATA_ROOT = "player_data"

# ---------------- COORD MAPPING ----------------
def world_to_pixel(x, z, cfg):
    u = (x - cfg["origin_x"]) / cfg["scale"]
    v = (z - cfg["origin_z"]) / cfg["scale"]
    px = u * 1024
    py = (1 - v) * 1024
    return px, py

def is_human(user_id):
    return "-" in str(user_id)

# ---------------- LOAD FILES ----------------
@st.cache_data
def build_manifest():
    manifest = []
    for date in os.listdir(DATA_ROOT):
        folder = os.path.join(DATA_ROOT, date)
        if not os.path.isdir(folder):
            continue

        for f in os.listdir(folder):
            if "_" in f:
                parts = f.split("_")
                match_id = parts[1].replace(".nakama-0", "")
                manifest.append({
                    "date": date,
                    "match_id": match_id,
                    "file": f
                })

    return pd.DataFrame(manifest)

@st.cache_data
def load_data(date, match_ids):
    folder = os.path.join(DATA_ROOT, date)
    frames = []

    for f in os.listdir(folder):
        if not f.endswith(".nakama-0"):
            continue

        # exact match_id check
        match_part = f.split("_")[1].replace(".nakama-0", "")
        if match_part not in match_ids:
            continue

        path = os.path.join(folder, f)

        try:
            df = pq.read_table(path).to_pandas()
            df["event"] = df["event"].apply(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)
            df["is_human"] = df["user_id"].apply(is_human)
            frames.append(df)
        except:
            continue

    if not frames:
        return pd.DataFrame(), None

    df = pd.concat(frames, ignore_index=True)

    map_id = df["map_id"].iloc[0]
    cfg = MAP_CONFIG[map_id]

    df["px"], df["py"] = zip(*df.apply(lambda r: world_to_pixel(r["x"], r["z"], cfg), axis=1))

    # timeline normalize
    df["ts"] = pd.to_datetime(df["ts"])
    start = df.groupby("match_id")["ts"].transform("min")
    df["match_sec"] = (df["ts"] - start).dt.total_seconds()

    return df, map_id

# ---------------- UI ----------------
st.title("🎮 Level Designer Behavior Tool")

manifest = build_manifest()

st.sidebar.markdown("""
<h2 style='margin-bottom: 0;'>
<span style='color:#00f5ff; text-shadow:0 0 6px #00f5ff;'>L</span>evel
<span style='color:#ff2e2e; text-shadow:0 0 6px #ff2e2e;'>S</span>ight
</h2>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

dates = sorted(manifest["date"].unique(), reverse=True)
selected_date = st.sidebar.selectbox("Select Date", dates)

map_list = ["AmbroseValley", "GrandRift", "Lockdown"]
selected_map = st.sidebar.selectbox("Select Map", map_list)

# sampling
all_matches = manifest[manifest["date"] == selected_date]["match_id"].unique().tolist()
random.shuffle(all_matches)
sampled_matches = all_matches[:40]

selected_match = st.sidebar.selectbox(
    "Match",
    ["All Sampled Matches"] + sampled_matches
)

view_mode = st.sidebar.radio("View Mode", ["Movement", "Heatmap"])

target_matches = sampled_matches if selected_match == "All Sampled Matches" else [selected_match]

df, map_id = load_data(selected_date, target_matches)
# 🔥 FORCE selected map instead of random
df = df[df["map_id"] == selected_map]

if df.empty:
    st.warning("No data for selected map")
    st.stop()

map_id = selected_map

# timeline
# timeline
if df["match_sec"].isnull().all():
    st.error("Timeline data missing")
    st.stop()

max_time = int(df["match_sec"].max())

# 🔥 FIX: handle edge cases
if max_time <= 0 or pd.isna(max_time):
    max_time = 1

time_val = st.slider("Timeline", 0, max_time, max_time)

df = df[df["match_sec"] <= time_val]

cfg = MAP_CONFIG[map_id]

# ---------------- PLOT ----------------
fig = go.Figure()

# minimap background (LOCAL FILE)
img = Image.open(cfg["img"])

fig.add_layout_image(
    dict(
        source=img,
        xref="x", yref="y",
        x=0, y=1024,
        sizex=1024, sizey=1024,
        sizing="stretch",
        layer="below"
    )
)

if view_mode == "Movement":

    # movement lines
    for (uid, mid), group in df.groupby(["user_id", "match_id"]):
        color = COLORS["human"] if group["is_human"].iloc[0] else COLORS["bot"]

        fig.add_trace(go.Scattergl(
            x=group["px"],
            y=group["py"],
            mode="lines",
            line=dict(color=color, width=1),
            opacity=0.3,
            hoverinfo="skip",
            showlegend=False
        ))

    # events
    event_colors = {
        "Kill": COLORS["Kill"],
        "BotKill": COLORS["Kill"],
        "Killed": COLORS["Death"],
        "BotKilled": COLORS["Death"],
        "KilledByStorm": COLORS["Storm"],
        "Loot": COLORS["Loot"]
    }

    for evt, color in event_colors.items():
        sub = df[df["event"] == evt]

        fig.add_trace(go.Scattergl(
            x=sub["px"],
            y=sub["py"],
            mode="markers",
            marker=dict(
                size=9,            
                color=color,
                line=dict(width=1.5, color="white")
            ),

            name=evt
        ))

else:
    # heatmap
    combat = df[df["event"].isin(["Kill", "BotKill", "Killed", "BotKilled"])]

    fig.add_trace(go.Histogram2dContour(
        x=combat["px"],
        y=combat["py"],
        colorscale="Hot",
        opacity=0.6,
        ncontours=20,
        showscale=False
    ))

# layout
map_guide = st.checkbox("🧭 Map Guide", value=False)
fig.update_layout(
    height=800,
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(range=[0, 1024], visible=False),
    yaxis=dict(range=[0, 1024], visible=False),
    plot_bgcolor="black",
    
    legend=dict(
    x=0,
    y=0.5,
    bgcolor="rgba(0,0,0,0.5)"
),
    showlegend=map_guide
)

st.plotly_chart(fig, use_container_width=True)
