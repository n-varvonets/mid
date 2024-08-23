class Vertex:
    """
    __init__(self, value): Инициализирует вершину с заданным значением и пустым списком смежных вершин.
    add_adjacent_vertex(self, vertex): Добавляет смежную вершину, создавая ребро между текущей вершиной и заданной вершиной.
    __str__(self): Возвращает строковое представление вершины и списка её смежных вершин.
    """

    def __init__(self, value):
        """
        Инициализация вершины.

        :param value: Значение вершины.
        """
        self.value = value  # Значение вершины (например, метка или данные или имя пользователя(соц.сети))
        self.adjacent_vertices = []  # Список смежных вершин (связи)

    def add_adjacent_vertex(self, vertex):
        """
        Добавление смежной вершины (ребро) к текущей вершине.

        подписка в соц.сети, добавление в друзья

        :param vertex: Вершина, с которой создается связь.
        """
        # 2.что б не зациклилось рекурсия на добавление в ответ ребра(двойнаправленность ребр), то добавим условие
        if any(v.value == self.value for v in vertex.adjacent_vertices):
            print(f"{self.value} уже есть в списке друзей у {vertex.value}")
            return

        # 0
        self.adjacent_vertices.append(vertex)  # Добавление вершины в список смежных вершин

        # 1.option to connect in react. что б сделать двунапрваленные связи
        vertex.adjacent_vertices.append(self)

    def dfs(self, visited=None):
        """
        Depth-first search - 1ый алгоритм поиска для Графа (поиск в глуибну по графа)

        Используя РЕКУРСИЮ

            A
          / | \
         K  B  J
         \ /    \
          D      G
                  \
                  I

        (предпологаем двунаправленность граней, что реализовано в add_adjacent_vertex)

        Хочу выполнить поиск относительно узла А(Alice)
            - начнем перебирать смежные вершины для A, начиная с К(kelly)
                - потом мы понимаем что у К в друзьях есть D(David):
                    - добавляем его в список найденных
                - у D есть в друзьях B (Bob)
                    - его тоже добавляем в список найденных
                - у B смежные узлы только D and A
                - т.к. мы УЖЕ знаем про  D and A  (они УЖЕ в списке найденных)
                -, поэтому на этом ветка поиска завершается.
            - вернувшись к вершине A, переходим ко второй смежной вершине — J (John).
                - У J есть один друг — G (George).
                - У G есть один друг — I (Isaac).
                - У I нет новых друзей, поэтому ветка поиска на этом завершается.
            - Возвращаемся к вершине A, и так как все смежные вершины были посещены, DFS завершен.

        Схема (A - Alice, B - Bob, K - Kelly, D - David, J - John, G - George, I - Isaac):

          A
         / \
        K   J
        |    \
        D     G
         \     \
          B     I
         /
        (уже посещено)

        В результате DFS должны быть посещены все вершины, которые связаны с начальной вершиной A (Alice).

        Метод будет выводить последовательность посещения вершин.
        """
        if visited is None:
            visited = set()  # Инициализация множества посещенных вершин

        visited.add(self)  # Добавление текущей вершины в множество посещенных
        print(self.value)  # Вывод значения текущей вершины

        for adjacent_vertex in self.adjacent_vertices:
            if adjacent_vertex not in visited:
                adjacent_vertex.dfs(visited)  # Рекурсивный вызов для непосещенных вершин

    def bfs(self):
        """
        Breadth-First Search (BFS) — Поиск в ширину по графу.

        Без РЕКУРСИИ, используя очередь(FIFO)

        Изначальная схема графа:

            A
          / | \
         K  B  J
         \ /    \
          D      G
                  \
                  I

        (предполагаем двунаправленность граней, что реализовано в add_adjacent_vertex)

        начинаем со смежных вершин[K,B,J],  которые записуются в очередь(почечаем их как visited),
        дальше берем первый елемент с очереди и смотрим кто у НЕГО смежные
            - и всех их добавляем в НАЧАЛЬНУЮ очередь на обработать, для K это только D
            - а саму К из очееди изымаем, НО она уже как visited
            - в результате обновленная очередь [B, J, D] - без К уже
            - потом к  B  и т.д.

        Хочу выполнить поиск относительно узла A (Alice).
            - Начнем с вершины A (Alice).
            - Добавляем всех смежных с A вершин (K, B, J) в очередь на посещение.
            - Извлекаем первую вершину из очереди — это K (Kelly).
                - У K есть один друг — D (David), которого добавляем в очередь.
                - B уже был добавлен, поэтому K завершаем.
            - Следующая в очереди — B (Bob).
                - У B смежные узлы только D и A, но они уже были добавлены/посещены, поэтому B завершаем.
            - Следующая в очереди — J (John).
                - У J есть один друг — G (George), которого добавляем в очередь.
            - Следующая в очереди — D (David).
                - У D смежные узлы — это K и B, которые уже были добавлены/посещены, поэтому D завершаем.
            - Следующая в очереди — G (George).
                - У G есть один друг — I (Isaac), которого добавляем в очередь.
            - Следующая в очереди — I (Isaac).
                - У I нет новых друзей, поэтому завершаем поиск.

        В результате BFS должны быть посещены все вершины, которые связаны с начальной вершиной A (Alice).

        порядок обхода вершин

               A
             /
            K     D
            |    /  \
            B  /     G
            |/        \
            J         I


        Ожидаемый порядок обхода вершин:
        A -> K -> B -> J -> D -> G -> I

        Метод будет выводить последовательность посещения вершин.
        """
        visited = set()  # Инициализация множества посещенных вершин
        queue = [self]  # Инициализация очереди с начальной вершиной

        while queue:  # крутимся, пока в очереди что-то есть
            current_vertex = queue.pop(0)  # Извлекаем первую вершину из очереди

            if current_vertex not in visited:
                visited.add(current_vertex)  # Добавляем вершину в посещенные
                print(current_vertex.value)  # Вывод значения текущей вершины

                # Добавляем в очередь все смежные вершины, которые еще не посещены
                for adjacent_vertex in current_vertex.adjacent_vertices:
                    if adjacent_vertex not in visited:
                        queue.append(adjacent_vertex)

    def __str__(self):
        """
        Строковое представление вершины и её связей.
        """
        return f"{self.value} connected to: {[v.value for v in self.adjacent_vertices]}"


# Создание вершин
alice = Vertex("Alice")
bob = Vertex("Bob")
john = Vertex("John")
kelly = Vertex("Kelly")
david = Vertex("David")
george = Vertex("George")
isaac = Vertex("Isaac")

# Добавление ребер
alice.add_adjacent_vertex(kelly)     # A -> K
alice.add_adjacent_vertex(bob)       # A -> B
alice.add_adjacent_vertex(john)      # A -> J
kelly.add_adjacent_vertex(david)     # K -> D
john.add_adjacent_vertex(george)     # J -> G
george.add_adjacent_vertex(isaac)    # G -> I


print(alice)
print(bob)
print(john)
print(kelly)

print("-----dfs-----")
# Запуск DFS от вершины Alice
alice.dfs()
# Alice
# Kelly
# David
# Bob
# John
# George
# Isaac


print("-----bfs-----")
# Запуск BFS от вершины Alice
alice.bfs()
# Alice
# Kelly
# Bob
# John
# David
# George
# Isaac


