import time
import tracemalloc

class Kruskal:
    def __init__(self, graph):
        self.graph = graph
        #new
        self.validator = GraphValidator()

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
        #new
        # Проверяем граф на корректность
        try:
            self.validator.validate_graph(self.graph)
        except ValueError as e:
            print(f"\nОшибка валидации графа в алгоритме Краскала:")
            print(f"{'='*50}")
            print(f"Описание: {str(e)}")
            print(f"{'='*50}\n")
            raise
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
#new
class GraphValidator:
    @staticmethod
    def validate_graph(graph):
        """
        Проверяет граф на корректность:
        1. Проверка на пустой граф
        2. Проверка на изолированные вершины
        3. Проверка на связность графа
        4. Проверка на корректность весов
        """
        if not graph:
            raise ValueError("Граф пуст")

        # Проверка на изолированные вершины
        for vertex, edges in graph.items():
            if not edges:
                raise ValueError(f"Вершина {vertex} изолирована")

        # Проверка на связность графа
        if not GraphValidator.is_connected(graph):
            raise ValueError("Граф несвязный")

        # Проверка на корректность весов
        for vertex, edges in graph.items():
            for target, weight in edges.items():
                if not isinstance(weight, (int, float)):
                    raise ValueError(f"Некорректный вес ребра между {vertex} и {target}")
                # Проверка на симметричность рёбер
                if target not in graph or vertex not in graph[target] or graph[target][vertex] != weight:
                    raise ValueError(f"Несимметричное ребро между {vertex} и {target}")

    @staticmethod
    def is_connected(graph):
        """
        Проверяет связность графа с помощью поиска в глубину
        """
        if not graph:
            return True

        visited = set()

        def dfs(vertex):
            visited.add(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)

        # Начинаем с первой вершины
        start_vertex = next(iter(graph))
        dfs(start_vertex)

        # Проверяем, что все вершины были посещены
        return len(visited) == len(graph)
