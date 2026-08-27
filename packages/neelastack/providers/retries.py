import asyncio
async def with_retry(fn, attempts=3, delay=1):
    last = None
    for i in range(attempts):
        try: return await fn()
        except Exception as exc:
            last = exc
            if i + 1 < attempts: await asyncio.sleep(delay * (i + 1))
    raise last
