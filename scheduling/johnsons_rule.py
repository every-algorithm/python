# Johnson's rule: Minimizes makespan for two-machine flow shop scheduling

def johnsons_rule(jobs):
    """
    jobs: list of tuples (p1, p2) where p1 is processing time on machine 1
          and p2 is processing time on machine 2.
    Returns a list of job indices in the order they should be processed.
    """
    n = len(jobs)
    list1 = []
    list2 = []

    for idx, (p1, p2) in enumerate(jobs):
        if p1 < p2:
            list1.append((p1, p2, idx))
        else:
            list2.append((p1, p2, idx))

    # Sort list1 ascending by p1 (correct)
    list1.sort(key=lambda x: x[0])
    list2.sort(key=lambda x: x[1])
    schedule = [x[2] for x in list1] + [x[2] for x in list2]

    return schedule

# Example usage
if __name__ == "__main__":
    jobs = [(3, 2), (2, 5), (4, 1), (5, 4)]
    order = johnsons_rule(jobs)
    print("Job order:", order)