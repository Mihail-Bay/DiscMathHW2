from HW2.src.Prim import Prim
from HW2.src.Kruskal import Kruskal


def create_graphs():
    # Создание различных типов графов для тестирования
    graphs = {
        "undirected_connected": {  # Неориентированный связный граф
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        },
        "undirected_disconnected": {  # Неориентированный несвязный граф
            'A': {'B': 1},
            'B': {'A': 1},
            'C': {'D': 2},
            'D': {'C': 2}
        },
        "directed": {  # Ориентированный граф (алгоритмы Прима и Краскала требуют неориентированные графы)
            'A': {'B': 1, 'C': 4},
            'B': {'C': 2},
            'C': {'A': 3}
        },
        "negative_weights": {  # Граф с отрицательными весами
            'A': {'B': -1, 'C': 4},
            'B': {'A': -1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        },
        "cyclic": {  # Циклический граф
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1, 'A': 3}
        },
        "acyclic": {  # Ациклический граф
            'A': {'B': 1, 'C': 4},
            'B': {'D': 2},
            'C': {'D': 1},
            'D': {}
        },
        "large": {  # Большой граф для тестирования производительности
            str(i): {str(j): i + j for j in range(1, 101) if j != i}
            for i in range(1, 101)
        }
    }
    return graphs

def test_algorithm(algorithm_class, graph, algorithm_name):
    algorithm = algorithm_class(graph)
    mst, total_cost = algorithm.min_spanning_tree()
    print(f"{algorithm_name} algorithm:")
    print("MST:", mst)
    print("Total cost:", total_cost)
    print("-" * 40)

def test_algorithms(graphs):
    for name, graph in graphs.items():
        print(f"Testing graph: {name}")
        test_algorithm(Prim, graph, "Prim")
        test_algorithm(Kruskal, graph, "Kruskal")

if __name__ == "__main__":
    graphs = create_graphs()
    test_algorithms(graphs)

