from instagrapi import Client
import os

SESSION_FILE = "session.json"

def login(username, password):
    cl = Client()

    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(username, password)
        else:
            cl.login(username, password)
            cl.dump_settings(SESSION_FILE)

        print("✅ Login success")
        return cl

    except Exception as e:
        msg = str(e).lower()

        if "challenge_required" in msg or "checkpoint" in msg:
            print("🚨 CHECKPOINT DETECTED")
            print("Login manually via phone first.")
        else:
            print("Login error:", e)

        raise SystemExit