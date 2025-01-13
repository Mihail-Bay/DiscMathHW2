import tkinter as tk
from tkinter import messagebox
from Kruskal import Kruskal, AsymmetricEdgeError, InvalidWeightError, DisconnectedGraphError, IsolatedVertexError, \
    EmptyGraphError
from Prim import Prim, AsymmetricEdgeError, InvalidWeightError, DisconnectedGraphError, IsolatedVertexError, \
    EmptyGraphError

class MSTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Алгоритмы поиска минимального остовного дерева")

        # Выбор алгоритма
        self.algorithm_var = tk.StringVar(value="Kruskal")
        tk.Label(root, text="Выберите алгоритм:").grid(row=0, column=0, padx=10, pady=10)
        tk.Radiobutton(root, text="Краскала", variable=self.algorithm_var, value="Kruskal").grid(row=0, column=1, padx=10, pady=10)
        tk.Radiobutton(root, text="Прима", variable=self.algorithm_var, value="Prim").grid(row=0, column=2, padx=10, pady=10)

        # Ввод данных
        tk.Label(root, text="Введите граф (в формате {'A': {'B': 1, 'C': 2}, ...}):").grid(row=1, column=0, padx=10, pady=10)
        self.graph_entry = tk.Entry(root, width=50)
        self.graph_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        # Добавляем контекстное меню для вставки
        self.graph_entry.bind("<Button-3>", self.show_context_menu)  # Button-3 - это правая кнопка мыши

        # Кнопка для выполнения
        tk.Button(root, text="Выполнить", command=self.run_algorithm).grid(row=2, column=1, padx=10, pady=10)

        # Поле для вывода результата
        self.result_label = tk.Label(root, text="Результат:")
        self.result_label.grid(row=3, column=0, padx=10, pady=10)
        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        # Контекстное меню для вставки
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Вставить", command=self.paste_text)

    def show_context_menu(self, event):
        # Показываем контекстное меню на месте клика
        self.context_menu.post(event.x_root, event.y_root)

    def paste_text(self):
        # Вставляем текст из буфера обмена в поле ввода
        self.graph_entry.event_generate("<<Paste>>")

    def run_algorithm(self):
        try:
            # Очищаем предыдущий результат
            self.result_text.delete(1.0, tk.END)

            # Пытаемся преобразовать введенный текст в словарь
            try:
                graph = eval(self.graph_entry.get())
            except:
                self.show_error(
                    "Ошибка формата",
                    "Неверный формат ввода графа",
                    "График должен быть представлен в виде словаря словарей\n\n" +
                    "Пример:\n{'A': {'B': 1, 'C': 2}, 'B': {'A': 1, 'C': 3}, 'C': {'A': 2, 'B': 3}}"
                )
                return

            if not isinstance(graph, dict):
                self.show_error(
                    "Ошибка типа данных",
                    "Введенные данные не являются словарем",
                    "Используйте формат словаря для представления графа"
                )
                return

            # Создаем и запускаем выбранный алгоритм
            try:
                algorithm = self.algorithm_var.get()
                if algorithm == "Kruskal":
                    mst_algorithm = Kruskal(graph)
                else:
                    mst_algorithm = Prim(graph)

                mst, total_cost = mst_algorithm.min_spanning_tree()

            except EmptyGraphError as e:
                self.show_error("Пустой граф", str(e), e.details)
                return
            except IsolatedVertexError as e:
                self.show_error("Изолированная вершина", str(e), e.details)
                return
            except DisconnectedGraphError as e:
                self.show_error("Несвязный граф", str(e), e.details)
                return
            except InvalidWeightError as e:
                self.show_error("Некорректный вес", str(e), e.details)
                return
            except AsymmetricEdgeError as e:
                self.show_error("Несимметричное ребро", str(e), e.details)
                return

            # Выводим результат
            self.result_text.insert(tk.END, "✅ Успешно!\n\n")
            self.result_text.insert(tk.END, f"Использован алгоритм: {algorithm}\n\n")
            self.result_text.insert(tk.END, "Минимальное остовное дерево:\n")
            self.result_text.insert(tk.END, "=" * 50 + "\n")
            for edge in mst:
                self.result_text.insert(tk.END, f"Ребро: {edge[0]} -- {edge[1]}, Вес: {edge[2]}\n")
            self.result_text.insert(tk.END, "=" * 50 + "\n")
            self.result_text.insert(tk.END, f"Общая стоимость: {total_cost}\n")

        except Exception as e:
            self.show_error(
                "Неизвестная ошибка",
                str(e),
                "Проверьте формат ввода и попробуйте снова"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = MSTApp(root)
    root.mainloop()
