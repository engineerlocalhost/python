import time

class AdaptiveRateLimiter:

    def __init__(self, base_delay):
        self.base_delay = base_delay
        self.penalty = 1.0

    def success(self):
        # perlahan kembali normal
        self.penalty = max(1.0, self.penalty * 0.9)

    def failure(self):
        # IG mulai curiga → perlambat drastis
        self.penalty *= 1.7
        print(f"⚠️ Rate penalty increased → x{self.penalty:.2f}")

    def wait(self):
        delay = self.base_delay * self.penalty
        print(f"🕒 Adaptive wait {delay:.1f}s")
        time.sleep(delay)