import time
import random
import logging
import heapq
from src.maze import Maze

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
        logging.debug('Class: Solver solve called')
        raise NotImplementedError

    def get_name(self):
        logging.debug('Class Solver get_name called')
        raise self.name

    def get_path(self):
        logging.debug('Class Solver get_path called')
        return self.path


class DijkstraSolver(Solver):
    def __init__(self, maze, quiet_mode=False, neighbor_method="fancy"):
        logging.debug('Class DijkstraSolver ctor called')
        self.name = "Dijkstra"
        super().__init__(maze, quiet_mode, neighbor_method)

    def solve(self):
        logging.debug('Class DijkstraSolver solve called')
        
        start = self.maze.entry_coor
        end = self.maze.exit_coor
        
        # Priority queue to store (distance, (k, l))
        pq = [(0, start)]
        distances = {start: 0}
        previous = {start: None}
        
        time_start = time.time()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node == end:
                # Backtrack to find the path
                path = []
                while current_node is not None:
                    path.append((current_node, False))
                    current_node = previous[current_node]
                path.reverse()
                
                if not self.quiet_mode:
                    print("Number of moves performed: {}".format(len(path)))
                    print("Execution time for algorithm: {:.4f}".format(time.time() - time_start))
                return path
            
            k_curr, l_curr = current_node
            self.maze.grid[k_curr][l_curr].visited = True

            neighbour_coors = self.maze.find_neighbours(k_curr, l_curr)
            neighbour_coors = self.maze.validate_neighbours_solve(
                neighbour_coors, k_curr, l_curr, end[0], end[1], self.neighbor_method
            )
            
            for neighbor in neighbour_coors:
                if neighbor not in distances or distances[neighbor] > current_distance + 1:
                    distances[neighbor] = current_distance + 1
                    priority = current_distance + 1
                    heapq.heappush(pq, (priority, neighbor))
                    previous[neighbor] = current_node


# Example usage
if __name__ == "__main__":
    # Assuming Maze class is properly implemented and can be instantiated
    maze = Maze()  # Placeholder for actual Maze instantiation
    solver = DijkstraSolver(maze, quiet_mode=False, neighbor_method="fancy")
    path = solver.solve()
    if path:
        print("Path found:", path)
    else:
        print("No path found.")
