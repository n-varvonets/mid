# Примеры работы с кортежем (tuple) и множеством (set), включая вложенные типы данных

# 1. Тип данных: кортеж и множество с разными типами значений (включая списки, словари и вложенные структуры)

# Кортеж может содержать различные типы данных, включая списки, словари и вложенные кортежи
my_tuple = (
    1,                            # Целое число
    3.14,                         # Число с плавающей точкой
    "строка",                     # Строка
    [1, 2, 3],                    # Список
    {"ключ": "значение"},          # Словарь
    (4, 5, 6)                     # Вложенный кортеж
)
print("Кортеж с разными типами данных:", my_tuple)

# Множество может содержать только неизменяемые объекты. Поэтому, например, список в множество добавлен быть не может.
my_set = {
    1,                            # Целое число
    1,                            # Целое число
    3.14,                         # Число с плавающей точкой
    "строка",                     # Строка
    frozenset([1, 2, 3]),         # Неизменяемое множество (frozenset)
    frozenset({"ключ": "значение"}),  # Неизменяемый аналог словаря через frozenset
    (4, 5, 6)                     # Вложенный кортеж
}
print("Множество с разными типами данных:", my_set)

# Попытка добавить изменяемый объект (например, список) в множество вызовет ошибку
try:
    my_set.add([1, 2, 3])  # Ошибка, так как список - изменяемый тип данных
except TypeError as e:
    print("Ошибка добавления списка в множество:", e)

# Попытка добавить повторяющееся значение в множество просто игнорируется
my_set.add(1)
print("Множество после попытки добавления повторного значения:", my_set)

# 2. Вложенные структуры: кортежи и множества могут быть вложены друг в друга

# Кортеж внутри кортежа
nested_tuple = (1, (2, 3), (4, (5, 6)))
print("Вложенный кортеж:", nested_tuple)

# Множество с вложенным множеством (используем frozenset для неизменяемости)
nested_set = {1, 2, frozenset({3, 4}), frozenset({frozenset({5, 6})})}
print("Вложенное множество:", nested_set)

# 3. Методы работы с кортежами и множествами

# Методы для кортежа (tuple)
print("Длина кортежа:", len(my_tuple))        # len() - получить длину кортежа
print("Индекс элемента 'строка':", my_tuple.index("строка"))  # index() - поиск индекса элемента

# Методы для множества (set)
my_set.add(7)                                 # add() - добавить элемент в множество
print("Множество после добавления элемента:", my_set)

my_set.remove(1)                              # remove() - удалить элемент из множества
print("Множество после удаления элемента:", my_set)

print("Объединение множеств:", my_set.union({8, 9}))  # union() - объединение множеств
print("Пересечение множеств:", my_set.intersection({7, 3.14}))  # intersection() - пересечение

# 4. Пользовательский тип данных в кортеж и множество

# Определим простой пользовательский класс
class MyData:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"MyData({self.value})"

# Создадим экземпляры пользовательского класса и добавим их в кортеж и множество
data1 = MyData(10)
data2 = MyData(20)

custom_tuple = (data1, data2)
print("Кортеж с пользовательскими типами данных:", custom_tuple)

custom_set = {data1, data2}
print("Множество с пользовательскими типами данных:", custom_set)

# Попробуем добавить объект с тем же значением в множество
duplicate_data = MyData(10)
custom_set.add(duplicate_data)
print("Множество после добавления объекта с тем же значением:", custom_set)
