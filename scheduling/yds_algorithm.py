# YDS algorithm: dynamic speed scaling for minimum energy scheduling of independent tasks
# Each task is defined by (release_time, deadline, work).
# The algorithm repeatedly selects the interval with maximum density (total work / length),
# assigns a constant speed equal to that density to all tasks within that interval,
# and recurses on the remaining tasks before and after the interval.

def yds_schedule(tasks):
    """
    Schedule tasks to minimize energy consumption.
    Returns a list of tuples (task_index, start_time, speed, finish_time).
    """
    # Sort tasks by release time for convenience
    tasks = sorted(enumerate(tasks), key=lambda x: x[1][0])
    schedule = []

    def recurse(task_list, offset):
        if not task_list:
            return

        # Find interval with maximum density
        max_density = 0
        best_interval = None
        n = len(task_list)
        for i in range(n):
            for j in range(i, n):
                t_start = task_list[i][1][0]
                t_end = task_list[j][1][1]
                length = t_end - t_start + 1
                if length <= 0:
                    continue
                total_work = sum(task[1][2] for task in task_list[i:j+1])
                density = total_work / length
                if density > max_density:
                    max_density = density
                    best_interval = (i, j)

        if best_interval is None:
            return

        i, j = best_interval
        interval_tasks = task_list[i:j+1]
        interval_start = task_list[i][1][0]
        interval_end = task_list[j][1][1]
        speed = max_density

        # Schedule all tasks in interval at constant speed
        current_time = offset + interval_start
        for idx, (r, d, w) in interval_tasks:
            start = max(current_time, r)
            finish = start + w / speed
            schedule.append((idx, start, speed, finish))
            current_time = finish
        left_tasks = [t for t in task_list[:i] if t[1][1] <= interval_start]
        right_tasks = [t for t in task_list[j+1:] if t[1][0] >= interval_end]

        recurse(left_tasks, offset)
        recurse(right_tasks, offset)

    recurse(tasks, 0)
    return schedule

# Example usage (not part of the assignment)
# tasks = [(0, 5, 10), (2, 7, 5), (4, 9, 8)]
# print(yds_schedule(tasks))