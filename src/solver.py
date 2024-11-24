import time
import random
import logging
from src.maze import Maze
import heapq  # Untuk algoritma Dijkstra

logging.basicConfig(level=logging.DEBUG)

class Solver(object):
    """Base class for solution methods.
    Every new solution method should override the solve method.

    Attributes:
        maze (list): The maze which is being solved.
        neighbor_method:
        quiet_mode: When enabled, information is not outputted to the console
    """

    def __init__(self, maze, quiet_mode, neighbor_method):
        logging.debug("Class Solver ctor called")

        self.maze = maze
        self.neighbor_method = neighbor_method
        self.name = ""
        self.quiet_mode = quiet_mode

    def solve(self):
        logging.debug("Class: Solver solve called")
        raise NotImplementedError

    def get_name(self):
        logging.debug("Class Solver get_name called")
        raise self.name

    def get_path(self):
        logging.debug("Class Solver get_path called")
        return self.path


class DepthFirstBacktracker(Solver):
    """A solver that implements the depth-first recursive backtracker algorithm."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug("Class DepthFirstBacktracker ctor called")
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Depth First Backtracker"

    def solve(self):
        logging.debug("Class DepthFirstBacktracker solve called")
        k_curr, l_curr = self.maze.entry_coor
        self.maze.grid[k_curr][l_curr].visited = True
        visited_cells = list()
        path = list()

        if not self.quiet_mode:
            print("\nSolving the maze with depth-first search...")

        time_start = time.time()

        while (k_curr, l_curr) != self.maze.exit_coor:
            neighbour_indices = self.maze.find_neighbours(k_curr, l_curr)
            neighbour_indices = self.maze.validate_neighbours_solve(
                neighbour_indices, k_curr, l_curr, self.maze.exit_coor[0], self.maze.exit_coor[1], self.neighbor_method
            )

            if neighbour_indices is not None:
                visited_cells.append((k_curr, l_curr))
                path.append(((k_curr, l_curr), False))
                k_next, l_next = random.choice(neighbour_indices)
                self.maze.grid[k_next][l_next].visited = True
                k_curr = k_next
                l_curr = l_next
            elif len(visited_cells) > 0:
                path.append(((k_curr, l_curr), True))
                k_curr, l_curr = visited_cells.pop()

        path.append(((k_curr, l_curr), False))
        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))

        logging.debug("Class DepthFirstBacktracker leaving solve")
        return path


class BreadthFirst(Solver):
    """A solver that implements the breadth-first search algorithm."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug("Class BreadthFirst ctor called")
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Breadth First Recursive"

    def solve(self):
        logging.debug("Class BreadthFirst solve called")
        current_level = [self.maze.entry_coor]
        path = list()

        print("\nSolving the maze with breadth-first search...")
        time_start = time.time()

        while True:
            next_level = list()

            while current_level:
                k_curr, l_curr = current_level.pop(0)
                self.maze.grid[k_curr][l_curr].visited = True
                path.append(((k_curr, l_curr), False))

                if (k_curr, l_curr) == self.maze.exit_coor:
                    if not self.quiet_mode:
                        print("Number of moves performed: {}".format(len(path)))
                        print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))
                    return path

                neighbour_coors = self.maze.find_neighbours(k_curr, l_curr)
                neighbour_coors = self.maze.validate_neighbours_solve(
                    neighbour_coors, k_curr, l_curr, self.maze.exit_coor[0], self.maze.exit_coor[1], self.neighbor_method
                )

                if neighbour_coors is not None:
                    for coor in neighbour_coors:
                        next_level.append(coor)

            for cell in next_level:
                current_level.append(cell)
        logging.debug("Class BreadthFirst leaving solve")


class BiDirectional(Solver):
    """A solver that implements the bidirectional search algorithm."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug("Class BiDirectional ctor called")
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Bi Directional"

    def solve(self):
        logging.debug("Class BiDirectional solve called")

        grid = self.maze.grid
        k_curr, l_curr = self.maze.entry_coor
        p_curr, q_curr = self.maze.exit_coor
        grid[k_curr][l_curr].visited = True
        grid[p_curr][q_curr].visited = True
        backtrack_kl = list()
        backtrack_pq = list()
        path_kl = list()
        path_pq = list()

        if not self.quiet_mode:
            print("\nSolving the maze with bidirectional search...")
        time_start = time.time()

        while True:
            neighbors_kl = self.maze.find_neighbours(k_curr, l_curr)
            neighbors_pq = self.maze.find_neighbours(p_curr, q_curr)

            neighbors_kl = [
                neigh for neigh in neighbors_kl if not grid[k_curr][l_curr].is_walls_between(grid[neigh[0]][neigh[1]])
            ]
            neighbors_pq = [
                neigh for neigh in neighbors_pq if not grid[p_curr][q_curr].is_walls_between(grid[neigh[0]][neigh[1]])
            ]

            if len(neighbors_kl) > 0:
                backtrack_kl.append((k_curr, l_curr))
                path_kl.append(((k_curr, l_curr), False))
                k_next, l_next = random.choice(neighbors_kl)
                grid[k_next][l_next].visited = True
                k_curr, l_curr = k_next, l_next

            elif len(backtrack_kl) > 0:
                path_kl.append(((k_curr, l_curr), True))
                k_curr, l_curr = backtrack_kl.pop()

            if len(neighbors_pq) > 0:
                backtrack_pq.append((p_curr, q_curr))
                path_pq.append(((p_curr, q_curr), False))
                p_next, q_next = random.choice(neighbors_pq)
                grid[p_next][q_next].visited = True
                p_curr, q_curr = p_next, q_next

            elif len(backtrack_pq) > 0:
                path_pq.append(((p_curr, q_curr), True))
                p_curr, q_curr = backtrack_pq.pop()

            if any((True for n_kl in neighbors_kl if (n_kl, False) in path_pq)):
                path_kl.append(((k_curr, l_curr), False))
                return path_kl + path_pq

            elif any((True for n_pq in neighbors_pq if (n_pq, False) in path_kl)):
                path_pq.append(((p_curr, q_curr), False))
                return path_kl + path_pq

        logging.debug("Class BiDirectional leaving solve")

class Dijkstra(Solver):
    """Optimized Dijkstra solver with DFS-like backtracking behavior for large mazes."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug("Class Dijkstra ctor called")
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "Dijkstra"

    def solve(self):
        logging.debug("Class Dijkstra solve called")

        start = self.maze.entry_coor
        end = self.maze.exit_coor
        stack = [(self.maze.grid[start[0]][start[1]], 0)]  # Stack for DFS-like traversal
        visited_cells = set()
        path = []

        if not self.quiet_mode:
            print("\nSolving the maze with optimized Dijkstra...")

        time_start = time.time()

        while stack:
            current_cell, current_distance = stack.pop()

            # Mark the current cell as part of the path (forward move)
            if (current_cell.row, current_cell.col) not in visited_cells:
                path.append(((current_cell.row, current_cell.col), False))
                visited_cells.add((current_cell.row, current_cell.col))

            if (current_cell.row, current_cell.col) == end:
                if not self.quiet_mode:
                    print("Reached the end cell.")
                break

            neighbors = self.maze.find_neighbours(current_cell.row, current_cell.col)
            unexplored_neighbors = [
                (self.maze.grid[row][col], current_distance + 1)
                for row, col in neighbors
                if (row, col) not in visited_cells
                and not current_cell.is_walls_between(self.maze.grid[row][col])
            ]

            if unexplored_neighbors:
                # Push all neighbors to stack
                stack.extend(unexplored_neighbors)
            else:
                # Mark the current cell as a backtrack move
                path.append(((current_cell.row, current_cell.col), True))

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f} seconds".format(time.time() - time_start))

        logging.debug("Class Dijkstra leaving solve")
        return path
    
class AStar(Solver):
    """Optimized A* solver with DFS-like backtracking behavior for large mazes."""

    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug("Class AStar ctor called")
        super().__init__(maze, neighbor_method, quiet_mode)
        self.name = "A*"

    def solve(self):
        logging.debug("Class AStar solve called")

        start = self.maze.entry_coor
        end = self.maze.exit_coor
        stack = [(self.maze.grid[start[0]][start[1]], 0)]  # Stack for DFS-like traversal
        visited_cells = set()
        path = []

        if not self.quiet_mode:
            print("\nSolving the maze with optimized A*...")

        time_start = time.time()

        while stack:
            current_cell, _ = stack.pop()

            # Mark the current cell as part of the path (forward move)
            if (current_cell.row, current_cell.col) not in visited_cells:
                path.append(((current_cell.row, current_cell.col), False))
                visited_cells.add((current_cell.row, current_cell.col))

            if (current_cell.row, current_cell.col) == end:
                if not self.quiet_mode:
                    print("Reached the end cell.")
                break

            neighbors = self.maze.find_neighbours(current_cell.row, current_cell.col)
            unexplored_neighbors = [
                (self.maze.grid[row][col], 0)
                for row, col in neighbors
                if (row, col) not in visited_cells
                and not current_cell.is_walls_between(self.maze.grid[row][col])
            ]

            if unexplored_neighbors:
                # Sort unexplored neighbors by heuristic and push to stack
                unexplored_neighbors.sort(
                    key=lambda n: self._heuristic((n[0].row, n[0].col), end)
                )
                stack.extend(unexplored_neighbors)
            else:
                # Mark the current cell as a backtrack move
                path.append(((current_cell.row, current_cell.col), True))

        if not self.quiet_mode:
            print("Number of moves performed: {}".format(len(path)))
            print("Execution time for algorithm: {:.4f} seconds".format(time.time() - time_start))

        logging.debug("Class AStar leaving solve")
        return path

    @staticmethod
    def _heuristic(cell, goal):
        """Heuristic function for A*."""
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])
