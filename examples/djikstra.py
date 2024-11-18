from __future__ import absolute_import
from src.maze_manager import MazeManager
from src.maze import Maze

def dijkstra(maze, start, goal):
    import heapq
    
    rows, cols = maze.rows, maze.cols
    distances = {node: float('infinity') for node in maze.get_all_nodes()}
    distances[start] = 0
    priority_queue = [(0, start)]
    came_from = {start: None}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == goal:
            break

        for neighbor in maze.get_neighbors(current_node):
            distance = current_distance + maze.get_cost(current_node, neighbor)

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                came_from[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct path from start to goal
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path

if __name__ == "__main__":

    # create a maze manager to handle all operations
    manager = MazeManager()

    # create a maze with a specific size
    maze = Maze(10, 10, algorithm="bin_tree")  # or another generation algorithm

    # add this maze to the maze manager
    maze = manager.add_existing_maze(maze)

    # Define start and goal points
    start = (0, 0)  # top-left corner
    goal = (9, 9)   # bottom-right corner

    # Find the shortest path using Dijkstra
    shortest_path = dijkstra(maze, start, goal)

    # Display the maze
    manager.show_maze(maze.id)

    # Visualize the path found by Dijkstra
    manager.show_path(maze.id, shortest_path)
