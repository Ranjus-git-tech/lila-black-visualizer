🎮 Lila Black – Player Behavior Visualizer

A simple, fast tool built to help Level Designers understand how players actually behave on a map.

> This is not a data dashboard. This is a decision tool.




---

🔗 Live Demo

👉 https://lila-black-visualizer-mplzxlctvwrcbaxzom7bcx.streamlit.app/


---

🧠 The Problem

Gameplay data is messy and overwhelming.

Too many files

Too much noise

Too hard to interpret


Designers don’t need raw data. They need to see patterns instantly.


---

🎯 The Solution

This tool converts gameplay data into clear, visual insights directly on the minimap.

Instead of digging through logs, designers can:

See where players move

Identify fight hotspots

Detect unused areas

Understand bot vs human behavior


All in seconds, not hours.


---

🚀 What You Can Do

🗺️ View player movement directly on the map

🔥 Spot high-traffic and combat zones using heatmaps

⚔️ Visualize kills, deaths, loot, and storm events

🎯 Filter by map, date, and match

🔵 Compare humans vs 🔴 bots instantly


No clutter. No over-engineering.


---

🧪 Key Insights

1. Loot Drives Player Behavior

Player movement and combat patterns strongly align with loot placement

Changing loot distribution directly reshapes player flow


2. Centralized Combat Patterns

Majority of matches cluster combat in central zones

Indicates over-reliance on specific high-value areas


3. Chokepoint vs Loot Zone Dynamics

Bots die along traversal paths (roads, chokepoints)

Humans die inside high-loot zones

Matches are often decided before peak loot is reached


> The map separates elimination phases: traversal filters bots, loot zones determine human outcomes.




---

⚡ Why It’s Fast

The original dataset is large and slow.

So the tool uses sampling instead of full loading:

Selects a small but representative set of matches

Keeps performance smooth and responsive

Preserves meaningful gameplay patterns



---

🔧 Preparing Your Data

Before running the app:

python sample_data.py

This will:

Randomly sample match files

Balance data across days

Create a lightweight dataset


Rename output:

sampled_data/ → player_data/


---

▶️ Run the App

pip install -r requirements.txt
streamlit run app.py


---

🎨 Visual System

🔵 Humans

🔴 Bots

🟢 Kills

⚪ Deaths

🟡 Loot

🟣 Storm


Designed for instant readability.


---

⚙️ How It Works

1. Load sampled parquet match data


2. Convert world coordinates → minimap pixels


3. Render:

Movement paths

Event markers

Heatmaps



4. Apply filters


5. Surface visual patterns




---

📐 Coordinate Mapping

Coordinates are transformed using:

Origin offsets (origin_x, origin_z)

Map scaling

Normalization to 1024×1024 space


Ensures accurate overlay on minimaps.


---

⚖️ Design Principles

Clarity over complexity

Visual over technical

Fast over complete

Built for designers, not analysts



---

⚖️ Design Decisions & Tradeoffs

Decision	Why	Tradeoff

Scattergl	Handles large data smoothly	Less styling control
Heatmaps	Clear density visualization	Less precise than raw points
Sampling	Fast performance	Not full dataset
Human vs Bot styling	Immediate clarity	More logic complexity



---

🚧 Assumptions

is_human correctly classifies players

Event logs are reliable

Map configs are accurate

Sampled matches reflect real behavior



---

📂 Project Structure

├── app.py
├── player_data/
├── minimaps/
├── sample_data.py
├── requirements.txt
├── INSIGHTS.md
├── ARCHITECTURE.md
└── README.md


---

🎯 Why This Matters

This tool shows how:

Game systems shape player decisions

Loot placement controls movement and combat

Visual data leads to better level design decisions



---

📌 Future Improvements

Timeline/replay slider

Zone shrink visualization

Smarter bot behavior analysis

UI polish and filtering improvements



---

🚀 Outcome

Helps designers:

Make faster decisions

Identify balance issues early

Design better maps using real behavior



---

👤 Author

Ranju Poddar


---

🙌 Final Note

> Good maps guide players.
Great maps control behavior without players noticing.
