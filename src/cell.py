class Cell:
    __slots__ = ('x', 'y', 'walls', 'distance', 'previous')

    DIRECTIONS = {'N': (0, -1, 'S'), 'S': (0, 1, 'N'), 'E': (1, 0, 'W'), 'W': (-1, 0, 'E')}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.distance = float('inf')
        self.previous = None

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def remove_wall(self, other, direction):
        self.walls[direction] = False
        opposite = self.DIRECTIONS[direction][2]
        other.walls[opposite] = False

    def get_neighbors(self, grid, cols, rows):
        neighbors = []
        x, y = self.x, self.y
        for direction, (dx, dy, _) in self.DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and not self.walls[direction]:
                neighbors.append(grid[ny][nx])
        return neighbors
