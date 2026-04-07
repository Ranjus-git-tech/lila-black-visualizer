# 🧩 Architecture – LevelSight

## 🛠️ What I Built & Why

I built a lightweight visualization tool using:

* **Streamlit** → fast iteration, minimal UI overhead
* **Plotly** → interactive rendering (zoom, hover, layering)
* **Pandas** → efficient data handling

The goal was not to build a dashboard, but a **decision tool for level designers** — prioritizing clarity and speed over complexity.

---

## 🔄 Data Flow

1. **Raw Data (Parquet / JSON-like logs)**
2. → Loaded into Pandas DataFrames
3. → Transformed into:

   * Player positions (x, z)
   * Event types (Kill, Death, Loot, Storm)
   * Player type (Human / Bot)
4. → Converted into pixel coordinates
5. → Rendered on minimap using Plotly

---

## 🗺️ Coordinate Mapping (Core Problem)

Game coordinates exist in a world space, not aligned with the minimap.

### Approach:

```python
u = (x - origin_x) / scale
v = (z - origin_z) / scale

px = u * 1024
py = (1 - v) * 1024
```

### Why this works:

* Normalizes coordinates into 0–1 range
* Maps them directly onto a 1024×1024 minimap
* Inverts Y-axis to match screen coordinates

### Assumptions:

* Each map has fixed origin and scale
* Data is consistent per map
* No rotation required (axis-aligned)

---

## ⚠️ Ambiguities & Handling

| Problem                                 | Solution                              |
| --------------------------------------- | ------------------------------------- |
| Bot vs Human unclear in events          | Used `is_human` flag                  |
| Duplicate event types (Kill vs BotKill) | Normalized via mapping                |
| Sparse data on certain days/maps        | Accepted as real distribution         |
| Large dataset                           | Used sampling to maintain performance |

---

## ⚖️ Tradeoffs

| Decision                         | Tradeoff                           |
| -------------------------------- | ---------------------------------- |
| Sampling instead of full dataset | Faster UI, less completeness       |
| Streamlit over full frontend     | Faster dev, less customization     |
| Visual encoding (color + shape)  | Simpler UX vs richer detail        |
| No backend                       | Easier deploy, limited scalability |

---

## 🚀 Key Design Principle

> This tool prioritizes **instant visual understanding** over analytical depth.

Level designers should:

* See patterns immediately
* Not interpret raw data

---

## 📦 Summary

* Lightweight, fast, and interactive
* Designed for **decision-making, not reporting**
* Solves the hardest problem: **mapping gameplay to spatial insight**
