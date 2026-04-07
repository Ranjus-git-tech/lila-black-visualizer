# 🧩 Architecture – LevelSight

A lightweight, visual-first system designed to turn raw gameplay logs into **spatial insight for level designers**.

> Built for decision-making, not reporting.

---

## 🛠️ What I Built & Why

* **Streamlit** → rapid development, minimal UI friction
* **Plotly (Scattergl + Heatmaps)** → interactive, GPU-accelerated rendering
* **Pandas** → fast, flexible data transformation

**Goal:** Not a dashboard. A **decision tool** that surfaces patterns instantly.

---

## 🔄 Data Flow

```
Raw Data (Parquet / logs)
        ↓
Load → Pandas DataFrames
        ↓
Transform → positions, events, player type
        ↓
Coordinate Mapping → world → minimap pixels
        ↓
Visualization → Plotly layers
        ↓
UI → Streamlit controls
```

### Transformed Fields

* Player positions: `(x, z)` → `(px, py)`
* Event types: `Kill, Death, Loot, Storm`
* Player type: `is_human`

---

## 🗺️ Coordinate Mapping (Core Problem)

Game data exists in **world space**, not aligned with the minimap.

### Approach

```
u = (x - origin_x) / scale
v = (z - origin_z) / scale

px = u * 1024
py = (1 - v) * 1024
```

### Why this works

* Normalizes coordinates into **[0, 1]**
* Maps directly to a **1024×1024 minimap**
* Inverts Y-axis to match screen coordinates

### Assumptions

* Fixed `origin` and `scale` per map
* Axis-aligned maps (no rotation)
* Consistent coordinate system per dataset

---

## 📦 Processing Layer

Handled with **Pandas**

Responsibilities:

* Filter by **date / map / match**
* Split into:

  * Movement data
  * Combat events
  * Loot / storm events
* Normalize event types (e.g., `Kill` vs `BotKill`)

---

## 🎯 Visualization Layer

Built with **Plotly (Scattergl)**

### Encoding System

* 🔵 Humans | 🔴 Bots
* ● Kills (circles)
* ✕ Deaths (X markers)
* 🟡 Loot
* 🟣 Storm

### Heatmaps

* Density-based contours to reveal:

  * Combat hotspots
  * Movement clusters

**Why Scattergl?**

* Handles large point sets smoothly
* Keeps interaction responsive (zoom, pan, hover)

---

## 🧠 Sampling Layer (Performance Strategy)

Script: `sample_data.py`

### Purpose

* Reduce dataset size
* Maintain representative patterns

### Steps

1. Randomly sample match files
2. Balance across days
3. Output lightweight dataset

### Tradeoff

* **Speed & usability** vs full completeness

---

## ⚠️ Ambiguities & Handling

| Problem               | Solution                     |
| --------------------- | ---------------------------- |
| Bot vs Human unclear  | Used `is_human` flag         |
| Duplicate event types | Normalized via mapping       |
| Sparse days/maps      | Treated as real distribution |
| Large dataset         | Sampling for performance     |

---

## ⚖️ Key Design Decisions

| Decision                   | Why                    | Tradeoff              |
| -------------------------- | ---------------------- | --------------------- |
| Sampling over full dataset | Fast, interactive UI   | Not exhaustive        |
| Streamlit UI               | Rapid build, simple UX | Limited customization |
| Visual-first encoding      | Instant readability    | Less numeric depth    |
| Separate event handling    | Cleaner visuals        | More logic            |

---

## 🚧 Limitations

* No real-time ingestion
* No replay/timeline system
* Sampling may miss edge cases
* Bot behavior inferred (not modeled)

---

## 🚀 Scalability Path

* Add **DuckDB / PostgreSQL** for larger datasets
* Incremental loading (windowed queries)
* Server-side filtering API
* Advanced WebGL optimizations for dense scenes

---

## 📦 Summary

* Lightweight, fast, interactive
* Maps gameplay → spatial insight
* Optimized for **clarity over complexity**

---

## 🎯 Final Principle

> The hardest problem is not storing data.
> It is making **patterns obvious instantly**.

**This system is designed to do exactly that.**
