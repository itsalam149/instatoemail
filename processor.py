import os
import datetime

async def process_instagram_data(links):
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"logs/input_{timestamp}.txt", "w") as f:
        for link in links:
            f.write(link.strip() + "\n")
