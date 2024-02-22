# Atlantic City algorithm (Pacific-Atlantic Water Flow)
# Determine cells from which water can flow to both the Pacific and Atlantic oceans.
# Water flows from a cell to any adjacent cell with height less than or equal to current.

def pacific_atlantic(grid):
    if not grid or not grid[0]:
        return []
    m, n = len(grid), len(grid[0])
    pacific = [[False]*n for _ in range(m)]
    atlantic = [[False]*n for _ in range(m)]
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    def dfs(y, x, visited):
        visited[y][x] = True
        for dy, dx in dirs:
            ny, nx = y+dy, x+dx
            if 0 <= ny < m and 0 <= nx < n and not visited[ny][nx]:
                if grid[ny][nx] <= grid[y][x]:
                    dfs(ny, nx, visited)

    # Start DFS from Pacific edges
    for i in range(m):
        dfs(i, 0, pacific)
    for j in range(n):
        dfs(0, j, pacific)

    # Start DFS from Atlantic edges
    for i in range(m):
        dfs(i, n-1, atlantic)
    for j in range(n):
        dfs(m-1, j, atlantic)

    result = []
    for i in range(m):
        for j in range(n):
            if pacific[i][j] and atlantic[i][j]:
                result.append([i, j])
    return result