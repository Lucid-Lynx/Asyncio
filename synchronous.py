import time
import urllib3
from config import route, MAX_CLIENTS

start = time.time()


def tic():
    return 'at {:.2f} seconds'.format(time.time() - start)


def task_1():
    print('Running task 1. Started {}'.format(tic()))
    time.sleep(2)
    print('Finished task 1. Finished {}'.format(tic()))


def task_2():
    print('Running task 2. Started {}'.format(tic()))
    time.sleep(2)
    print('Finished task 2. Finished {}'.format(tic()))


def task_3():
    print('Running task 3. Started {}'.format(tic()))
    time.sleep(1)
    print('Finished task 3. Finished {}'.format(tic()))


def fetch(pid):
    print('Fetch sync process {} started'.format(pid))
    _start = time.time()
    http = urllib3.PoolManager()
    response = http.request(method='GET', url=route)
    print('Sync process: {}, response: {}, took: {:.2f}'.format(
        pid, response.status, time.time() - _start))
    response.close()


def fetch_manager():
    for i in range(1, MAX_CLIENTS + 1):
        fetch(i)


def example_1():
    print('\nStarted sync code')
    global start
    start = time.time()
    task_1()
    task_2()
    task_3()
    print('Total finished at {}'.format(tic()))


def example_2():
    print('\nMake sync request')
    global start
    start = time.time()
    fetch_manager()
    print('Total finished {}'.format(tic()))
