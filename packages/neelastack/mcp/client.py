import httpx
async def call(server_url, name, arguments=None):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(server_url, json={"name": name, "arguments": arguments or {}})
        r.raise_for_status()
        return r.json()
