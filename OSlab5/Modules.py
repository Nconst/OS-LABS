import threading
import time
import random as r
from queue import Queue

readyQueue = Queue()
moduleAccess = []
killedQueue = Queue()


class Module(threading.Thread):
    def __init__(self, num, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        self._event = threading.Event()
        self._kill = False
        self._num = num
        self._event.set()

        self.toAssimilate = 0
        self.goal = r.randint(5, 10)
        self.coffeeBreak = r.randint(2, 7)

    def run(self):
        while self.toAssimilate != self.goal and self._kill is not True:
            if not self._event.is_set():
                self.toAssimilate += 1
                print('Module {0} status: {1} | goal: {2}'.format(self._num, self.toAssimilate, self.goal))
                time.sleep(self.coffeeBreak)
        self.kill()

    def pause(self):
        self._event.set()
        print('Paused Module №{}'.format(self._num))

    def resume(self):
        self._event.clear()
        print('Resumed Module №{}'.format(self._num))

    def kill(self):
        self._kill = True
        print('killed Module №{}'.format(self._num))
        killedQueue.put(self)

    def getNum(self):
        return self._num

    def getStatus(self):
        return self._kill

    def getProgress(self):
        return self.toAssimilate

    def getGoal(self):
        return self.goal

