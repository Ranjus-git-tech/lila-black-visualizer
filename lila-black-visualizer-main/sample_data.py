import os
import random
import shutil

SOURCE = "player_data"
DEST = "sampled_data"

FILES_PER_DAY = 18  # change if needed

os.makedirs(DEST, exist_ok=True)

for day in os.listdir(SOURCE):
    day_path = os.path.join(SOURCE, day)

    if not os.path.isdir(day_path):
        continue

    files = [f for f in os.listdir(day_path) if f.endswith(".nakama-0")]

    sampled = random.sample(files, min(FILES_PER_DAY, len(files)))

    dest_day = os.path.join(DEST, day)
    os.makedirs(dest_day, exist_ok=True)

    for f in sampled:
        shutil.copy(
            os.path.join(day_path, f),
            os.path.join(dest_day, f)
        )

print("✅ Sampling done!")