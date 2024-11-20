import heapq

def dijkstra(start_cell, end_cell, grid, cols, rows):
    """Menggunakan algoritma Dijkstra untuk menemukan jalur terpendek dalam maze."""
    start_cell.distance = 0
    unvisited_queue = [(start_cell.distance, start_cell)]
    heapq.heapify(unvisited_queue)

    while unvisited_queue:
        current_distance, current_cell = heapq.heappop(unvisited_queue)
        current_cell.visited = True

        if current_cell == end_cell:
            break  # Jalur terpendek telah ditemukan

        for neighbor in current_cell.get_neighbors(grid, cols, rows):
            if neighbor.visited:
                continue
            tentative_distance = current_distance + 1  # Asumsi semua edge memiliki bobot 1
            if tentative_distance < neighbor.distance:
                neighbor.distance = tentative_distance
                neighbor.previous = current_cell
                heapq.heappush(unvisited_queue, (neighbor.distance, neighbor))

    # Membangun jalur terpendek dari end_cell ke start_cell
    path = []
    current = end_cell
    while current.previous:
        path.append(current)
        current = current.previous
    path.append(start_cell)
    path.reverse()
    return path
