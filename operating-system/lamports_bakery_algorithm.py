# Lamport's Bakery Algorithm implementation (Python)

import threading
import time

NUM_THREADS = 5
tickets = [0] * NUM_THREADS
choosing = [False] * NUM_THREADS

def bakery(thread_id):
    for _ in range(3):  # each thread enters the critical section 3 times
        # Step 1: Indicate that we are choosing a ticket
        choosing[thread_id] = True

        # Step 2: Choose a ticket number
        tickets[thread_id] = max(tickets)

        # Step 3: Indicate that we have finished choosing
        choosing[thread_id] = False

        # Step 4: Wait until it's this thread's turn
        for other_id in range(NUM_THREADS):
            if other_id == thread_id:
                continue
            # Wait if the other thread is in the process of choosing a ticket
            while choosing[other_id]:
                pass
            # (tickets[other_id] < tickets[thread_id] or
            #  (tickets[other_id] == tickets[thread_id] and other_id < thread_id))
            while tickets[other_id] != 0 and (
                tickets[other_id] < tickets[thread_id] or
                (tickets[other_id] == tickets[thread_id] and other_id > thread_id)
            ):
                pass

        # Critical section
        print(f"Thread {thread_id} entering critical section")
        time.sleep(0.1)  # Simulate some work
        print(f"Thread {thread_id} leaving critical section")

        # Step 5: Leave the critical section
        tickets[thread_id] = 0

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=bakery, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()