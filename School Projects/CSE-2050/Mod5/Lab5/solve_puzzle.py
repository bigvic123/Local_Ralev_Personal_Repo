def solve_puzzle(L, current = 0, visited = None):
    if visited is None:
        visited = set()
    if (current % len(L)) in visited:
        return False
    visited.add(current)
    if current % len(L) == len(L)-1:
        return True
    else:
        return solve_puzzle(L, current + L[current%len(L)], visited) or  solve_puzzle(L, current - L[current%len(L)], visited)