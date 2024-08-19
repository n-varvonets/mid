class DoubleNode:
    """
    Каждый элемент двусвязного списка будет представлен узлом, который хранит данные,
    указатель на следующий узел и указатель на предыдущий узел.
    """
    def __init__(self, data):
        self.data = data  # Данные, хранящиеся в узле
        self.next = None  # Указатель на следующий узел
        self.prev = None  # Указатель на предыдущий узел


class DoubleLinkedList:
    """
    Двусвязный список, в котором каждый узел знает о следующем и предыдущем узлах.
    """
    def __init__(self):
        self.head = None  # Начало списка (первый узел)

    def append(self, data):
        """Добавление элемента в конец списка."""
        new_node = DoubleNode(data)
        if not self.head:  # Если список пуст
            self.head = new_node
            return

        current_node = self.head
        while current_node.next:  # Ищем последний узел
            current_node = current_node.next

        current_node.next = new_node  # Устанавливаем связь текущего последнего узла с новым узлом
        new_node.prev = current_node  # Устанавливаем связь нового узла с предыдущим узлом

    def prepend(self, data):
        """Добавление элемента в начало списка."""
        new_node = DoubleNode(data)
        if not self.head:  # Если список пуст
            self.head = new_node
            return

        new_node.next = self.head  # Новый узел указывает на текущий первый узел
        self.head.prev = new_node  # Текущий первый узел указывает на новый узел как на предыдущий
        self.head = new_node  # Новый узел становится началом списка

    def delete(self, key):
        """Удаление узла по значению."""
        current_node = self.head

        while current_node:
            if current_node.data == key:
                if current_node.prev:  # Если это не первый узел
                    current_node.prev.next = current_node.next
                else:  # Если это первый узел
                    self.head = current_node.next

                if current_node.next:  # Если это не последний узел
                    current_node.next.prev = current_node.prev

                return  # Выход из функции после удаления

            current_node = current_node.next

    def print_list(self):
        """Вывод всех элементов списка."""
        current_node = self.head
        while current_node:
            print(current_node.data, end=" <-> ")
            current_node = current_node.next
        print("None")


dll = DoubleLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
dll.append(8)

dll.prepend(0)
dll.prepend(-1)

dll.print_list()  # Вывод: -1 <-> 0 <-> 1 <-> 2 <-> 3 <-> 8 <-> None

dll.delete(2)
dll.print_list()  # Вывод: -1 <-> 0 <-> 1 <-> 3 <-> 8 <-> None
