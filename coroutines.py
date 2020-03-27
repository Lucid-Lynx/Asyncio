import asyncio
import aiohttp
import time
import random
from concurrent.futures import FIRST_COMPLETED
from config import route, MAX_CLIENTS

start = time.time()


def tic():
    return 'at {:.2f} seconds'.format(time.time() - start)


async def coroutine_1():
    print('Running coroutine 1. Started {}'.format(tic()))
    await asyncio.sleep(2)
    print('Finished coroutine 1. Finished {}'.format(tic()))


async def coroutine_2():
    print('Running coroutine 2. Started {}'.format(tic()))
    await asyncio.sleep(2)
    print('Finished coroutine 2. Finished {}'.format(tic()))


async def coroutine_3():
    print('Running coroutine 3. Started {}'.format(tic()))
    await asyncio.sleep(1)
    print('Finished coroutine 3. Finished {}'.format(tic()))


async def fetch(pid):
    print('Fetch async process {} started'.format(pid))
    _start = time.time()
    session = aiohttp.ClientSession()

    try:
        response = await session.get(url=route)
        print('Async process: {}, response: {}, took: {:.2f}'.format(
            pid, response.status, time.time() - _start))
        response.close()

    finally:
        await session.close()


async def fetch_silent(pid):
    print('Fetch async process {} started'.format(pid))
    _start = time.time()
    session = aiohttp.ClientSession()

    try:
        response = await session.get(url=route)
        status = response.status
        response.close()
        time.sleep(random.randint(1, 10))
        return ('Async process: {}, response: {}, took: {:.2f}'.format(
            pid, status, time.time() - _start))

    finally:
        await session.close()


async def fetch_manager():
    tasks = [asyncio.create_task(fetch(i)) for i in range(1, MAX_CLIENTS + 1)]
    await asyncio.wait(tasks)


async def fetch_manager_silent():
    tasks = [asyncio.create_task(fetch_silent(i)) for i in range(1, MAX_CLIENTS + 1)]

    for i, task in enumerate(asyncio.as_completed(tasks)):
        result = await task
        print(result)


async def fetch_manager_one():
    tasks = [asyncio.create_task(fetch_silent(i)) for i in range(1, MAX_CLIENTS + 1)]
    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
    print(done.pop().result())

    for task in pending:
        task.cancel()


def example_1():
    print('\nStarted async code')
    global start
    start = time.time()
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(coroutine_1()),
        ioloop.create_task(coroutine_2()),
        ioloop.create_task(coroutine_3()),
    ]
    wait_tasks = asyncio.wait(tasks)
    ioloop.run_until_complete(wait_tasks)
    print('Total finished {}'.format(tic()))


def example_2():
    print('\nMake async request')
    global start
    start = time.time()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(fetch_manager())
    print('Total finished {}'.format(tic()))


def example_3():
    print('\nMake async silent request')
    global start
    start = time.time()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(fetch_manager_silent())
    print('Total finished {}'.format(tic()))


def example_4():
    print('\nMake async one request')
    global start
    start = time.time()
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(fetch_manager_one())
    print('Total finished {}'.format(tic()))


def close_ioloop():
    ioloop = asyncio.get_event_loop()
    ioloop.close()
