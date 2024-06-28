from collections import deque
import sys

def parse_grid(grid_string):
    grid = grid_string.strip().split('\n')
    height, width = len(grid), len(grid[0])
    lambdaman_pos = None
    pills = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'L':
                lambdaman_pos = (x, y)
            elif cell == '.':
                pills.append((x, y))

    return grid, lambdaman_pos, pills, height, width

def is_valid_move(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'

def bfs(grid, start, pills):
    height, width = len(grid), len(grid[0])
    queue = deque([(start, '')])
    visited = set([start])
    pills_set = set(pills)
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) in pills_set:
            pills_set.remove((x, y))
            if not pills_set:
                return path
        
        for dx, dy, move in [(0, -1, 'U'), (1, 0, 'R'), (0, 1, 'D'), (-1, 0, 'L')]:
            nx, ny = x + dx, y + dy
            if is_valid_move(grid, nx, ny) and (nx, ny) not in visited:
                queue.append(((nx, ny), path + move))
                visited.add((nx, ny))
    
    return None  # No solution found

def solve_lambdaman(grid_string):
    grid, lambdaman_pos, pills, height, width = parse_grid(grid_string)
    path = bfs(grid, lambdaman_pos, pills)
    return path if path else "No solution found"

# Example usage
if __name__ == "__main__":
    # Read input from stdin
    grid_string = sys.stdin.read()
    solution = solve_lambdaman(grid_string)
    print(solution)