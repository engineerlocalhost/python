from behavior import human_delay, simulate_user_behavior, random_idle
from rate_limit import AdaptiveRateLimiter

def smart_clean(cl, config, medias):

    limiter = AdaptiveRateLimiter(config["min_delay"])

    actions_done = 0
    max_actions = config["max_actions_per_run"]

    # Warm-up mode (akun terlihat aktif dulu)
    if config["warmup_mode"]:
        print("🔥 Warmup mode active")
        simulate_user_behavior(cl)

    for media in medias:

        if actions_done >= max_actions:
            print("✅ Safe action limit reached")
            break

        try:
            simulate_user_behavior(cl)

            if config["mode"] == "archive":
                print("📦 Archiving:", media.id)
                cl.media_archive(media.id)

            elif config["mode"] == "delete":
                print("🗑️ Deleting:", media.id)
                cl.media_delete(media.id)

            limiter.success()
            limiter.wait()

            human_delay(
                config["min_delay"],
                config["max_delay"]
            )

            random_idle()

            actions_done += 1

        except Exception as e:
            print("⚠️ Exception detected:", e)

            limiter.failure()

            # kemungkinan rate limit / soft block
            print("Cooling down 5 minutes...")
            import time
            time.sleep(300)

    print(f"✨ Finished. Actions performed: {actions_done}")