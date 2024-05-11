class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def is_empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

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
                    if contents[i, j] == "A":
                        self.start = (i, j)
                        wall_rows.append(False)
                    elif contents[i, j] == "B":
                        self.end = (i, j)
                        wall_rows.append(False)
                    elif contents[i, j] == " ":
                        wall_rows.append(False)
                    else:
                        wall_rows.append(True)
                except IndexError:
                    wall_rows.append(False)
            
            self.walls.append(wall_rows)

        self.solution = None
        self.total_explored = 0

    def get_neighbors(self, state):
        current_row, current_column = state
        candidates = [
            ("up", (current_row - 1, current_column)),
            ("down", (current_row + 1, current_column)),
            ("left", (current_row, current_column - 1)),
            ("right", (current_row - 1, current_column + 1))
        ]
        
        result = []
        for action, (row, column) in candidates:
            if 0 <= row < self.height and 0 <= column < self.width:
                result.append((action, (row, column)))
        
        return result
    
    def solve(self):
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)
    
# print(node.state)
print("Hello World!")