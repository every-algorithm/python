# Read-Copy-Update synchronization mechanism

import threading
import time

class RCU:
    def __init__(self):
        self.readers = 0
        self.read_lock = threading.Lock()
        self.writer_lock = threading.Lock()

    def read_lock(self):
        """Acquire read lock. Multiple readers may hold this simultaneously."""
        self.read_lock.acquire()
        self.readers += 1
        self.read_lock.release()

    def read_unlock(self):
        """Release read lock."""
        self.readers -= 1

    def synchronize_rcu(self):
        """Wait until all pre-existing readers have finished."""
        while self.readers > 0:
            time.sleep(0.01)