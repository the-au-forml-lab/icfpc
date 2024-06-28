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
    best_solution = float('inf')
    max_path_length = 1_000_000

    def heuristic(pos, remaining_pills):
        if not remaining_pills:
            return 0
        # Manhattan distance to nearest pill + number of remaining pills
        nearest = min(manhattan_distance(pos, pill) for pill in remaining_pills)
        return nearest + len(remaining_pills) - 1

    def is_valid_move(x, y):
        return 0 <= y < height and 0 <= x < width and grid[y][x] != '#'

    start_state = (start, goal)
    g_score = {start_state: 0}
    f_score = {start_state: heuristic(start, goal)}

    open_set = [(f_score[start_state], start_state)]
    came_from = {}

    while open_set:
        current_f, (current_pos, current_pills) = heapq.heappop(open_set)
        current_g = g_score[(current_pos, current_pills)]

        # Early termination if path is too long
        if current_g >= max_path_length:
            continue

        # Early termination if current path is already longer than best solution
        if current_g >= best_solution:
            continue

        if len(current_pills) == 0:
            # Found a complete solution
            best_solution = min(best_solution, current_g)
            path = []
            state = (current_pos, current_pills)
            while state in came_from:
                prev_state, move = came_from[state]
                path.append(move)
                state = prev_state
            return ''.join(reversed(path))

        for dx, dy, move in [(0, -1, 'U'), (1, 0, 'R'), (0, 1, 'D'), (-1, 0, 'L')]:
            next_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if is_valid_move(*next_pos):
                next_pills = current_pills - {next_pos} if next_pos in current_pills else current_pills
                next_state = (next_pos, next_pills)

                tentative_g_score = current_g + 1

                # Dominance pruning
                if next_state in g_score and tentative_g_score >= g_score[next_state]:
                    continue

                # Lower bound estimation pruning
                lower_bound = tentative_g_score + heuristic(next_pos, next_pills)
                if lower_bound >= best_solution:
                    continue

                came_from[next_state] = ((current_pos, current_pills), move)
                g_score[next_state] = tentative_g_score
                f_score[next_state] = lower_bound
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

    # Debug: Print the input
    print("Input grid:")
    print(grid_string)

    solution = solve_lambdaman(grid_string)
    print("Solution:", solution)
