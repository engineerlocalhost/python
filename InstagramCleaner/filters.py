from datetime import datetime, timedelta

def filter_old_posts(medias, days):
    limit = datetime.now() - timedelta(days=days)

    old = []
    for m in medias:
        if m.taken_at < limit:
            old.append(m)

    return old