import httpx
import asyncio

async def test():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://127.0.0.1:11434/v1/models")
        print(resp.status_code)

asyncio.run(test())