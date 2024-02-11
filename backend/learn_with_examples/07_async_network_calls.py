import asyncio
import time
import requests
import aiohttp


async def make_request(session, req_n):
    url = "https://httpbin.com/get"
    print(f"making request {req_n}")
    async with session.get(url) as resp:
        if resp.status == 200:
            await resp.text()


async def main():
    request_count = 100
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[make_request(session, idx) for idx in range(request_count)]
        )


loop = asyncio.get_event_loop()
start = time.time()
loop.run_until_complete(main())
end = time.time()
print(f"Time elapsed: {end-start}")
