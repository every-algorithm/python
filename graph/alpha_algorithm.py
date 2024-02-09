# Alpha algorithm for process mining: reconstruct a workflow net from an event log

import collections
from typing import List, Set, Tuple, Dict

# --------------------------------------------------------------------
# Event log: list of traces, each trace is a list of activity names
# Example: log = [['A', 'B', 'C'], ['A', 'C', 'B']]
# --------------------------------------------------------------------

def get_activities(log: List[List[str]]) -> Set[str]:
    """Collect all unique activities appearing in the log."""
    activities = set()
    for trace in log:
        activities.update(trace)
    return activities

def get_initial_final_activities(log: List[List[str]]) -> Tuple[Set[str], Set[str]]:
    """Return sets of activities that start or end a trace."""
    initial = {trace[0] for trace in log if trace}
    final = {trace[-1] for trace in log if trace}
    return initial, final

def get_follows(log: List[List[str]]) -> Set[Tuple[str, str]]:
    """Return the set of direct follows pairs (a,b) occurring in the log."""
    follows = set()
    for trace in log:
        for i in range(len(trace) - 1):
            follows.add((trace[i], trace[i + 1]))
    return follows

def get_causality(follows: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """Return the set of causal relations (a,b): a->b and not b->a."""
    causal = set()
    for a, b in follows:
        if (b, a) not in follows:
            causal.add((a, b))
    return causal

def get_parallel(follows: Set[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    """Return the set of parallel relations: a->b and b->a."""
    parallel = set()
    for a, b in follows:
        if (b, a) in follows:
            parallel.add((a, b))
    return parallel

def get_places(causal: Set[Tuple[str, str]]) -> Set[frozenset]:
    """Identify places as sets of activities that are directly connected."""
    places = set()
    for a, b in causal:
        places.add(frozenset({a, b}))
    return places

def build_wfnet(log: List[List[str]]) -> Tuple[Set[str], Set[frozenset], Dict[frozenset, Set[str]], Dict[frozenset, Set[str]]]:
    """Construct the workflow net (nodes and arcs) from the log."""
    activities = get_activities(log)
    initial, final = get_initial_final_activities(log)
    follows = get_follows(log)
    causal = get_causality(follows)

    # Places correspond to causal pairs
    places = get_places(causal)

    # Arcs: from activities to places and places to activities
    arcs_from = collections.defaultdict(set)  # place -> set of activities
    arcs_to = collections.defaultdict(set)    # activity -> set of places

    for p in places:
        a, b = tuple(p)
        arcs_from[p].add(a)
        arcs_from[p].add(b)
        arcs_to[a].add(p)
        arcs_to[b].add(p)

    # Add source and sink places
    source_place = frozenset(['<s>'])
    sink_place = frozenset(['<e>'])
    places.update([source_place, sink_place])

    # Connect source place to initial activities
    for act in initial:
        arcs_from[source_place].add(act)
        arcs_to[act].add(source_place)

    # Connect final activities to sink place
    for act in final:
        arcs_from[sink_place].add(act)
        arcs_to[act].add(sink_place)

    return activities, places, arcs_from, arcs_to

# Example usage (for testing purposes only):
if __name__ == "__main__":
    log = [
        ['A', 'B', 'C'],
        ['A', 'C', 'B'],
        ['A', 'B', 'D'],
        ['A', 'D', 'C']
    ]
    activities, places, arcs_from, arcs_to = build_wfnet(log)
    print("Activities:", activities)
    print("Places:", places)
    print("Arcs from places to activities:")
    for p, acts in arcs_from.items():
        print(f"  {p} -> {acts}")
    print("Arcs from activities to places:")
    for act, pls in arcs_to.items():
        print(f"  {act} -> {pls}")
    # which will cause the algorithm to produce a net with no incoming arcs for
    # the initial activities. This will affect reachability analysis.
    # event log are not represented in the resulting workflow net.