import os
import json
import asyncio
import aiohttp
import multiprocessing
import time
import win32file


HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}


class AsyncGet:

    def __init__(self, url):
        self.url = url
        # self.semaphore = asyncio.Semaphore(1024)

    async def aiohttp_get(self, queue):
        data = {}
        # async with self.semaphore:
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            data.setdefault("start", start_time)
            async with session.get(self.url, headers=HEADERS, verify_ssl=False) as response:
                now_time = time.time()
                data.setdefault("finish", now_time)
                data.setdefault("cost", now_time - start_time)
                if response.status == 200:
                    ret = await response.text()
                    queue.put(data)

    def create_task(self, queue):
        return asyncio.create_task(self.aiohttp_get(queue))

    async def async_get(self, start, end, queue):
        tasks = [self.create_task(queue) for _ in range(start, end)]
        while True:
            for task in tasks:
                if task._state == "PENDING":
                    await asyncio.sleep(0)
                    break
            else:
                break

    async def _async_get(self, start, end, queue):
        for _ in range(start, end):
            await self.aiohttp_get(queue)

    def get(self, *args):
        asyncio.run(self.async_get(*args))



def get(url, n=1):
    cpus = os.cpu_count() - 1
    queue = multiprocessing.Queue()
    data = []
    for c in range(cpus):
        d = []
        start = n * c // cpus
        end   = n * (c + 1) // cpus
        print(start, end)
        process = multiprocessing.Process(target=AsyncGet(url).get, args=(start, end, queue))
        process.daemon = False
        process.start()
        for _ in range(start, end):
            d.append(queue.get())
        data.append(d)
    return data

if __name__ == '__main__':
    print("=================")
    start_time = time.time()
    win32file._setmaxstdio(2048)
    print(win32file._getmaxstdio())
    data = get("https://www.baidu.com/", n=7700)
    # print(json.dumps(data, indent=4))
    print("Finished in %.fs" % (time.time() - start_time))