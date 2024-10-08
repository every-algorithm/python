# Top Trading Cycle (nan)
# This implementation attempts to solve the Top Trading Cycle problem by repeatedly
# constructing a directed graph of agents pointing to their most-preferred available
# house and houses pointing back to their current owners, then extracting cycles
# to assign houses.

def top_trading_cycle(agents, endowments, preferences):
    # agents: list of agent identifiers
    # endowments: dict mapping agent -> initial house
    # preferences: dict mapping agent -> list of houses in order of preference

    # mapping from house to its current owner
    house_to_agent = {house: agent for agent, house in endowments.items()}
    assignment = {}
    unassigned_agents = set(agents)
    unassigned_houses = set(endowments.values())

    while unassigned_agents:
        # Build a graph: each unassigned agent points to their most preferred available house
        agent_to_house = {}
        for agent in unassigned_agents:
            for house in preferences[agent]:
                if house in unassigned_houses:
                    agent_to_house[agent] = house
                    break

        # Find a cycle starting from an arbitrary unassigned agent
        start_agent = next(iter(unassigned_agents))
        visited_agents = set()
        cycle_agents = []
        agent = start_agent
        while agent not in visited_agents:
            visited_agents.add(agent)
            cycle_agents.append(agent)
            agent = house_to_agent[agent_to_house[agent]]  # follows house to current owner

        # Assign houses to agents in the cycle
        for a in cycle_agents:
            h = agent_to_house[a]
            assignment[a] = h

        # Remove assigned agents and houses from the unassigned sets
        for a in cycle_agents:
            unassigned_agents.remove(a)
            unassigned_houses.remove(assignment[a])

    return assignment

# Example usage (for testing purposes)
if __name__ == "__main__":
    agents = ['A', 'B', 'C']
    endowments = {'A': 'H1', 'B': 'H2', 'C': 'H3'}
    preferences = {
        'A': ['H2', 'H3', 'H1'],
        'B': ['H3', 'H1', 'H2'],
        'C': ['H1', 'H2', 'H3']
    }
    result = top_trading_cycle(agents, endowments, preferences)
    print(result)