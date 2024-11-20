class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.distance = float('inf')
        self.previous = None

    def remove_wall(self, other, wall):
        """Menghapus dinding antara sel ini dan sel lainnya."""
        self.walls[wall] = False
        opposites = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
        other.walls[opposites[wall]] = False

    def get_neighbors(self, grid, cols, rows):
        """Mengembalikan daftar tetangga yang bisa diakses (tanpa dinding)."""
        neighbors = []
        directions = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        for direction, (dx, dy) in directions.items():
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                neighbor = grid[ny][nx]
                if not self.walls[direction]:
                    neighbors.append(neighbor)
        return neighbors
