import os
import asyncio
import aiohttp
import multiprocessing
import time


HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}

class AsyncGet:

    def __init__(self, url, threads_number=1):
        self.url = url
        self.threads_number = threads_number

    async def aiohttp_get(self, url):
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, verify_ssl=False) as response:
                if response.status == 200:
                    print(time.time() - start_time)
                    return await response.text()

    async def get(self, url, queue):
        """
        基于协程的get接口
        args:
            url: api address
        returns:
            a list include all data
        """
        ret = await self.aiohttp_get(url)
        queue.put(ret)


def async_get(url, queue):
    asyncio.run(AioHttp().get(url, queue))


def get(url, n=1):
    cpus = os.cpu_count() - 1
    queue = multiprocessing.Queue()
    result = []
    for c in range(cpus):
        start = n * c // cpus
        end   = n * (c + 1) // cpus
        process = multiprocessing.Process(target=async_get, target)
    return [asyncio.run(request) for _ in range(n)]


(get("https://www.csdn.net/", n=10))