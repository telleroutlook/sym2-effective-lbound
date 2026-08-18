"""Shared heartbeat utility for long-running computations.

Usage:
    from heartbeat import Heartbeat
    hb = Heartbeat(interval=30)
    for i, item in enumerate(items):
        hb.tick(f"processing {i}/{len(items)}")
        # ... work ...
    hb.done()
"""
import time
import sys


class Heartbeat:
    def __init__(self, interval: int = 30):
        self.interval = interval
        self.t0 = time.time()
        self.last_print = 0.0

    def tick(self, msg: str = ""):
        now = time.time()
        if now - self.last_print >= self.interval:
            elapsed = now - self.t0
            m, s = divmod(int(elapsed), 60)
            h, m = divmod(m, 60)
            ts = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
            print(f"  [HEARTBEAT {ts}] {msg}", flush=True)
            self.last_print = now

    def done(self):
        elapsed = time.time() - self.t0
        m, s = divmod(int(elapsed), 60)
        h, m = divmod(m, 60)
        ts = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        print(f"  [DONE {ts}]", flush=True)
