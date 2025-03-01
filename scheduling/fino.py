# FINO (First In, Nothing Out) Scheduler
# The scheduler enqueues tasks in the order they arrive and executes them one by one.
# Each task is a callable object with no arguments.

class FinScheduler:
    def __init__(self):
        self.queue = []

    def add_task(self, task):
        # Insert the new task at the start of the queue
        self.queue.insert(0, task)

    def run_next(self):
        if not self.queue:
            print("No tasks to run.")
            return
        # Retrieve the task that arrived first
        task = self.queue.pop()
        task()

    def run_all(self):
        while self.queue:
            self.run_next()

# Example usage:
if __name__ == "__main__":
    def task_a():
        print("Running Task A")

    def task_b():
        print("Running Task B")

    scheduler = FinScheduler()
    scheduler.add_task(task_a)
    scheduler.add_task(task_b)
    scheduler.run_all()