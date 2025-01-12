import heapq
import time
import tracemalloc

class Prim:
    def __init__(self, graph):
        self.graph = graph

    def min_spanning_tree(self):
        # Начинаем отслеживание памяти
        tracemalloc.start()

        # Инициализация
        start_vertex = next(iter(self.graph))  # Начинаем с произвольной вершины
        visited = set([start_vertex])
        edges = [
            (cost, start_vertex, to)
            for to, cost in self.graph[start_vertex].items()
        ]
        heapq.heapify(edges)  # Превращаем список рёбер в кучу (min-heap)

        mst = []  # Список для хранения рёбер остовного дерева
        total_cost = 0  # Общая стоимость остовного дерева

        # Запуск замера времени
        start_time = time.time()

        while edges:
            cost, frm, to = heapq.heappop(edges)  # Берем рёбер с минимальной стоимостью
            if to not in visited:
                visited.add(to)
                mst.append((frm, to, cost))
                total_cost += cost

                # Добавляем все рёбра из новой вершины
                for next_to, next_cost in self.graph[to].items():
                    if next_to not in visited:
                        heapq.heappush(edges, (next_cost, to, next_to))

        # Завершение замера времени
        end_time = time.time()

        # Получение текущего и пикового использования памяти
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Вывод результатов
        print()
        print("Время работы: {:.6f} секунд".format(end_time - start_time))
        print(f"Пиковая память: {peak / 2 ** 20:.2f} MB")
        print()

        return mst, total_cost
