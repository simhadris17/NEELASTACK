import asyncio
class Scheduler:
    async def submit(self, coro): return await asyncio.create_task(coro)
