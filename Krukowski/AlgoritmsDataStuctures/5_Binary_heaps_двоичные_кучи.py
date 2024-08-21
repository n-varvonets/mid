class BinaryHeap:
    """
    Краткое описание:
        -insert(value): добавляет новый элемент в кучу и восстанавливает её свойства с помощью trickle_up.
        -delete(): удаляет корневой элемент (максимум) и восстанавливает свойства кучи с помощью trickle_down.
        _trickle_up(index): вспомогательный метод, который поднимает элемент вверх по дереву, пока не будет выполнено свойство кучи.
        _trickle_down(index): вспомогательный метод, который опускает элемент вниз по дереву, восстанавливая свойства кучи.

    А КАК тогда найти потомков/родителей по индексу<u>**(т.к. НЕ используется ЛИНКИ, а используем МАССИВ с индексами)**</u>
    - У выбранного елемента ЕСТЬ индекс  (из массива) **ДЛЯ ПОИСКА ЕГО ПОТОМКОВ В ДРЕВЕ** расчитываются по простым формулам
      left_child(i) = 2 * i + 1
      right_child(i) = 2 * i + 2
      parent(i) = (i - 1) // 2
    """
    def __init__(self):
        self.data = []

    def insert(self, value):
        # Добавляем элемент в конец массива
        self.data.append(value)
        # Восстанавливаем свойства кучи (перемещаем элемент вверх)
        self._trickle_up(len(self.data) - 1)

    def delete(self):
        if len(self.data) == 0:
            return None
        # Заменяем корень последним элементом
        root = self.data[0]
        self.data[0] = self.data.pop()
        # Восстанавливаем свойства кучи (перемещаем элемент вниз)
        self._trickle_down(0)
        return root

    def _trickle_up(self, index):
        parent_index = (index - 1) // 2
        # Пока не достигнут корень и значение узла больше значения родителя
        # можно через рекурсию,
        # - ПОКА ИНДЕКС СТРОГО БОЛЬШЕ НУЛЯ
        # - и ПОКА ТЕКЩЕЕ ЗНАЧЕНИЕ ИНДЕКСА БОЛЬШЕ значения родителя, пока больше - мы просто подымаем его выше
        while index > 0 and self.data[index] > self.data[parent_index]:
            # Меняем местами узел с его родителем
            self.data[index], self.data[parent_index] = self.data[parent_index], self.data[index]
            # Переходим к родителю
            index = parent_index
            parent_index = (index - 1) // 2

    def _trickle_down(self, index):
        # нужно определить индексы потомков относительно текущего нода (ЛЕВЫЙ)
        child_index = 2 * index + 1
        # Пока есть хотя бы левый потомок
        while child_index < len(self.data):
            # Проверяем, если есть правый потомок и он больше левого
            if child_index + 1 < len(self.data) and self.data[child_index + 1] > self.data[child_index]:
                child_index += 1
            # Если текущий узел больше потомка, значит, всё в порядке
            if self.data[index] >= self.data[child_index]:
                break
            # Меняем местами узел с его потомком
            self.data[index], self.data[child_index] = self.data[child_index], self.data[index]
            # Переходим к потомку
            index = child_index
            child_index = 2 * index + 1

    def get_max(self):
        # Возвращаем максимум (корень)
        return self.data[0] if self.data else None

    def size(self):
        return len(self.data)

    def is_empty(self):
        return len(self.data) == 0

    def get_data(self):
        # Возвращаем текущие данные кучи
        return self.data

# Пример использования с большими данными
heap = BinaryHeap()

# Вставляем несколько элементов
elements = [15, 10, 20, 17, 8, 25, 30, 5, 40, 105]
for element in elements:
    heap.insert(element)

print("Куча после вставки элементов:", heap.get_data())  # Выводит: [105, 40, 30, 25, 17, 8, 15, 20, 5, 10]

# Получаем максимальный элемент, ХОТЯ БЫЛ САМЫМ ПОСЛЕДНИМ, при вставке
print("Максимум:", heap.get_max())  # Выводит: 105

# Удаляем максимальный элемент
removed_element = heap.delete()
print(f"Удалён элемент: {removed_element}")
print("Куча после удаления максимума:", heap.get_data())  # Выводит кучу после удаления

# Продолжаем удалять элементы до тех пор, пока куча не станет пустой
while not heap.is_empty():
    removed_element = heap.delete()
    print(f"Удалён элемент: {removed_element}")
    print("Куча после удаления:", heap.get_data())

