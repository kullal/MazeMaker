from __future__ import absolute_import
from maze_manager import MazeManager

from main.maze_viz import Visualizer  # Import Visualizer untuk visualisasi perbandingan
import time

if __name__ == "__main__":

    # Create the manager
    manager = MazeManager()

    # Add a 20x10 maze to the manager (this maze will be used for all solvers)
    maze = manager.add_maze(20, 20)

    # Daftar algoritma yang ingin dijalankan
    algorithms = ["Dijkstra", "AStar"]  # Tambahkan algoritma lain jika diperlukan

    # Dictionary untuk menyimpan hasil eksekusi setiap algoritma
    results = {}

    print("\n--- Memulai eksekusi algoritma ---")

    # Iterasi algoritma yang dipilih
    for algorithm in algorithms:
        print(f"\n=== Menjalankan algoritma: {algorithm} ===")
        
        # Catat waktu mulai
        start_time = time.perf_counter()
        
        # Solve the maze using the selected algorithm
        manager.solve_maze(maze.id, algorithm)
        
        # Catat waktu selesai
        end_time = time.perf_counter()
        
        # Hitung durasi eksekusi dan jumlah langkah
        duration = end_time - start_time
        steps = len(maze.solution_path) if maze.solution_path else 0

        # Simpan hasil ke dictionary
        results[algorithm] = {"time": duration, "steps": steps}

        # Display the maze
        manager.show_maze(maze.id)

        # Show how the maze was generated
        # manager.show_generation_animation(maze.id)

        # Show how the maze was solved
        manager.show_solution_animation(maze.id)

    print("\n--- Semua algoritma telah selesai dijalankan ---")

    # Panggil fungsi untuk membuat visualisasi perbandingan hasil
    Visualizer.compare_execution_time(results, algorithms)  # Grafik waktu eksekusi
    Visualizer.compare_solution_steps(results, algorithms)  # Grafik langkah solusi
