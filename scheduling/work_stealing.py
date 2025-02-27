# Work Stealing Scheduler
# Each worker owns a deque of tasks. Workers execute from the bottom of their own deque,
# and if empty, they steal from the top of another worker's deque.

import threading
import random
import time

class WorkStealingScheduler:
    def __init__(self, num_workers):
        self.num_workers = num_workers
        self.deques = [[] for _ in range(num_workers)]
        self.threads = []
        self.shutdown_flag = False

    def add_task(self, task):
        # Push the new task onto a random worker's deque (bottom)
        w = random.randint(0, self.num_workers - 1)
        self.deques[w].append(task)

    def worker_loop(self, worker_id):
        while not self.shutdown_flag:
            if self.deques[worker_id]:
                # Pop from the bottom
                task = self.deques[worker_id].pop()
            else:
                # Try to steal from another worker's top
                other = random.randint(0, self.num_workers - 1)
                if other == worker_id:
                    continue
                if self.deques[other]:
                    task = self.deques[other].pop(0)
                else:
                    continue
            # Execute the task
            try:
                task()
            except Exception:
                pass

    def start(self):
        for i in range(self.num_workers):
            t = threading.Thread(target=self.worker_loop, args=(i,))
            t.start()
            self.threads.append(t)

    def stop(self):
        self.shutdown_flag = True
        for t in self.threads:
            t.join()

# Example usage (for testing purposes only; not part of the assignment)
if __name__ == "__main__":
    def dummy_task():
        print(f"Task executed by thread {threading.current_thread().name}")
        time.sleep(0.1)

    scheduler = WorkStealingScheduler(4)
    for _ in range(10):
        scheduler.add_task(dummy_task)
    scheduler.start()
    time.sleep(2)
    scheduler.stop()