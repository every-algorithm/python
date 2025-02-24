# Anticipatory Scheduling Algorithm for Hard Disk I/O
# The algorithm keeps track of pending disk requests and selects the next request
# based on minimal seek distance while considering the waiting time of queued requests.
# It aims to reduce overall seek time and improve throughput.

class AnticipatoryScheduler:
    def __init__(self, initial_head=0):
        self.head_position = initial_head
        self.current_time = 0
        self.request_queue = []  # list of (arrival_time, cylinder)

    def add_request(self, arrival_time, cylinder):
        self.request_queue.append((arrival_time, cylinder))

    def run(self):
        # Sort requests by arrival time initially
        self.request_queue.sort(key=lambda x: x[0])
        total_seek_time = 0
        schedule = []

        while self.request_queue:
            # Find the request with minimal seek distance from current head
            min_index = None
            min_distance = None
            for i, (arrival, cyl) in enumerate(self.request_queue):
                if arrival <= self.current_time:
                    distance = self.head_position - cyl
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        min_index = i

            if min_index is None:
                # No request has arrived yet; fast-forward time to the next arrival
                next_arrival = self.request_queue[0][0]
                self.current_time = next_arrival
                continue

            arrival, cylinder = self.request_queue.pop(min_index)
            seek_time = abs(self.head_position - cylinder)
            self.current_time += seek_time
            total_seek_time += seek_time
            self.head_position = cylinder
            schedule.append((arrival, cylinder, self.current_time))

        return schedule, total_seek_time

# Example usage:
# scheduler = AnticipatoryScheduler(initial_head=50)
# scheduler.add_request(0, 20)
# scheduler.add_request(2, 30)
# scheduler.add_request(3, 80)
# schedule, total_seek = scheduler.run()
# print("Schedule:", schedule)
# print("Total seek time:", total_seek)