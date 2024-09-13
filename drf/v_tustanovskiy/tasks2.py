################################ gen vs iter ################################
# Примером итератора
numbers = [1, 2, 3]
it = iter(numbers)

print(it) # <list_iterator object at 0x0000021587163460>
print(next(it))  # 1
print(next(it))  # 2
print(next(it))  # 3

# Пример генератора:
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(gen)  # <generator object my_generator at 0x0000021586DA4880>
print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3

numbers_1 = [i ** 2 for i in range(1, 100, 2)]
print(numbers_1)  # [1, 9, 25, 49, 81, 121, 169, 225, 289, 361, 441, 529, 625, 729, 841, ...]
# print(next(numbers_1))  # error

numbers_1 = iter(numbers_1)
print(numbers_1)  # <list_iterator object at 0x00000215B5D93760>
print(next(numbers_1))  # 1


################################ gen vs iter ################################
data = [[]] * 3  # поскольку используется операция умножения *, все три элемента списка ссылаются на один и тот же вложенный список []
data2 = data
print(data)  # [[], [], []]
data[1].append(1)
print(data)  # [[1], [1], [1]]
print(data2)  # [[1], [1], [1]]

data3 = [[], [], []]  # явно создаем три отдельных списка, каждый из которых независим и находится в своей области памяти
data3[1].append(1)
print(data3)  # [[], [1], []]
data4 = [[] for _ in range(3)]
data4[1].append(0)
print(data4)  # [[], [0], []]


################################ or vs and ################################
print(True or False)  # True: 'or' возвращает первое истинное значение, True здесь истинное
print(True and False)  # False: 'and' возвращает первое ложное значение, False здесь ложное

print(10 or 0)  # 10: 'or' возвращает первое истинное значение, 10 здесь истинное
print(10 and 0)  # 0: 'and' возвращает первое ложное значение, 0 здесь ложное

print(10 or [])  # 10: 'or' возвращает первое истинное значение, 10 здесь истинное
print(10 and [])  # []: 'and' возвращает первое ложное значение, [] является ложным значением


# 3
some_var = None
some_lst = [0, None, False, '', '-First True Value-', '-Another Value-', 1, False]
for el in some_lst:
    some_var = some_var or el
    # 1. Первое значение 0 (ложное), поэтому some_var становится 0
    # 2. Далее идет None (ложное), поэтому some_var становится None
    # 3. Затем идет False (ложное), и some_var становится False
    # 4. Пустая строка '' тоже ложное значение, some_var становится ''
    # 5. На '-First True Value-' встречается первое истинное значение, присваивается оно
    print(some_var)
print(f"last print={some_var}")  # Выведет: '-First True Value-'

print('' is None)  # False: '' — это пустая строка, а None — специальное значение
print([] is None)  # False: [] — это пустой список, а None — это объект, представляющий отсутствие значения
print([] is [])  # False: это два разных объекта (разные списки) в памяти
print("" is '')  # True: все пустые строки (литералы) указывают на один и тот же объект в памяти
print("" is False)  # False
print(None is None)  # True: None — это синглтон, один и тот же объект везде
