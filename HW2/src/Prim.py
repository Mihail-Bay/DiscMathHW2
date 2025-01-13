import heapq
import time
import tracemalloc

class Prim:
    def __init__(self, graph):
        self.graph = graph
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

# new
class GraphError(Exception):
    """Базовый класс для ошибок графа"""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or "Нет дополнительной информации"


class EmptyGraphError(GraphError):
    """Ошибка пустого графа"""
    pass


class IsolatedVertexError(GraphError):
    """Ошибка изолированной вершины"""
    pass


class DisconnectedGraphError(GraphError):
    """Ошибка несвязного графа"""
    pass


class InvalidWeightError(GraphError):
    """Ошибка некорректного веса"""
    pass


class AsymmetricEdgeError(GraphError):
    """Ошибка несимметричного ребра"""
    pass


class GraphValidator:
    @staticmethod
    def validate_graph(graph):
        """Проверяет граф на корректность"""
        if not graph:
            raise EmptyGraphError(
                "Граф пуст",
                "График должен содержать хотя бы одну вершину и ребро"
            )

        # Проверка на изолированные вершины
        for vertex, edges in graph.items():
            if not edges:
                raise IsolatedVertexError(
                    f"Обнаружена изолированная вершина: {vertex}",
                    "Каждая вершина должна иметь хотя бы одно ребро"
                )

        # Проверка на связность графа
        if not GraphValidator.is_connected(graph):
            raise DisconnectedGraphError(
                "Граф несвязный",
                "Должен существовать путь между любыми двумя вершинами графа"
            )

        # Проверка на корректность весов и симметричность рёбер
        for vertex, edges in graph.items():
            for target, weight in edges.items():
                if not isinstance(weight, (int, float)):
                    raise InvalidWeightError(
                        f"Некорректный вес ребра между {vertex} и {target}",
                        "Вес ребра должен быть числом"
                    )

                if target not in graph or vertex not in graph[target] or graph[target][vertex] != weight:
                    raise AsymmetricEdgeError(
                        f"Несимметричное ребро между {vertex} и {target}",
                        "В неориентированном графе каждое ребро должно быть двунаправленным с одинаковым весом"
                    )

    @staticmethod
    def is_connected(graph):
        """Проверяет связность графа"""
        if not graph:
            return True

        visited = set()
        start_vertex = next(iter(graph))

        def dfs(vertex):
            visited.add(vertex)
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start_vertex)
        return len(visited) == len(graph)
