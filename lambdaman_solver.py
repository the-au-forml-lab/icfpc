import sys
import heapq
from collections import defaultdict

def parse_grid(grid_string):
    grid = grid_string.strip().split('\n')
    height, width = len(grid), len(grid[0])
    lambdaman_pos = None
    pills = set()

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'L':
                lambdaman_pos = (x, y)
            elif cell == '.':
                pills.add((x, y))

    return grid, lambdaman_pos, pills, height, width

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def nearest_pill(pos, pills):
    return min(pills, key=lambda p: manhattan_distance(pos, p)) if pills else None

def a_star_search(grid, start, pills):
    height, width = len(grid), len(grid[0])
    goal = frozenset(pills)

    def heuristic(pos, remaining_pills):
        if not remaining_pills:
            return 0
        nearest = nearest_pill(pos, remaining_pills)
        return manhattan_distance(pos, nearest) + len(remaining_pills) - 1

    start_state = (start, goal)
    g_score = defaultdict(lambda: float('inf'))
    g_score[start_state] = 0
    f_score = defaultdict(lambda: float('inf'))
    f_score[start_state] = heuristic(start, goal)

    open_set = [(f_score[start_state], start_state)]
    came_from = {}

    while open_set:
        current_f, (current_pos, current_pills) = heapq.heappop(open_set)

        if len(current_pills) == 0:
            path = []
            while (current_pos, current_pills) in came_from:
                (prev_pos, prev_pills), move = came_from[(current_pos, current_pills)]
                path.append(move)
                current_pos, current_pills = prev_pos, prev_pills
            return ''.join(reversed(path))

        for dx, dy, move in [(0, -1, 'U'), (1, 0, 'R'), (0, 1, 'D'), (-1, 0, 'L')]:
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if 0 <= next_pos[1] < height and 0 <= next_pos[0] < width and grid[next_pos[1]][next_pos[0]] != '#':
                next_pills = current_pills - {next_pos} if next_pos in current_pills else current_pills
                next_state = (next_pos, next_pills)

                tentative_g_score = g_score[(current_pos, current_pills)] + 1

                if tentative_g_score < g_score[next_state]:
                    came_from[next_state] = ((current_pos, current_pills), move)
                    g_score[next_state] = tentative_g_score
                    f_score[next_state] = tentative_g_score + heuristic(next_pos, next_pills)
                    heapq.heappush(open_set, (f_score[next_state], next_state))

    return None

def solve_lambdaman(grid_string):
    grid, lambdaman_pos, pills, height, width = parse_grid(grid_string)
    path = a_star_search(grid, lambdaman_pos, pills)
    return path if path else "No solution found"

# Example usage
if __name__ == "__main__":
    # Read input from stdin
    grid_string = sys.stdin.read()
    solution = solve_lambdaman(grid_string)
    print(solution)
