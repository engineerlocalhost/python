import random, time

def human_delay(min_s, max_s):
    delay = random.uniform(min_s, max_s)
    print(f"⏳ Human delay {delay:.1f}s")
    time.sleep(delay)


def simulate_user_behavior(cl):
    """
    Simulasi user browsing:
    buka feed, lihat beberapa post
    """

    try:
        print("👀 Simulating feed browsing...")
        medias = cl.timeline_feed()["feed_items"][:3]

        for _ in medias:
            time.sleep(random.uniform(2, 6))

    except:
        pass


def random_idle():
    if random.random() < 0.2:
        idle = random.uniform(40, 120)
        print(f"☕ User idle simulation {idle:.0f}s")
        time.sleep(idle)