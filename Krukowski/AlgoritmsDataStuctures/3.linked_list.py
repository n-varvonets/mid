class Node:
    """
    Каждый элемент списка будет представлен узлом, который хранит данные и указатель на следующий узел.
    """
    def __init__(self, data):
        self.data = data  # Данные, хранящиеся в узле
        self.next = None  # Указатель на следующий узел


class LinkedList:
    """
    Теперь создадим сам список, который будет управлять узлами.
    """
    def __init__(self):
        self.head = None  # Начало списка (первый узел)

    def append(self, data):
        """Добавление элемента В КОНЕЦ списка.

        Представь, что у тебя есть цепочка, где каждый звено знает только о следующем.
        Чтобы добавить новое звено в конец цепочки, нужно пройти от начала до последнего звена,
        чтобы прикрепить новое звено к его концу, например:
            Допустим, у тебя есть список с элементами [1 -> 2 -> 3]:
                self.head указывает на первый элемент (1).
                last_node сначала тоже указывает на 1.
                Цикл while пройдет через все узлы: 1 -> 2 -> 3.
                После цикла last_node будет указывать на 3 (последний узел).
                Теперь ты можешь добавить новый элемент 4, установив last_node.next = new_node.а новый будет new_node
        """
        new_node = Node(data)
        if not self.head:  # для первого елемента(при создании нового списка)
            self.head = new_node
            return

        current_node = self.head  # Начинаем с первого узла (head) для поиска последнего узла в списке.
        while current_node.next:  # Пока у текущего узла есть следующий узел, двигаемся дальше.
            current_node = current_node.next  # Переходим к следующему узлу в списке.
            # Как только нашли NULL, текущий узел становится предпоследним, то в цикл уже не ходим и осталось только....
        current_node.next = new_node  # ...устанавливить ссылку текущего узла(предпоследнего уже) добавив к нему НАШ НОВЫЙ УЖЕ с null ссылкой

    def insert(self, data, position):
        """Добавление элемента в указанную позицию списка."""
        new_node = Node(data)

        if position == 0:  # Если вставка в начало списка
            new_node.next = self.head
            self.head = new_node
            return

        current_node = self.head
        current_position = 0

        # Идем по списку до узла перед позицией вставки
        while current_node is not None and current_position < position - 1:
            current_node = current_node.next
            current_position += 1

        # Если дошли до конца списка, но позиция больше длины списка
        if current_node is None:
            print("Позиция вне диапазона")
            return

        # Вставляем новый узел, переназначив указатели
        new_node.next = current_node.next
        current_node.next = new_node

    def prepend(self, data):
        """Добавление элемента в начало списка."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        """Удаление узла по значению."""
        if self.head and self.head.data == key:
            self.head = self.head.next
            return
        current_node = self.head
        while current_node and current_node.next:
            if current_node.next.data == key:
                current_node.next = current_node.next.next
                return
            current_node = current_node.next

    def print_list(self):
        """Вывод всех элементов списка."""
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")


ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.append(8)

ll.prepend(0)
ll.prepend(-1)

ll.print_list()  # Вывод: 0 -> 1 -> 2 -> 3 -> None

ll.delete(2)
ll.print_list()  # Вывод: 0 -> 1 -> 3 -> None


