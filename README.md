# 🎮 Lila Black – Player Behavior Visualizer

A simple tool built to help **Level Designers** quickly understand how players interact with a map.

This is not a data dashboard.
This is a **decision tool**.

---

## 🧠 The Problem

Gameplay data is messy and overwhelming.

* Too many files
* Too much noise
* Too hard to interpret

Designers don’t need raw data.
They need to **see patterns instantly**.

---

## 🎯 The Solution

This tool turns gameplay data into **clear visual insights on the minimap**.

Instead of digging through data, designers can:

* See where players move
* Identify fight hotspots
* Detect unused areas
* Understand bot vs human behavior

All in a few seconds.

---

## 🚀 What You Can Do

* 🗺️ View player movement directly on the map
* 🔥 Spot high-traffic and combat zones using heatmaps
* 🎯 Filter by match and time
* 🔵 Compare humans vs 🔴 bots visually

No complex controls. No clutter.

---

## ⚡ Why It’s Fast

The original dataset is large and slow to work with.

So instead of loading everything, this tool uses a **sampling approach**:

* Only a small, representative set of matches is used
* Keeps the app fast and responsive
* Still preserves meaningful gameplay patterns

---

## 🔧 Preparing Your Data

Before running the app, you need to reduce the dataset.

Run:

```
python sample_data.py
```

This will:

* Automatically pick a random set of match files
* Keep the selection balanced across days
* Create a new lightweight dataset

Output:

```
sampled_data/
```

Rename it to:

```
player_data/
```

---

## ▶️ Run the App

```
pip install -r requirements.txt
streamlit run app.py
```

---

## 🎨 Visual System

* 🔵 Humans
* 🔴 Bots
* 🟢 Kills
* ⚫ Deaths
* 🟡 Loot
* 🟣 Storm

Designed to be readable at a glance.

---

## 🧩 Design Principles

* Clarity over complexity
* Visual over technical
* Fast over complete
* Built for designers, not analysts

---

## 📁 Project Structure

```
lila-black-visualizer/
│
├── minimaps/
├── player_data/
├── sample_data.py
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Outcome

This tool helps designers:

* Make faster decisions
* Spot balance issues early
* Improve map design using real player behavior

---

## 👤 Author

Ranju Poddar

---
