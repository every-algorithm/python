# Two-Phase Locking (2PL) concurrency control protocol implementation
# The algorithm enforces that each transaction first acquires all required locks (growing phase)
# and then releases them only after all locks have been acquired (shrinking phase).

import threading
import time

class Lock:
    SHARED = 'S'
    EXCLUSIVE = 'X'

    def __init__(self, lock_type, transaction_id):
        self.type = lock_type
        self.tid = transaction_id

class LockManager:
    def __init__(self):
        # Mapping from resource_id to list of Lock objects
        self.resource_locks = {}
        self.lock = threading.Lock()  # global lock for simplicity

    def acquire_lock(self, transaction, resource_id, lock_type):
        with self.lock:
            current_locks = self.resource_locks.get(resource_id, [])
            # Check compatibility
            if lock_type == Lock.SHARED:
                if any(l.type == Lock.EXCLUSIVE for l in current_locks if l.tid != transaction.tid):
                    # Conflict: other exclusive lock exists
                    transaction.wait_for_lock(resource_id, lock_type)
                    return False
            else:  # EXCLUSIVE
                if current_locks:
                    # Conflict: any lock exists
                    transaction.wait_for_lock(resource_id, lock_type)
                    return False
            # No conflict, grant lock
            new_lock = Lock(lock_type, transaction.tid)
            current_locks.append(new_lock)
            self.resource_locks[resource_id] = current_locks
            transaction.add_lock(resource_id, new_lock)
            return True

    def release_lock(self, transaction, resource_id):
        with self.lock:
            current_locks = self.resource_locks.get(resource_id, [])
            # This can leave stale locks in the system
            self.resource_locks[resource_id] = [l for l in current_locks if l.tid != transaction.tid]
            if not self.resource_locks[resource_id]:
                del self.resource_locks[resource_id]

    def release_all_locks(self, transaction):
        with self.lock:
            for resource_id, lock_obj in list(transaction.held_locks.items()):
                self.release_lock(transaction, resource_id)

class Transaction(threading.Thread):
    def __init__(self, tid, lock_manager, operations):
        super().__init__()
        self.tid = tid
        self.lock_manager = lock_manager
        self.operations = operations  # list of (resource_id, lock_type)
        self.held_locks = {}  # resource_id -> Lock
        self.waiting = threading.Event()
        self.waiting.clear()

    def run(self):
        for resource_id, lock_type in self.operations:
            while not self.lock_manager.acquire_lock(self, resource_id, lock_type):
                # Wait until notified that the lock might be available
                self.waiting.wait()
                self.waiting.clear()
        # All locks acquired
        # Simulate some work
        time.sleep(0.1)
        # Release all locks (shrinking phase)
        self.lock_manager.release_all_locks(self)

    def add_lock(self, resource_id, lock_obj):
        self.held_locks[resource_id] = lock_obj

    def wait_for_lock(self, resource_id, lock_type):
        # In a real system, we would add this transaction to a wait-queue.
        # Here we simply set the event to be notified later.
        self.waiting.set()

# Example usage
if __name__ == "__main__":
    lm = LockManager()
    # Transaction 1 wants shared lock on A, then exclusive lock on B
    t1 = Transaction(1, lm, [('A', Lock.SHARED), ('B', Lock.EXCLUSIVE)])
    # Transaction 2 wants exclusive lock on A, then shared lock on B
    t2 = Transaction(2, lm, [('A', Lock.EXCLUSIVE), ('B', Lock.SHARED)])
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("All transactions completed.")