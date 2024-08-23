import heapq

class Station:
    """
    Класс, представляющий станцию в графе с весовыми ребрами.

    Атрибуты:
    - name: Название станции.
    - routes: Словарь, где ключи - это смежные станции, а значения - веса (время) ребер.
    """

    def __init__(self, name):
        """
        Инициализирует объект Station.

        :param name: Название станции.
        """
        self.name = name  # Имя станции (например, "A")
        self.routes = {}  # Словарь смежных станций и времени в пути до них

    def add_route(self, station, time):
        """
        Добавляет маршрут (ребро) к другой станции с определенным временем в пути (весом).

        :param station: Станция, к которой добавляется маршрут.
        :param time: Время в пути до станции (вес ребра).
        """
        self.routes[station] = time  # Добавление ребра к другой станции с весом (время пути)

    def shortest_path_to(self, target_station):
        """
        Находит кратчайший путь от текущей станции до указанной целевой станции.

        :param target_station: Целевая станция, до которой нужно найти кратчайший путь.
        :return: Кратчайшее расстояние до целевой станции и путь (список станций).

        Вершина   | A | B | D | C | E |
        Расстояние| 0 | 5 | 8 | ∞ | ∞ |
        Предыдущая| - | A | A | - | - |
        """
        # Инициализируем словарь с бесконечными расстояниями до всех станций
        shortest_distances = {station: float('infinity') for station in Station.all_stations}
        # Расстояние до начальной станции (self) = 0
        shortest_distances[self] = 0

        # Множество для хранения посещенных станций
        visited_stations = set()

        # Для восстановления пути: предыдущие станции
        previous_stations = {station: None for station in Station.all_stations}

        while shortest_distances:
            # Находим станцию с минимальным известным расстоянием, которую еще не посещали
            current_station = min(shortest_distances, key=shortest_distances.get)

            # distances = {
            #     a: 0,   # расстояние до a = 0
            #     b: 5,   # расстояние до b = 5
            #     d: 8,   # расстояние до d = 8
            #     c: 11,  # расстояние до c = 11
            #     e: 12   # расстояние до e = 12
            # }
            # Вызов min(shortest_distances, key=shortest_distances.get) будет работать так:
            # shortest_distances.get(a) вернет 0
            # shortest_distances.get(b) вернет 5
            # shortest_distances.get(d) вернет 8
            # shortest_distances.get(c) вернет 11
            # shortest_distances.get(e) вернет 12

            # Извлекаем минимальное расстояние для текущей станции и удаляем ее из словаря
            current_distance = shortest_distances.pop(current_station)

            # Если достигли целевой станции, строим путь и возвращаем результат
            if current_station == target_station:
                best_path = []  # Инициализация списка для хранения пути
                while current_station:
                    best_path.append(current_station.name)  # Добавляем текущую станцию в путь
                    current_station = previous_stations[current_station]  # Переходим к предыдущей станции
                return current_distance, best_path[
                                         ::-1]  # Возвращаем путь в правильном порядке (от начальной до целевой)

            # Добавляем текущую станцию в множество посещенных
            visited_stations.add(current_station)

            # Обрабатываем всех соседей текущей станции
            for adjacent_station, travel_time in current_station.routes.items():
                # Пропускаем уже посещенные станции
                if adjacent_station in visited_stations:
                    continue

                # Рассчитываем новое потенциальное расстояние до соседней станции
                potential_new_distance = current_distance + travel_time

                # Если найден более короткий путь к соседней станции
                if potential_new_distance < shortest_distances.get(adjacent_station, float('infinity')):
                    # distances.get(neighbor, float('infinity')) означает:
                    # "Получить значение для neighbor из словаря shortest_distances. Если его там нет,
                    # использовать значение float('infinity')", что представляет бесконечность.

                    # Обновляем минимальное известное расстояние до соседней станции
                    shortest_distances[adjacent_station] = potential_new_distance

                    # Запоминаем, что кратчайший путь к этой соседней станции проходит через текущую станцию
                    previous_stations[adjacent_station] = current_station

        # Если путь не найден, возвращаем бесконечность и пустой путь
        return float('infinity'), []

    def __str__(self):
        """
        Возвращает строковое представление станции и её маршрутов.
        """
        return f"Station {self.name} connected to: {[(station.name, time) for station, time in self.routes.items()]}"


# Список всех станций для использования в алгоритме
Station.all_stations = []

# Создание станций
a = Station('A')
b = Station('B')
c = Station('C')
d = Station('D')
e = Station('E')

# Добавляем станции в общий список
Station.all_stations.extend([a, b, c, d, e])

# Добавление маршрутов между станциями с указанием времени в пути (весов)
a.add_route(b, 5)  # A -> B с весом 5
a.add_route(d, 8)  # A -> D с весом 8

# b.add_route(a, 5)  # B -> A с весом 5
b.add_route(c, 6)  # B -> C с весом 6
b.add_route(d, 9)  # B -> D с весом 9

c.add_route(e, 15) # C -> E с весом 15

d.add_route(c, 3)  # D -> C с весом 3
d.add_route(e, 4)  # D -> E с весом 4

# Пример использования метода для поиска кратчайшего пути
distance, path = a.shortest_path_to(e)
print(f"Кратчайший путь от A до E: {path} с расстоянием {distance}")
