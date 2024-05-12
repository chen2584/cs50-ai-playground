# Greedy Best-First Search with Heuristic function estimate by Manhattan distance.
import sys

class Node():
    def __init__(self, state: tuple[int, int], parent, action: str, distance: int):
        self.state = state
        self.parent = parent
        self.action = action
        self.distance = distance

class Frontier:
    def __init__(self):
        self.frontier: list[Node] = []

    def add(self, node: Node):
        self.frontier.append(node)

    def is_contains_state(self, state: tuple[int, int]):
        return any(node.state == state for node in self.frontier)

    def is_empty(self):
        return len(self.frontier) == 0
    
    def remove(self) -> Node:
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            #self.frontier.sort(key=lambda x: x.distance) # big o is worse.
            next_remove_node = self.frontier[0]
            for node in self.frontier:
                if next_remove_node.distance > node.distance:
                    next_remove_node = node
            self.frontier.remove(next_remove_node)
            return next_remove_node

class Maze:
    def __init__(self, file_path):
        
        with open(file_path) as file_io_wrapper:
            file_text = file_io_wrapper.read()

        contents = file_text.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            wall_rows = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        wall_rows.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        wall_rows.append(False)
                    elif contents[i][j] == " ":
                        wall_rows.append(False)
                    else:
                        wall_rows.append(True)
                except IndexError:
                    wall_rows.append(False)
            
            self.walls.append(wall_rows)

        self.solution = None
        self.total_explored = 0
        self.explored_states = set()

    def get_distance_from_goal(self, state: tuple[int, int]) -> int:
        goal_row, goal_col = self.goal
        row, col = state
        x_distance = abs(goal_col - col)
        y_distance = abs(goal_row - row)
        return x_distance + y_distance

    def get_neighbors(self, state) -> tuple[str, tuple[int, int]]:
        current_row, current_column = state
        candidates = [
            ("up", (current_row - 1, current_column)),
            ("down", (current_row + 1, current_column)),
            ("left", (current_row, current_column - 1)),
            ("right", (current_row, current_column + 1))
        ]
        
        result = []
        for action, (row, column) in candidates:
            if 0 <= row < self.height and 0 <= column < self.width and not self.walls[row][column]:
                distance = self.get_distance_from_goal((row, column))
                result.append((action, (row, column), distance))
        
        return result
    
    def print_solution(self):
        solution = self.solution[0] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def print_explored(self):
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif (i, j) in self.explored_states:
                    print("=", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def solve(self):

        start = Node(state=self.start, parent=None, action=None, distance=-1)
        frontier = Frontier()
        frontier.add(start)

        while True:

            if frontier.is_empty():
                raise Exception("no solution")
            
            node = frontier.remove()
            self.total_explored += 1

            if node.state == self.goal:
                states = []
                actions = []
                while node.parent is not None:
                    states.append(node.state)
                    actions.append(node.action)
                    node = node.parent

                states.reverse()
                actions.reverse()
                self.solution = [states, actions]
                return
            
            self.explored_states.add(node.state)
            neighbors = self.get_neighbors(node.state)
            for action, state, distance in neighbors:
                if not frontier.is_contains_state(state) and state not in self.explored_states:
                    neighbor_node = Node(state=state, parent=node, action=action, distance=distance)
                    frontier.add(neighbor_node)

print(sys.argv)
if len(sys.argv) != 2:
    raise Exception("Usage: python maze.py maze.txt")

maze = Maze(sys.argv[1])
maze.solve()
print("Total Explored Node: ", maze.total_explored)
print("Explored Node:")
maze.print_explored()
print("Solution:")
maze.print_solution()