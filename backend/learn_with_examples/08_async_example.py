import asyncio
import time


async def countdown(num: int):
    print(f"task {num} started.")

    # async function need something 'awaitable' to be asynchronous
    await asyncio.sleep(0.01)

    print(f"task {num} finished.")


async def spawn_task():
    task_list = []

    for n in range(1001):
        task_list.append(asyncio.create_task(countdown(n)))

    await asyncio.gather(*task_list)


start = time.time()
asyncio.run(spawn_task())
end = time.time()
print(f"Time elapsed: {end-start}")
