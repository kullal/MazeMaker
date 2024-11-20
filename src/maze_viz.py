import time
import random
import logging
import heapq
import matplotlib.pyplot as plt
from matplotlib import animation
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


class Visualizer(object):
    """Class that handles all aspects of visualization.

    Attributes:
        maze: The maze that will be visualized
        cell_size (int): How large the cells will be in the plots
        height (int): The height of the maze
        width (int): The width of the maze
        ax: The axes for the plot
        lines:
        squares:
        media_filename (string): The name of the animations and images

    """
    def __init__(self, maze, cell_size, media_filename):
        self.maze = maze
        self.cell_size = cell_size
        self.height = maze.num_rows * cell_size
        self.width = maze.num_cols * cell_size
        self.ax = None
        self.lines = dict()
        self.squares = dict()
        self.media_filename = media_filename

    def set_media_filename(self, filename):
        """Sets the filename of the media
            Args:
                filename (string): The name of the media
        """
        self.media_filename = filename

    def show_maze(self):
        """Displays a plot of the maze without the solution path"""

        # Create the plot figure and style the axes
        fig = self.configure_plot()

        # Plot the walls on the figure
        self.plot_walls()

        # Display the plot to the user
        plt.show()

        # Handle any potential saving
        if self.media_filename:
            fig.savefig("{}{}.png".format(self.media_filename, "_generation"), frameon=None)

    def plot_walls(self):
        """ Plots the walls of a maze. This is used when generating the maze image"""
        for i in range(self.maze.num_rows):
            for j in range(self.maze.num_cols):
                if self.maze.initial_grid[i][j].is_entry_exit == "entry":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "START", fontsize=7, weight="bold")
                elif self.maze.initial_grid[i][j].is_entry_exit == "exit":
                    self.ax.text(j*self.cell_size, i*self.cell_size, "END", fontsize=7, weight="bold")
                if self.maze.initial_grid[i][j].walls["top"]:
                    self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, i*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["right"]:
                    self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
                                 [i*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["bottom"]:
                    self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, (i+1)*self.cell_size], color="k")
                if self.maze.initial_grid[i][j].walls["left"]:
                    self.ax.plot([j*self.cell_size, j*self.cell_size],
                                 [(i+1)*self.cell_size, i*self.cell_size], color="k")

    def configure_plot(self):
        """Sets the initial properties of the maze plot. Also creates the plot and axes"""

        # Create the plot figure
        fig = plt.figure(figsize = (7, 7*self.maze.num_rows/self.maze.num_cols))

        # Create the axes
        self.ax = plt.axes()

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        title_box = self.ax.text(0, self.maze.num_rows + self.cell_size + 0.1,
                            r"{}$\times${}".format(self.maze.num_rows, self.maze.num_cols),
                            bbox={"facecolor": "gray", "alpha": 0.5, "pad": 4}, fontname="serif", fontsize=15)

        return fig

    def show_maze_solution(self):
        """Function that plots the solution to the maze. Also adds indication of entry and exit points."""

        # Create the figure and style the axes
        fig = self.configure_plot()

        # Plot the walls onto the figure
        self.plot_walls()

        list_of_backtrackers = [path_element[0] for path_element in self.maze.solution_path if path_element[1]]

        # Keeps track of how many circles have been drawn
        circle_num = 0

        self.ax.add_patch(plt.Circle(((self.maze.solution_path[0][0][1] + 0.5)*self.cell_size,
                                      (self.maze.solution_path[0][0][0] + 0.5)*self.cell_size), 0.2*self.cell_size,
                                     fc=(0, circle_num/(len(self.maze.solution_path) - 2*len(list_of_backtrackers)),
                                         0), alpha=0.4))

        for i in range(1, self.maze.solution_path.__len__()):
            if self.maze.solution_path[i][0] not in list_of_backtrackers and\
                    self.maze.solution_path[i-1][0] not in list_of_backtrackers:
                circle_num += 1
                self.ax.add_patch(plt.Circle(((self.maze.solution_path[i][0][1] + 0.5)*self.cell_size,
                    (self.maze.solution_path[i][0][0] + 0.5)*self.cell_size), 0.2*self.cell_size,
                    fc = (0, circle_num/(len(self.maze.solution_path) - 2*len(list_of_backtrackers)), 0), alpha = 0.4))

        # Display the plot to the user
        plt.show()

        # Handle any saving
        if self.media_filename:
            fig.savefig("{}{}.png".format(self.media_filename, "_solution"), frameon=None)
#awd
# Example usage
if __name__ == "__main__":
    # Assuming Maze class is properly implemented and can be instantiated
    maze = Maze()  # Placeholder for actual Maze instantiation
    solver = DijkstraSolver(maze, quiet_mode=False, neighbor_method="fancy")
    path = solver.solve()
    if path:
        print("Path found:", path)
        # Visualize the maze and solution
        visualizer = Visualizer(maze, cell_size=20, media_filename="dijkstra_solution")
        visualizer.show_maze()
        visualizer.show_maze_solution()
    else:
        print("No path found.")
