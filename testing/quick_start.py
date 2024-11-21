from __future__ import absolute_import
from testing.maze_manager import MazeManager
from testing.maze import Maze

if __name__ == "__main__":

    # Membuat instance dari MazeManager yang mengelola operasi labirin
    manager = MazeManager()

    # Tambahkan labirin ke manager dengan metode pertama, membuat labirin langsung di manager
    maze = manager.add_maze(10, 10)

    # Tambahkan labirin lain yang dibuat secara terpisah ke manager (metode kedua)
    maze2 = Maze(10, 10)
    maze2 = manager.add_existing_maze(maze2)

    # Membuat labirin menggunakan metode binary tree
    maze_binTree = Maze(10, 10, algorithm="bin_tree")
    maze_binTree = manager.add_existing_maze(maze_binTree)

    # Mode tanpa output (opsional)
    # manager.set_quiet_mode(True)

    # Menyelesaikan labirin menggunakan Dijkstra (tambahan untuk quick start)
    manager.solve_maze(maze.id, "Dijkstra")

    # Menyimpan gambar dan animasi labirin beserta solusinya
    manager.set_filename("myFileName")

    # Menampilkan labirin yang belum terpecahkan
    manager.show_maze(maze.id)

    # Menampilkan animasi bagaimana labirin dibuat
    manager.show_generation_animation(maze.id)

    # Menampilkan animasi bagaimana solver Dijkstra menemukan solusi
    manager.show_solution_animation(maze.id)

    # Menampilkan gambar labirin dengan solusi overlay (jika `set_filename` dipanggil, akan disimpan otomatis)
    manager.show_solution(maze.id)
