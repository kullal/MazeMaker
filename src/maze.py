import random
import math
import time
import heapq 
from src.cell import Cell
from src.algorithm import depth_first_recursive_backtracker, binary_tree


class Maze(object):
    """Class representing a maze; a 2D grid of Cell objects. Contains functions
    for generating randomly generating the maze as well as for solving the maze.

    Attributes:
        num_cols (int): The height of the maze, in Cells
        num_rows (int): The width of the maze, in Cells
        id (int): A unique identifier for the maze
        grid_size (int): The area of the maze, also the total number of Cells in the maze
        entry_coor: Entry location cell of maze
        exit_coor: Exit location cell of maze
        generation_path: The path that was taken when generating the maze
        solution_path: The path that was taken by a solver when solving the maze
        initial_grid (list): A list with Cell objects at each position
        grid (list): A copy of initial_grid (possibly unneeded)
    """

    def __init__(self, num_rows, num_cols, id=0, algorithm="dfs_backtrack"):
        """Creates a grid of Cell objects that are neighbors to each other.

        Args:
            num_rows (int): The width of the maze, in cells
            num_cols (int): The height of the maze in cells
            id (id): A unique identifier
        """
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.id = id
        self.grid_size = num_rows * num_cols
        self.entry_coor = self._pick_random_entry_exit(None)
        self.exit_coor = self._pick_random_entry_exit(self.entry_coor)
        self.generation_path = []
        self.solution_path = None
        self.initial_grid = self.generate_grid()
        self.grid = self.initial_grid
        self.generate_maze(algorithm, (0, 0))

    def generate_grid(self):
        """Function that creates a 2D grid of Cell objects. This can be thought of as a
        maze without any paths carved out

        Return:
            A list with Cell objects at each position
        """
        grid = list()
        for i in range(self.num_rows):
            grid.append(list())
            for j in range(self.num_cols):
                grid[i].append(Cell(i, j))
        return grid

    def find_neighbours(self, cell_row, cell_col):
        """Finds all existing neighbors of a cell in the grid. Returns a list of tuples.

        Args:
            cell_row (int): Row index of the cell
            cell_col (int): Column index of the cell

        Return:
            list: A list of neighbors that have not been visited
        """
        neighbours = list()

        def check_neighbour(row, col):
            if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
                neighbours.append((row, col))

        check_neighbour(cell_row - 1, cell_col)     # Top neighbour
        check_neighbour(cell_row, cell_col + 1)     # Right neighbour
        check_neighbour(cell_row + 1, cell_col)     # Bottom neighbour
        check_neighbour(cell_row, cell_col - 1)     # Left neighbour

        return neighbours if neighbours else None

    def _pick_random_entry_exit(self, used_entry_exit=None):
        """Function that picks random coordinates along the maze boundary to represent either
        the entry or exit point of the maze. Makes sure they are not at the same place.

        Args:
            used_entry_exit

        Return:
            (tuple): Coordinates for entry/exit point
        """
        rng_entry_exit = used_entry_exit

        while rng_entry_exit == used_entry_exit:
            rng_side = random.randint(0, 3)
            if rng_side == 0:     # Top side
                rng_entry_exit = (0, random.randint(0, self.num_cols - 1))
            elif rng_side == 2:   # Right side
                rng_entry_exit = (self.num_rows - 1, random.randint(0, self.num_cols - 1))
            elif rng_side == 1:   # Bottom side
                rng_entry_exit = (random.randint(0, self.num_rows - 1), self.num_cols - 1)
            elif rng_side == 3:   # Left side
                rng_entry_exit = (random.randint(0, self.num_rows - 1), 0)

        return rng_entry_exit

    def generate_maze(self, algorithm, start_coor=(0, 0)):
        """This takes the internal grid object and removes walls between cells using the
        specified algorithm.

        Args:
            start_coor: The starting point for the algorithm
        """
        if algorithm == "dfs_backtrack":
            depth_first_recursive_backtracker(self, start_coor)
        elif algorithm == "bin_tree":
            binary_tree(self, start_coor)

    def solve_with_dijkstra(self):
        """Solve the maze using Dijkstra's algorithm to find the shortest path from entry to exit."""
        distances = { (i, j): float('inf') for i in range(self.num_rows) for j in range(self.num_cols) }
        predecessors = { (i, j): None for i in range(self.num_rows) for j in range(self.num_cols) }
        distances[self.entry_coor] = 0

        priority_queue = [(0, self.entry_coor)]

        while priority_queue:
            current_dist, (row, col) = heapq.heappop(priority_queue)

            if (row, col) == self.exit_coor:
                self.solution_path = self._reconstruct_path(predecessors)
                return self.solution_path

            neighbors = self.find_neighbours(row, col)
            if neighbors:
                for n_row, n_col in neighbors:
                    if self.grid[row][col].is_walls_between(self.grid[n_row][n_col]):
                        continue

                    new_dist = current_dist + 1  # Each step has equal weight

                    if new_dist < distances[(n_row, n_col)]:
                        distances[(n_row, n_col)] = new_dist
                        predecessors[(n_row, n_col)] = (row, col)
                        heapq.heappush(priority_queue, (new_dist, (n_row, n_col)))

        self.solution_path = None
        return None

    def _reconstruct_path(self, predecessors):
        """Reconstruct the path from entry to exit using predecessors."""
        path = []
        current = self.exit_coor
        while current:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        return path