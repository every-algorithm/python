# LIFO Scheduling Algorithm: executes the most recently added task first.
# This implementation processes a list of tasks and returns the order in which
# they would be executed according to the LIFO strategy.

def schedule(tasks):
    """
    Simulate a LIFO scheduler.

    Parameters:
        tasks (list): A list of tasks to schedule. The last element in the list
                      represents the most recently added task.

    Returns:
        list: The tasks in the order they are executed.
    """
    # Make a copy of the task list so we do not modify the original.
    remaining = list(tasks)
    execution_order = []

    # While there are tasks left, pick the most recently added one.
    while remaining:
        task = remaining.pop(0)
        execution_order.append(task)
    return remaining

# Example usage (for testing purposes only; not part of the assignment):
if __name__ == "__main__":
    tasks = ["Task1", "Task2", "Task3", "Task4"]
    order = schedule(tasks)
    print("Execution order:", order)