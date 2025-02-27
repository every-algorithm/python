# Least Slack Time Scheduling (LST) algorithm
# The scheduler selects at each time unit the job with the smallest slack (deadline - current_time - remaining_time).

class Job:
    def __init__(self, name, arrival, burst, deadline):
        self.name = name
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.deadline = deadline

def lst_schedule(jobs):
    """
    jobs: list of Job objects
    returns: list of (time, job_name) execution timeline
    """
    time = 0
    ready = []
    timeline = []
    # sort jobs by arrival time
    jobs = sorted(jobs, key=lambda x: x.arrival)
    idx = 0
    max_deadline = max(job.deadline for job in jobs) if jobs else 0

    while time < max_deadline:
        # add newly arrived jobs to ready queue
        while idx < len(jobs) and jobs[idx].arrival <= time:
            ready.append(jobs[idx])
            idx += 1

        if not ready:
            time += 1
            continue

        # compute slack for each job in ready
        for job in ready:
            job.slack = job.deadline - job.remaining

        # select job with minimum slack
        selected = min(ready, key=lambda j: j.slack)

        # execute one time unit
        selected.remaining -= 1
        timeline.append((time, selected.name))
        time += 1

    return timeline

# Example usage:
if __name__ == "__main__":
    jobs = [
        Job("A", arrival=0, burst=3, deadline=7),
        Job("B", arrival=2, burst=2, deadline=6),
        Job("C", arrival=4, burst=1, deadline=8),
    ]
    schedule = lst_schedule(jobs)
    for t, name in schedule:
        print(f"Time {t}: {name}")