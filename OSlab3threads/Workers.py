import threading
import time
import random
from queue import Queue

q = Queue(200)


class Producer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self._event = threading.Event()

    def run(self):
        nums = range(1, 101)
        global q
        while q.qsize() <= 100:
            if self._event.is_set():
                break
            num = random.choice(nums)
            q.put(num)
            print('Produced ', num)
            time.sleep(2 + random.random())
        while True:
            if q.qsize() <= 80:
                if self._event.is_set():
                    break
                num = random.choice(nums)
                q.put(num)
                print('Produced ', num)
                time.sleep(2 + random.random())

    def sit_down(self):
        self._event.set()


class Consumer(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self._event = threading.Event()

    def run(self):
        global q
        while True:
            if self._event.is_set() and q.empty():
                print('Job is Done')
                break
            if not q.empty():
                num = q.get()
                print('---Consumed---', num)
                time.sleep(2.5 + random.random())

    def last_day_of_work(self):
        self._event.set()
