import os
import time
import asyncio
import aiohttp
import datetime
import platform
import traceback
import multiprocessing

from common.helper import G, get_execution


__all__ = ("get", "post")


HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}


def current_time():
    return datetime.datetime.now().strftime("%X")


class AsyncGet:

    def __init__(self, url, queue, test_start_time):
        self.url = url
        self.queue = queue
        if platform.system() != "Windows":
            self.semaphore = asyncio.Semaphore(1024)
        self.test_start_time = test_start_time

    async def get(self):
        data = {}
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url, headers=HEADERS, ssl=False)
            if response.status == 200:
                ret = await response.text()

    async def _await(self):
        for task in self.pool:
            try:
                await task
            except:
                traceback.print_exc()

    async def run(self, scope):
        self.pool = [asyncio.create_task(self.get()) for _ in range(*scope)]
        await self._await()

    def start(self, scope):
        G.test_start_time = self.test_start_time
        print("测试开始%.3fs后, 进程启动" % (time.time() - self.test_start_time))
        asyncio.run(self.run(scope))
        # G.record()
        self.queue.put(G.data)


class AsyncPost:

    def __init__(self, url, queue, test_start_time):
        self.url = url
        self.queue = queue
        if platform.system() != "Windows":
            self.semaphore = asyncio.Semaphore(1024)
        self.test_start_time = test_start_time

    async def post(self, data):
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, data=data, headers=HEADERS, ssl=False)
            if response.status == 200:
                ret = await response.text()

    async def _await(self):
        for task in self.pool:
            try:
                await task
            except:
                traceback.print_exc()

    async def run(self, data):
        self.pool = [asyncio.create_task(self.post(d)) for d in data]
        await self._await()

    def start(self, data):
        G.test_start_time = self.test_start_time
        print("测试开始%.3fs后, 进程启动" % (time.time() - self.test_start_time))
        asyncio.run(self.run(data))
        # G.record()
        self.queue.put(G.data)


def get(url, number=1):
    cpus = os.cpu_count() - 1
    if number < cpus:
        for _ in range(number):
            asyncio.run(AsyncGet(url).get())
        return
    file = os.path.join(get_execution(), "result.txt")
    result = []
    for c in range(cpus):
        x = number * c // cpus
        y = number * (c + 1) // cpus
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=AsyncGet(url, queue, time.time()).start, args=((x, y),))
        process.daemon = False
        process.start()
        for data in queue.get():
            result.append(data)
    return result


def post(url, data):
    cpus = os.cpu_count() - 1
    number = len(data)
    if number < cpus:
        for i in range(number):
            asyncio.run(AsyncPost(url).post(data[i]))
    result = []
    for c in range(cpus):
        x = number * c // cpus
        y = number * (c + 1) // cpus
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=AsyncPost(url, queue, time.time()).start, args=(data[x:y],))
        process.daemon = False
        process.start()
        for data in queue.get():
            result.append(data)
    return result
