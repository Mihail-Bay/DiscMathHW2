import heapq
import time
import tracemalloc

class Prim:
    def __init__(self, graph):
        self.graph = graph
        #new
        self.validator = GraphValidator()
        
    def min_spanning_tree(self):
        #new
        # Проверяем граф на корректность
        try:
            self.validator.validate_graph(self.graph)
        except ValueError as e:
            print(f"\nОшибка валидации графа в алгоритме Прима:")
            print(f"{'='*50}")
            print(f"Описание: {str(e)}")
            print(f"{'='*50}\n")
            raise
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
