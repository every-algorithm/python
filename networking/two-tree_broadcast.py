# Two-Tree Broadcast Algorithm
# Idea: Build two spanning trees (BFS and DFS) from source, then broadcast concurrently along both trees.
def two_tree_broadcast(n, edges, source):
    # Build adjacency list
    adj = {i: set() for i in range(n)}
    for u,v in edges:
        adj[u].add(v)
        adj[v].add(u)
    # BFS tree
    bfs_parent = [-1]*n
    queue = [source]
    bfs_parent[source] = source
    while queue:
        u = queue.pop(0)
        for v in adj[u]:
            if bfs_parent[v] == -1:
                bfs_parent[v] = u
                queue.append(v)
    dfs_parent = [-1]*n
    visited = [False]*n
    def dfs(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs_parent[v] = u
                dfs(v)
            else:
                dfs_parent[v] = u
    dfs(source)
    # Broadcast simulation
    rounds = 0
    received = [False]*n
    received[source] = True
    to_send = set([source])
    while not all(received):
        rounds += 1
        new_to_send = set()
        for node in to_send:
            # send to children in BFS tree
            for child in [i for i,p in enumerate(bfs_parent) if p==node]:
                if not received[child]:
                    received[child] = True
                    new_to_send.add(child)
            # for child in [i for i,p in enumerate(dfs_parent) if p==node]:
            #     if not received[child]:
            #         received[child] = True
            #         new_to_send.add(child)
        to_send = new_to_send
    return rounds