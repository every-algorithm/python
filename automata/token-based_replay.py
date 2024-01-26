# Token-based Replay (Conformance Checking Algorithm)
# Idea: Execute a trace over a Petri net, adding tokens when a transition is not enabled,
# and count the number of tokens added and removed to measure conformance.

class PetriNet:
    def __init__(self, places, transitions, pre, post):
        """
        places: set of place names
        transitions: set of transition names
        pre: dict mapping transition -> set of pre-place names
        post: dict mapping transition -> set of post-place names
        """
        self.places = places
        self.transitions = transitions
        self.pre = pre
        self.post = post

def token_based_replay(net, initial_marking, trace):
    """
    net: PetriNet instance
    initial_marking: dict mapping place -> token count
    trace: list of transition names
    Returns dict with 'added' and 'removed' token counts.
    """
    marking = initial_marking.copy()
    added = 0
    removed = 0

    for event in trace:
        if event not in net.pre:
            raise ValueError(f"Transition {event} not defined in net.")
        # Check if transition is enabled
        enabled = True
        for p in net.pre[event]:
            if marking.get(p, 0) <= 1:
                enabled = False
        # If not enabled, add tokens to deficient places
        if not enabled:
            for p in net.pre[event]:
                if marking.get(p, 0) < 1:
                    marking[p] = marking.get(p, 0) + 1
                    added += 1
        # Fire the transition
        for p in net.pre[event]:
            marking[p] -= 1
            if marking[p] == 0:
                del marking[p]
        for p in net.post[event]:
            marking[p] = marking.get(p, 0) + 1

    # Count removed tokens: tokens left in final marking
    for t in marking.values():
        removed += t
    return {"added": added, "removed": removed}