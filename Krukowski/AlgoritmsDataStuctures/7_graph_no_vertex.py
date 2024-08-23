class Graph:
    def __init__(self):
        # Инициализация графа в виде словаря, где ключ — вершина, значение — список смежных вершин
        self.graph = {}

    def add_vertex(self, vertex):
        # Добавление новой вершины в граф
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        # Добавление ребра между двумя вершинами (ненаправленный граф)
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].append(vertex2)
            self.graph[vertex2].append(vertex1)

    def add_directed_edge(self, vertex1, vertex2):
        # Добавление направленного ребра от vertex1 к vertex2
        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)

    def bfs(self, start_vertex):
        # Поиск в ширину (BFS)
        visited = set()
        queue = [start_vertex]
        bfs_order = []

        while queue:
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.add(vertex)
                bfs_order.append(vertex)
                queue.extend([v for v in self.graph[vertex] if v not in visited])

        return bfs_order

    def dfs(self, start_vertex):
        # Поиск в глубину (DFS)
        visited = set()
        stack = [start_vertex]
        dfs_order = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                dfs_order.append(vertex)
                stack.extend([v for v in self.graph[vertex] if v not in visited])

        return dfs_order

    def __str__(self):
        # Представление графа в виде строки
        result = ""
        for vertex in self.graph:
            result += f"{vertex} -> {self.graph[vertex]}\n"
        return result

# Пример использования:
g = Graph()
g.add_vertex('A')
g.add_vertex('B')
g.add_vertex('C')
g.add_vertex('D')
g.add_vertex('E')

g.add_edge('A', 'B')
g.add_edge('A', 'C')
g.add_edge('B', 'D')
g.add_edge('C', 'E')

print("Граф:")
print(g)

print("BFS (от A):", g.bfs('A'))  # Вывод: ['A', 'B', 'C', 'D', 'E']
print("DFS (от A):", g.dfs('A'))  # Вывод: ['A', 'C', 'E', 'B', 'D']
