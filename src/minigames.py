from __future__ import absolute_import
from main.maze_manager import MazeManager
from main.maze import Maze

if __name__ == "__main__":

    # Membuat instance dari MazeManager yang mengelola operasi labirin
    manager = MazeManager()

    sizes = [20, 30, 40]  # Tambahkan algoritma lain jika diperlukan

    for size in sizes:
        # Tambahkan labirin ke manager dengan metode pertama, membuat labirin langsung di manager
        maze = manager.add_maze(size, size)

        # Tambahkan labirin lain yang dibuat secara terpisah ke manager (metode kedua)
        maze2 = Maze(size, size)
        maze2 = manager.add_existing_maze(maze2)

        # Membuat labirin menggunakan metode binary tree
        maze_binTree = Maze(size, size, algorithm="bin_tree")
        maze_binTree = manager.add_existing_maze(maze_binTree)

        # Mode tanpa output (opsional)
        manager.set_quiet_mode(True)

        # Menyelesaikan labirin menggunakan Dijkstra
        manager.solve_maze(maze.id, "Dijkstra")

        # Menampilkan labirin yang belum terpecahkan
        manager.show_maze(maze.id)

        # Menampilkan animasi bagaimana solver Dijkstra menemukan solusi
        manager.show_solution_animation(maze.id)

        # Menampilkan gambar labirin dengan solusi overlay (jika `set_filename` dipanggil, akan disimpan otomatis)
        manager.show_solution(maze.id)