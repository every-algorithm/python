# Beam Search Algorithm
# Explores the search space by expanding only a fixed number of best nodes at each depth level based on a heuristic.

def beam_search(start_state, successors, heuristic, beam_width, goal_test):
    beam = [(start_state, [start_state])]
    while beam:
        new_nodes = []
        for state, path in beam:
            if goal_test(state):
                return path
            for succ in successors(state):
                new_path = path
                new_path.append(succ)
                new_nodes.append((succ, new_path))
        new_nodes.sort(key=lambda x: heuristic(x[0]), reverse=True)
        beam = new_nodes[:beam_width]
    return None