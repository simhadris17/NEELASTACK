from collections import defaultdict, deque
from threading import Lock
from time import monotonic, time

from fastapi import Request
from fastapi.responses import JSONResponse

from packages.neelastack.core.config import settings


class InMemoryRateLimiter:
    """Small single-process limiter; deploy a shared Redis limiter for multi-worker use."""

    def __init__(self):
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> tuple[bool, int]:
        now = monotonic()
        cutoff = now - settings.rate_limit_window_seconds
        with self._lock:
            hits = self._hits[key]
            while hits and hits[0] <= cutoff:
                hits.popleft()
            if len(hits) >= settings.rate_limit_requests:
                retry_after = max(1, int(hits[0] + settings.rate_limit_window_seconds - now))
                return False, retry_after
            hits.append(now)
            return True, 0


limiter = InMemoryRateLimiter()


class RedisRateLimiter:
    """Atomic fixed-window limiter shared by all API replicas."""

    def __init__(self):
        self.client = None
        try:
            import redis
            self.client = redis.Redis.from_url(
                settings.redis_url, socket_connect_timeout=0.2, socket_timeout=0.2,
                decode_responses=True,
            )
        except Exception:
            self.client = None

    def allow(self, key: str) -> tuple[bool, int]:
        if self.client is None:
            return limiter.allow(key)
        epoch = time()
        bucket = int(epoch // settings.rate_limit_window_seconds)
        redis_key = f"neelastack:ratelimit:{bucket}:{key}"
        try:
            count = int(self.client.incr(redis_key))
            if count == 1:
                self.client.expire(redis_key, settings.rate_limit_window_seconds + 1)
            if count > settings.rate_limit_requests:
                return False, max(1, settings.rate_limit_window_seconds - int(epoch) % settings.rate_limit_window_seconds)
            return True, 0
        except Exception:
            return limiter.allow(key)


shared_limiter = RedisRateLimiter() if settings.rate_limit_use_redis else limiter


async def rate_limit_middleware(request: Request, call_next):
    if request.method == "OPTIONS" or request.url.path in {"/health", "/api/v1/health"}:
        return await call_next(request)
    # Limit every non-health request; this also protects read endpoints from scraping.
    protected = True
    if protected:
        client = request.client.host if request.client else "unknown"
        if settings.trust_proxy_headers:
            client = request.headers.get("x-forwarded-for", client).split(",")[0].strip()
        allowed, retry_after = shared_limiter.allow(client)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded", "retry_after": retry_after},
                headers={"Retry-After": str(retry_after)},
            )
    return await call_next(request)
