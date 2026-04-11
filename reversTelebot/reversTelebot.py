#!/usr/bin/env python3
import requests
import threading
import time
import os
from queue import Queue

# ===== CONFIG =====
BOT_TOKEN = "7957950976:AAEmOQA_zfEXmEUn_LBDMDBF2Yog9JjoyWg"  # WAJIB GANTI
CHAT_ID = "8152707019"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

IMAGE_PATH = "tanos.webp"  # pastikan file ada
WORKER_COUNT = 2          # jangan besar-besar
DELAY_PER_MESSAGE = 1     # 1 detik (aman dari limit)

# ===== QUEUE SYSTEM =====
queue = Queue()

class TelegramSender:
    def __init__(self):
        self.success = 0
        self.failed = 0

    def send_image(self):
        try:
            with open(IMAGE_PATH, "rb") as f:
                files = {"photo": f}
                data = {
                    "chat_id": CHAT_ID,
                    "caption": f"image_{int(time.time())}"
                }

                resp = requests.post(URL, data=data, files=files, timeout=10)

            # DEBUG RESPONSE
            if resp.status_code == 200:
                self.success += 1
                print(f"✅ Sent #{self.success}")
            else:
                self.failed += 1
                print(f"❌ Failed ({resp.status_code}): {resp.text}")

                # HANDLE RATE LIMIT
                if resp.status_code == 429:
                    retry_after = resp.json().get("parameters", {}).get("retry_after", 5)
                    print(f"⏳ Rate limited. Sleep {retry_after}s")
                    time.sleep(retry_after)

        except Exception as e:
            self.failed += 1
            print(f"❌ Error: {e}")

    def worker(self):
        while True:
            queue.get()
            self.send_image()
            time.sleep(DELAY_PER_MESSAGE)
            queue.task_done()


def main():
    print("🚀 Telegram Sender Started")

    # cek file dulu
    if not os.path.exists(IMAGE_PATH):
        print("❌ File image.jpg tidak ditemukan")
        return

    sender = TelegramSender()

    # start worker threads
    for _ in range(WORKER_COUNT):
        t = threading.Thread(target=sender.worker, daemon=True)
        t.start()

    # enqueue jobs (bisa diatur sesuai kebutuhan)
    try:
        while True:
            queue.put(1)
            time.sleep(0.5)  # producer speed
            print(f"📊 Success: {sender.success} | Failed: {sender.failed}")
    except KeyboardInterrupt:
        print("\n🛑 Stopped")


if __name__ == "__main__":
    main()