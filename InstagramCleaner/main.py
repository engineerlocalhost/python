import json
from auth import login
from filters import filter_old_posts
from cleaner import smart_clean

print("=== INSTAGRAM SMART CLEANER ===")

with open("config.json") as f:
    config = json.load(f)

cl = login(config["username"], config["password"])

print("📡 Fetching medias...")
medias = cl.user_medias(cl.user_id, amount=200)

print("Filtering old posts...")
old_posts = filter_old_posts(
    medias,
    config["older_than_days"]
)

print(f"Found {len(old_posts)} old posts")

if len(old_posts) == 0:
    print("Nothing to clean.")
    exit()

smart_clean(cl, config, old_posts)