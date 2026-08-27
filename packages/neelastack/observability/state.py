from collections import deque
from threading import Lock
from time import perf_counter


class RequestMetrics:
    def __init__(self):
        self._lock = Lock()
        self.requests = 0
        self.errors = 0
        self.total_ms = 0.0
        self.recent: deque[dict] = deque(maxlen=100)

    def observe(self, method: str, path: str, status: int, started: float):
        duration = round((perf_counter() - started) * 1000, 2)
        with self._lock:
            self.requests += 1
            self.errors += int(status >= 400)
            self.total_ms += duration
            self.recent.append({"method": method, "path": path, "status": status, "duration_ms": duration})

    def snapshot(self):
        with self._lock:
            return {
                "requests": self.requests,
                "errors": self.errors,
                "average_latency_ms": round(self.total_ms / self.requests, 2) if self.requests else 0,
                "recent": list(self.recent),
            }


metrics = RequestMetrics()
