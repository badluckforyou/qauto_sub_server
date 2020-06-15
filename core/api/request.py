import os
import json
import time
import asyncio
import aiohttp
import datetime
import multiprocessing
# import win32file


__all__ = ("get", "post")


HEADERS = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}


def current_time():
    return datetime.datetime.now().strftime("%X")


class AsyncGet:

    def __init__(self, url, queue):
        self.url = url
        self.semaphore = asyncio.Semaphore(1024)
        self.queue = queue
        self.count = 0

    async def get(self):
        data = {}
        async with aiohttp.ClientSession() as session:
            # start_time = time.time()
            response = await session.get(self.url, headers=HEADERS, ssl=False)
            # print("Get cost %.2fs" % (time.time() - start_time))
            if response.status == 200:
                self.count += 1
                ret = await response.text()

    def create_task(self):
        return asyncio.create_task(self.get())

    async def check_status(self, tasks):
        while True:
            for task in tasks:
                if task._state == "PENDING":
                    await asyncio.sleep(0.0001)
                    break
            else:
                break

    async def run_stasks(self, scope):
        tasks = [self.create_task() for _ in range(*scope)]
        await self.check_status(tasks)
        self.queue.put(self.count)

    def start(self, *args):
        # self.start_time = time.time()
        asyncio.run(self.run_stasks(*args))

    def _start(self, scope):
        for _ in range(*scope):
            asyncio.run(self.get())


class AsyncPost:

    def __init__(self, url):
        self.url = url

    async def post(self, data):
        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, data=data, headers=HEADERS, ssl=False)
            if response.status == 200:
                ret = await response.text()

    def create_task(self, data):
        return asyncio.create_task(self.post(data))

    async def check_status(self, tasks):
        while True:
            for task in tasks:
                if task._state == "PENDING":
                    await asyncio.sleep(0.0001)
                    break
            else:
                break

    async def run_tasks(self, data):
        await self.check_status(
                [self.create_task(d) for d in data])

    def start(self, *args):
        asyncio.run(self.run_tasks(*args))


def get(url, number=1):
    cpus = os.cpu_count() - 1
    if number < cpus:
        for _ in range(number):
            asyncio.run(AsyncGet(url).get())
        return
    count_200 = []
    for c in range(cpus):
        x = number * c // cpus
        y = number * (c + 1) // cpus
        print(x, y)
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=AsyncGet(url, queue)._start, args=((x, y),))
        process.daemon = False
        process.start()
        count_200.append(queue.get())
    print("返回码为200的数量: %s" % sum(count_200))
    # AsyncGet(url).start((0, number))


def post(url, data):
    cpus = os.cpu_count() - 1
    number = len(data)
    if number < cpus:
        for i in range(number):
            asyncio.run(AsyncPost(url).post(data[i]))
    for c in range(cpus):
        x = number * c // cpus
        y = number * (c + 1) // cpus
        process = multiprocessing.Process(target=AsyncPost(url).start, args=(data[x:y],))
        process.daemon = False
        process.start()
