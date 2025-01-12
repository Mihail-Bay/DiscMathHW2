import time
import tracemalloc

class Kruskal:
    def __init__(self, graph):
        self.graph = graph

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def min_spanning_tree(self):
        # Начинаем отслеживание памяти
        tracemalloc.start()

        edges = []
        for frm in self.graph:
            for to, cost in self.graph[frm].items():
                edges.append((cost, frm, to))

        # Сортируем рёбра по весу
        edges.sort(key=lambda x: x[0])

        parent = {}
        rank = {}

        # Инициализация
        for vertex in self.graph:
            parent[vertex] = vertex
            rank[vertex] = 0

        mst = []  # Список для хранения рёбер остовного дерева
        total_cost = 0  # Общая стоимость остовного дерева

        # Запуск замера времени
        start_time = time.time()

        for cost, frm, to in edges:
            x = self.find(parent, frm)
            y = self.find(parent, to)

            # Если не образует цикл, добавляем в остовное дерево
            if x != y:
                mst.append((frm, to, cost))
                total_cost += cost
                self.union(parent, rank, x, y)

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
