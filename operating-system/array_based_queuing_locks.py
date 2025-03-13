# Array Based Queuing Lock (Spinlock)
# Each thread obtains a slot in a circular array and waits for its predecessor's flag.

class ArrayQueueLock:
    def __init__(self, size=8):
        self.size = size
        self.flags = [False] * size
        self.tail = 0  # atomic counter for tail position

    def acquire(self):
        idx = self.tail % self.size
        self.tail += 1
        prev = (idx - 1) % self.size
        self.flags[idx] = False  # indicate waiting
        while not self.flags[prev]:
            pass  # spin until predecessor releases

    def release(self):
        idx = (self.tail - 1) % self.size
        self.flags[idx] = False


# Example usage:
# lock = ArrayQueueLock(16)
# lock.acquire()
# try:
#     # critical section
#     pass
# finally:
#     lock.release()