import copy

def read_3d_program(file_path):
    with open(file_path, 'r') as file:
        # Read all lines and strip whitespace
        lines = [line.strip() for line in file.readlines()]
        
        # Convert each line into a list of tokens
        program = [line.split() for line in lines if line]  # Ignore empty lines
        
        # Replace '.' with None for empty cells
        program = [[None if cell == '.' else cell for cell in row] for row in program]
        
        # Convert numeric strings to integers
        for i in range(len(program)):
            for j in range(len(program[i])):
                if program[i][j] is not None:
                    try:
                        program[i][j] = int(program[i][j])
                    except ValueError:
                        # If it's not a number, keep it as a string
                        pass
    
    return program

class ProgramState:
    def __init__(self, initial_grid):
        self.current_grid = initial_grid
        self.history = [copy.deepcopy(initial_grid)]
        self.time = 1
        self.submitted_value = None
        self.running = True

    def apply_op(self, x, y):
        op = self.current_grid[y][x]
        if op is None:
            return

        print(f"Applying op {op} at ({x}, {y})")  # Debug print

        if op in ['<', '>', '^', 'v']:
            self.move_op(x, y, op)
        elif op in ['+', '-', '*', '/', '%']:
            self.arithmetic_op(x, y, op)
        elif op == '=':
            self.equality_op(x, y)
        elif op == '#':
            self.inequality_op(x, y)
        elif op == '@':
            self.time_warp_op(x, y)
        elif op == 'S':
            self.submit_op(x, y)

    def move_op(self, x, y, direction):
        dx, dy = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}[direction]
        tx, ty = x + dx, y + dy
        if 0 <= ty < len(self.current_grid) and 0 <= tx < len(self.current_grid[ty]) and self.current_grid[ty][tx] is None:
            self.current_grid[ty][tx], self.current_grid[y][x] = self.current_grid[y][x], None
            print(f"Moved {direction} from ({x}, {y}) to ({tx}, {ty})")  # Debug print

    def arithmetic_op(self, x, y, op):
        ops = {'+': lambda a, b: a + b,
               '-': lambda a, b: a - b,
               '*': lambda a, b: a * b,
               '/': lambda a, b: a // b,
               '%': lambda a, b: a % b}
        
        if y > 0 and x < len(self.current_grid[y-1]) - 1 and isinstance(self.current_grid[y-1][x], int) and isinstance(self.current_grid[y-1][x+1], int):
            a, b = self.current_grid[y-1][x], self.current_grid[y-1][x+1]
            result = ops[op](a, b)
            if x < len(self.current_grid[y]) - 1:
                self.current_grid[y][x+1] = result
            if y < len(self.current_grid) - 1 and x < len(self.current_grid[y+1]):
                self.current_grid[y+1][x] = result
            self.current_grid[y-1][x] = self.current_grid[y-1][x+1] = None
            print(f"Arithmetic op {op}: {a} {op} {b} = {result}")  # Debug print

    def equality_op(self, x, y):
        if y > 0 and x < len(self.current_grid[y-1]) - 1 and self.current_grid[y-1][x] == self.current_grid[y-1][x+1]:
            value = self.current_grid[y-1][x]
            self.current_grid[y-1][x] = self.current_grid[y-1][x+1] = None
            if y < len(self.current_grid) - 1 and x < len(self.current_grid[y+1]):
                self.current_grid[y+1][x] = value
            print(f"Equality op: values are equal, result {value}")  # Debug print

    def inequality_op(self, x, y):
        if y > 0 and x < len(self.current_grid[y-1]) - 1 and self.current_grid[y-1][x] != self.current_grid[y-1][x+1]:
            value = self.current_grid[y-1][x]
            self.current_grid[y-1][x] = self.current_grid[y-1][x+1] = None
            if x < len(self.current_grid[y]) - 1:
                self.current_grid[y][x+1] = value
            print(f"Inequality op: values are not equal, result {value}")  # Debug print

    def time_warp_op(self, x, y):
        if y > 0 and y < len(self.current_grid) - 1 and x > 0 and x < len(self.current_grid[y]) - 1:
            dx = self.current_grid[y][x-1]
            dy = self.current_grid[y][x+1]
            dt = self.current_grid[y+1][x]
            v = self.current_grid[y-1][x]

            if all(isinstance(val, int) for val in [dx, dy, dt, v]):
                if dt > 0 and dt < self.time:
                    target_time = self.time - dt
                    target_x = x - dx
                    target_y = y - dy

                    if 0 <= target_x < len(self.history[target_time-1]) and 0 <= target_y < len(self.history[target_time-1][target_x]):
                        # Perform the time warp
                        self.history[target_time-1][target_y][target_x] = v
                        # Truncate history and reset current state
                        self.history = self.history[:target_time]
                        self.current_grid = copy.deepcopy(self.history[-1])
                        self.time = target_time
                        print(f"Time warp: dt={dt}, new time={self.time}, value {v} at ({target_x}, {target_y})")  # Debug print

    def submit_op(self, x, y):
        if y > 0 and isinstance(self.current_grid[y-1][x], int):
            self.submitted_value = self.current_grid[y-1][x]
            self.running = False
            print(f"Submit op: submitting value {self.submitted_value}")  # Debug print
        else:
            print(f"Submit op: no valid value to submit at ({x}, {y-1})")  # Debug print

    def tick(self):
        print(f"\nTick {self.time}")  # Debug print
        for y in range(len(self.current_grid)):
            for x in range(len(self.current_grid[y])):
                self.apply_op(x, y)
        self.time += 1
        self.history.append(copy.deepcopy(self.current_grid))
        self.print_grid()  # Debug print

    def print_grid(self):
        for row in self.current_grid:
            print(' '.join(str(cell) if cell is not None else '.' for cell in row))


def run_program(initial_grid, max_ticks=1_000_000):
    state = ProgramState(initial_grid)
    while state.running and state.time <= max_ticks:
        state.tick()
    return state.submitted_value


# Example usage
file_path = '3d_input.txt'
program = read_3d_program(file_path)
res = run_program(program)

print(res)
# for row in program:
#     print(row)
