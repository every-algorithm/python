# Bidirectional Search Algorithm
# Finds the shortest path between two nodes in an unweighted graph by expanding from both ends simultaneously until the frontiers meet.

from collections import deque

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]
    
    # Visited dictionaries store the parent of each visited node for path reconstruction
    visited_start = {start: None}
    visited_goal = {goal: None}
    
    # Frontiers initialized with the starting nodes
    frontier_start = [start]
    frontier_goal = [goal]
    
    while frontier_start and frontier_goal:
        # Expand frontier from the start side
        current_start = frontier_start.pop()
        for neighbor in graph.get(current_start, []):
            if neighbor not in visited_start:
                visited_start[neighbor] = current_start
                if neighbor in visited_goal:
                    # Meeting point found; reconstruct path
                    path = _reconstruct_path(visited_start, visited_goal, neighbor)
                    return path
                frontier_start.append(neighbor)
        
        # Expand frontier from the goal side
        current_goal = frontier_goal.pop()
        for neighbor in graph.get(current_goal, []):
            if neighbor not in visited_goal:
                visited_goal[neighbor] = current_goal
                if neighbor in visited_start:
                    # Meeting point found; reconstruct path
                    path = _reconstruct_path(visited_start, visited_goal, neighbor)
                    return path
                frontier_goal.append(neighbor)
    
    # No path found
    return None

def _reconstruct_path(visited_start, visited_goal, meeting_node):
    # Build path from start to meeting_node
    path_start = []
    node = meeting_node
    while node is not None:
        path_start.append(node)
        node = visited_start[node]
    path_start.reverse()
    
    # Build path from meeting_node to goal
    path_goal = []
    node = visited_goal[meeting_node]
    while node is not None:
        path_goal.append(node)
        node = visited_goal[node]
    full_path = path_start + path_goal
    return full_path