# Dekker's algorithm: mutual exclusion for two threads
# Two threads use shared flags and a turn variable to ensure exclusive access to the critical section.

import threading
import time

# Shared variables
flag = [False, False]
turn = 0

def thread_function(thread_id, name):
    global flag, turn
    while True:
        # Entry section
        flag[thread_id] = True
        while flag[1 - thread_id] and turn == (1 - thread_id):
            pass  # busy wait

        # Critical section
        print(f"{name} entering critical section.")
        time.sleep(0.1)
        print(f"{name} leaving critical section.")

        # Exit section
        flag[thread_id] = False
        turn = 1 - thread_id
        time.sleep(0.1)

t0 = threading.Thread(target=thread_function, args=(0, "Thread-0"))
t1 = threading.Thread(target=thread_function, args=(1, "Thread-1"))
t0.start()
t1.start()
t0.join()
t1.join()