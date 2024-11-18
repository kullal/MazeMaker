from __future__ import absolute_import
from src.maze_manager import MazeManager

if __name__ == "__main__":

    # Membuat instance dari MazeManager
    manager = MazeManager()

    # Menambahkan labirin 10x10 ke dalam manager
    maze = manager.add_maze(10, 10)

    # Menyelesaikan labirin menggunakan algoritma Dijkstra
    manager.solve_maze(maze.id, "Dijkstra", "fancy")

    # Menampilkan labirin yang belum terpecahkan
    manager.show_maze(maze.id)

    # Menampilkan animasi bagaimana labirin dibuat
    manager.show_generation_animation(maze.id)

    # Menampilkan animasi bagaimana solver Dijkstra menemukan solusi
    manager.show_solution_animation(maze.id)

    # Menampilkan labirin dengan solusi overlay
    manager.show_solution(maze.id)
